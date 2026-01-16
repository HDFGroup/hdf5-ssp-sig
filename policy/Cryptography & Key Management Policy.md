# Cryptography & Key Management Policy

**Policy intent:** Ensure cryptographic features (signatures, integrity mechanisms, potential encryption features) are implemented with modern practices and safe operational key management.

S2‑D2 and SC25 materials emphasize digitally signed plugins and exploring signing tools such as Sigstore and others.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-CRYPTO‑01 | The project SHALL not implement “roll-your-own crypto”; only vetted libraries and standardized algorithms are allowed. | Crypto design doc; dependency list. | Review crypto usage; confirm no bespoke primitives. |
| HDF5-SHINES-CRYPTO‑02 | Signing keys (release signing, plugin signing roots) SHALL be protected with least privilege, logged access, and defined rotation/revocation procedures. | Key management SOP; access logs (redacted). | Confirm rotation/revocation exists; test tabletop “key compromise” drill. |
| HDF5-SHINES-CRYPTO‑03 | Plugin signature verification SHALL validate authenticity and tamper detection and define handling of expired/revoked credentials. | Verification policy; enforcement levels (warn/strict). | Verify behavior in warn vs strict; confirm expired key handling documented. |
| HDF5-SHINES-CRYPTO‑04 | If Sigstore-like keyless signing is used, transparency log references SHOULD be retained as build evidence. | Rekor/log pointers stored with release metadata. | Confirm log entries exist and are retrievable for latest artifacts. |
| HDF5-SHINES-CRYPTO‑05 | Cryptographic configuration defaults SHALL be documented for compliance-sensitive environments (e.g., FIPS expectations), without claiming certification unless achieved. | Compliance notes in hardening guide. | Confirm claims are accurate and scoped. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-CRYPTO‑01 | OSPS-SA-01.01 (partial) | Crypto design doc + dependency list + code refs |
| HDF5-SHINES-CRYPTO‑02 | OSPS-BR-07.02 (partial) | Key management SOP + access logs + rotation schedule |
| HDF5-SHINES-CRYPTO‑03 | OSPS-BR-06.01 (partial); OSPS-DO-03.01 (partial) | Plugin signature verification documentation |
| HDF5-SHINES-CRYPTO‑04 | OSPS-DO-03.02 (partial); OSPS-BR-06.01 (partial) | Transparency log references + attestation metadata |
| HDF5-SHINES-CRYPTO‑05 | — (gap) | Compliance notes + hardening addendum |
