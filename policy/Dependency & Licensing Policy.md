# Dependency & Licensing Policy

**Policy intent:** Ensure downstream trust and legal clarity, and reduce supply-chain exposure from third-party libraries and transitive components (e.g., compression backends, build tooling).

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-DEP‑01 | The project SHALL maintain an inventory of direct runtime and build-time dependencies (including optional feature toggles). | Dependency inventory doc + build option matrix. | Confirm list covers common build configs; spot-check against build scripts. |
| HDF5-SHINES-DEP‑02 | Each release SHALL publish a license manifest for bundled/linked third-party components (including notices). | `THIRD_PARTY_NOTICES*` or release bundle notice file. | Verify file exists in release artifacts; verify updates each release. |
| HDF5-SHINES-DEP‑03 | Each release SHOULD produce an SBOM for core artifacts and (where feasible) official plugins. | SBOM files attached to releases (SPDX/CycloneDX). | Confirm SBOM presence for latest release + one prior release. |
| HDF5-SHINES-DEP‑04 | Dependencies SHALL be monitored for known vulnerabilities; remediation timelines SHALL be defined (severity-based). | Vulnerability tracking issue labels; dependency scanning reports. | Sample recent dependency CVE; confirm triage + fix timeline. |
| HDF5-SHINES-DEP‑05 | New third-party code adoption SHALL require: license review, provenance check, and security review (per SDLC‑02). | PR checklist completion; provenance note. | Sample 3 dependency-introducing PRs; confirm evidence. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-DEP‑01 | OSPS-DO-06.01 (partial); OSPS-QA-02.01 (partial)	| Dependency documentation + build notes |
| HDF5-SHINES-DEP‑02 | OSPS-LE-02.01 (partial); OSPS-LE-02.02 (partial); OSPS-LE-03.01 (covered); OSPS-LE-03.02 (partial) | LICENSE + third-party notices in source and release tarballs |
| HDF5-SHINES-DEP‑03 | OSPS-QA-02.02 (partial) | SBOMs attached to releases |
| HDF5-SHINES-DEP‑04 | OSPS-VM-05.01 (partial); OSPS-VM-05.02 (partial); OSPS-VM-05.03 (partial) | Dependency scan outputs + tracking + PSIRT linkage |
| HDF5-SHINES-DEP‑05 | OSPS-VM-05.02 (partial); OSPS-VM-05.01 (partial) | PR checklist + license review approvals |
