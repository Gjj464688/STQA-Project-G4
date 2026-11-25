"""Page object for the register, login and logout flows."""
from selenium.webdriver.common.by import By

from pages.waits import click_and_wait_for_new_page


class AuthPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def _submit(self, path, username, password, button):
        self.driver.get(f"{self.base_url}{path}")
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        button_el = self.driver.find_element(By.XPATH, f"//button[normalize-space()='{button}']")
        click_and_wait_for_new_page(self.driver, button_el)

    def register(self, username, password):
        self._submit("/register", username, password, "Register")

    def login(self, username, password):
        self._submit("/login", username, password, "Log in")

    def logout(self):
        click_and_wait_for_new_page(self.driver, self.driver.find_element(By.LINK_TEXT, "Log out"))

    def error_text(self):
        errors = self.driver.find_elements(By.CSS_SELECTOR, "p.error")
        return errors[0].text if errors else ""

    def signed_in_user(self):
        users = self.driver.find_elements(By.CSS_SELECTOR, ".nav-user")
        return users[0].text if users else None

    def heading(self):
        return self.driver.find_element(By.TAG_NAME, "h1").text
