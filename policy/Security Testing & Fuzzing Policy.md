# Security Testing & Fuzzing Policy

**Policy intent:** Continuously discover parsing, plugin, and ecosystem vulnerabilities proactively (not “whack-a-mole”), consistent with Safe‑OSE and S2‑D2 emphasis on fuzzing, edge cases, and vulnerability testing frameworks.

The HDF5 repo surfaces signals of active security testing such as OSS-Fuzz status and CVE regression indicators.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-TEST‑01 | The project SHALL maintain fuzz harnesses for file parsing and metadata handling, including corpora and minimization workflows. | `tests/fuzz/` (or equivalent); corpus repo location. | Confirm harness exists; verify it is runnable and documented. |
| HDF5-SHINES-TEST‑02 | Fuzzing SHALL be run continuously (nightly minimum) with sanitizers enabled for supported platforms. | CI schedules; sanitizer builds. | Check CI schedules; verify sanitizer jobs run and alert. |
| HDF5-SHINES-TEST‑03 | Plugin loader paths and configuration surfaces (e.g., plugin path variables) SHOULD be fuzzed or adversarially tested. | Targeted tests; fuzz harness notes. | Verify at least one adversarial suite exists for plugin loading. |
| HDF5-SHINES-TEST‑04 | Findings from fuzzing/static/dynamic tools SHALL be triaged with severity and tracked to closure. | Issue labels; triage notes. | Sample 5 findings; verify time-to-triage and closure evidence. |
| HDF5-SHINES-TEST‑05 | Security regression tests SHALL be added for every fixed vulnerability class and retained indefinitely. | Regression test list; mapping to advisories/CVEs. | Sample 3 CVEs; confirm tests exist and are stable.               |
| HDF5-SHINES-TEST‑06 | Security testing metrics (coverage deltas, fuzz exec rate, unique crashes) SHOULD be reported quarterly to the SIG. | Quarterly report. | Verify report exists; verify actions taken on trends. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-TEST‑01 | OSPS-SA-03.01 (partial) | Fuzz harnesses + corpus + docs |
| HDF5-SHINES-TEST‑02 | OSPS-SA-03.01 (partial); OSPS-QA-06.01 (partial) | Scheduled CI + sanitizer builds + OSS-Fuzz refs |
| HDF5-SHINES-TEST‑03 | OSPS-SA-03.01 (partial) | Adversarial plugin loader tests + fuzz targets |
| HDF5-SHINES-TEST‑04 | OSPS-VM-01.01 (partial) | Triage tracker + SLA doc |
| HDF5-SHINES-TEST‑05 | OSPS-QA-06.03 (partial); OSPS-QA-06.01 (partial) | CVE regression tests mapped from advisories |
| HDF5-SHINES-TEST‑06 | OSPS-GV-02.01 (partial) | Quarterly metrics + SIG meeting minutes review |
