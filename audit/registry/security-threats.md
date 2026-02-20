# HDF5 Registry Security Threats

Risk scoring used: **Severity (1-5) x Likelihood (1-5) = Risk (1-25)**

Risk bands: **1-5 Low, 6-10 Moderate, 11-15 High, 16-20 Very High, 21-25
Critical**

See also: [HDF5 Registry Asset Register](./asset-register.md)

## Threat Register

### 1. Heap-based buffer overflow

Type: `Threat`

What can go wrong:
A crafted HDF5 input can trigger a heap-based buffer overflow, causing a
crash and possible code execution.

Severity: `5`

Likelihood: `3`

Risk: **15 (High)**

Historical examples:

- [CVE-2025-6516](https://nvd.nist.gov/vuln/detail/CVE-2025-6516): A heap-based buffer overflow in `H5F_addr_decode_len` can be triggered by crafted HDF5 input, leading to crashes and potential code execution.
- [CVE-2025-2153](https://nvd.nist.gov/vuln/detail/CVE-2025-2153): A heap-based buffer overflow in `H5SM_delete` can be exploited by malicious HDF5 files, resulting in crashes and possible code execution.
- [CVE-2025-6270](https://nvd.nist.gov/vuln/detail/CVE-2025-6270): A heap-based overflow in `H5FS__sect_find_node` can be triggered by crafted HDF5 input, causing crashes and potential code execution.
- [CVE-2022-26061](https://nvd.nist.gov/vuln/detail/CVE-2022-26061): A heap-based overflow in `gif2h5` can be triggered by crafted GIF input, leading to crashes and potential code execution.
- [CVE-2020-10809](https://nvd.nist.gov/vuln/detail/CVE-2020-10809): A heap-based overflow in `gif2h5` can be triggered by crafted GIF input, leading to crashes and potential code execution.
- [CVE-2019-8396](https://nvd.nist.gov/vuln/detail/CVE-2019-8396): A heap-based overflow in `H5O__layout_encode` can be triggered by crafted HDF5 input during repack, causing crashes and potential code execution.

Top controls (do first):

- Patch and upgrade HDF5 quickly under dependency SLAs.
- Sandbox untrusted-file parsing with least privilege and no secrets.
- Add input limits, including object counts, chunk dimensions, and allocation
  caps, before parsing.
- Isolate ingestion tools such as `h5dump` and `h5repack` in locked-down
  containers.
- Enable hardening, including ASLR, DEP, stack protector, and sanitized CI
  builds.
- Pre-validate metadata sizes and structures before allocation-heavy paths.
- Sandbox parsers and enforce CPU, memory, and time limits.
- Remove or disable tool from production images if unused.
- If needed, run conversion in an isolated job runner with no credentials and
  no network.
- Patch and upgrade the toolchain.
- Run converters with strict resource limits, such as `ulimit`, cgroups, and
  timeouts.
- Quarantine untrusted inputs and validate before conversion.
- Never repack untrusted inputs in privileged environments.
- Repack in a sandbox and validate output before publishing.

### 2. Stack-based overflow

Type: `Threat`

What can go wrong:
A crafted HDF5 input can trigger a stack-based overflow, causing a crash and
possible code execution.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Historical examples:

- [CVE-2025-6857](https://nvd.nist.gov/vuln/detail/CVE-2025-6857): A stack-based overflow in `H5G__node_cmp3` can be triggered by crafted HDF5 input, leading to crashes and potential code execution.

Top controls (do first):

- Patch and upgrade HDF5 quickly.
- Compile with strong stack protections, including canaries and runtime
  hardening.
- Run open, convert, and view workflows in low-privilege sandboxes.

### 3. Out-of-bounds read

Type: `Threat`

What can go wrong:
An out-of-bounds read can cause DoS or information disclosure.

Severity: `4`

Likelihood: `3`

Risk: **12 (High)**

Historical examples:

- [CVE-2018-11205](https://nvd.nist.gov/vuln/detail/CVE-2018-11205): An out-of-bounds read in `H5VM_memcpyvv` can be triggered by crafted HDF5 input, leading to crashes and potential information disclosure.

Top controls (do first):

- Patch and upgrade HDF5.
- Ensure ingestion services keep no in-process secrets, including tokens and
  keys.
- Disable core dumps for ingestion daemons and isolate crash logs.

### 4. Dynamic plugin, filter, or VOL loading abuse

Type: `Threat`

What can go wrong:
Environment variables such as `HDF5_PLUGIN_PATH` can control plugin loading,
and plugins are executable code in the I/O path.

Severity: `5`

Likelihood: `2`

Risk: **10 (Moderate)**

Top controls (do first):

- Disable plugin loading unless required and explicitly control load state.
- Lock plugin directories so they are root-owned and not writable, and ignore
  environment variables in privileged services.
- Use signed or verified plugins, or an allowlisted plugin registry.

### 5. External links can cross file boundaries unexpectedly

Type: `Threat`

What can go wrong:
External links can point to objects in different files, resolve only on
access, and dangle, which can lead to boundary crossing and unintended file
access.

Severity: `4`

Likelihood: `2`

Risk: **8 (Moderate)**

Top controls (do first):

- Disable or gate external-link resolution for untrusted files.
- Allowlist target directories and URIs, and reject absolute paths and `..`
  traversal patterns.
- Run with minimal filesystem visibility and no sensitive mounts.
