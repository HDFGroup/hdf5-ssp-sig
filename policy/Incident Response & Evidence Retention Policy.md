# Incident Response & Evidence Retention Policy

**Policy intent:** Prepare for security incidents affecting code, build systems, releases, or plugin ecosystem; preserve evidence for remediation, audits, and downstream notifications. This aligns with the Safe‑OSE plan to maintain an SSP audit archive of artifacts and procedures.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-IR‑01 | The project SHALL maintain an incident response runbook covering: repo compromise, signing key compromise, malicious release, malicious plugin, and vulnerability embargo failure. | `docs/security/ir-runbook.md` | Confirm scenarios covered; check last review date. |
| HDF5-SHINES-IR‑02 | Evidence retention SHALL include CI logs, build inputs, SBOMs, provenance attestations, and release artifacts for a defined retention period (e.g., 2 years). | Retention policy + storage location list. | Verify retention settings; sample retrieval of prior evidence. |
| HDF5-SHINES-IR‑03 | Security-relevant evidence SHALL be integrity-protected (access controls + tamper-evident storage, checksums/signatures). | Hash manifests; signed log bundles. | Verify at-rest integrity controls; sample hash verification. |
| HDF5-SHINES-IR‑04 | Incident communications SHALL include coordinated messages to users and downstream packagers, with clear mitigations. | Comms templates; past incident comms. | Review template; confirm escalation path and approval. |
| HDF5-SHINES-IR‑05 | A post-incident review SHALL be performed and SHALL result in tracked action items and policy updates where needed. | PIR report; action item tracker. | Sample PIR; verify closure of actions. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-IR‑01	| — (gap) | IR runbook + tabletop exercises |
| HDF5-SHINES-IR‑02	| — (gap) | CI retention + artifact storage + release archive index |
| HDF5-SHINES-IR‑03 | OSPS-BR-06.01 (partial) | Signed hash manifests + tamper-evident/WORM storage |
| HDF5-SHINES-IR‑04 | OSPS-VM-04.01 (partial) | Comms templates + escalation roster + announcements history |
| HDF5-SHINES-IR‑05 | — (gap) | Post-incident review docs + action tracker |
