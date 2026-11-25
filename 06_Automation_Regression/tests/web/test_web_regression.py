"""Web regression layer: HTML pages and form posts through the Flask test client.

These tests send the same form fields a browser would, then read the
returned HTML. They cover the Week 1 browser workflows without the cost and
flakiness of driving a real browser; a small Selenium layer (tests/ui)
checks the same flows end to end.
"""
import re
from datetime import date, timedelta

import pytest

pytestmark = pytest.mark.web

trace = pytest.mark.trace
known_defect = pytest.mark.known_defect
PASSWORD = "abcdefghi"


def due(days):
    return (date.today() + timedelta(days=days)).isoformat()


def register(client, username, password=PASSWORD):
    return client.post("/register", data={"username": username, "password": password})


def titles(client, query=""):
    html = client.get(f"/{query}").get_data(as_text=True)
    return [t.strip() for t in re.findall(r'<td class="title-cell">(.*?)</td>', html, re.S)]


def task_ids(client):
    html = client.get("/").get_data(as_text=True)
    return [int(i) for i in re.findall(r"/tasks/(\d+)/edit", html)]


def stats(client):
    html = client.get("/dashboard").get_data(as_text=True)
    pairs = re.findall(r'<div class="stat-value">(\d+)</div>\s*<div class="stat-label">(.*?)</div>', html)
    return {label: int(value) for value, label in pairs}


def create(client, title, category_id="", due_date="", description=""):
    return client.post("/tasks/new", data={
        "title": title, "description": description, "category_id": category_id, "due_date": due_date})


# ---------------------------------------------------------------------------
# Accounts and session (R-01, R-02)
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@trace("AUTO-WEB-001", manual=["TC-BB-001"], req=["R-01"])
def test_register_form_signs_user_in(client):
    response = register(client, "abc")
    assert response.status_code == 302 and response.headers["Location"].endswith("/")
    page = client.get("/").get_data(as_text=True)
    assert "My Tasks" in page and '<span class="nav-user">abc</span>' in page


@trace("AUTO-WEB-002", manual=["TC-BB-005"], req=["R-01"])
def test_register_form_rejects_invalid_character(client):
    page = register(client, "abc-1").get_data(as_text=True)
    assert "Username must be 3-20 characters" in page


@known_defect("DEF-W1-001")
@trace("AUTO-WEB-003", manual=["TC-BB-007"], req=["R-01"])
def test_register_form_accepts_eight_char_password(client):
    response = register(client, "pw8user", password="abcdefgh")
    assert response.status_code == 302, "Registration form re-displayed with an error"


@trace("AUTO-WEB-004", manual=["TC-BB-009"], req=["R-02"])
def test_login_form_rejects_wrong_password(new_client):
    register(new_client(), "loginuser")
    page = new_client().post("/login", data={"username": "loginuser", "password": "wrongpass1"}).get_data(as_text=True)
    assert "Invalid username or password." in page


@pytest.mark.smoke
@trace("AUTO-WEB-005", manual=["TC-BB-010"], req=["R-02"])
def test_logout_then_protected_page_redirects(client):
    register(client, "logoutuser")
    client.get("/logout")
    for path in ("/", "/dashboard", "/tasks/new"):
        response = client.get(path)
        assert response.status_code == 302 and response.headers["Location"].endswith("/login"), path


# ---------------------------------------------------------------------------
# Task workflows (R-03 to R-06)
# ---------------------------------------------------------------------------

@trace("AUTO-WEB-006", manual=["TC-BB-012"], req=["R-04"])
def test_create_task_without_optional_fields(client):
    register(client, "taskuser")
    create(client, "Read chapter 5")
    page = client.get("/").get_data(as_text=True)
    assert titles(client) == ["Read chapter 5"] and "No due date" in page


@pytest.mark.smoke
@known_defect("DEF-W1-004")
@trace("AUTO-WEB-007", manual=["TC-BB-014"], req=["R-04"])
def test_whitespace_only_title_is_rejected(client):
    register(client, "taskuser")
    create(client, "   ")
    assert titles(client) == [], "A task with a blank title was created"


@trace("AUTO-WEB-008", manual=["TC-BB-015"], req=["R-05"])
def test_edit_changes_only_selected_task(client, category_ids):
    register(client, "taskuser")
    create(client, "Draft lab")
    create(client, "Untouched")
    newest, oldest = task_ids(client)  # list is newest first
    client.post(f"/tasks/{oldest}/edit", data={
        "title": "Updated lab", "description": "", "category_id": category_ids["Study"], "due_date": due(2)})
    page = client.get("/").get_data(as_text=True)
    assert titles(client) == ["Untouched", "Updated lab"]
    assert "Study" in page and due(2) in page


