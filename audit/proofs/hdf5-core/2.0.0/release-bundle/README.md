# hdf5-core — release-bundle

## What to put here

- Artifact manifest (`manifest.json`) listing filenames, sizes, and SHA256 digests
- Attestations (SLSA/Sigstore/in-toto) if available
- Signing materials and verification instructions
- Build logs (CI run URLs, console logs, parameters)

## Locators

[Immutable locators](./locators.yml) (tags, asset URLs, CVE/NVD links, workflow URLs, and governance repo SHAs)

### Official releases & release notes
The canonical *HDF5 2.0.0* release is published on the main repo’s Releases page with assets and SHA‑256 hashes for each binary and source distribution; it’s tagged `2.0.0` and was published on ~Nov 10‑11 2025. Source, binaries, and checksums are all visible there.

### Source tree, changelog & release docs
The *HDFGroup/hdf5* GitHub repository holds the complete source history and **CHANGELOG.md** (in `release_docs/`) documenting features and differences between versions. The official docs also publish a *release_spec_20* page with structured release info and upgrade guidance.

### Security policy & disclosure channels
Security guidance and vulnerability reporting instructions live in the repo’s security overview (e.g., how issues should be disclosed privately before public advisory). This is the ground for any responsible disclosure trace. ([GitHub][3])

### Published CVEs & advisories (audit‑grade traces)
There are multiple GitHub Security Advisories (GHSA) for vulnerabilities affecting HDF5 prior to 2.0 — ranging in severity and often cross‑referenced to CVEs in NVD. Examples include a critical heap‑based overflow advisory (linked to CVE‑2025‑6269) and moderate advisories affecting older releases.

### CI/workflow endpoints
The HDF5 repository’s GitHub Actions workflows and historical run logs (including the main CI workflows) are accessible via the *Actions* tab. Individual runs include logs and artifact links that can be replayed or downloaded by commit/shas. *(Typically at) `https://github.com/HDFGroup/hdf5/actions`. *
