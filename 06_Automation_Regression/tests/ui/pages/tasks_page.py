"""Page objects for the task list, task form and dashboard."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.waits import click_and_wait_for_new_page


class TasksPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(f"{self.base_url}/")

    def create(self, title, category=None, due_date=None, description=""):
        self.driver.get(f"{self.base_url}/tasks/new")
        self.driver.find_element(By.NAME, "title").send_keys(title)
        self.driver.find_element(By.NAME, "description").send_keys(description)
        if category:
            Select(self.driver.find_element(By.NAME, "category_id")).select_by_visible_text(category)
        if due_date:
            # Date inputs read typed keys in the computer's locale order
            # (dd/mm/yyyy in Malaysia); setting the ISO value avoids that.
            field = self.driver.find_element(By.NAME, "due_date")
            self.driver.execute_script("arguments[0].value = arguments[1];", field, due_date)
        click_and_wait_for_new_page(
            self.driver, self.driver.find_element(By.XPATH, "//button[normalize-space()='Create Task']"))

    def titles(self):
        return [cell.text for cell in self.driver.find_elements(By.CSS_SELECTOR, "td.title-cell")]

    def row(self, title):
        return self.driver.find_element(
            By.XPATH, f"//tr[td[@class='title-cell' and normalize-space()='{title}']]")

    def urgency(self, title):
        return self.row(title).find_element(By.CSS_SELECTOR, "span.badge").text

    def is_done(self, title):
        return "done" in (self.row(title).get_attribute("class") or "").split()

    def toggle(self, title):
        click_and_wait_for_new_page(self.driver, self.row(title).find_element(By.CSS_SELECTOR, "button.check-btn"))

    def delete(self, title):
        button = self.row(title).find_element(By.XPATH, ".//button[normalize-space()='Delete']")
        # The app asks "Delete this task?" in a browser dialog; accept it.
        click_and_wait_for_new_page(self.driver, button, after_click=lambda: self.driver.switch_to.alert.accept())


class DashboardPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def counter(self, label):
        self.driver.get(f"{self.base_url}/dashboard")
        card = self.driver.find_element(
            By.XPATH, f"//div[@class='stat-label' and normalize-space()='{label}']/..")
        return int(card.find_element(By.CSS_SELECTOR, ".stat-value").text)
