# HDF5 Registry Asset Register

This register lists primary HDF5 assets and interfaces that are likely attacker targets for software weaknesses, misconfiguration, and inappropriate API use.

## Asset Register

| Asset / Interface | Primary CWE Families | Typical Attack Preconditions | Recommended Guardrails |
| --- | --- | --- | --- |
| Core file parser (superblock, object headers, message decoders) | `CWE-787`, `CWE-125`, `CWE-122`, `CWE-121`, `CWE-119`, `CWE-20` | Attacker can supply or influence an HDF5 file | Parse in sandbox, patch quickly, strict metadata bounds before allocation |
| Address/offset/size math paths (metadata decode/encode, free-space structures) | `CWE-190`, `CWE-191`, `CWE-131`, `CWE-704` | Crafted metadata with extreme or invalid sizes or offsets | Checked arithmetic helpers, fail-closed on overflow or underflow, fuzz edge-size cases |
| Datatype conversion and memory-move routines | `CWE-787`, `CWE-126`, `CWE-127`, `CWE-704` | Mismatched datatype or shape metadata, conversion from untrusted files | Validate source and target extents, conversion invariants, sanitizer-backed CI |
| Chunk and filter pipeline (including decompression) | `CWE-122`, `CWE-787`, `CWE-770`, `CWE-400`, `CWE-789` | Attacker controls chunk dimensions or filter parameters | Hard limits on chunk dimensions and allocation, decompression quotas, CPU and memory and time caps |
| Plugin or VOL or VFD dynamic loading (`HDF5_PLUGIN_PATH`, preload) | `CWE-427`, `CWE-20` | Environment variables or writable plugin paths influence runtime | Disable by default, allowlist or signed plugins, ignore environment overrides in privileged services |
| External-link resolution and path handling | `CWE-22`, `CWE-200` | File includes external links; service has broad filesystem visibility | Disable or gate for untrusted files, path allowlists, reject absolute and `..` targets |
| CLI tools (`h5dump`, `h5repack`, converters like `gif2h5`) | `CWE-122`, `CWE-787`, `CWE-125`, `CWE-400` | Untrusted files reach tooling pipelines | Run tools in isolated containers, least privilege, remove from production images if unused |
| Memory lifecycle and error-unwind paths | `CWE-416`, `CWE-415`, `CWE-476`, `CWE-401` | Complex failures during parse or transform, repeated cleanup paths | Ownership discipline, single-free patterns, ASan and UBSan in CI, regression tests per CVE class |
| Concurrency and locking and SWMR interfaces | `CWE-362` | Multiple readers or writers, disabled locking, SWMR misuse | Single-writer architecture, enforced locking policy, SWMR-only where semantics fit |
| Resource-governor surfaces (object counts, recursion depth, cache growth) | `CWE-770`, `CWE-400`, `CWE-789` | Large or adversarial metadata graphs | Configurable hard caps, safe defaults, monitor and abort on budget exhaustion |
| Logging and crash artifacts and diagnostics | `CWE-200` | Crash on malicious input with sensitive process context | Redact defaults, disable core dumps for ingestion daemons, isolate crash logs |
| Language bindings and high-level loaders using HDF5 | `CWE-20`, `CWE-502`, `CWE-200` | Application loads untrusted `.h5` without trust checks | Treat files as untrusted input, isolate load path, enforce explicit safe-load policy |
