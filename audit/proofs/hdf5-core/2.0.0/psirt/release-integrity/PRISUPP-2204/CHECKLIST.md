# PRISUPP-2204 Checklist — HDF5 2.0.0 source integrity triage

> Goal: determine whether a checksum mismatch is **benign packaging variance** or a **material content difference** requiring corrective action.

## 0) Incident metadata

- [x] Incident / ticket: PRISUPP-2204
- [x] Release version: 2.0.0
- [x] Git tag: hdf5_2.0.0
- [x] Date opened: 2026-01-13
- [x] Owner: Gerd Heber
- [x] Reviewers: Scot Breitenfeld, Glenn Song, Larry Knox
- [x] Status: ☐ triage ☐ investigating ☑ resolved ☐ published

## 1) Identify the exact artifacts (URLs + sizes + timestamps)

- [?] Support tarball (HDF Group downloads):
  - URL: https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz
  - Filename: hdf5-2.0.0.tar.gz
  - Size: 42016043
  - Published checksum/signature files (if any): `<URLS>`
- [?] GitHub archive:
  - URL: https://github.com/HDFGroup/hdf5/releases/download/2.0.0/hdf5-2.0.0.tar.gz
  - Filename: hdf5-2.0.0.tar.gz
  - Size: 42014805

**Notes:** record the *exact* URL, including query strings, redirects, mirrors, and any “latest” endpoints.

## 2) Recompute checksums (store output)

- [x] Download both artifacts fresh (ideally from two networks/machines).
- [x] Compute SHA-256 and SHA-512.
- [x] Save command output to `artifacts/logs/checksums.txt`.

Suggested commands:

```bash
set -euo pipefail
mkdir -p artifacts/{support,github,logs}

# downloads (replace with real URLs)
curl -L https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz -o artifacts/support/hdf5-2.0.0.tar.gz
curl -L https://github.com/HDFGroup/hdf5/releases/download/2.0.0/hdf5-2.0.0.tar.gz    -o artifacts/github/hdf5-2.0.0.tar.gz

# checksums
( cd artifacts &&   sha256sum support/hdf5-2.0.0.tar.gz github/hdf5-2.0.0.tar.gz | tee logs/sha256sum.txt &&   sha512sum support/hdf5-2.0.0.tar.gz github/hdf5-2.0.0.tar.gz | tee logs/sha512sum.txt )
```

## 3) Verify Git provenance (tag → commit → signer)

- [x] Record tag object and commit:
  - `git show --pretty=raw <GITHUB_TAG>`
  - `git rev-parse <GITHUB_TAG>`
- [n/a] Verify tag signature (if annotated and signed):
  - `git verify-tag <GITHUB_TAG>`
- [n/a] Verify commit signature (if signed):
  - `git verify-commit <COMMIT_SHA>`
- [n/a] Record maintainer key fingerprints and trust path (GPG/Sigstore/etc.).

Save outputs to `artifacts/git/` and/or `artifacts/logs/git-verify.txt`.

## 4) Compare unpacked contents (normalized)

### 4.1 Unpack both archives

- [x] Unpack support tarball into `work/support/`
- [x] Unpack GitHub archive into `work/github/`

```bash
set -euo pipefail
rm -rf work && mkdir -p work/support work/github

tar -xf artifacts/support/<CANONICAL_FILENAME> -C work/support --strip-components=1
tar -xf artifacts/github/<GITHUB_FILENAME>       -C work/github   --strip-components=1
```

### 4.2 Generate deterministic file manifests

- [x] Capture file lists, permissions, and hashes:
  - `find ... -print0 | sort -z | xargs -0 ...`

```bash
set -euo pipefail
mkdir -p artifacts/diffs

for d in support github; do
  ( cd work/$d &&     find . -type f -print0 | sort -z | xargs -0 sha256sum > ../../artifacts/diffs/${d}.file-sha256.txt &&     find . -printf '%y %m %u %g %s %p
' | LC_ALL=C sort > ../../artifacts/diffs/${d}.stat.txt )
done
```

### 4.3 Tree diff (content-first)

- [x] Compare file hash manifests:
  - `diff -u support.file-sha256.txt github.file-sha256.txt`
- [x] Compare full trees (including missing files):
  - `diff -ruN work/support work/github > artifacts/diffs/tree.diff`

```bash
diff -u artifacts/diffs/support.file-sha256.txt artifacts/diffs/github.file-sha256.txt | tee artifacts/diffs/filehash.diff || true
diff -ruN work/support work/github | tee artifacts/diffs/tree.diff || true
```

## 5) Repack reproducibility test (optional but recommended)

If you suspect differences are due to tar/gzip metadata (timestamps, ordering):

- [x] Normalize mtimes, owners, modes (as appropriate), and repack deterministically.
- [x] Compare repacked checksums to see if they converge.

Example (GNU tar + gzip):

```bash
set -euo pipefail
rm -rf repack && mkdir -p repack/{support,github}

# Normalize mtimes (choose a reference timestamp, e.g. tag commit time: git show -s --format=%ct a6ff8ae)
REF_EPOCH=1762819001

for d in support github fossies; do
  rsync -a --delete work/$d/ repack/$d/
  find repack/$d -exec touch -h -d "@${REF_EPOCH}" {} +

  ( cd repack/$d &&     tar --sort=name --owner=0 --group=0 --numeric-owner         --mtime="@${REF_EPOCH}" -cf ../${d}.tar . )
  gzip -n -9 -f repack/${d}.tar
done

sha256sum repack/*.tar.gz | tee artifacts/logs/repacked.sha256.txt
```

## 6) Risk screen (decision gate)

- [x] **If any code content differs** (hash manifest diff shows changes in `.c`, `.h`, build scripts, etc.): treat as **potential supply-chain risk** until explained.
- [x] If diffs are limited to packaging metadata / timestamps / generated files: likely **benign**, but document the root cause and prevention.

## 7) Resolution + communication

- [x] Decision: ☑ benign packaging variance ☑ artifact replaced ☐ advisory published ☐ further investigation
- [ ] Root cause summary: `<ROOT_CAUSE>`
- [ ] Corrective actions:
  - [ ] Align packaging pipeline to deterministic archive generation
  - [ ] Publish signed checksums for support tarballs
  - [ ] Add CI job to compare published artifact vs. CI-produced artifact
- [ ] Public note added to release notes: ☐ yes ☐ no (link: `<URL/COMMIT>`)

## 8) Evidence pointer

Update `EVIDENCE-TABLE.md` with links/paths to:

- downloaded artifacts
- checksum outputs
- tag/commit verification output
- diffs / manifests
- packaging recipe / CI logs
