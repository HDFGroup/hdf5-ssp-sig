# Data Handling & Privacy Policy

**Policy intent:** Ensure users are clear on how HDF5 handles user data, what HDF5 does/does not protect by default, and recommended options to implement added protection.

Safe‑OSE highlights operational/privacy risks such as metadata leakage and logging leaks, and notes the lack of built-in privacy mechanisms in current HDF5 usage patterns.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-PRIV‑01 | Project documentation SHALL clearly state what HDF5 does/does not protect by default (data vs metadata, logs), and provide safe usage guidance. | Privacy/security guidance page. | Verify clarity and accuracy; check for misleading claims. |
| HDF5-SHINES-PRIV‑02 | Logging and diagnostics SHALL be designed to avoid exposing user identifiers and sensitive metadata unless explicitly enabled. | Logging policy + tests. | Review default logs; confirm sensitive fields absent. |
| HDF5-SHINES-PRIV‑03 | If integrity/encryption features are introduced, the project SHALL publish threat model assumptions and key management expectations (CRYPTO alignment). | Design docs + threat model updates. | Confirm alignment with CRYPTO and TM controls. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-PRIV‑01 | OSPS-DO-01.01 (partial) | Privacy/security guidance with explicit statements on defaults |
| HDF5-SHINES-PRIV‑02 | — (gap) | Logging tests + redaction verification |
| HDF5-SHINES-PRIV‑03 | OSPS-SA-03.02 (partial); OSPS-BR-07.02 (partial) | Integrity/encryption design + key mgmt expectations + TM updates |
