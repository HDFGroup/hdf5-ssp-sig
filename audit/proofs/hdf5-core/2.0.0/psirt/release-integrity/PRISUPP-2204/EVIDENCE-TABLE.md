# Evidence table — PRISUPP-2204 (HDF5 2.0.0)

## Artifact register

| Item | Source | URL / locator | Local path | Size (bytes) | SHA-256 | SHA-512 | Notes |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| Support source tarball | HDF Group downloads | [HDF Group support (hdf5-2.0.0.tar.gz)](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.tar.gz) | artifacts/support/hdf5-2.0.0.tar.gz | 42016043 | 6e45a4213cb11bb5860e1b0a7645688ab55562cc2d55c6ff9bcb0984ed12b22b | 1ac690454925cdf511cae4f6571f113e1386acc6bba3248f2abb4c30f25b012418ee059b15029132e35ef3af52dff43358ce93a0a335288aef358abe3eb70b02 | The file at the URL has since been replaced with the GitHub archive. |
| Support checksum file(s) | HDF Group downloads | [HDF Group support (hdf5-2.0.0.sha256sums.txt)](https://support.hdfgroup.org/releases/hdf5/v2_0/v2_0_0/downloads/hdf5-2.0.0.sha256sums.txt) | artifacts/support/hdf5-2.0.0.sha256sums.txt | 1568 | 1a1d20edfdf2bd57590e22cd05b7a4402efddffbac8c502541539d10ca1f3182 | 6c6b2cc193c1cd2521b48af810674eafdc1a6addd327d7655c26af361271717172b89f5c51cd727dd54b7cc920ac4274a1e104e0120e47e09266659c4c2461d9 | The original file was overwritten and is no longer available. The file at the URL was replaced with the corrected version. |
| Support signature file(s) | HDF Group downloads | `<SIG_URLS>` | `artifacts/support/` | `<BYTES>` | `<SHA256>` | `<SHA512>` | `<NOTES>` |
| GitHub auto-archive | GitHub tag archive | [GitHub release archive (hdf5-2.0.0.tar.gz)](https://github.com/HDFGroup/hdf5/releases/download/2.0.0/hdf5-2.0.0.tar.gz) | artifacts/github/hdf5-2.0.0.tar.gz | 42014805 | f4c2edc5668fb846627182708dbe1e16c60c467e63177a75b0b9f12c19d7efed | 2174b0ecea4ba209e59eec6d07f896d36e570161fd014df2b6e1b63e5835d4a682d201b1e9e54fdb090bb1879015d025c8514f6f5cda991f7311879bf94ea52a | |

## Control → evidence mapping

> Replace the control IDs below with HDF5-SHINES control IDs if they differ.

| Control | Requirement / intent | Evidence captured | Where (path / link) | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| SHINES-SCM-01 | Provenance of release tags (tag → commit) | `git show --pretty=raw`, `git rev-parse` | `artifacts/git/commit.txt`, `artifacts/git/tag.txt` | ☑ pass ☐ fail ☐ n/a | |
| SHINES-SCM-02 | Tag/commit authenticity (signature verification) | `git verify-tag`, `git verify-commit`, key fingerprints | `artifacts/logs/git-verify.txt` | ☐ pass ☐ fail ☑ n/a | |
| SHINES-REL-04 | Checksum publication & verification | `sha256sum.txt`, `sha512sum.txt` | `artifacts/logs/sha256sum.txt`, `artifacts/logs/sha512sum.txt` | ☐ pass ☑ fail | |
| SHINES-REL-03 | Reproducible source packaging | Deterministic repack test, normalized tarball checksums | `artifacts/logs/repacked.sha256.txt` | ☑ pass ☐ fail ☐ n/a | |
| SHINES-REL-02 | Release artifact completeness | File manifests, tree diff | `artifacts/diffs/*.txt`, `artifacts/diffs/tree.diff` | ☑ pass ☐ fail | |
| SHINES-VUL-01 | Integrity finding triage + decision record | This ticket’s timeline + decision log | `SAFE-OSE-evidence.md` | ☐ complete ☐ incomplete | |
| SHINES-GOV-02 | Public communication of security-relevant notes | Release notes / advisory link | `<URL/COMMIT>` | ☐ published ☐ not needed | |

## Key diffs summary

- File-hash manifest diff: `artifacts/diffs/github-support.filehash.diff`
  - Summary: Files are identical after normalizing timestamps and permissions.
- Tree diff: `artifacts/diffs/github-support.tree.diff`
  - Summary: Trees are identical after normalizing timestamps and permissions.
- Repack reproducibility: `artifacts/logs/repacked.sha256.txt`
  - Summary: Repacked tarballs are identical after normalizing timestamps and permissions.
