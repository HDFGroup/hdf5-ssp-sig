# HDF5 Registry Privacy Exposures

Risk scoring used: **Severity (1-5) x Likelihood (1-5) = Risk (1-25)**

Risk bands: **1-5 Low, 6-10 Moderate, 11-15 High, 16-20 Very High, 21-25 Critical**

## Exposure Register

### 1. No standard whole-file encryption by default

Type: `Privacy exposure`

What can go wrong:
HDF5 does not provide a standard "encrypt the whole file" mechanism by
default, so teams may store or share sensitive HDF5 files without adequate
protection.

Severity: `5`

Likelihood: `4`

Risk: **20 (Very High)**

Top controls (do first):

- Enforce encryption at rest (filesystem or object store) and TLS in
  transit.
- Centralize key management (KMS/HSM), rotate keys, and audit access.
- Classify datasets and block exporting unencrypted sensitive HDF5 data.

### 2. Metadata leakage even if payload is encrypted

Type: `Privacy exposure`

What can go wrong:
Names, structure, and attributes can reveal meaning, and a description of
what is encoded can remain visible.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Minimize sensitive data in object names and attributes, and use opaque IDs.
- Separate sensitive metadata from HDF5 or encrypt at a layer that also
  covers metadata.
- Add a privacy linter for metadata before publishing.

### 3. Data remanence after dataset deletion

Type: `Privacy exposure`

What can go wrong:
Deleted datasets can leave sensitive bytes in free space, so delete may not
meet secure erase or RTBF requirements.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Use short-lived rolling files and secure destruction for sensitive
  workloads.
- If deletion is required, rebuild or repack into a fresh file in a
  controlled pipeline.
- Document retention and deletion semantics and verify with tests.

### 4. Remote storage VFDs expand the privacy boundary

Type: `Privacy exposure`

What can go wrong:
When using remote storage VFDs such as ROS3 or S3, access control, logging,
and network paths become part of the privacy boundary.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Apply strict bucket and object ACLs, block public access, and use private
  networking.
- Use least-privilege credentials scoped only to required objects.
- Audit access logs and alert on anomalous object reads.

### 5. Credential handling for ROS3 and tooling can leak secrets

Type: `Privacy exposure`

What can go wrong:
Credential passing is cumbersome, and tokens or credentials handled through
APIs, environment variables, or CLI arguments may leak in env dumps, process
lists, or logs.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Prefer instance roles or short-lived tokens over static secrets.
- Never pass secrets on CLI; use standard credential providers or config
  files.
- Scrub environment variables in crash reports and rotate on suspected
  exposure.

### 6. Plugin and filter code can exfiltrate data

Type: `Privacy exposure`

What can go wrong:
Plugins are executable code and are often controlled by environment variables
such as `HDF5_PLUGIN_PATH`.

Severity: `5`

Likelihood: `2`

Risk: **10 (Moderate)**

Top controls (do first):

- Disable plugins by default and enable only required types.
- Lock plugin directories and ignore environment-variable overrides in
  production services.
- Use signed or verified plugins, or an allowlisted plugin registry.

### 7. Object-store access logging can leak identifiers

Type: `Privacy exposure`

What can go wrong:
Operational logging of object-store access patterns can leak object names,
identifiers, and access behavior.

Severity: `3`

Likelihood: `3`

Risk: **9 (Moderate)**

Top controls (do first):

- Treat logs as sensitive, restrict access, redact identifiers, and set
  retention limits.
- Separate performance telemetry from production identifiers by tokenizing or
  hashing.
- Review logging defaults on upgrades, especially ROS3 behavior.

### 8. External links may dangle and leak internal targets

Type: `Privacy exposure`

What can go wrong:
External links may not be validated at creation time, so files can embed
internal endpoints, paths, or identifiers that leak when shared.

Severity: `4`

Likelihood: `2`

Risk: **8 (Moderate)**

Top controls (do first):

- Enforce an allowlist for link targets and reject unknown schemes or paths.
- Rewrite or normalize link targets on export, or remove links entirely.
- Run link resolution with least-privilege filesystem sandboxing.

### 9. External links reveal filenames and object paths

Type: `Privacy exposure`

What can go wrong:
Path disclosure can leak user IDs and internal mount names.

Severity: `3`

Likelihood: `2`

Risk: **6 (Moderate)**

Top controls (do first):

- Strip or prohibit external links in files intended for external sharing.
- Scan for external links during export and in CI publish steps.
- Redact paths in logs and error messages.

### 10. User block can hide arbitrary data

Type: `Privacy exposure`

What can go wrong:
PII or secrets can be embedded outside typical object traversal and overlooked
in reviews.

Severity: `3`

Likelihood: `2`

Risk: **6 (Moderate)**

Top controls (do first):

- Disallow user blocks in regulated datasets unless explicitly justified.
- Require sanitizers to inspect and clear user blocks before publish.
- Add CI checks to detect non-zero user blocks.
