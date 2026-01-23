#!/usr/bin/env bash
# collect-evidence.sh — minimal evidence capture for PRISUPP-2204-style checksum mismatch
set -euo pipefail

RELEASE_VERSION="${RELEASE_VERSION:-2.0.0}"
SUPPORT_URL="${SUPPORT_URL:-}"
GITHUB_URL="${GITHUB_URL:-}"
SUPPORT_FILE="${SUPPORT_FILE:-support.tar.gz}"
GITHUB_FILE="${GITHUB_FILE:-github.tar.gz}"

mkdir -p artifacts/{support,github,logs,diffs}

echo "[*] Downloading artifacts..."
curl -L "$SUPPORT_URL" -o "artifacts/support/${SUPPORT_FILE}"
curl -L "$GITHUB_URL"    -o "artifacts/github/${GITHUB_FILE}"

echo "[*] Checksums..."
sha256sum "artifacts/support/${SUPPORT_FILE}" "artifacts/github/${GITHUB_FILE}" | tee "artifacts/logs/sha256sum.txt"
sha512sum "artifacts/support/${SUPPORT_FILE}" "artifacts/github/${GITHUB_FILE}" | tee "artifacts/logs/sha512sum.txt"

echo "[*] Unpack..."
rm -rf work && mkdir -p work/{support,github}
tar -xf "artifacts/support/${SUPPORT_FILE}" -C work/support --strip-components=1
tar -xf "artifacts/github/${GITHUB_FILE}"       -C work/github   --strip-components=1

echo "[*] Manifests..."
for d in fossies github support; do
  ( cd work/$d &&     find . -type f -print0 | sort -z | xargs -0 sha256sum > ../../artifacts/diffs/${d}.file-sha256.txt &&     find . -printf '%y %m %u %g %s %p\n' | LC_ALL=C sort > ../../artifacts/diffs/${d}.stat.txt )
done

echo "[*] Diffs (non-fatal)..."
diff -u artifacts/diffs/support.file-sha256.txt artifacts/diffs/github.file-sha256.txt | tee artifacts/diffs/filehash.diff || true
diff -ruN work/support work/github | tee artifacts/diffs/tree.diff || true

echo "[*] Done. Fill EVIDENCE-TABLE.md and SAFE-OSE-evidence.md with the results."
