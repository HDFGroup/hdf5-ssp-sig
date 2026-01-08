# HDF5 Privacy Threat (Exposure) Model

This document defines a *privacy* threat model for the HDF5 ecosystem focused on **accidental or unintended exposure** of sensitive information across the HDF5 data lifecycle.

## 1) Scope, assumptions, and non-goals

### Scope (what this model applies to)

- Individual HDF5 files and collections of files
- Objects stored in HDF5 (datasets, groups, named datatypes, attributes)
- HDF5 structural metadata and on-disk layout characteristics
- HDF5 plugins (VOL connectors, VFDs, filters) and tools
- Applications and workflows that create, transform, publish, or archive HDF5 data

### Assumptions (important)

- HDF5 **does not provide privacy by design** and does not enforce privacy standards.
- This model focuses on **accidental or unintended exposure** (not a malicious attacker choosing to exfiltrate data).
- Authentication/authorization/filesystem controls are external to HDF5.
- Privacy risks span the full lifecycle and often **increase over time** as data is reused, aggregated, and shared.
- Plugins, conversion tools, and wrappers can change privacy characteristics.

### Non-goals

- Risk scoring and impact quantification
- Selecting specific legal/regulatory requirements (those are context-dependent)
- Detailed mitigation engineering (we provide practical guidance and artifacts, not an exhaustive controls catalog)

## 2) The exposure chain: Trigger → Exposure surface → Disclosure

For privacy, a useful incident representation is:

### Trigger → Exposure surface → Disclosure

- **Trigger**: a workflow event that changes exposure (publish, convert, log, archive, merge).
- **Exposure surface**: where sensitive information is present or inferable (metadata, layout, derived data, side artifacts).
- **Disclosure**: sensitive information becomes accessible to an unintended audience (often without malicious intent).

## 3) Privacy assets (what needs protection)

Privacy assets include more than raw dataset values.

### 3.1 Data assets

- Datasets, groups, files; datatypes and dataspaces
- **Example:** biomedical signals, genomic data, location traces, proprietary experimental results

### 3.2 Metadata assets (high-risk in self-describing formats)

- Attributes (names, values, units, timestamps)
- Object names (group/dataset/link names)
- Names of compound fields / enumerations
- **Example:** dataset name encodes subject ID; attributes include GPS coordinates or clinician initials

### 3.3 Structural and format-derived assets

- Hierarchy shape, linkage types (external links, object/region references, VDS mappings)
- Storage properties (chunking, external storage, filters used)
- Internal metadata blobs (e.g., global heaps; variable-length strings)
- **Example:** a file’s structure reveals study design or participant count

### 3.4 Side artifacts / workflow emissions

- Logs, error messages, debug dumps
- Temporary/intermediate HDF5 files produced by tools and pipelines
- “Snapshots” or cached metadata copies (e.g., SWMR-related artifacts)
- **Example:** a CI job stores failing test artifacts containing real data

### 3.5 Derived information (inference)

- Sensitive information reconstructed by correlating:
  - multiple HDF5 files,
  - auxiliary datasets (masks, quality flags),
  - metadata conventions,
  - public reference data
- **Example:** re-identification via linkage + timestamps + geolocation

## 4) Threat sources (who/what causes exposure)

Common privacy threat sources include:

- Authorized users acting within expected permissions (but sharing too broadly)
- Applications, plugins, and ecosystem tools (conversion utilities, wrappers)
- Automated workflows (ETL, training pipelines, archiving jobs)
- Interoperability mechanisms (e.g., adding metadata for netCDF4 conventions)
- Publication and archival processes

## 5) Tightened exposure taxonomy

These categories describe **how** information becomes exposed. Each category includes examples and “what to look for”.

### P1 — Semantic metadata exposure (names + attributes)

Sensitive meaning is encoded in user-level metadata.

- Examples: subject IDs in dataset names; attributes with GPS, timestamps, clinician/device IDs; compound field names revealing “raw” semantics.
- **What to look for**: “human-readable” identifiers anywhere a name/value appears.

### P2 — Structural / on-disk leakage

HDF5 internal structures leak information without reading data values.

- Examples: strings in internal metadata, global heaps containing VL strings, layout revealing approximate record counts or data sparsity.
- **What to look for**: leaks visible via low-level inspection tools (even “strings(1)”).

### P3 — Raw-data pattern leakage (even when values are “protected”)

Patterns and representations leak.

- Examples: fixed-length string datasets stored contiguously; descriptive text copies of complex datatypes stored in attributes; partial encryption leaving recognizable headers/blocks.
- **What to look for**: recognizable markers, headers, unencrypted metadata describing encrypted payloads.

### P4 — Unintended inclusion during processing/conversion

Workflows add data or metadata that was not intended for downstream sharing.

- Examples: conversion expands implicit fields into explicit ones; tools attach provenance that includes usernames/paths; intermediate outputs are accidentally packaged.
- **What to look for**: auto-generated attributes, replicated keys, hidden objects, embedded serialized blobs (`pickle`/JSON/XML).

### P5 — Aggregation, correlation, and inference

Non-sensitive elements become sensitive when combined.

- Examples: combining meshes + variables + masks enables sensitive interpretation; joining multiple releases allows re-identification; VDS/external links “point” to sensitive sources.
- **What to look for**: cross-file linkages, auxiliary datasets, stable identifiers, join keys.

