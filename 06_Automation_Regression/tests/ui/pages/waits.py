"""Shared wait helper: after a click that submits a form, wait for the new page."""
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT_S = 10


def click_and_wait_for_new_page(driver, element, after_click=None):
    """Click, optionally handle a dialog, then wait until the new page has loaded.

    Without a wait, a test can read the old page (or navigate away) before the
    server's response has loaded, so results depend on timing.

    The first version used Selenium's built-in staleness_of() condition. In
    agent run 1 that caused a setup ERROR: while the page was changing, Chrome
    answered "Node with given id does not belong to the document", an error
    staleness_of() does not expect. This version treats any error during the
    page change as "still loading" and then also waits for the new document to
    finish loading.
    """
    old_page = driver.find_element("tag name", "html")
    element.click()
    if after_click:
        after_click()

    def old_page_gone(drv):
        try:
            old_page.tag_name  # still attached: old page is showing
            return False
        except StaleElementReferenceException:
            return True
        except WebDriverException:
            return False  # mid-navigation; ask again

    def new_page_loaded(drv):
        try:
            return drv.execute_script("return document.readyState") == "complete"
        except WebDriverException:
            return False

    WebDriverWait(driver, TIMEOUT_S).until(old_page_gone)
    WebDriverWait(driver, TIMEOUT_S).until(new_page_loaded)
