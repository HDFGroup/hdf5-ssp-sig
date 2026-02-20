# HDF5 Registry Safety Hazards

Risk scoring used: **Severity (1-5) x Likelihood (1-5) = Risk (1-25)**

Risk bands: **1-5 Low, 6-10 Moderate, 11-15 High, 16-20 Very High, 21-25 Critical**

## Hazard Register

### 1. Crash / power loss / SIGKILL during write

Type: `Hazard`

What can go wrong:
Inconsistent metadata; file may not open; unrelated datasets can become inaccessible; recovery is “very hard.”

Severity: `5`

Likelihood: `4`

Risk: **20 (High)**

Top controls (do first):

- Architect for crash tolerance: write to a new file and atomic rename on “commit”; keep last-good generation.
- Checkpoint via close at safe points (time- or size-based rollover).
- Use SWMR only where it fits and follow its model (see below).

### 2. Dirty metadata window

Type: `Hazard`

What can go wrong:
Metadata cache flush happens later, often at close → you “think it’s written”, but the file is still being updated; a crash can lose/garble recent structure changes.

Severity: `4`

Likelihood: `4`

Risk: **16 (High)**

Top controls (do first):

- Define explicit “durability boundaries”: call `H5Fflush` / `H5Dflush` at checkpoints and/or close/reopen at phases.
- Keep metadata churn low during long acquisition runs (batch structural changes).

### 3. Out-of-space (ENOSPC) during write or close

Type: `Hazard`

What can go wrong:
Writes fail and close itself can fail; no transactional “proper close” exists today; may require process exit to release space/handles.

Severity: `5`

Likelihood: `3`

Risk: **15 (High)**

Top controls (do first):

- Prevent it: enforce free-space headroom (quotas/alerts), preflight capacity before large writes, reserve a safety margin.
- On ENOSPC treat the file as failed (do not keep using it); switch to a new target location/file generation.


### 4. Concurrent readers while a writer is writing without SWMR

Type: `Hazard`

Severity: `5`

Likelihood: `3`

Risk: **15 (High)**

Top controls (do first):

- Adopt SWMR for the single-writer, multi-reader pattern.
- Otherwise enforce external locking and publish via write-then-rename.
- Add crash/restart and concurrency integration tests.

### 5. Multiple writers to the same file outside SWMR

Type: `Hazard`

What can go wrong:
Multiple concurrent writers to a single file can cause corruption.

Severity: `5`

Likelihood: `3`

Risk: **15 (High)**

Top controls (do first):

- Enforce a single-writer architecture with queued writes or file sharding.
- For true concurrency, use a design built for it, such as Parallel
  HDF5/MPI-IO.
- Add a writer lease guardrail, such as PID/host plus heartbeat.

### 6. False sense of durability from flush

Type: `Hazard`

What can go wrong:
HDF5 flushes its buffers then asks the OS to flush; OS buffering is outside HDF5’s full control.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- For high-value checkpoints: combine `H5Fflush` with an operational durability strategy (close file, snapshot/copy, atomic generation switch).
- Document what “durable” means in your environment (local FS vs network FS vs object store).


### 7. SWMR deployment misfit

Type: `Hazard`

What can go wrong:
Requires POSIX `write()` semantics and supports limited writer operations,
which can cause correctness surprises on some storage environments.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Verify filesystem semantics in staging, especially network and HPC FS.
- Follow SWMR programming constraints and document allowed writer ops.
- Add telemetry for reader errors, stale reads, and retry patterns.

### 8. File locking pitfalls or disabling via environment variable

Type: `Hazard`

What can go wrong:
Concurrent access hazards and corruption incidents.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Do not disable locking unless you replace it with robust coordination.
- Standardize environment settings and prevent `HDF5_USE_FILE_LOCKING`
  overrides in production.
- Test locking behavior on the target filesystems.

### 9. Thread-safe build uses a global lock

Type: `Hazard`

