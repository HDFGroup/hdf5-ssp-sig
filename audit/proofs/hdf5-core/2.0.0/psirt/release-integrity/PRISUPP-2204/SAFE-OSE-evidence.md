# Safe-OSE evidence — PRISUPP-2204 (HDF5 <RELEASE_VERSION>)

**Title:** HDF5 <RELEASE_VERSION> source-artifact integrity check — PRISUPP-2204  
**Date:** `<YYYY-MM-DD>`  
**Owner:** `<NAME>`  
**Reviewers:** `<NAME(S)>`  
**Status:** ☐ draft ☐ in review ☐ final  

## 1) Summary

A checksum mismatch was reported between:

- the **HDF Group support source tarball** for HDF5 <RELEASE_VERSION>, and
- the **GitHub auto-generated “Source code” archive** for tag `<GITHUB_TAG>`.

This record documents the investigation, compares unpacked contents, verifies tag provenance (where possible), and records the final decision.

## 2) Scope

**In scope**
- Support tarball: `<SUPPORT_TARBALL_URL>`  
- GitHub archive: `<GITHUB_ARCHIVE_URL>`  
- Tag / commit: `<GITHUB_TAG>` → `<COMMIT_SHA>`

**Out of scope** (unless explicitly required)
- Build output reproducibility
- Third-party mirrored downloads

## 3) Evidence collected

Primary evidence artifacts are listed in `EVIDENCE-TABLE.md`, and stored under `artifacts/` (downloaded archives, checksum logs, git verification logs, and diffs).

## 4) Methods (what we did)

1. Downloaded both artifacts and recomputed SHA-256/SHA-512.
2. Verified Git provenance for the tag (tag object → commit), and verified signatures where present.
3. Unpacked both archives and performed **content-first comparisons** using normalized file-hash manifests and tree diffs.
4. (Optional) Performed a deterministic repack to test whether differences were only archive metadata.

## 5) Findings

### 5.1 Checksums

- Support tarball SHA-256: `<SHA256_SUPPORT>`
- GitHub archive SHA-256: `<SHA256_GITHUB>`
- Support tarball SHA-512: `<SHA512_SUPPORT>`
- GitHub archive SHA-512: `<SHA512_GITHUB>`

Mismatch: ☐ yes ☐ no

### 5.2 Tag provenance / authenticity

- `<GITHUB_TAG>` resolves to commit: `<COMMIT_SHA>`
- Tag signature status: `<TAG_SIGNATURE_STATUS>`
- Commit signature status: `<COMMIT_SIGNATURE_STATUS>`
- Verified signer identity / key fingerprint: `<SIGNER_AND_FP>` (or “n/a”)

### 5.3 Content comparison

**Result:** `<MATCH_RESULT>`

Fill in one of:
- ☐ Code content matches; differences limited to archive metadata and/or non-semantic packaging differences.
- ☐ Material differences found in tracked source files (list below).

**Material differences (if any)**
- `<FILE_1>` — `<DIFF_SUMMARY>`
- `<FILE_2>` — `<DIFF_SUMMARY>`

### 5.4 Root cause

`<ROOT_CAUSE>`

Examples (pick what applies):
- GitHub archive includes/excludes different files than the project tarball.
- Different timestamp normalization, file modes, or ordering in tar/gzip.
- Generated files included in one artifact but not the other.
- Submodule / vendored content differences.

## 6) Risk assessment

**Risk level:** ☐ low (benign packaging) ☐ medium ☐ high (possible supply-chain issue)

**Rationale:** `<RISK_RATIONALE>`

Decision gate applied:
- Any **code-content difference** is treated as a potential supply-chain risk until explained and remediated.
- Pure archive-metadata differences are treated as low risk, but require documentation and prevention steps.

## 7) Decision

**Decision:** `<DECISION>`

Choose one:
- ☐ Benign packaging variance; support artifact is correct; publish explanation.
- ☐ Replace/pull artifact; re-cut release artifacts; publish advisory.
- ☐ Further investigation required; tracking issue `<LINK>`.

**Rationale:** `<RATIONALE>`

## 8) Corrective & preventive actions

- [ ] Make support tarball generation deterministic (documented recipe; normalized times/ownership; consistent compression flags).
- [ ] Publish signed checksum files for support artifacts (and document verification steps).
- [ ] Add CI job that compares a CI-produced tarball to the published one (fail on unexpected deltas).
- [ ] Document that GitHub auto-archives are convenience artifacts and may differ byte-for-byte.

Owners / due dates:
- `<ACTION_1>` — owner `<NAME>` — due `<YYYY-MM-DD>`
- `<ACTION_2>` — owner `<NAME>` — due `<YYYY-MM-DD>`

## 9) Public communication

- Release note added: ☐ yes ☐ no
  - Link: `<RELEASE_NOTES_URL_OR_COMMIT>`
- Advisory needed: ☐ yes ☐ no
  - Link: `<ADVISORY_URL_OR_ID>`

## 10) Appendix: command transcripts

See `CHECKLIST.md` and the saved logs under `artifacts/logs/` for exact command outputs.
