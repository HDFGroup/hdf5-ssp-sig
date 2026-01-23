# Evidence table — PRISUPP-2204 (HDF5 2.0.0)

## Artifact register

| Item | Source | URL / locator | Local path | Size (bytes) | SHA-256 | SHA-512 | Notes |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| Support source tarball | HDF Group downloads | https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz | artifacts/support/support.hdf5-2.0.0.tar.gz | 42016043 | 6e45a4213cb11bb5860e1b0a7645688ab55562cc2d55c6ff9bcb0984ed12b22b | 1ac690454925cdf511cae4f6571f113e1386acc6bba3248f2abb4c30f25b012418ee059b15029132e35ef3af52dff43358ce93a0a335288aef358abe3eb70b02 | The file at the URL has since been repplaced with the GitHub archive. |
| Support checksum file(s) | HDF Group downloads | https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.sha256sums.txt | artifacts/support/support.hdf5-2.0.0.sha256sums.txt` | `<BYTES>` | `<SHA256>` | `<SHA512>` | `<NOTES>` |
| Support signature file(s) | HDF Group downloads | `<SIG_URLS>` | `artifacts/support/` | `<BYTES>` | `<SHA256>` | `<SHA512>` | `<NOTES>` |
| GitHub auto-archive | GitHub tag archive | `<GITHUB_ARCHIVE_URL>` | `artifacts/github/<GITHUB_FILENAME>` | `<BYTES>` | `<SHA256_GITHUB>` | `<SHA512_GITHUB>` | `<NOTES>` |

## Control → evidence mapping

> Replace the control IDs below with HDF5-SHINES control IDs if they differ.

| Control | Requirement / intent | Evidence captured | Where (path / link) | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| SO-SCM-01 | Provenance of release tags (tag → commit) | `git show --pretty=raw`, `git rev-parse` | `artifacts/logs/git-provenance.txt` | ☐ pass ☐ fail ☐ n/a |  |
| SO-SCM-02 | Tag/commit authenticity (signature verification) | `git verify-tag`, `git verify-commit`, key fingerprints | `artifacts/logs/git-verify.txt` | ☐ pass ☐ fail ☐ n/a |  |
| SO-REL-04 | Checksum publication & verification | `sha256sum.txt`, `sha512sum.txt` | `artifacts/logs/sha256sum.txt`, `artifacts/logs/sha512sum.txt` | ☐ pass ☐ fail |  |
| SO-REL-03 | Reproducible source packaging | Deterministic repack test, normalized tarball checksums | `artifacts/logs/repacked.sha256.txt` | ☐ pass ☐ fail ☐ n/a |  |
| SO-REL-02 | Release artifact completeness | File manifests, tree diff | `artifacts/diffs/*.txt`, `artifacts/diffs/tree.diff` | ☐ pass ☐ fail |  |
| SO-VUL-01 | Integrity finding triage + decision record | This ticket’s timeline + decision log | `SAFE-OSE-evidence.md` | ☐ complete ☐ incomplete |  |
| SO-GOV-02 | Public communication of security-relevant notes | Release notes / advisory link | `<URL/COMMIT>` | ☐ published ☐ not needed |  |

## Key diffs summary

- File-hash manifest diff: `artifacts/diffs/filehash.diff`
  - Summary: `<ONE-LINE_SUMMARY>`
- Tree diff: `artifacts/diffs/tree.diff`
  - Summary: `<ONE-LINE_SUMMARY>`
- Repack reproducibility: `artifacts/logs/repacked.sha256.txt`
  - Summary: `<ONE-LINE_SUMMARY>`
