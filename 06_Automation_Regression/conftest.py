"""Shared PyTest setup for the Week 6 regression suite.

The suite tests the supplied PyTodo Pro source without changing it:

* The app folder is found from the PYTODO_SOURCE_DIR environment variable
  (the same one the Week 3/4 runners use; PYTODO_APP_DIR also works), or
  defaults to a ``pytodo_pro_student`` folder beside the project folder.
* Every test that touches the app gets its own empty SQLite file in a
  temporary folder, so tests never share data and the real
  ``pytodo_pro.db`` is never opened.
* Two custom markers keep the suite traceable:
    @pytest.mark.trace("AUTO-API-001", manual=["TC-BB-001"], req=["R-01"])
    @pytest.mark.known_defect("DEF-W1-001")
  A known-defect test is run as a strict expected failure. While the defect
  is present it reports XFAIL. If the app is fixed it reports a failing
  XPASS, which tells the team to retest the defect and update its status.
* A small plugin writes one JSON line per test to the evidence folder so the
  runner can map results back to manual test cases.
"""
import hashlib
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
DEFAULT_APP_DIR = HERE.parents[1] / "pytodo_pro_student"
APP_DIR = Path(os.environ.get("PYTODO_SOURCE_DIR") or os.environ.get("PYTODO_APP_DIR") or DEFAULT_APP_DIR).resolve()

# SHA-256 of the supplied files, as recorded in Weeks 1 and 2.
BASELINE_HASHES = {
    "app.py": "050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f",
    "helpers.py": "bf9140338277534439b38599f5ac3ef722880cced732bba8f1f313147d466d80",
}

VALID_PASSWORD = "abcdefghi"  # 9 characters: accepted by the current app


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def app_version_info():
    """Return hashes of the app under test and whether they match the baseline."""
    info = {"app_dir": str(APP_DIR), "files": {}}
    for name, expected in BASELINE_HASHES.items():
        path = APP_DIR / name
        actual = sha256(path) if path.exists() else None
        info["files"][name] = {"sha256": actual, "matches_week1_baseline": actual == expected}
    info["matches_week1_baseline"] = all(f["matches_week1_baseline"] for f in info["files"].values())
    return info


# ---------------------------------------------------------------------------
# Markers and known-defect handling
# ---------------------------------------------------------------------------

def pytest_configure(config):
    if not (APP_DIR / "app.py").exists():
        raise pytest.UsageError(
            f"PyTodo Pro source not found at {APP_DIR}.\n"
            "Extract pytodo_pro_student.zip next to the STQA_Week5_6 folder, "
            "or set PYTODO_SOURCE_DIR to the folder that contains app.py."
        )
    config.addinivalue_line("markers", "trace(auto_id, manual=(), req=()): link to manual cases")
    config.addinivalue_line("markers", "known_defect(defect_id): strict expected failure for an open defect")


def pytest_collection_modifyitems(config, items):
    for item in items:
        marker = item.get_closest_marker("known_defect")
        if marker:
            defect = marker.args[0]
            item.add_marker(pytest.mark.xfail(
                strict=True,
                reason=f"{defect} is open; this test confirms it is still present",
            ))


def pytest_report_header(config):
    info = app_version_info()
    state = "matches Week 1/2 baseline" if info["matches_week1_baseline"] else "DIFFERS from Week 1/2 baseline"
    return [f"PyTodo Pro under test: {APP_DIR} ({state})"]


# ---------------------------------------------------------------------------
# Result log for the runner
# ---------------------------------------------------------------------------

def _trace_of(item):
    marker = item.get_closest_marker("trace")
    if not marker:
        return {"auto_id": None, "manual": [], "req": []}
    auto_id = marker.args[0]
    manual = list(marker.kwargs.get("manual", ()))
    req = list(marker.kwargs.get("req", ()))
    return {"auto_id": auto_id, "manual": manual, "req": req}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    log_dir = os.environ.get("REGRESSION_EVIDENCE_DIR")
    if not log_dir:
        return
    # Record the call phase, or the setup phase if setup failed or skipped.
    if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
        if report.when == "setup":
            result = "ERROR" if report.failed else "SKIPPED"
        elif hasattr(report, "wasxfail"):
            # Expected failure observed (defect still present).
            result = "XFAIL" if report.skipped else "XPASS"
        elif report.failed and "XPASS(strict)" in str(report.longrepr):
            # Known-defect test unexpectedly passed: the defect may be fixed.
            result = "XPASS"
        else:
            result = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIPPED"}[report.outcome]
        defect_marker = item.get_closest_marker("known_defect")
        layer = next((m for m in ("unit", "api", "web", "ui") if item.get_closest_marker(m)), None)
        record = {
            "nodeid": item.nodeid,
            "layer": layer,
            "smoke": bool(item.get_closest_marker("smoke")),
            "result": result,
            "duration_s": round(report.duration, 4),
            "known_defect": defect_marker.args[0] if defect_marker else None,
            **_trace_of(item),
        }
        if result in ("FAIL", "ERROR", "XPASS"):
            text = str(report.longrepr)
            error_lines = [line[1:].strip() for line in text.splitlines() if line.startswith("E ")]
            record["message"] = (error_lines[0] if error_lines else text.splitlines()[-1])[:300]
        with open(Path(log_dir) / "results.jsonl", "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# App fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app_module():
    """Import the supplied app.py once, unchanged."""
    if str(APP_DIR) not in sys.path:
        sys.path.insert(0, str(APP_DIR))
    module = importlib.import_module("app")
    module.app.config["TESTING"] = True
    return module


@pytest.fixture(scope="session")
def helpers_module(app_module):
    """The helpers module the app itself imported."""
    return sys.modules["helpers"]


@pytest.fixture
def pytodo(app_module, tmp_path, monkeypatch):
    """Point the app at a fresh, empty database for one test."""
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "regression.db"))
    app_module.init_db()
    return app_module


@pytest.fixture
def new_client(pytodo):
    """Factory for independent clients (separate cookie jars / sessions)."""
    def make():
        return pytodo.app.test_client()
    return make


@pytest.fixture
def client(new_client):
    return new_client()


@pytest.fixture
def api_user(client):
    """Register through the API; the client stays signed in as that user."""
    def register(username="reguser", password=VALID_PASSWORD, on=None):
        target = on or client
        response = target.post("/api/register", json={"username": username, "password": password})
        assert response.status_code == 201, response.get_json()
        return response.get_json()
    return register


@pytest.fixture
def category_ids(client):
    rows = client.get("/api/categories").get_json()
    return {row["name"]: row["id"] for row in rows}
