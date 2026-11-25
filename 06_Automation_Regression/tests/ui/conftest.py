"""Selenium setup for the browser layer.

A live copy of the supplied app is served on 127.0.0.1 (port 5002 by
default) from a throwaway database, in a background thread of the test run.
Nothing is started on port 5000, and the real pytodo_pro.db is not used.

Environment variables:
    PYTODO_BROWSER   chrome (default, as in Lab 5) or edge
    PYTODO_HEADED    set to 1 to watch the browser instead of running headless
    PYTODO_UI_PORT   port for the isolated server (default 5002)
    CHROMEDRIVER     optional path to a chromedriver; normally Selenium
                     Manager downloads the right driver automatically
"""
import itertools
import json
import os
import secrets
import sys
import threading
from pathlib import Path

import pytest
from selenium import webdriver
from werkzeug.serving import make_server

PORT = int(os.environ.get("PYTODO_UI_PORT", "5002"))
BROWSER = os.environ.get("PYTODO_BROWSER", "chrome").lower()
HEADED = os.environ.get("PYTODO_HEADED") == "1"
_counter = itertools.count(1)


@pytest.fixture(scope="session")
def ui_database(tmp_path_factory):
    return str(tmp_path_factory.mktemp("ui") / "ui_regression.db")


@pytest.fixture(scope="session")
def live_server(app_module, ui_database):
    original = app_module.DATABASE
    app_module.DATABASE = ui_database
    app_module.init_db()
    server = make_server("127.0.0.1", PORT, app_module.app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{PORT}"
    server.shutdown()
    app_module.DATABASE = original


@pytest.fixture(autouse=True)
def _use_ui_database(app_module, ui_database, monkeypatch):
    # Other layers swap the database per test; keep UI tests on the server's file.
    monkeypatch.setattr(app_module, "DATABASE", ui_database)


@pytest.fixture
def base_url(live_server):
    return live_server


@pytest.fixture
def unique_name():
    """Usernames are unique per test because the UI database is shared by the session."""
    def make(prefix="ui"):
        return f"{prefix}{next(_counter):03d}_{secrets.token_hex(2)}"
    return make


def _make_driver():
    if BROWSER == "edge":
        options = webdriver.EdgeOptions()
    else:
        options = webdriver.ChromeOptions()
    if not HEADED:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    if sys.platform.startswith("linux"):
        options.add_argument("--no-sandbox")
    if BROWSER == "edge":
        return webdriver.Edge(options=options)
    driver_path = os.environ.get("CHROMEDRIVER")
    service = webdriver.ChromeService(executable_path=driver_path) if driver_path else None
    return webdriver.Chrome(options=options, service=service) if service else webdriver.Chrome(options=options)


def _record_browser(drv):
    """Write the browser name/version once per run, for the execution report."""
    folder = os.environ.get("REGRESSION_EVIDENCE_DIR")
    if not folder:
        return
    path = Path(folder) / "browser.json"
    if not path.exists():
        caps = drv.capabilities
        path.write_text(json.dumps({
            "browser": caps.get("browserName"), "version": caps.get("browserVersion"),
            "headless": not HEADED, "window": "1280x900",
        }, indent=2), encoding="utf-8")


@pytest.fixture
def driver(live_server):
    drv = _make_driver()
    drv.implicitly_wait(3)
    _record_browser(drv)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot after each UI test and attach it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return
    folder = Path(os.environ.get("REGRESSION_EVIDENCE_DIR", ".")) / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{item.name}.png"
    drv.save_screenshot(str(path))
    try:
        from pytest_html import extras
        report.extras = getattr(report, "extras", []) + [extras.png(drv.get_screenshot_as_base64())]
    except ImportError:
        pass
