"""API regression layer: JSON endpoints through the Flask test client.

Each test gets an empty database (see the ``pytodo`` fixture). These tests
re-check Week 1 behaviour one layer below the browser: faster and more
stable than UI tests, and they still cover the same requirements.
"""
from datetime import date, timedelta

import pytest

pytestmark = pytest.mark.api

trace = pytest.mark.trace
known_defect = pytest.mark.known_defect


def due(days):
    return (date.today() + timedelta(days=days)).isoformat()


# ---------------------------------------------------------------------------
# Registration and login (R-01, R-02)
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@trace("AUTO-API-001", manual=["TC-BB-001"], req=["R-01"])
def test_register_valid_account(client):
    response = client.post("/api/register", json={"username": "abc", "password": "abcdefghi"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["username"] == "abc" and isinstance(body["id"], int)


@pytest.mark.parametrize("username, status", [
    pytest.param("ab", 400, id="2-chars", marks=trace("AUTO-API-002a", manual=["TC-BB-002"], req=["R-01"])),
    pytest.param("abcdefghijklmnopqrst", 201, id="20-chars", marks=trace("AUTO-API-002b", manual=["TC-BB-003"], req=["R-01"])),
    pytest.param("abcdefghijklmnopqrstu", 400, id="21-chars", marks=trace("AUTO-API-002c", manual=["TC-BB-004"], req=["R-01"])),
    pytest.param("abc-1", 400, id="hyphen", marks=trace("AUTO-API-002d", manual=["TC-BB-005"], req=["R-01"])),
])
def test_register_username_boundaries(client, username, status):
    response = client.post("/api/register", json={"username": username, "password": "abcdefghi"})
    assert response.status_code == status
    if status == 400:
        assert response.get_json() == {"error": "invalid username"}


@trace("AUTO-API-003", manual=["TC-BB-006"], req=["R-01"])
def test_register_rejects_seven_char_password(client):
    response = client.post("/api/register", json={"username": "pw7user", "password": "abcdefg"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "invalid password"}


@pytest.mark.smoke
@known_defect("DEF-W1-001")
@trace("AUTO-API-004", manual=["TC-BB-007"], req=["R-01"])
def test_register_accepts_eight_char_password(client):
    response = client.post("/api/register", json={"username": "pw8user", "password": "abcdefgh"})
    assert response.status_code == 201, response.get_json()


@pytest.mark.smoke
@trace("AUTO-API-005", manual=["TC-BB-008"], req=["R-02"])
def test_login_with_correct_credentials(new_client, api_user):
    api_user("loginuser")
    fresh = new_client()
    response = fresh.post("/api/login", json={"username": "loginuser", "password": "abcdefghi"})
    assert response.status_code == 200
    assert response.get_json()["username"] == "loginuser"
    assert fresh.get("/api/tasks").status_code == 200


@trace("AUTO-API-006", manual=["TC-BB-009"], req=["R-02"])
def test_login_with_wrong_password(new_client, api_user):
    api_user("loginuser")
    fresh = new_client()
    response = fresh.post("/api/login", json={"username": "loginuser", "password": "wrongpass1"})
    assert response.status_code == 401
    assert response.get_json() == {"error": "invalid credentials"}


@pytest.mark.smoke
@trace("AUTO-API-007", manual=["TC-BB-010"], req=["R-02"])
def test_task_list_requires_sign_in(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401
    assert response.get_json() == {"error": "authentication required"}


@trace("AUTO-API-008", manual=[], req=["R-04"])
def test_categories_are_seeded(client):
    names = [row["name"] for row in client.get("/api/categories").get_json()]
    assert names == ["Personal", "Study", "Urgent", "Work"]


# ---------------------------------------------------------------------------
# Task creation, reading, update and deletion (R-04, R-05, R-06)
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@trace("AUTO-API-009", manual=["TC-BB-011"], req=["R-04"])
def test_create_task_with_all_fields(client, api_user, category_ids):
    api_user()
    payload = {"title": "Lab report", "description": "Week 6", "category_id": category_ids["Study"], "due_date": due(5)}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    task = response.get_json()
    assert (task["title"], task["description"], task["category"], task["due_date"]) == (
        "Lab report", "Week 6", "Study", due(5))
    assert task["done"] is False and task["urgency"] == "Upcoming"


@trace("AUTO-API-010", manual=["TC-BB-012"], req=["R-04"])
def test_create_task_without_optional_fields(client, api_user):
    api_user()
    task = client.post("/api/tasks", json={"title": "Minimal"}).get_json()
    assert task["category"] is None and task["due_date"] is None
    assert task["urgency"] == "No due date"


@pytest.mark.parametrize("title", [
    pytest.param("", id="empty", marks=trace("AUTO-API-011a", manual=["TC-BB-013"], req=["R-04"])),
    pytest.param("   ", id="spaces", marks=trace("AUTO-API-011b", manual=["TC-BB-014"], req=["R-04"])),
])
def test_create_task_rejects_blank_title(client, api_user, title):
    """The API strips and rejects blank titles; compare AUTO-WEB-007 for the web form."""
    api_user()
    response = client.post("/api/tasks", json={"title": title})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title is required"}


@trace("AUTO-API-012", manual=["TC-BB-015"], req=["R-05"])
def test_get_and_partially_update_task(client, api_user, category_ids):
    api_user()
    first = client.post("/api/tasks", json={"title": "Draft lab"}).get_json()
    second = client.post("/api/tasks", json={"title": "Untouched"}).get_json()
    response = client.put(f"/api/tasks/{first['id']}", json={
        "title": "Updated lab", "category_id": category_ids["Study"], "due_date": due(2)})
    assert response.status_code == 200
    updated = client.get(f"/api/tasks/{first['id']}").get_json()
    assert (updated["title"], updated["category"], updated["due_date"]) == ("Updated lab", "Study", due(2))
    assert client.get(f"/api/tasks/{second['id']}").get_json()["title"] == "Untouched"


@pytest.mark.smoke
@trace("AUTO-API-013", manual=["TC-BB-016"], req=["R-06"])
def test_mark_done_then_reopen(client, api_user):
    api_user()
    task = client.post("/api/tasks", json={"title": "Toggle me", "due_date": due(1)}).get_json()
    done = client.put(f"/api/tasks/{task['id']}", json={"done": True}).get_json()
    assert done["done"] is True and done["urgency"] == "Done" and done["completed_at"]
    reopened = client.put(f"/api/tasks/{task['id']}", json={"done": False}).get_json()
    assert reopened["done"] is False and reopened["completed_at"] is None
    assert reopened["urgency"] == "Due Soon"


@pytest.mark.smoke
@trace("AUTO-API-014", manual=["TC-BB-017"], req=["R-05"])
def test_delete_own_task(client, api_user):
    api_user()
    keep = client.post("/api/tasks", json={"title": "Keep"}).get_json()
    gone = client.post("/api/tasks", json={"title": "Remove"}).get_json()
    assert client.delete(f"/api/tasks/{gone['id']}").get_json() == {"result": "ok"}
    assert client.get(f"/api/tasks/{gone['id']}").status_code == 404
    assert client.get(f"/api/tasks/{keep['id']}").status_code == 200


@trace("AUTO-API-015", manual=["TC-BB-018"], req=["R-03"])
def test_task_list_shows_only_own_tasks(new_client, api_user):
    alice, bob = new_client(), new_client()
    api_user("alice_reg", on=alice)
    api_user("bob_reg", on=bob)
    alice.post("/api/tasks", json={"title": "Alice only"})
    bob.post("/api/tasks", json={"title": "Bob only"})
    assert [t["title"] for t in bob.get("/api/tasks").get_json()] == ["Bob only"]


# ---------------------------------------------------------------------------
# Urgency labels (R-07): boundary values around today
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("offset, label", [
    pytest.param(None, "No due date", id="no-date", marks=trace("AUTO-API-016a", manual=["TC-BB-012"], req=["R-07"])),
    pytest.param(-1, "Overdue", id="yesterday", marks=trace("AUTO-API-016b", manual=["TC-BB-019"], req=["R-07"])),
    pytest.param(0, "Due Today", id="today", marks=[
        pytest.mark.smoke, known_defect("DEF-W1-002"),
        trace("AUTO-API-016c", manual=["TC-BB-020"], req=["R-07"])]),
    pytest.param(1, "Due Soon", id="plus-1", marks=trace("AUTO-API-016d", manual=["TC-BB-021"], req=["R-07"])),
    pytest.param(2, "Due Soon", id="plus-2", marks=trace("AUTO-API-016e", manual=["TC-BB-022"], req=["R-07"])),
    pytest.param(3, "Upcoming", id="plus-3", marks=trace("AUTO-API-016f", manual=["TC-BB-023"], req=["R-07"])),
])
def test_urgency_label(client, api_user, offset, label):
    api_user()
    payload = {"title": f"Due {offset}", "due_date": None if offset is None else due(offset)}
    task = client.post("/api/tasks", json=payload).get_json()
    assert task["urgency"] == label


# ---------------------------------------------------------------------------
# Filters, search and dashboard (R-08, R-09): Week 1 decision table
# ---------------------------------------------------------------------------

@pytest.fixture
def four_task_fixture(client, api_user, category_ids):
    """Work open A, Work done B, Personal open C, Personal done D (Week 1 fixture)."""
    api_user("filteruser1")
    ids = {}
    for title, category in [("Work open A", "Work"), ("Work done B", "Work"),
                            ("Personal open C", "Personal"), ("Personal done D", "Personal")]:
        ids[title] = client.post("/api/tasks", json={"title": title, "category_id": category_ids[category]}).get_json()["id"]
    for title in ("Work done B", "Personal done D"):
        client.put(f"/api/tasks/{ids[title]}", json={"done": True})
    return client


@pytest.mark.parametrize("query, expected", [
    pytest.param("category=Work&status=open", ["Work open A"], id="work-open",
                 marks=trace("AUTO-API-017a", manual=["TC-BB-024"], req=["R-08"])),
    pytest.param("category=Work&status=done", ["Work done B"], id="work-done",
                 marks=trace("AUTO-API-017b", manual=["TC-BB-025"], req=["R-08"])),
    pytest.param("category=Personal&status=open", ["Personal open C"], id="personal-open",
                 marks=trace("AUTO-API-017c", manual=["TC-BB-026"], req=["R-08"])),
    pytest.param("status=done", ["Personal done D", "Work done B"], id="any-done",
                 marks=trace("AUTO-API-017d", manual=["TC-BB-027"], req=["R-08"])),
    pytest.param("q=open", ["Personal open C", "Work open A"], id="search-open",
                 marks=trace("AUTO-API-017e", manual=["TC-BB-028"], req=["R-08"])),
])
def test_filters_and_search(four_task_fixture, query, expected):
    titles = [t["title"] for t in four_task_fixture.get(f"/api/tasks?{query}").get_json()]
    assert titles == expected


@pytest.mark.smoke
@trace("AUTO-API-018", manual=["TC-BB-029"], req=["R-09"])
def test_dashboard_counts(four_task_fixture):
    counts = four_task_fixture.get("/api/dashboard").get_json()
    assert counts == {"total": 4, "open": 2, "overdue": 0, "due_soon": 0, "completed_this_week": 2}


# ---------------------------------------------------------------------------
# Week 4 confirmed robustness defects (one regression check each)
# With TESTING=True, Flask passes the app's unhandled exceptions to the test,
# so while a defect is open the test stops with that exception (XFAIL).
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@known_defect("DEF-W4-001")
@trace("AUTO-API-019", manual=["API-32"], req=["R-04", "R-10"])
def test_number_title_is_rejected_cleanly(client, api_user):
    api_user()
    response = client.post("/api/tasks", json={"title": 123})
    assert response.status_code == 400


@pytest.mark.smoke
@known_defect("DEF-W4-002")
@trace("AUTO-API-020", manual=["API-42"], req=["R-05", "R-10"])
def test_null_title_update_is_rejected_cleanly(client, api_user):
    api_user()
    task = client.post("/api/tasks", json={"title": "Keep my title"}).get_json()
    response = client.put(f"/api/tasks/{task['id']}", json={"title": None})
    assert response.status_code == 400
    assert client.get(f"/api/tasks/{task['id']}").get_json()["title"] == "Keep my title"


@pytest.mark.smoke
@known_defect("DEF-W4-003")
@trace("AUTO-API-021", manual=["API-49", "API-50"], req=["R-04", "R-10"])
def test_invalid_due_date_is_rejected_and_list_still_works(client, api_user):
    api_user()
    response = client.post("/api/tasks", json={"title": "Invalid Date Test", "due_date": "not-a-date"})
    assert response.status_code == 400
    assert client.get("/api/tasks").status_code == 200