@pytest.mark.smoke
@trace("AUTO-WEB-009", manual=["TC-BB-016"], req=["R-06", "R-09"])
def test_toggle_done_and_reopen_updates_dashboard(client):
    register(client, "taskuser")
    create(client, "Toggle me")
    (task_id,) = task_ids(client)
    client.post(f"/tasks/{task_id}/toggle")
    assert stats(client)["Completed (last 7 days)"] == 1 and stats(client)["Open"] == 0
    client.post(f"/tasks/{task_id}/toggle")
    assert stats(client)["Completed (last 7 days)"] == 0 and stats(client)["Open"] == 1


@trace("AUTO-WEB-010", manual=["TC-BB-017"], req=["R-05"])
def test_delete_removes_only_selected_task(client):
    register(client, "taskuser")
    create(client, "Keep me")
    create(client, "Delete me")
    newest, _ = task_ids(client)
    client.post(f"/tasks/{newest}/delete")
    assert titles(client) == ["Keep me"]


@trace("AUTO-WEB-011", manual=["TC-BB-018"], req=["R-03"])
def test_each_user_sees_only_own_list(new_client):
    alice, bob = new_client(), new_client()
    register(alice, "alice_web")
    register(bob, "bob_web")
    create(alice, "Alice private")
    assert titles(bob) == []
    assert titles(alice) == ["Alice private"]


@pytest.mark.parametrize("offset, label", [
    pytest.param(-1, "Overdue", id="yesterday", marks=trace("AUTO-WEB-012a", manual=["TC-BB-019"], req=["R-07"])),
    pytest.param(0, "Due Today", id="today", marks=[
        known_defect("DEF-W1-002"), trace("AUTO-WEB-012b", manual=["TC-BB-020"], req=["R-07"])]),
    pytest.param(3, "Upcoming", id="plus-3", marks=trace("AUTO-WEB-012c", manual=["TC-BB-023"], req=["R-07"])),
])
def test_urgency_badge_in_list(client, offset, label):
    register(client, "dateuser")
    create(client, "Dated task", due_date=due(offset))
    badges = re.findall(r'<span class="badge [^"]*">(.*?)</span>', client.get("/").get_data(as_text=True))
    assert badges == [label]


# ---------------------------------------------------------------------------
# Filters and dashboard (R-08, R-09)
# ---------------------------------------------------------------------------

@pytest.fixture
def filter_fixture(client, category_ids):
    register(client, "filteruser1")
    for title, category in [("Work open A", "Work"), ("Work done B", "Work"),
                            ("Personal open C", "Personal"), ("Personal done D", "Personal")]:
        create(client, title, category_id=category_ids[category])
    ids = dict(zip(titles(client), task_ids(client)))
    for title in ("Work done B", "Personal done D"):
        client.post(f"/tasks/{ids[title]}/toggle")
    return client


@pytest.mark.parametrize("query, expected", [
    pytest.param("?category=Work&status=open", ["Work open A"], id="work-open",
                 marks=trace("AUTO-WEB-013a", manual=["TC-BB-024"], req=["R-08"])),
    pytest.param("?category=Work&status=done", ["Work done B"], id="work-done",
                 marks=trace("AUTO-WEB-013b", manual=["TC-BB-025"], req=["R-08"])),
    pytest.param("?category=Personal&status=open", ["Personal open C"], id="personal-open",
                 marks=trace("AUTO-WEB-013c", manual=["TC-BB-026"], req=["R-08"])),
    pytest.param("?category=&status=done", ["Personal done D", "Work done B"], id="any-done",
                 marks=trace("AUTO-WEB-013d", manual=["TC-BB-027"], req=["R-08"])),
    pytest.param("?q=Personal", ["Personal done D", "Personal open C"], id="search",
                 marks=trace("AUTO-WEB-013e", manual=["TC-BB-028"], req=["R-08"])),
])
def test_list_filters(filter_fixture, query, expected):
    assert titles(filter_fixture, query) == expected


@pytest.mark.smoke
@known_defect("DEF-W3-002")
@trace("AUTO-WEB-015", manual=["ACC-TC-008"], req=["R-11"])
def test_new_task_fields_have_programmatic_labels(client):
    """Each form control needs an id and a <label for="that id"> (WCAG 1.3.1)."""
    register(client, "labeluser")
    html = client.get("/tasks/new").get_data(as_text=True)
    label_targets = set(re.findall(r'<label[^>]*\bfor="([^"]+)"', html))
    for name in ("title", "description", "category_id", "due_date"):
        control = re.search(rf'<(?:input|textarea|select)[^>]*\bname="{name}"[^>]*>', html).group(0)
        control_id = re.search(r'\bid="([^"]+)"', control)
        assert control_id and control_id.group(1) in label_targets, f"'{name}' has no associated label"


@pytest.mark.smoke
@trace("AUTO-WEB-014", manual=["TC-BB-029"], req=["R-09"])
def test_dashboard_page_counters(filter_fixture):
    assert stats(filter_fixture) == {
        "Total Tasks": 4, "Open": 2, "Overdue": 0, "Due Soon": 0, "Completed (last 7 days)": 2}
