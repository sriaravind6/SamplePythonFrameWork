"""
environment.py - Behave Hooks
Lifecycle hooks: before_all, before_scenario, after_step, after_scenario.
Screenshots are captured for EVERY step and attached to Allure automatically.
"""

import logging
import allure

from utils.config import Config
from utils.driver_factory import DriverFactory
from utils.screenshot_helper import capture_and_attach

logger = logging.getLogger("environment")


# ═══════════════════════════════════════════════════════════
#  BEFORE ALL
# ═══════════════════════════════════════════════════════════
def before_all(context):
    """
    Runs once before the entire test suite.
    - Validates config
    - Creates required directories
    - Logs config summary
    """
    Config.ensure_directories()
    Config.log_config()

    # Store config on context so steps can access it
    context.config_obj = Config
    logger.info("before_all: Framework initialised.")


# ═══════════════════════════════════════════════════════════
#  BEFORE SCENARIO
# ═══════════════════════════════════════════════════════════
def before_scenario(context, scenario):
    """
    Runs before each scenario.
    - Launches a fresh browser instance
    - Navigates to the base URL
    """
    logger.info(f"▶ Starting scenario: [{scenario.name}]")

    context.driver = DriverFactory.get_driver()
    context.driver.get(Config.BASE_URL)

    logger.info(f"Navigated to: {Config.BASE_URL}")


# ═══════════════════════════════════════════════════════════
#  AFTER STEP
# ═══════════════════════════════════════════════════════════
def after_step(context, step):
    """
    Runs after EVERY step (pass or fail).
    - Captures a screenshot
    - Attaches it to the Allure report with pass/fail context
    """
    step_label = f"{step.keyword} {step.name}"
    status_emoji = "✅" if step.status == "passed" else "❌"
    display_name = f"{status_emoji} {step_label}"

    logger.info(f"after_step [{step.status.upper()}]: {step_label}")

    driver = getattr(context, "driver", None)
    if driver:
        capture_and_attach(driver, step_name=display_name)

    # For failed steps — add additional Allure severity tag
    if step.status == "failed":
        allure.attach(
            f"Step failed: {step_label}\nError: {step.exception}",
            name="Failure Details",
            attachment_type=allure.attachment_type.TEXT,
        )
        logger.error(f"Step FAILED: {step_label} | Error: {step.exception}")


# ═══════════════════════════════════════════════════════════
#  AFTER SCENARIO
# ═══════════════════════════════════════════════════════════
def after_scenario(context, scenario):
    """
    Runs after each scenario.
    - Attaches scenario-level logs
    - Quits the WebDriver
    """
    logger.info(f"◼ Finished scenario: [{scenario.name}] | Status: {scenario.status}")

    # Attach scenario result summary as text
    allure.attach(
        f"Scenario : {scenario.name}\n"
        f"Status   : {scenario.status}\n"
        f"Tags     : {', '.join(scenario.tags) or 'None'}",
        name="Scenario Summary",
        attachment_type=allure.attachment_type.TEXT,
    )

    driver = getattr(context, "driver", None)
    if driver:
        try:
            driver.quit()
            logger.info("WebDriver quit successfully.")
        except Exception as exc:
            logger.warning(f"Error quitting driver: {exc}")
        context.driver = None
