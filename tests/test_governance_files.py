import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _read(name: str) -> str:
    path = ROOT / name
    assert path.exists(), f"Missing required file: {name}"
    return path.read_text(encoding="utf-8")


def test_charter_has_required_sections():
    text = _read("CHARTER.md")
    # minimal structure checks; extend as needed
    for heading in [
        "# HDF5 Safety, Security & Privacy (SSP) SIG — Charter",
        "## 1. Purpose",
        "## 2. Scope",
        "## 3. Membership & Roles",
        "## 4. Operating Rhythm",
        "## 5. Decision-Making",
    ]:
        assert heading in text, f"Expected heading not found: {heading}"


def test_governance_exists_and_mentions_decision_log():
    text = _read("GOVERNANCE.md")
    assert "Decision lifecycle" in text or "Decision Lifecycle" in text
    assert "DECISION_LOG.md" in text, "Governance should reference DECISION_LOG.md"


def test_security_policy_mentions_coordinated_disclosure():
    text = _read("SECURITY.md")
    assert "coordinated disclosure" in text.lower()
