# Security Threat Registry

This folder contains the detailed security threat records for the HDF5 registry.

| ID | Short name | Risk rating |
| --- | --- | --- |
| `ATK-001` | Malicious metadata size and address fields corrupt parser memory | `25 (Critical)` |
| `ATK-002` | Crafted object-header messages overflow metadata serialization paths | `20 (Very High)` |
| `ATK-003` | Heap and shared-message deserialization corrupts core metadata state | `20 (Very High)` |
| `ATK-004` | Built-in filter pipelines overflow during decode and integrity checks | `20 (Very High)` |
| `ATK-005` | Datatype decoding and conversion logic corrupts memory | `20 (Very High)` |
| `ATK-006` | Core vector-copy helpers amplify corruption across many data paths | `20 (Very High)` |
| `ATK-007` | Free-list and cache lifetime bugs permit use-after-free and double free | `15 (High)` |
| `ATK-008` | Stack-based overflows in decode and traversal logic crash the parser | `15 (High)` |
| `ATK-009` | Malformed files can exhaust memory or CPU and deny service | `16 (Very High)` |
| `ATK-010` | Malformed metadata can trigger null or uninitialized pointer dereference | `12 (High)` |
