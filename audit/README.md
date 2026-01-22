# Safe-OSE Audit Evidence Repo (Scaffold)

Evidence vault for Safe‑OSE audits covering:

- **hdf5-core**
- **hdfview**

Structure follows **Policy → Process → Proof** with an audit index per component/version.

## Quick start

```bash
python scripts/check_scaffold.py
python scripts/new_release.py hdf5-core 2.0.0
python scripts/new_release.py hdfview 3.4.0
```

Then populate the five MUST‑HAVE proof folders under `proofs/<component>/<version>/`.

Scaffold created: **2025-12-18**
