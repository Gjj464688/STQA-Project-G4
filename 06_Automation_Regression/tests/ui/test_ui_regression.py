"""Browser layer: a few end-to-end Selenium checks of the most important flows.

Kept deliberately small (top of the test pyramid). The same rules are
covered in more detail, and much faster, by the api and web layers.
"""
from datetime import date, timedelta

import pytest

from pages.auth_page import AuthPage
from pages.tasks_page import DashboardPage, TasksPage

pytestmark = pytest.mark.ui

trace = pytest.mark.trace
PASSWORD = "abcdefghi"


def due(days):
    return (date.today() + timedelta(days=days)).isoformat()


@pytest.fixture
def auth(driver, base_url):
    return AuthPage(driver, base_url)


@pytest.fixture
def tasks(driver, base_url):
    return TasksPage(driver, base_url)


@pytest.fixture
def signed_in(auth, unique_name):
    username = unique_name()
    auth.register(username, PASSWORD)
    return username


@pytest.mark.smoke
@trace("AUTO-UI-001", manual=["TC-BB-001"], req=["R-01"])
def test_register_lands_on_task_list(auth, unique_name):
    username = unique_name()
    auth.register(username, PASSWORD)
    assert auth.heading() == "My Tasks"
    assert auth.signed_in_user() == username


@pytest.mark.known_defect("DEF-W1-001")
@trace("AUTO-UI-002", manual=["TC-BB-007"], req=["R-01"])
def test_register_with_eight_char_password(auth, unique_name):
    auth.register(unique_name("pw8"), "abcdefgh")
    assert auth.error_text() == "", f"Form showed: {auth.error_text()}"
    assert auth.heading() == "My Tasks"


@trace("AUTO-UI-003", manual=["TC-BB-008", "TC-BB-009"], req=["R-02"])
def test_login_correct_then_wrong_password(auth, signed_in):
    auth.logout()
    auth.login(signed_in, "wrongpass1")
    assert auth.error_text() == "Invalid username or password."
    auth.login(signed_in, PASSWORD)
    assert auth.heading() == "My Tasks" and auth.signed_in_user() == signed_in


@pytest.mark.smoke
@trace("AUTO-UI-004", manual=["TC-BB-011"], req=["R-04", "R-07"])
def test_create_task_with_category_and_due_date(tasks, signed_in):
    tasks.create("Lab 6 report", category="Study", due_date=due(5), description="Selenium")
    assert tasks.titles() == ["Lab 6 report"]
    assert tasks.urgency("Lab 6 report") == "Upcoming"


@pytest.mark.smoke
@trace("AUTO-UI-005", manual=["TC-BB-016"], req=["R-06", "R-09"])
def test_mark_done_and_reopen(tasks, signed_in, driver, base_url):
    dashboard = DashboardPage(driver, base_url)
    tasks.create("Toggle in browser")
    tasks.toggle("Toggle in browser")
    assert tasks.is_done("Toggle in browser") and tasks.urgency("Toggle in browser") == "Done"
    assert dashboard.counter("Completed (last 7 days)") == 1
    tasks.open()
    tasks.toggle("Toggle in browser")
    assert not tasks.is_done("Toggle in browser")
    assert dashboard.counter("Completed (last 7 days)") == 0


@trace("AUTO-UI-006", manual=["TC-BB-017"], req=["R-05"])
def test_delete_one_task_with_confirmation(tasks, signed_in):
    tasks.create("Keep in browser")
    tasks.create("Delete in browser")
    tasks.delete("Delete in browser")
    assert tasks.titles() == ["Keep in browser"]


def _contrast_ratio(rgb_a, rgb_b):
    """WCAG 2 contrast ratio between two 'rgb(r, g, b)' / 'rgba(...)' colours."""
    def luminance(css):
        r, g, b = [int(v) for v in css[css.index("(") + 1:css.index(")")].split(",")[:3]]
        def channel(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)
    high, low = sorted((luminance(rgb_a), luminance(rgb_b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


@pytest.mark.smoke
@pytest.mark.known_defect("DEF-W3-001")
@trace("AUTO-UI-008", manual=["ACC-TC-002"], req=["R-11"])
def test_completed_title_text_contrast(tasks, signed_in, driver):
    """Normal-size text needs at least 4.5:1 contrast (WCAG 1.4.3)."""
    tasks.create("Contrast check")
    tasks.toggle("Contrast check")
    cell = tasks.row("Contrast check").find_element("css selector", "td.title-cell")
    text_colour, background = driver.execute_script("""
        const el = arguments[0];
        let node = el, bg = 'rgba(0, 0, 0, 0)';
        while (node) {
            bg = getComputedStyle(node).backgroundColor;
            if (bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') break;
            node = node.parentElement;
            bg = 'rgb(255, 255, 255)';
        }
        return [getComputedStyle(el).color, bg];""", cell)
    ratio = _contrast_ratio(text_colour, background)
    assert ratio >= 4.5, f"{text_colour} on {background} = {ratio:.2f}:1"


@trace("AUTO-UI-007", manual=["TC-BB-010"], req=["R-02"])
def test_logout_blocks_protected_page(auth, signed_in, driver, base_url):
    auth.logout()
    driver.get(f"{base_url}/dashboard")
    assert driver.current_url.endswith("/login")
    assert auth.heading() == "Log in"
