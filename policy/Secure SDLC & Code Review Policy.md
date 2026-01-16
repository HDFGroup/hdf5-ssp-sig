# Secure SDLC & Code Review Policy

**Policy intent:** Prevent introduction of SSP defects through disciplined engineering practices appropriate for a widely embedded, security-sensitive parsing library and ecosystem.

This aligns with known HDF5 SSP risk drivers (memory safety, plugins, supply chain, and “AI-generated code risk”).

## Controls

| Control ID | Control statement | Minimum evidence | Audit checklist (how to test) |
| ---------- | ----------------- | ---------------- | ----------------------------- |
| HDF5-SHINES-SDLC‑01 | The default branches SHALL be protected with required reviews and CI status checks before merge. | Branch protection settings export/screenshots; required status checks list. | Verify branch rules; sample 10 merged PRs for compliance. |
| HDF5-SHINES-SDLC‑02 | Security-sensitive changes (file parsing, metadata handling, plugin loader, cryptography, build scripts) SHALL receive at least one review from a designated “security reviewer” or SIG delegate. | PR labels + reviewer list; CODEOWNERS (or equivalent). | Sample PRs touching parsing/plugin areas; confirm reviewer role. |
| HDF5-SHINES-SDLC‑03 | A secure coding standard SHALL be maintained for C/C++ (bounds checks, integer safety, safe alloc patterns, banned APIs, error handling). | `docs/security/secure-coding.md` (or equivalent); lint/static-analysis configuration. | Confirm existence; confirm it is referenced in CONTRIBUTING. |
| HDF5-SHINES-SDLC‑04 | Changes SHALL be risk-ranked (Low/Med/High). High-risk changes SHALL include a security impact note and test plan updates. | PR template fields; security impact section in PR description. | Sample PRs; verify risk ranking + security notes. |
| HDF5-SHINES-SDLC‑05 | CI SHALL run on every PR and SHALL include at least: build, unit/regression tests, and security checks configured by this manual (see TEST/BUILD policies). | `.github/workflows/*` and CI logs; badge/status pages. | Review workflow definitions; confirm required jobs are mandatory for merge. |
| HDF5-SHINES-SDLC‑06 | Maintainer accounts SHALL use strong authentication (MFA) and privileged access SHALL be reviewed at least quarterly. | GitHub org security settings attestation; quarterly access review record. | Request most recent access review record; validate scope and signoff. |

## OSPS crosswalk

See [Open Source Project Security (OSPS) Baseline](https://baseline.openssf.org/versions/devel).

### Status legend

* **covered:** the SHINES control is intended to satisfy that OSPS requirement.
* **partial:** overlaps, but the evidence pointers don’t confirm all OSPS specifics (or OSPS expects additional policy/automation not visible here).
* **gap:** no clear OSPS requirement to map to (often means the SHINES control is additional/beyond OSPS, or OSPS has no equivalent).

| HDF5‑SHINES control | Candidate OSPS control IDs (status) | Basis |
| ------------------- | ----------------------------------- | ----- |
| HDF5-SHINES-SDLC‑01 | OSPS-AC-03.01 (covered); OSPS-AC-03.02 (partial); OSPS-QA-03.01 (covered); OSPS-QA-07.01 (partial) | Branch protection, required status checks, merge rules |
| HDF5-SHINES-SDLC‑02 | OSPS-QA-07.01 (partial) | CODEOWNERS, “security-review” labeling, reviewer roster |
| HDF5-SHINES-SDLC‑03 | OSPS-VM-06.01 (partial); OSPS-VM-06.02 (partial); OSPS-GV-03.02 (partial) | Secure-coding doc + static analysis configs + CONTRIBUTING references |
| HDF5-SHINES-SDLC‑04 | OSPS-GV-03.02 (partial)	| PR template + risk labels/checklists (contribution requirements signal) |
| HDF5-SHINES-SDLC‑05 | OSPS-QA-03.01 (partial); OSPS-QA-06.01 (partial) | CI workflows + logs + “required checks” list |
| HDF5-SHINES-SDLC‑06 | OSPS-AC-01.01 (partial); OSPS-AC-02.01 (partial); OSPS-GV-04.01 (partial); OSPS-GV-01.01 (partial) | Org security settings + quarterly access review minutes |
