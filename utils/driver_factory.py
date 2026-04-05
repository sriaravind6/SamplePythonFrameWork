"""
driver_factory.py - WebDriver Initialization Factory
Supports Chrome (default), Firefox, and Edge via WebDriver Manager.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.config import Config

logger = logging.getLogger("driver_factory")


class DriverFactory:
    """
    Factory class to create and configure Selenium WebDriver instances.
    Uses webdriver-manager to auto-download the correct driver binary.
    """

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
        """
        Instantiate and return a configured WebDriver.

        Args:
            browser  : Browser name override (chrome | firefox | edge).
                       Falls back to Config.BROWSER.
            headless : Headless mode override. Falls back to Config.HEADLESS.

        Returns:
            Configured Selenium WebDriver instance.
        """
        browser = (browser or Config.BROWSER).lower()
        headless = headless if headless is not None else Config.HEADLESS

        logger.info(f"Initialising '{browser}' driver | headless={headless}")

        if browser == "chrome":
            driver = DriverFactory._chrome_driver(headless)
        elif browser == "firefox":
            driver = DriverFactory._firefox_driver(headless)
        elif browser in ("edge", "msedge"):
            driver = DriverFactory._edge_driver(headless)
        else:
            raise ValueError(
                f"Unsupported browser: '{browser}'. "
                "Supported values: chrome | firefox | edge"
            )

        # ── Common Post-Init Settings ─────────────
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        driver.maximize_window()

        logger.info(f"'{browser}' WebDriver started successfully.")
        return driver

    # ─────────────────────────────────────────────
    # Private Browser Builders
    # ─────────────────────────────────────────────

    @staticmethod
    def _chrome_driver(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if headless:
            options.add_argument("--headless=new")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _firefox_driver(headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _edge_driver(headless: bool) -> webdriver.Edge:
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        if headless:
            options.add_argument("--headless=new")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