### P6 — Persistence beyond intended lifetime (retention failures)

Sensitive material remains accessible longer than intended.

- Examples: temp files, backups, restored snapshots, archived outputs without review, split/onion VFD outputs left behind.
- **What to look for**: retention policies, artifact stores, “working directories” published as-is.

### P7 — Misplaced trust in “privacy by format”

Users assume anonymization or partial encryption is sufficient and skip review.

- Examples: “de-identified” data still leaks via metadata; “encrypted dataset” still reveals structure and labels.
- What to look for: documentation gaps, missing threat review gates, unclear “what is protected”.

## 6) Lifecycle view (where to expect exposures)

| Lifecycle stage | Highest-likelihood categories |
| --- | --- |
| Creation | P1, P2, P3 |
| Storage | P2, P3, P6 |
| Sharing / publication | P1–P7 (all), especially P4–P7 |
| Transfer | P1–P3, P6 |
| Processing / ingestion | P1–P7 (all), especially P4–P5 |
| Archiving | P6, P5, P7 |

## 7) How to apply this model in practice (artifacts + workflow)

### 7.1 Repository artifacts to maintain

Suggested layout:

```text
models/
  Privacy Threats.md
  Privacy/
    data-inventory.md
    classification.md
    exposure-register.md
    redaction-rules.md
    release-privacy-notes.md
    privacy-review-checklist.md
```

Recommended artifacts:

1. **Data inventory**: what files/objects exist, what they contain, owners, intended audience
2. **Sensitivity classification**: what counts as sensitive in your context (IDs, location, health, proprietary)
3. **Exposure register**: entries written as Trigger → Exposure surface → Disclosure, with category tags (P1–P7)
4. **Redaction rules**: naming conventions, attribute allow/deny lists, metadata scrubbing policy
5. **Release privacy notes**: explicit statement of assumptions and residual exposures

### 7.2 Workflow (tight, repeatable)

1. **Classify data early**: decide what is sensitive *before* file layout is finalized.
2. **Design for least disclosure**:
   - avoid encoding sensitive meaning in names and free-text attributes
   - separate sensitive and non-sensitive products when practical
3. **Pre-publication scan** (automate this):
   - scan names/attributes for identifiers
   - inspect internal metadata strings
   - check for external links/references and embedded blobs
4. **Apply redaction / transformation**:
   - scrub/rename metadata
   - remove unintended artifacts (logs, temp outputs)
   - document what was changed and what remains inferable
5. **Gate releases and archives**:
   - require a privacy checklist for “share/publish/archive”
   - store “privacy notes” alongside the data product
6. **Review drift over time**:
   - periodic re-review of archival datasets (new correlation risks emerge)

### 7.3 Exposure register template (copy/paste)

```markdown
## EXP-###: <short name>
- Category: <P1..P7>
- HDF5 SSP vulnerability tags: <PRV|OPS|EXT|FMT|LIB|TCD|SCD|UNK>
- Trigger:
- Exposure surface:
- Disclosure:
- Affected assets:
- Detection (how we would notice):
- Mitigations / process controls:
- Residual risk / assumptions:
- Owner / status / milestone:
```

## 8) Threat taxonomy aligned with HDF5 SSP vulnerability categories

HDF5 SSP vulnerability categories span the ecosystem (FMT, LIB, EXT, TCD, OPS, PRV, SCD, UNK).

For privacy exposures, **PRV** is central, but exposures are often enabled by other categories:

| Vulnerability category | How it shows up in privacy exposures | Most common P-categories |
| --- | --- | --- |
| **PRV** (Privacy-specific) | metadata leakage, traceability, insufficient anonymization, cross-file linkage | P1–P7 |
| **OPS** (Operational/usage) | oversharing, unsafe defaults, logs/artifact retention, weak review gates | P4, P6, P7 |
| **FMT** (File format) | structural metadata leaks, external links, references, VDS mappings | P2, P5 |
| **LIB** (Core library) | debug/error outputs, cache behavior, temp files created by tools | P6, P2 |
| **EXT** (Extensions/plugins) | plugins add metadata, export telemetry, create extra artifacts | P4, P6 |
| **TCD** (Toolchain/deps) | converters/wrappers inject metadata; build/test artifacts leak samples | P4, P6 |
| **SCD** (Supply chain/dist.) | untrusted tooling changes privacy behavior unexpectedly | P4, P7 |
| **UNK** (Unknown) | new leak paths via novel features and emergent conventions | Any |

## 9) Quick checklists

### 9.1 “Before sharing” checklist

- [ ] No sensitive identifiers in names (files, groups, datasets, fields, enums).
- [ ] Attributes reviewed: timestamps, location, device/user IDs, free-text.
- [ ] External links / object references / VDS mappings reviewed.
- [ ] No embedded serialized blobs unless explicitly intended and reviewed.
- [ ] No logs / temp files / intermediate outputs bundled.
- [ ] Release privacy notes written (what is protected vs still inferable).

### 9.2 “Before archiving” checklist

- [ ] Retention and access policy documented.
- [ ] Long-term correlation risk considered (stable IDs, join keys, structure).
- [ ] Provenance and audit metadata reviewed for identifiers.
- [ ] A re-review date/owner assigned.
