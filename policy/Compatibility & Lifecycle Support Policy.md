# Compatibility & Lifecycle Support Policy

**Policy intent:** Balance HDF5’s strong interoperability expectations with security realities (vulnerable legacy deployments and upgrade inertia).

Broad compatibility can reduce upgrade incentives and keep vulnerable versions in long-term use.

HDF5 release process documentation states maintenance releases are backward- and forward-compatible for the file format and notes interface compatibility caveats and reporting.

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-COMP‑01 | The project SHALL publish a compatibility contract covering: file format, API, ABI, and plugin interfaces (what is guaranteed vs not). | `docs/compatibility.md` referencing official guidance. | Confirm contract exists; confirm it matches observed practices. |
| HDF5-SHINES-COMP‑02 | Supported versions/branches and end-of-support (EOS) dates SHALL be published. | Support matrix page. | Verify it’s current; confirm old branches marked EOS. |
| HDF5-SHINES-COMP‑03 | Security fixes SHALL be backported to supported branches according to severity and feasibility, with transparent disclosure of what is/not patched. | Backport policy; advisory notes. | Sample one high severity issue; verify backport decision record. |
| HDF5-SHINES-COMP‑04 | Breaking changes SHALL require migration guidance and advance notice (forum/newsletter/discussions), unless urgent for security. | Migration doc; announcement references. | Verify one recent change followed this process. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-COMP‑01 | OSPS-DO-01.01 (partial) | Compatibility docs + compatibility macros references |
| HDF5-SHINES-COMP‑02 | OSPS-DO-04.01 (partial); OSPS-DO-05.01 (partial) | Support/EOS matrix + release branch list |
| HDF5-SHINES-COMP‑03 | OSPS-DO-05.01 (partial) | Backport decision records + fixed-version lists |
| HDF5-SHINES-COMP‑04 | OSPS-DO-04.01 (partial); OSPS-DO-05.01 (partial) | Migration guides + deprecation notices |
