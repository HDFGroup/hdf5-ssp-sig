# Secure Build, Provenance, and Distribution Policy

**Policy intent:** Reduce supply-chain risk in released libraries/tools/plugins and ensure downstream users can verify authenticity and integrity.

Safe‑OSE explicitly calls for SBOMs and increased adoption of signed, reproducible build processes.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-BUILD‑01 | Release builds SHALL be performed in controlled environments (documented toolchains, pinned dependencies where feasible). | Build recipes; CI workflow definitions. | Verify build definitions; confirm immutability/pinning approach. |
| HDF5-SHINES-BUILD‑02 | Each release SHALL publish cryptographic checksums for all artifacts and SHALL retain them for the lifecycle of the release. | `SHA256SUMS` (or equivalent) and signatures. | Verify checksums for latest release; confirm archival. |
| HDF5-SHINES-BUILD‑03 | Official release artifacts SHOULD be signed (code signing for installers; signature files for tarballs) and signature verification instructions SHALL be published. | Signed installer note (Windows) and signing docs. | Verify artifacts are signed; verify instructions are complete. |
| HDF5-SHINES-BUILD‑04 | Each release SHOULD include provenance attestations (builder identity, source revision, build steps). | Provenance attestation files; CI run references. | Verify attestation links to exact git commit and workflow run. |
| HDF5-SHINES-BUILD‑05 | Reproducibility SHOULD be measured (at least for a reference platform), and discrepancies SHALL be investigated. | Reproducibility report. | Review last report; verify follow-ups exist. |
| HDF5-SHINES-BUILD‑06 | Distribution channels SHALL be enumerated and monitored for integrity risks (unofficial mirrors, trojanized packages). | “Official channels” page; monitoring notes. | Verify list is current; confirm response steps for discovered spoofing. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-BUILD‑01 | OSPS-BR-05.01 (partial) | CI build workflows + pinned toolchains |
| HDF5-SHINES-BUILD‑02 | OSPS-BR-06.01 (partial); OSPS-DO-03.01 (partial) | Hash manifests (SHA256SUMS) + release attachments |
| HDF5-SHINES-BUILD‑03 | OSPS-BR-06.01 (partial); OSPS-DO-03.01 (partial) | Signed installers + signature verification docs |
| HDF5-SHINES-BUILD‑04 | OSPS-BR-02.02 (partial); OSPS-DO-03.02 (partial) | Provenance attestations tied to release tags |
| HDF5-SHINES-BUILD‑05 | OSPS-DO-03.01 (partial) | Reproducibility reports + independent rebuild notes |
| HDF5-SHINES-BUILD‑06 | OSPS-BR-03.01 (partial); OSPS-BR-03.02 (partial) | “Official channels” docs + monitoring for spoofed artifacts |
