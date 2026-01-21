#!/usr/bin/env python3
"""
h5lint.py — Minimal HDF5 verifier for Safe‑OSE demos.

Scans an HDF5 file’s object graph and reports:
- Structural issues: broken links, empty groups, oversized attributes, soft/external link targets.
- Semantic smells: NaNs/inf in datasets, shape/dtype anomalies, extreme chunk/comp ratio heuristics.
- Safety flags: external links, user‑block presence, very large attributes, suspicious names.

Output: JSON to stdout (one object).
"""
import argparse, json, math, os, sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

try:
    import h5py
except Exception as e:
    sys.stderr.write("ERROR: h5py is required. pip install h5py\n")
    sys.exit(2)

# ---------- helpers

@dataclass
class Finding:
    level: str            # "info" | "warn" | "error" | "safety"
    code: str             # machine-readable identifier
    path: str             # HDF5 path where observed
    msg: str              # human-readable message
    extra: Dict[str, Any] # small, JSON-safe context

def safe_name(name: str) -> bool:
    bad = ["..", "//", "\x00"]
    return not any(b in name for b in bad)

def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except Exception:
            return obj.hex()
    try:
        import numpy as np
        if isinstance(obj, np.void):
            if obj.dtype.fields:
                return {k: json_safe(obj[k]) for k in obj.dtype.fields}
            return json_safe(obj.item())
        if isinstance(obj, np.generic):
            return json_safe(obj.item())
        if isinstance(obj, np.ndarray):
            return json_safe(obj.tolist())
    except Exception:
        pass
    if hasattr(obj, "tolist"):
        try:
            return json_safe(obj.tolist())
        except Exception:
            pass
    return obj

def dtype_is_text(dt) -> bool:
    # Treat fixed/variable-length ASCII/UTF-8 as text
    try:
        import numpy as np
        return (h5py.check_string_dtype(dt) is not None) or (dt.kind in ["S", "U"])
    except Exception:
        return h5py.check_string_dtype(dt) is not None

def is_probably_metadata(name: str) -> bool:
    lower = name.lower()
    return any(k in lower for k in ["meta", "attr", "schema", "desc"])

# ---------- core scan

