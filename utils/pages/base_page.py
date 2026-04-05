"""
base_page.py - Base Page Object
All page objects inherit from this class.
Provides shared WebDriver utilities and explicit wait helpers.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.config import Config

logger = logging.getLogger("base_page")


class BasePage:
    """
    Base class for all Page Objects.
    Wraps common Selenium actions so individual pages stay clean and DRY.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    # ─────────────────────────────────────────────
    #  Element Finders
    # ─────────────────────────────────────────────

    def find(self, locator):
        """Wait for element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        """Wait for element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_visible(self, locator) -> bool:
        """Return True if element is visible on page."""
        try:
            self.find(locator)
            return True
        except Exception:
            return False

    # ─────────────────────────────────────────────
    #  Actions
    # ─────────────────────────────────────────────

    def click(self, locator):
        """Click an element after waiting for it to be clickable."""
        element = self.find_clickable(locator)
        element.click()
        logger.debug(f"Clicked: {locator}")

    def type_text(self, locator, text):
        """Clear field and type text."""
        field = self.find(locator)
        field.clear()
        field.send_keys(text)
        logger.debug(f"Typed '{text}' into: {locator}")

    def get_text(self, locator) -> str:
        """Return visible text of an element."""
        element = self.find(locator)
        return element.text

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title
