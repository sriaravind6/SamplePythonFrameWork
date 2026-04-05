"""
screenshot_helper.py - Screenshot Capture Utility
Handles screenshot creation, storage, and Allure report attachment.
"""

import os
import re
import logging
from datetime import datetime

import allure
from selenium import webdriver
from utils.config import Config

logger = logging.getLogger("screenshot_helper")


def _sanitise_name(name: str) -> str:
    """Replace characters that are unsafe in file names."""
    return re.sub(r"[^\w\-]", "_", name)


def take_screenshot(driver: webdriver.Remote, step_name: str) -> str | None:
    """
    Capture a screenshot and save it to the screenshots directory.

    Args:
        driver    : Active Selenium WebDriver instance.
        step_name : Descriptive label (used in the file name).

    Returns:
        Absolute path of the saved screenshot file, or None on failure.
    """
    if driver is None:
        logger.warning("Screenshot skipped — driver is None.")
        return None

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_name = _sanitise_name(step_name)
        filename = f"{timestamp}_{safe_name}.png"
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)

        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved → {filepath}")
        return filepath

    except Exception as exc:
        logger.error(f"Failed to capture screenshot for step '{step_name}': {exc}")
        return None


def attach_screenshot_to_allure(
    filepath: str,
    name: str = "Screenshot",
) -> None:
    """
    Attach a PNG screenshot file to the current Allure report step.

    Args:
        filepath : Absolute path to the PNG file.
        name     : Display name shown in the Allure report.
    """
    if not filepath or not os.path.isfile(filepath):
        logger.warning(f"Allure attach skipped — file not found: {filepath}")
        return

    try:
        allure.attach.file(
            filepath,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        logger.debug(f"Screenshot attached to Allure: {name}")
    except Exception as exc:
        logger.error(f"Failed to attach screenshot to Allure: {exc}")


def capture_and_attach(
    driver: webdriver.Remote,
    step_name: str,
) -> str | None:
    """
    Convenience function: capture screenshot and attach it to Allure in one call.

    Args:
        driver    : Active Selenium WebDriver instance.
        step_name : Step description used for file name and Allure display.

    Returns:
        Absolute path of the saved screenshot, or None on failure.
    """
    filepath = take_screenshot(driver, step_name)
    if filepath:
        attach_screenshot_to_allure(filepath, name=step_name)
    return filepath