class H5Lint:
    def __init__(self, path: str, soft_fail: bool = False):
        self.file_path = path
        self.soft_fail = soft_fail
        self.findings: List[Finding] = []
        self.summary: Dict[str, Any] = {
            "file": path,
            "size_bytes": os.path.getsize(path) if os.path.exists(path) else None,
            "num_objects": 0,
            "num_groups": 0,
            "num_datasets": 0,
            "num_links_soft": 0,
            "num_links_external": 0,
            "userblock_bytes": 0,
        }

    def add(self, level, code, path, msg, **extra):
        self.findings.append(Finding(level, code, path, msg, extra))

    def run(self):
        with h5py.File(self.file_path, "r", libver="latest") as f:
            # Userblock check
            try:
                ub = f.userblock_size
                self.summary["userblock_bytes"] = int(ub)
                if ub and ub > 0:
                    self.add("safety","USERBLOCK_PRESENT","/",
                             f"user block present ({ub} bytes) — inspect for embedded content",
                             userblock_bytes=ub)
            except Exception as e:
                self.add("warn","USERBLOCK_UNKNOWN","/","unable to read userblock_size", error=str(e))

            def visit(name, obj):
                self.summary["num_objects"] += 1
                if isinstance(obj, h5py.Group):
                    self.summary["num_groups"] += 1
                    # Empty group
                    if len(obj.keys()) == 0:
                        self.add("info","EMPTY_GROUP",obj.name,"empty group")
                elif isinstance(obj, h5py.Dataset):
                    self.summary["num_datasets"] += 1
                    self.check_dataset(obj)

                # Check attributes on any object
                self.check_attributes(obj)

            # Walk including links
            def visit_items(name, obj):
                visit(name, obj)
                # Check members for link types and name hygiene
                if isinstance(obj, h5py.Group):
                    for k in obj.keys():
                        if not safe_name(k):
                            self.add("safety","SUSPICIOUS_NAME",obj.name,
                                     f"suspicious member name: {k}", member=k)
                        try:
                            linfo = obj.get(k, getlink=True)
                            if isinstance(linfo, h5py.SoftLink):
                                self.summary["num_links_soft"] += 1
                                self.add("safety","SOFT_LINK",obj.name,
                                         f"soft link -> {linfo.path}", target=linfo.path, member=k)
                            elif isinstance(linfo, h5py.ExternalLink):
                                self.summary["num_links_external"] += 1
                                self.add("safety","EXTERNAL_LINK",obj.name,
                                         f"external link -> {linfo.filename}:{linfo.path}",
                                         target_file=linfo.filename, target_path=linfo.path, member=k)
                        except Exception as e:
                            self.add("error","LINK_INSPECT_FAIL",obj.name,"failed to inspect link", member=k, error=str(e))

                # Recurse children
                if isinstance(obj, h5py.Group):
                    for k, child in obj.items():
                        visit_items(child.name, child)

            visit_items("/", f["/"])

        # Simple tallies
        severities = {"info":0,"warn":0,"error":0,"safety":0}
        for fnd in self.findings:
            severities[fnd.level] = severities.get(fnd.level,0) + 1
        self.summary["counts"] = severities
        return {
            "summary": self.summary,
            "findings": [asdict(f) for f in self.findings],
        }

    # ---------- component checks

    def check_attributes(self, obj):
        for aname, aval in obj.attrs.items():
            try:
                # Size heuristic (attributes used as data payloads)
                size = None
                try:
                    import numpy as np
                    arr = np.array(aval)
                    size = int(arr.nbytes)
                except Exception:
                    if isinstance(aval, (bytes, str)):
                        size = len(aval.encode() if isinstance(aval, str) else aval)
                if size is not None and size > 1_000_000:
                    self.add("warn","HUGE_ATTRIBUTE",obj.name,
                             f"attribute '{aname}' is very large ({size} bytes)",
                             attribute=aname, size=size)

                # Name hygiene
                if not safe_name(aname):
                    self.add("safety","SUSPICIOUS_ATTR_NAME",obj.name,
                             f"suspicious attribute name: {aname}", attribute=aname)

            except Exception as e:
                self.add("error","ATTR_READ_FAIL",obj.name,
                         f"failed to read attribute '{aname}'",
                         attribute=aname, error=str(e))

    def check_dataset(self, dset: "h5py.Dataset"):
        info = {
            "shape": tuple(dset.shape) if dset.shape else (),
            "dtype": str(dset.dtype),
            "chunks": dset.chunks,
            "compression": dset.compression,
            "fillvalue": dset.fillvalue,
        }

        # Chunking + compression heuristics
        if dset.chunks is None and dset.compression:
            self.add("warn","COMPRESSION_WITHOUT_CHUNKING",dset.name,
                     "compression set but dataset is not chunked", **info)

        if dset.chunks:
            # extremely tiny or huge chunks heuristic
            nelems = 1
            for s in dset.shape or ():
                nelems *= max(1, int(s))
            celems = 1
            for c in dset.chunks or ():
                celems *= max(1, int(c))
            if celems < 8:
                self.add("warn","TINY_CHUNKS",dset.name,"very small chunk size", **info)
            if nelems > 0 and celems > nelems:
                self.add("warn","CHUNK_LARGER_THAN_DATASET",dset.name,"chunk covers more than dataset", **info)

        # Quick scan for NaN/Inf for numeric dtypes (sampled)
        try:
            import numpy as np
            if dset.dtype.kind in "f":  # floats
                sample = dset[tuple(slice(0, min(1024, s)) for s in (dset.shape or (1,)))]
                if np.any(np.isnan(sample)):
                    self.add("warn","NAN_VALUES",dset.name,"NaN detected in sampled values")
                if np.any(np.isinf(sample)):
                    self.add("warn","INF_VALUES",dset.name,"Inf detected in sampled values")
        except Exception as e:
            self.add("error","DATA_SAMPLE_FAIL",dset.name,"failed to sample dataset", error=str(e))

        # Text datasets: look for binary-ish content in VLEN strings
        try:
            sdt = h5py.check_string_dtype(dset.dtype)
            if sdt is not None and sdt.length is None:
                # vlen strings → sample a few elements
                take = 64
                sel = tuple(slice(0, min(take, s)) for s in (dset.shape or (1,)))
                try:
                    vals = dset[sel]
                    suspicious = 0
                    flat = vals.ravel() if hasattr(vals, "ravel") else vals
                    for i, v in enumerate(flat[:take]):
                        if isinstance(v, (bytes, bytearray)):
                            b = bytes(v)
                            if any(c < 9 or (13 < c < 32) for c in b[:128]): # control chars excluding \t\n\r
                                suspicious += 1
                        elif isinstance(v, str):
                            if any(ord(c) < 9 or (13 < ord(c) < 32) for c in v[:128]):
                                suspicious += 1
                    if suspicious > 0:
                        self.add("warn","TEXT_CONTROL_CHARS",dset.name,
                                 f"{suspicious} sampled string(s) contain control characters")
                except Exception as e:
                    self.add("error","TEXT_SAMPLE_FAIL",dset.name,"failed to sample text dataset", error=str(e))
        except Exception:
            pass

# ---------- CLI

def main():
    ap = argparse.ArgumentParser(description="Safe‑OSE minimal HDF5 verifier")
    ap.add_argument("file", help="path to .h5/.hdf5 file")
    ap.add_argument("--soft-fail", action="store_true",
                    help="exit 0 even if errors/safety findings are present")
    args = ap.parse_args()

    if not os.path.exists(args.file):
        sys.stderr.write(f"ERROR: file not found: {args.file}\n")
        sys.exit(2)

    lint = H5Lint(args.file, soft_fail=args.soft_fail)
    report = lint.run()
    print(json.dumps(json_safe(report), indent=2))

    # exit policy
    has_bad = any(f["level"] in ("error","safety") for f in report["findings"])
    sys.exit(0 if (args.soft_fail or not has_bad) else 1)

if __name__ == "__main__":
    main()
