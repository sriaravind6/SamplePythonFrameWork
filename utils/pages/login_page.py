"""
login_page.py - Login Page Object
Encapsulates all UI interactions with the Login page.

Page URL: https://practicetestautomation.com/practice-test-login/

Rule: This file ONLY knows about the page UI.
      It does NOT contain any test assertions or business logic.
"""

import logging
from selenium.webdriver.common.by import By
from utils.pages.base_page import BasePage

logger = logging.getLogger("login_page")


class LoginPage(BasePage):
    """
    Page Object for the Login page.
    Inherits common utilities from BasePage.
    """

    # ─────────────────────────────────────────────
    #  Locators (all stored centrally here)
    # ─────────────────────────────────────────────
    _USERNAME   = (By.ID, "username")
    _PASSWORD   = (By.ID, "password")
    _LOGIN_BTN  = (By.ID, "submit")
    _ERROR_MSG  = (By.ID, "error")

    # ─────────────────────────────────────────────
    #  Page Actions
    # ─────────────────────────────────────────────

    def enter_username(self, username: str):
        """Type username into the username field."""
        logger.info(f"Entering username: {username}")
        self.type_text(self._USERNAME, username)

    def enter_password(self, password: str):
        """Type password into the password field."""
        logger.info("Entering password: [hidden]")
        self.type_text(self._PASSWORD, password)

    def click_login(self):
        """Click the Login / Submit button."""
        logger.info("Clicking login button")
        self.click(self._LOGIN_BTN)

    def login(self, username: str, password: str):
        """Convenience method: enter credentials and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_on_login_page(self) -> bool:
        """Return True if the username field is visible (login page loaded)."""
        return self.is_visible(self._USERNAME)

    # ─────────────────────────────────────────────
    #  Data Readers (for assertions in step defs)
    # ─────────────────────────────────────────────

    def get_error_message(self) -> str:
        """Return the error message text shown after a failed login."""
        return self.get_text(self._ERROR_MSG)

    def is_error_displayed(self) -> bool:
        """Return True if an error message is visible."""
        return self.is_visible(self._ERROR_MSG)
