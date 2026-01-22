# Contributing (Audit Evidence Repo)

- Do not commit secrets (tokens, private keys, customer data).
- Prefer immutable references (release tags, CI run URLs, signed digests).
- If something is not applicable, use `NOT_APPLICABLE.md` and explain why.

## Add a new release evidence set

1. `python scripts/new_release.py <component> <version>`
2. Replace `PLACEHOLDER.md` files with evidence
3. Update `proofs/<component>/index.md` and root `index.md`
4. Run `python scripts/check_scaffold.py`
