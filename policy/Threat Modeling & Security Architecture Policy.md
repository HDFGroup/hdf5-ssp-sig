# Threat Modeling & SSP Architecture Policy

**Policy intent:** Create and maintain adequate threat models for HDF5 safety, security, and privacy vulnerabilities.

Data management libraries have unique attack surfaces (file structures, metadata graphs, plugin boundaries).
DML-focused security threat modeling approaches (e.g., CASSE) emphasize modeling file structures and library layers rather than only generic STRIDE categories.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-TM‑01 | The project SHALL maintain a threat model covering core parsing paths, format structures, and plugin trust boundaries. | Threat model doc + update log. | Confirm threat model exists; check last update aligns with major changes. |
| HDF5-SHINES-TM‑02 | Threat modeling SHALL explicitly include file structure elements (superblock/object headers/messages), plugin loader flows, and configuration entry points. | DFDs + structure diagrams. | Verify inclusion of file-structure modeling. |
| HDF5-SHINES-TM‑03 | Threat models SHALL drive test planning (fuzz targets, regression suites) and hardening priorities. | Link from TM findings to TEST backlog. | Sample 3 TM findings → verify linked tests/backlog items. |
| HDF5-SHINES-TM‑04 | The SIG SHOULD review threat model changes for high-risk features (new plugin types, integrity/encryption features). | SIG minutes noting TM reviews. | Verify review trail for a recent high-risk change. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-TM‑01 | OSPS-SA-03.02 (partial); OSPS-SA-01.01 (partial) | Threat model doc + DFDs + update log |
| HDF5-SHINES-TM‑02 | OSPS-SA-01.01 (partial); OSPS-SA-02.01 (partial) | File/plugin flow diagrams + trust boundary notes |
| HDF5-SHINES-TM‑03 | OSPS-SA-03.02 (partial) | TM findings linked to testing backlog + fuzz target list |
| HDF5-SHINES-TM‑04 | OSPS-GV-02.01 (partial) | Minutes recording TM reviews for major features |
