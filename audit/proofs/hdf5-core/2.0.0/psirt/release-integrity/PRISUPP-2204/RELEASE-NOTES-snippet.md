# Source integrity / checksum note (PRISUPP-2204)

Some users observed that the checksum of the **HDF Group source tarball** for **HDF5 `<RELEASE_VERSION>`** differs from the checksum of the **GitHub auto-generated “Source code” archive** for the same tag.

## Support source artifact

The support release source artifact is the HDF Group tarball:

- `<SUPPORT_TARBALL_URL>`

## Checksums

Support tarball:

- SHA-256: `<SHA256_SUPPORT>`
- SHA-512: `<SHA512_SUPPORT>`

GitHub auto-archive (informational):

- URL: `<GITHUB_ARCHIVE_URL>`
- SHA-256: `<SHA256_GITHUB>`
- SHA-512: `<SHA512_GITHUB>`

## Verification performed (summary)

- Tag `<GITHUB_TAG>` points to commit `<COMMIT_SHA>` and `<TAG_SIGNATURE_STATUS>`.
- Unpacked-content comparison result: `<MATCH_RESULT>` (for example: “code matches; differences limited to archive metadata / generated files”).

**Conclusion:** `<DECISION>` — `<RATIONALE>`

## Recommendation

For supply-chain verification, prefer the support tarball plus published checksums (and any provided signature). GitHub “Source code” archives are provided for convenience and may differ at the byte level even when the underlying code is the same.
