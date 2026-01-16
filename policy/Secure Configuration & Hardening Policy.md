# Secure Configuration & Hardening Policy

**Policy intent:** Provide secure-by-default options that do not unduly break existing applications, while enabling stronger enforcement for high-assurance deployments. 

Safe‑OSE proposes policy-driven runtime enforcement (YAML/JSON), including controlling minimum file format version and preventing DoS/resource exhaustion.
HDF5 plugin loading behavior can be controlled via APIs and environment variables such as `HDF5_PLUGIN_PRELOAD` and `HDF5_PLUGIN_PATH`, which are therefore security-relevant surfaces.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-HARD‑01 | The project SHALL document a “baseline” and “hardened” configuration profile (including plugin behavior). | `docs/security/hardening.md` | Verify profiles exist; verify each maps to settings/options. |
| HDF5-SHINES-HARD‑02 | Security-relevant environment variables and runtime knobs SHALL be enumerated with guidance for locking down in production. | Hardening guide section on env vars. | Confirm list completeness; confirm mitigations (allowlist paths, disable env overrides). |
| HDF5-SHINES-HARD‑03 | Hardened profile SHOULD support: signed‑plugin enforcement, plugin allowlisting, and optional disabling of dynamic plugin loading. | Build/runtime options; examples. | Verify options are testable and documented with examples. |
| HDF5-SHINES-HARD‑04 | The library SHOULD provide or recommend resource-limiting controls to reduce file‑based DoS (bounds on sizes, recursion, allocations). | Limits documentation; tests. | Review limits; confirm tests exist and defaults are safe. |
| HDF5-SHINES-HARD‑05 | Debug and diagnostic logging SHALL avoid leaking sensitive metadata by default; sensitive logging MUST be explicitly enabled and documented. | Logging policy + redaction rules. | Sample logs in default mode; verify sensitive fields are absent. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-HARD‑01 | OSPS-DO-01.01 (partial) | Hardening guide + baseline/hardened profiles |
| HDF5-SHINES-HARD‑02 | OSPS-DO-01.01 (partial) | Enumerated runtime knobs/env vars + lockdown guidance |
| HDF5-SHINES-HARD‑03 | OSPS-BR-06.01 (partial) | Signed-plugin enforcement examples + allowlists |
| HDF5-SHINES-HARD‑04 | OSPS-SA-03.01 (partial); OSPS-QA-06.01 (partial) | Resource limits + parsing limit tests + DoS guidance |
| HDF5-SHINES-HARD‑05 | — (gap) | Logging policy + redaction rules + default log samples |
