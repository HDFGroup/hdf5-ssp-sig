# HDF5 Security Threat Model

This document defines a *security* threat model for the HDF5 library and file format using the **CASSE** approach (“Core library, Application, Storage, System, External libraries”). CASSE was introduced specifically for data management libraries (DML) to overcome the limitations of traditional threat models such as STRIDE.

**Reference:** [https://dl.acm.org/doi/full/10.1145/3731599.3767556](https://dl.acm.org/doi/full/10.1145/3731599.3767556)

## Contents

- [1) Scope and security goals](#1-scope-and-security-goals)
- [2) CASSE model](#2-casse-model)
- [3) Threat enumeration workflow](#3-threat-enumeration-workflow)
- [4) Practical examples](#4-practical-examples)
- [5) Attack register template](#5-attack-register-template)
- [6) Threat taxonomy aligned with HDF5 SSP SIG vulnerability categories](#6-threat-taxonomy-aligned-with-hdf5-ssp-sig-vulnerability-categories)
- [7) Checklist for reviewers](#7-checklist-for-reviewers)

## 1) Scope and security goals

### In scope

- HDF5 files (on disk structures and semantic expectations)
- Core HDF5 library (parsing, APIs, caching, SWMR, etc.)
- Extension points (VOL connectors, VFDs, filters, language bindings, tools)
- Build/distribution and “how users actually get HDF5” (packages, containers, CI outputs)
- Typical deployments: desktop, HPC, cloud object stores, embedded/edge workflows

### Primary security goals (what we defend)

- **Integrity**: stored data/metadata and transformations are correct and detectable when incorrect
- **Availability**: reading/writing does not allow easy denial of service or resource exhaustion
- **Confidentiality** (where relevant): prevent unauthorized disclosure via security weaknesses
- **Execution safety**: parsing untrusted inputs must not lead to arbitrary code execution
- **Supply chain integrity**: users can verify what code they are running

## 2) CASSE model

For security work, the most useful unit is the attack chain:

> **Source -> Method -> Target**

CASSE classifies attacks by combining:

- **Source**: `Data` or `Library`
- **Method**: `Modification` or `Poisoning`
- **Target**: one of `Core library`, `Application`, `Storage`, `System`, `External libraries`

So an attack label looks like: **Data • Poisoning • Core library**.

CASSE is most effective when we maintain three complementary models.

### Data-flow diagram (DFD)

A DFD shows the layers/trust boundaries data passes through. For HDF5, this includes external data sources, the application, the core library, extensions (filters/VOL/VFD), and storage backends.

```mermaid
flowchart LR
  subgraph H["HDF5"]
    direction TB
    H_app["Application"]
    H_ext["External Interface<br/>(e.g., H5py)"]
    H_api["HDF5 Public API"]
    H_vol["VOL Connector"]
    H_core["Core HDF5 Library"]
    H_vfd["VFD"]
    H_storage["Storage"]

    %% Raw data path
    H_app --> H_api

    %% SDDL object path
    H_app --> H_ext
    H_ext --> H_api
    H_api --> H_vol
    H_vol --> H_core
    H_core --> H_vfd

    %% File path
    H_vol --> H_storage
    H_vfd --> H_storage
  end

  subgraph L["Legend"]
    direction TB
    lr0(( )) --> lr1["Raw Data"]
    ls0(( )) --> ls1["SDDL Objects"]
    lf0(( )) --> lf1["Files"]
  end

  style lr0 fill:none,stroke:none
  style ls0 fill:none,stroke:none
  style lf0 fill:none,stroke:none

  %% Links:
  %% 0 app->api
  %% 1 app->ext, 2 ext->api, 3 api->vol, 4 vol->core, 5 core->vfd
  %% 6 vol->storage, 7 vfd->storage
  %% 8 raw legend, 9 sddl legend, 10 files legend

  %% Raw Data (dotted)
  linkStyle 0,8 stroke-dasharray: 2 2,stroke-width:2px

  %% SDDL Objects (dash-dot)
  linkStyle 1,2,3,4,5,9 stroke-dasharray: 8 3 2 3,stroke-width:2px

  %% Files (thick dashed)
  linkStyle 6,7,10 stroke-dasharray: 10 4,stroke-width:3px
```

### Abstract data model

This model captures how HDF5 objects relate (groups, datasets, attributes, datatypes, etc.), data shape, element types and layout.

```mermaid
flowchart TB
    root["Root Group (/)"]

    root -->|+| sub["Sub Group"]
    root -->|+| cdt["Committed<br/>Datatype"]
    root -->|+| dset["Dataset"]
    root -->|+| rattr["Attribute"]

    rattr --> rtype["Datatype"]
    rattr --> rspace["Dataspace"]
    rattr --> rdata["Data"]

    sub -->|+| subAttr["Attribute"]
    sub --> more["..."]

    cdt -->|+| cdtAttr["Attribute"]

    dset -->|+| dsAttr["Attribute"]
    dset --> dsSpace["Dataspace"]
    dset --> dsType["Datatype"]
    dset --> dsData["Data"]

    classDef dashed stroke-dasharray: 5 5,fill:#fff,stroke:#333,color:#111;
    class rtype,rspace,subAttr,cdtAttr,dsAttr,dsSpace,dsType dashed;
```

### Concrete/on-disk model

This model captures key on-disk structures and pointers/offsets that parsers traverse and where critical pointers/offsets/sizes are that attackers might target. For HDF5, this includes the superblock, object headers, B-trees, message lists, references, external links, etc.

```mermaid
flowchart TB
    SB["Superblock"] --> OH0["Object Header<br/>(Root Group)"]

    OH0 --> M0["Message<br/>(B-Tree)"]
    OH0 -->|+| M0x["Message"]
    M0 --> BT["B-Tree"]

    BT --> OH1["Object Header<br/>(Dataset)"]
    BT -->|+| OH2["Object Header<br/>(Com. Datatype)"]
    BT -->|+| OH3["Object Header<br/>(Subgroup)"]

    OH1 --> M1["Message<br/>(Layout)"]
    OH1 -->|+| M1x["Message"]
    M1 --> D["Data"]

    OH2 --> M2["Message"]
    OH3 --> M3["Message"]

    classDef msg stroke-dasharray: 5 5,fill:#fff,stroke:#333,color:#111;
    class M0,M0x,M1,M1x,M2,M3 msg;
```

## 3) Threat enumeration workflow

### Step 0 — Set boundaries and assumptions

Document:

- what inputs are **untrusted**
- where plugins may be loaded from
- where data may cross trust boundaries (internet, shared FS, object store)
- which workloads must remain available (HPC job, cloud service, device)

### Step 1 — Build the DFD + identify trust boundaries

- Add a boundary anywhere the *trust level changes* (external file → internal parse, plugin load, network I/O, etc.)
- List the critical data flows: read path, write path, conversion, plugin discovery, distribution

### Step 2 — Model HDF5 structures that matter for attacks

Focus on:

- **links/offsets/pointers** (B-trees, message lists, references, external links)
- **sizes and counts** (datatype sizes, dataspace dims, chunk indexing, heap sizes)
- **parsing hot paths** (superblock, object headers, messages, filters, VFD/VOL entry points)

### Step 3 — Enumerate attacks using CASSE combinations

Start with the highest-risk combinations (typical for DMLs):

- **Data • Poisoning • Core library**
- **Data • Poisoning • External libraries**
- **Library • Poisoning • Application/System/Storage**
- **Data • Poisoning • Storage** (DML-controlled I/O patterns can DoS backends)

### Step 4 — Attach vulnerability mechanisms and evidence

For each attack, record:

- which **CWE-like weakness** it uses (bounds errors, integer overflows, improper validation, unsafe deserialization, etc.)
- which components are affected (format parser, filter pipeline, plugin loader, tool)
- how to reproduce (test case, fuzz seed, PoC file)
- expected impact and exploitability (rough triage is fine at first)

### Step 5 — Map to HDF5 SSP SIG vulnerability categories

The HDF5 SSP SIG uses categories spanning the stack (FMT, LIB, EXT, TCD, OPS, PRV, SCD, UNK). For each CASSE attack entry, tag it with **one or more** of these categories (see §6).

### Step 6 — Turn threats into mitigations + tests

Threat modeling is only “done” when we create:

- mitigations (code changes, defaults, policies, docs)
- regression tests (fuzz seeds, negative tests, signature checks)
- operational guidance (hardening options, safe configs)

## 4) Practical examples

### Example 1 — Data • Poisoning • Core library (FMT/LIB)

**Scenario**: A crafted HDF5 file triggers a parsing edge case leading to out-of-bounds write.

- Source: Data (untrusted file)
- Method: Poisoning (malicious file distributed)
- Target: Core library
- Likely categories: **FMT**, **LIB**
- Typical outcomes: crash, memory corruption, possible code execution

**Mitigations**:

- bounds checks and sanity limits for counts/offsets
- fuzzing (including checksum/integrity-aware fuzzing where relevant)
- “fail-closed” parsing policies for invalid structures

### Example 2 — Data • Poisoning • External libraries (EXT/TCD/SCD)

**Scenario**: A workflow reads a file that causes it to load a third-party filter/VOL/VFD with unsafe behavior.

- Source: Data
- Method: Poisoning (file expects a plugin/filter by ID or environment-driven discovery)
- Target: External libraries (plugins)
- Likely categories: **EXT**, **SCD**, sometimes **OPS** (misconfiguration)

**Mitigations**:

- policy-driven plugin loading (allowlist, version constraints)
- signature verification for plugins
- sandboxing/isolation for plugin execution

### Example 3 — Data • Poisoning • Storage (OPS)

**Scenario**: An attacker publishes a dataset with extremely small chunks so reading it causes many tiny I/O ops, overloading a shared filesystem or object store.

- Source: Data
- Method: Poisoning
- Target: Storage
- Likely categories: **OPS** (and possibly **FMT** if layout metadata is abused)

**Mitigations**:

- enforce minimum chunk sizes / I/O rate limits in pipelines
- preflight scanning of chunk layouts before “full ingest”
- storage-side throttling and workload isolation

### Example 4 — Library • Poisoning • System (SCD/TCD)

**Scenario**: A trojanized HDF5 binary/package is installed and executes arbitrary code on load.

- Source: Library
- Method: Poisoning (compromised distribution)
- Target: System
- Likely categories: **SCD**, **TCD**

**Mitigations**:

- signed artifacts, verified provenance, reproducible builds
- SBOMs + dependency pinning
- constrained execution environments for high-risk contexts

## 5) Attack register template

```markdown
## ATK-###: <short name>
- CASSE: <Data|Library> • <Modification|Poisoning> • <Core|App|Storage|System|External>
- HDF5 SSP vulnerability tags: <FMT|LIB|EXT|TCD|OPS|PRV|SCD|UNK>
- Preconditions:
- Trigger / entry point:
- Vulnerability mechanism (CWE-style):
- Expected impact:
- Exploitability notes:
- Detection:
- Mitigations:
- Tests / evidence:
- Owner / status / milestone:
```

## 6) Threat taxonomy aligned with HDF5 SSP SIG vulnerability categories

Use this table to tag each threat (many threats span multiple categories):

| Vulnerability category | What to look for in a security review | CASSE targets most often affected |
| --- | --- | --- |
| **FMT** (File format) | ambiguous specs, crafted structures, pointer/offset abuse, malformed metadata | Core library, Storage |
| **LIB** (Core library) | memory safety bugs, UB, race conditions, insecure defaults, parsing hot paths | Core library, System |
| **EXT** (Extensions/plugins) | plugin hijacking, unsafe filters/VOL/VFD, covert channels, privilege misuse | External libraries, System, Storage |
| **TCD** (Toolchain/deps) | vulnerable deps, unpinned builds, insecure build scripts, wrapper flaws | Application, External libraries, System |
| **OPS** (Operational/usage) | misconfigurations, unsafe file sharing, logging leaks, missing access controls | Application, Storage |
| **PRV** (Privacy-specific) | security weaknesses that enable disclosure (distinct from accidental exposure) | Core library, Application, External |
| **SCD** (Supply chain/dist.) | unsigned artifacts, typosquatting, compromised repos, provenance gaps | System, Application |
| **UNK** (Unknown) | novel vulnerability classes, cross-layer chains | Any |

## 7) Checklist for reviewers

### When a change touches parsing or on-disk structures

- [ ] require negative tests for invalid sizes/offsets
- [ ] add fuzz seeds for new messages/layouts
- [ ] add explicit resource limits (time/memory)

### When a change touches plugin loading

- [ ] document trust assumptions
- [ ] provide a safe default (deny/allow list) for high-risk contexts
- [ ] add tests for path hijack and “fail closed” behavior

### When a change touches distribution

- [ ] ensure artifacts are signed and verifiable
- [ ] publish SBOMs
- [ ] ensure CI produces reproducible outputs where feasible
  