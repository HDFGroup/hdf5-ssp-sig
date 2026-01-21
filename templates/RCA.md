# Root‑Cause and Lessons‑Learned Template

## Background

### Trigger

What happened, when, and how it was detected. Include affected versions/components and blast radius.

### Containment

Immediate steps taken to stop impact and restore service/safety.

### 5 Whys

1. Why did it happen?
2. Why was that possible?
3. Why wasn’t it prevented?
4. Why wasn’t it detected sooner?
5. Why wasn’t the impact smaller?

### Contributing Factors

Environment, process, tooling, human, dependencies, third‑party, documentation.

### Corrective Actions (CAs)

Concrete fixes to remove root cause(s). Each CA has: owner, due date, verification method, rollback plan.

### Preventive Actions (PAs)

Systemic changes to prevent recurrence (guardrails, automation, checklists, training, policy).

### Verification

How you’ll prove the controls/changes work (tests, chaos drills, audit artifacts, metrics/thresholds).

### Communications

Who needs to know what, by when (internal teams, users, partners, board), plus artifacts (changelog, release notes, advisories).

## SSDF + NIST mapping

Map each RCA item to [NIST SSDF v1.1, Practice RV.3 (Identify and Confirm Root Causes of Vulnerabilities)](https://csrc.nist.gov/pubs/sp/800/218/final):

* **RV.3.1 – Capture incident/vuln details** → Trigger, Containment
* **RV.3.2 – Analyze to find root causes** → 5 Whys, Contributing Factors
* **RV.3.3 – Prioritize and implement remediations** → Corrective Actions
* **RV.3.4 – Update processes/controls to prevent recurrence** → Preventive Actions, Communications

And align **Verification** with [NIST SP 800‑53A Rev.5](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final): verify control effectiveness (evidence that the change works in practice), not just checklist completion. Examples:

* Evidence: test logs, CI runs, signed release artifacts, SBOM diffs, monitoring alerts suppressed/converted to SLO‑healthy, drill results.
* Methods: examination, interviews, testing (unit/integration/fuzz/chaos), continuous monitoring.

## Lightweight template

```md
# RCA: <Title>  (ID: <INC-1234>)  | Owner: <name>  | Date: <YYYY-MM-DD>

## Trigger

- Event & detection:
- Scope/impact:
- Versions/components:

## Containment

- Steps taken:
- Time to contain/restore:

## 5 Whys

1. Why did it happen?
2. Why was that possible?
3. Why wasn’t it prevented?
4. Why wasn’t it detected sooner?
5. Why wasn’t the impact smaller?

## Contributing Factors

- Environment:
- Process:
- Tooling:
- Human:
- Dependencies/3rd-party:
- Documentation:

## Corrective Actions (RV.3.3)

| CA ID | Action | Owner | Due | Evidence/Verification | Status |
|------|--------|-------|-----|-----------------------|--------|

## Preventive Actions (RV.3.4)

| PA ID | Change (policy/process/automation/training) | Owner | Due | Evidence/Verification | Status |

## Verification (800-53A)

- What we will test:
- How we will test (methods, frequency):
- Pass criteria (metrics/SLOs):
- Artifacts to store (where):

## Communications

- Audiences & messages:
- Artifacts (advisory, release notes, changelog):
- Deadlines:

```
