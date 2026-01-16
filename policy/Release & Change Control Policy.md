# Release & Change Control Policy

**Policy intent:** Ensure releases are controlled, reviewable, and safe—especially given file format stability expectations and broad downstream embedding.

(HDF5’s release process documentation states that maintenance releases are backward- and forward-compatible regarding the file format and discusses interface compatibility reporting.)

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-REL‑01 | Each release SHALL have a named release manager (or delegate) and an approved release plan (scope, risk items, go/no-go checks). | Release checklist; signed approval record. | Confirm latest release has completed checklist + approver identity. |
| HDF5-SHINES-REL‑02 | All changes in a release SHALL be traceable to issues/PRs and categorized (feature/bug/security). | Changelog/release notes; issue/PR links. | Sample 20 entries; confirm traceability. |
| HDF5-SHINES-REL‑03 | Security fixes SHALL be clearly identified in release notes (with safe wording if embargoed) and linked to advisories when public. | Release notes + advisory links. | Verify latest security fix disclosure is consistent with VULN policy. |
| HDF5-SHINES-REL‑04 | Changes that may affect file-format compatibility SHALL undergo explicit compatibility testing and sign-off (see COMP policy). | Compatibility test reports; signoff. | Confirm presence when format-level behavior changes. |
| HDF5-SHINES-REL‑05 | A deprecation process SHALL exist with documented timelines and migration guidance for breaking changes. | Deprecation doc; migration guide updates.  | Verify notices exist for any removed/deprecated APIs. |
| HDF5-SHINES-REL‑06 | Release artifacts SHALL be reproducible or independently verifiable to the extent feasible (see BUILD policy). | Build attestation + checksums. | Verify provenance exists and matches released hashes. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-REL‑01 | OSPS-BR-02.01 (partial); OSPS-BR-02.02 (partial) | Release checklist + release manager signoff |
| HDF5-SHINES-REL‑02 | OSPS-BR-04.01 (covered); OSPS-BR-02.01 (partial) | Changelog + GitHub release notes + PR/issue refs |
| HDF5-SHINES-REL‑03 | OSPS-BR-04.01 (partial); OSPS-VM-04.01 (partial) | Release notes + advisory links + disclosure record |
| HDF5-SHINES-REL‑04 | OSPS-QA-06.01 (partial) | Compatibility test logs + CI outputs |
| HDF5-SHINES-REL‑05 | OSPS-DO-04.01 (partial); OSPS-DO-05.01 (partial) | Migration guides + deprecation policy + announcements |
| HDF5-SHINES-REL‑06 | OSPS-BR-06.01 (partial); OSPS-DO-03.01 (partial); OSPS-DO-03.02 (partial) | Provenance attestations + reproducibility + checksums |
