"""
dashboard_page.py - Dashboard Page Object
Encapsulates all UI interactions with the post-login Dashboard page.

Page URL: https://practicetestautomation.com/logged-in-successfully/

Rule: This file ONLY knows about the page UI.
      It does NOT contain any test assertions or business logic.
"""

import logging
from selenium.webdriver.common.by import By
from utils.pages.base_page import BasePage

logger = logging.getLogger("dashboard_page")


class DashboardPage(BasePage):
    """
    Page Object for the Dashboard (Logged-In) page.
    Inherits common utilities from BasePage.
    """

    # ─────────────────────────────────────────────
    #  Locators
    # ─────────────────────────────────────────────
    _PAGE_HEADING   = (By.CSS_SELECTOR, "h1.post-title")
    _SUCCESS_TEXT   = (By.CSS_SELECTOR, ".post-content p")
    _LOGOUT_BUTTON  = (By.CSS_SELECTOR, "a.wp-block-button__link")

    # ─────────────────────────────────────────────
    #  Page Actions
    # ─────────────────────────────────────────────

    def click_logout(self):
        """Click the Logout button."""
        logger.info("Clicking logout button")
        self.click(self._LOGOUT_BUTTON)

    # ─────────────────────────────────────────────
    #  Data Readers
    # ─────────────────────────────────────────────

    def get_heading_text(self) -> str:
        """Return the main page heading text."""
        return self.get_text(self._PAGE_HEADING)

    def get_success_message(self) -> str:
        """Return the success paragraph text."""
        return self.get_text(self._SUCCESS_TEXT)

    def is_dashboard_displayed(self) -> bool:
        """Return True if the page heading is visible."""
        return self.is_visible(self._PAGE_HEADING)