What can go wrong:
Throughput collapse and latency spikes because only one thread can enter
HDF5 at a time.

Severity: `3`

Likelihood: `4`

Risk: **12 (High)**

Top controls (do first):

- Prefer multiprocessing and file sharding over threading for heavy I/O.
- Batch reads and writes, and reduce call frequency with larger I/O
  operations.
- Benchmark with representative access patterns.

### 10. Chunk size too small

Type: `Hazard`

What can go wrong:
Severe performance degradation and excess metadata or storage overhead.

Severity: `3`

Likelihood: `4`

Risk: **12 (High)**

Top controls (do first):

- Define organization-wide chunking guidelines, targeting MB-range chunks
  per workload.
- Profile common slicing patterns and align chunks to access patterns.
- Fail fast on pathological chunk configuration in schema validation.

### 11. Deleting data does not shrink files by default

Type: `Hazard`

What can go wrong:
Storage bloat, fragmentation, and operational incidents.

Severity: `3`

Likelihood: `4`

Risk: **12 (High)**

Top controls (do first):

- Adopt file space management strategies plus scheduled repack or compact
  jobs.
- Prefer rolling and time-partitioned files over frequent delete-in-place
  operations.
- Monitor logical versus physical size drift and alert on bloat.

### 12. Recovery tooling limits

Type: `Hazard`

What can go wrong:
`h5clear` helps only in certain SWMR-created cases; otherwise recovery from corrupted metadata is difficult.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Top controls (do first):

- Treat recovery as exceptional: keep last-good generations, backups, and replayable input streams.
- Automate integrity validation in pipelines (detect corruption early).


### 13. High-level API thread-safety gaps

Type: `Hazard`

What can go wrong:
Crashes or undefined behavior when mixing thread-safe settings with
high-level libraries and bindings.

Severity: `3`

Likelihood: `3`

Risk: **9 (Moderate)**

Top controls (do first):

- Standardize a tested build matrix across HDF5 flags and binding versions.
- Run concurrency stress tests in CI, including sanitizers where possible.
- Document the supported threading model for each language binding.

### 14. Portability hazard from missing filter plugins

Type: `Hazard`

What can go wrong:
Datasets become unreadable on systems that lack required filter plugins.

Severity: `3`

Likelihood: `3`

Risk: **9 (Moderate)**

Top controls (do first):

- Standardize approved filters and bundle required plugins in deployed
  apps or containers.
- Validate decoder availability at ingest and fail early.
- Record filter requirements in metadata and data contracts.

### 15. Misuse of metadata-cache flush controls

Type: `Hazard`

What can go wrong:
(`H5Odisable_mdc_flushes`, etc.) → can make data inaccessible or corrupt files if used incorrectly (explicit warning).

Severity: `4`

Likelihood: `2`

Risk: **8 (Moderate)**

Top controls (do first):

- Use these APIs only with a tested “transaction-like” pattern; add invariants/tests; keep usage centralized (not scattered across app code).

### 16. Lack of built-in “crashproof” transactions/WAL in common deployments

Type: `Hazard`

What can go wrong:
Teams assume DB-like safety but don’t have it; active work exists (journaling/WAL/checkpointing) but you can’t assume it’s in your deployed stack.

Severity: `4`

Likelihood: `2`

Risk: **8 (Moderate)**

Top controls (do first):

- Use application-level checkpoint + generation patterns now; track HDF5 crashproofing efforts separately as a roadmap item.


### 17. Chunk cache mis-sizing (`rdcc_nbytes`, `rdcc_nslots`)

Type: `Hazard`

What can go wrong:
Unpredictable regressions, including cases where larger caches are slower.

Severity: `2`

Likelihood: `3`

Risk: **6 (Moderate)**

Top controls (do first):

- Provide known-good cache presets per workload class.
- Add performance regression tests for key queries and slices.
- Expose cache sizing as managed configuration, not ad-hoc script tuning.
