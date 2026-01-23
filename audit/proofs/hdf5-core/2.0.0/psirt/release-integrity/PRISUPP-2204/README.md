# Summary of HDF5 2.0.0 source-artifact integrity check — PRISUPP-2204

**Title:** HDF5 2.0.0 source-artifact integrity check — PRISUPP-2204  
**Date:** 2026-01-22  
**Owner:** Gerd Heber  
**Reviewers:** Scot Breitenfeld, Glenn Song, Larry Knox  
**Status:** ☑ draft ☐ in review ☐ final  

## 1) Summary

A checksum mismatch was reported between:

- the **HDF Group support source tarball** for HDF5 2.0.0, and
- the **GitHub auto-generated “Source code” archive** for tag `hdf5_2.0.0`.

This record documents the investigation, compares unpacked contents, verifies tag provenance (where possible), and records the final decision.

## 2) Scope

**In scope**

- Support tarball: [support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz)  
- GitHub archive: [github.com/HDFGroup/hdf5/releases/download/2.0.0/hdf5-2.0.0.tar.gz](https://github.com/HDFGroup/hdf5/releases/download/2.0.0/hdf5-2.0.0.tar.gz)  
- Tag / commit: `hdf5_2.0.0` → `a6ff8ae`

**Out of scope** (unless explicitly required)

- Build output reproducibility
- Third-party mirrored downloads

## 3) Evidence collected

Primary evidence artifacts are listed in [`EVIDENCE-TABLE.md`](./EVIDENCE-TABLE.md), and stored under [`artifacts/`](./artifacts/) (downloaded archives, checksum logs, git verification logs, and diffs).

## 4) Methods (what we did)

1. Downloaded both artifacts and recomputed SHA-256/SHA-512.
2. Verified Git provenance for the tag (tag object → commit), and verified signatures where present.
3. Unpacked both archives and performed **content-first comparisons** using normalized file-hash manifests and tree diffs.
4. (Optional) Performed a deterministic repack to test whether differences were only archive metadata.

## 5) Findings

### 5.1 Checksums

- Support tarball SHA-256: `6e45a4213cb11bb5860e1b0a7645688ab55562cc2d55c6ff9bcb0984ed12b22b`
- GitHub archive SHA-256: `f4c2edc5668fb846627182708dbe1e16c60c467e63177a75b0b9f12c19d7efed`
- Support tarball SHA-512: `1ac690454925cdf511cae4f6571f113e1386acc6bba3248f2abb4c30f25b012418ee059b15029132e35ef3af52dff43358ce93a0a335288aef358abe3eb70b02`
- GitHub archive SHA-512: `2174b0ecea4ba209e59eec6d07f896d36e570161fd014df2b6e1b63e5835d4a682d201b1e9e54fdb090bb1879015d025c8514f6f5cda991f7311879bf94ea52a`

Mismatch: ☑ yes ☐ no

### 5.2 Tag provenance / authenticity

- `hdf5_2.0.0` resolves to commit: `a6ff8aed236ee1e1deff6415e88b16c42b22f17c`
- Tag signature status: “n/a”
- Commit signature status: “n/a”
- Verified signer identity / key fingerprint: “n/a”

### 5.3 Content comparison

**Result:** Code content matches exactly; differences limited to archive metadata and/or non-semantic packaging differences.

### 5.4 Root cause

GitHub auto-archives are convenience artifacts and may differ byte-for-byte.

## 6) Risk assessment

**Risk level:** ☑ low (benign packaging) ☐ medium ☐ high (possible supply-chain issue)

**Rationale:** Both archives are materially identical.

Decision gate applied:

- Any **code-content difference** is treated as a potential supply-chain risk until explained and remediated.
- Pure archive-metadata differences are treated as low risk, but require documentation and prevention steps.

## 7) Decision

**Decision:** Benign packaging variance; support artifact is correct; publish explanation.

Choose one:

- ☑ Benign packaging variance; support artifact is correct; publish explanation.
- ☑ Replace/pull artifact; re-cut release artifacts; publish advisory.
- ☐ Further investigation required; tracking issue `<LINK>`.

**Rationale:** `<RATIONALE>`

## 8) Corrective & preventive actions

- [x] Make support tarball generation deterministic (documented recipe; normalized times/ownership; consistent compression flags).
- [x] Publish signed checksum files for support artifacts (and document verification steps).
- [x] Add CI job that compares a CI-produced tarball to the published one (fail on unexpected deltas).
- [x] Document that GitHub auto-archives are convenience artifacts and may differ byte-for-byte.

Owners / due dates:
- `<ACTION_1>` — owner `<NAME>` — due `<YYYY-MM-DD>`
- `<ACTION_2>` — owner `<NAME>` — due `<YYYY-MM-DD>`

## 9) Public communication

- Release note added: ☐ yes ☐ no
  - Link: `<RELEASE_NOTES_URL_OR_COMMIT>`
- Advisory needed: ☐ yes ☐ no
  - Link: `<ADVISORY_URL_OR_ID>`

## 10) Appendix: command transcripts

See [`CHECKLIST.md`](./CHECKLIST.md) and the saved logs under [`artifacts/logs/`](./artifacts/logs/) for exact command outputs.
