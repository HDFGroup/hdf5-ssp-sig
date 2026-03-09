# Safety Hazards

This folder contains standalone hazard entries for the HDF5 safety hazard registry.

## Hazard Files

- [HAZ-001.md](./HAZ-001.md) - Crash during metadata update (Risk: 20, Very High)
- [HAZ-002.md](./HAZ-002.md) - Concurrent access without safe coordination (Risk: 15, High)
- [HAZ-003.md](./HAZ-003.md) - Extension boundary violates core invariants (Risk: 15, High)
- [HAZ-004.md](./HAZ-004.md) - Metadata and artifacts leak sensitive information (Risk: 12, High)
- [HAZ-005.md](./HAZ-005.md) - Out-of-space (ENOSPC) during write or close (Risk: 15, High)
- [HAZ-006.md](./HAZ-006.md) - False sense of durability from flush (Risk: 12, High)
- [HAZ-007.md](./HAZ-007.md) - SWMR deployment misfit (Risk: 12, High)
- [HAZ-008.md](./HAZ-008.md) - File locking pitfalls or disabling via environment variable (Risk: 12, High)
- [HAZ-009.md](./HAZ-009.md) - Thread-safe build uses a global lock (Risk: 12, High)
- [HAZ-010.md](./HAZ-010.md) - Chunk size too small (Risk: 12, High)
- [HAZ-011.md](./HAZ-011.md) - Deleting data does not shrink files by default (Risk: 12, High)
- [HAZ-012.md](./HAZ-012.md) - Recovery tooling limits (Risk: 12, High)
- [HAZ-013.md](./HAZ-013.md) - High-level API thread-safety gaps (Risk: 9, Moderate)
- [HAZ-014.md](./HAZ-014.md) - Portability hazard from missing filter plugins (Risk: 9, Moderate)
- [HAZ-015.md](./HAZ-015.md) - Misuse of metadata-cache flush controls (Risk: 8, Moderate)
- [HAZ-016.md](./HAZ-016.md) - Chunk cache mis-sizing (`rdcc_nbytes`, `rdcc_nslots`) (Risk: 6, Moderate)
