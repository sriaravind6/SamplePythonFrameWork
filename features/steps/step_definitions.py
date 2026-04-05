"""
step_definitions.py - Behave Step Implementations (POM-integrated)
Maps every Gherkin step to a real browser action via Page Objects.

Layer Map:
  Feature File  →  Step Definitions  →  Page Objects  →  BasePage  →  Selenium
"""

import logging

import allure
from behave import given, when, then

from utils.config import Config
from utils.pages.login_page import LoginPage
from utils.pages.dashboard_page import DashboardPage
from utils.screenshot_helper import capture_and_attach

logger = logging.getLogger("step_definitions")


# ─────────────────────────────────────────────
#  POM Helper: create page objects on context
# ─────────────────────────────────────────────
def _login_page(context) -> LoginPage:
    return LoginPage(context.driver)

def _dashboard_page(context) -> DashboardPage:
    return DashboardPage(context.driver)


# ═══════════════════════════════════════════════════════════
#  GIVEN Steps
# ═══════════════════════════════════════════════════════════

@given('the user is on the login page')
@allure.step("Given: User is on the login page")
def step_user_on_login_page(context):
    """Verify login page is ready by checking the username field."""
    logger.info(f"Current URL: {context.driver.current_url}")

    page = _login_page(context)
    assert page.is_on_login_page(), (
        f"Login page not loaded. Current URL: {context.driver.current_url}"
    )
    assert "login" in context.driver.current_url.lower(), (
        f"Expected login URL, got: {context.driver.current_url}"
    )
    logger.info("✅ Login page confirmed.")


# ═══════════════════════════════════════════════════════════
#  WHEN Steps
# ═══════════════════════════════════════════════════════════

@when('the user enters username "{username}" and password "{password}"')
@allure.step("When: Enter username and password")
def step_enter_credentials(context, username, password):
    """Fill login form using the LoginPage POM."""
    logger.info(f"Entering credentials — username: {username}")
    page = _login_page(context)
    page.enter_username(username)
    page.enter_password(password)
    logger.info("Credentials entered.")


@when('the user clicks the login button')
@allure.step("When: Click the login button")
def step_click_login(context):
    """Click the submit/login button via LoginPage POM."""
    _login_page(context).click_login()
    logger.info("Login button clicked.")


@when('the user clicks the logout button')
@allure.step("When: Click the logout button")
def step_click_logout(context):
    """Click the logout button via DashboardPage POM."""
    _dashboard_page(context).click_logout()
    logger.info("Logout button clicked.")


# ═══════════════════════════════════════════════════════════
#  THEN Steps
# ═══════════════════════════════════════════════════════════

@then('the user should be redirected to the dashboard')
@allure.step("Then: User is on the dashboard")
def step_verify_dashboard(context):
    """Assert the dashboard heading confirms successful login."""
    page = _dashboard_page(context)
    heading = page.get_heading_text()

    assert "Logged In Successfully" in heading, (
        f"Expected dashboard heading, got: '{heading}'"
    )
    logger.info(f"✅ Dashboard heading: '{heading}'")


@then('the dashboard should display a success message')
@allure.step("Then: Dashboard shows success message")
def step_verify_success_message(context):
    """Check success paragraph body text and attach it to Allure."""
    page = _dashboard_page(context)
    msg = page.get_success_message()

    assert "Congratulations" in msg or "successfully" in msg.lower(), (
        f"Unexpected message: '{msg}'"
    )
    allure.attach(
        msg,
        name="Dashboard Success Message",
        attachment_type=allure.attachment_type.TEXT,
    )
    logger.info(f"✅ Success message: '{msg}'")


@then('an error message should be displayed')
@allure.step("Then: Error message is visible")
def step_verify_error_visible(context):
    """Assert the error element is displayed on the login page."""
    page = _login_page(context)
    assert page.is_error_displayed(), "Error message is NOT visible."

    context.error_text = page.get_error_message()
    logger.info(f"✅ Error visible: '{context.error_text}'")


@then('the error message should contain "{expected_text}"')
@allure.step("Then: Error message contains expected text")
def step_verify_error_text(context, expected_text):
    """Verify the error text matches expectation."""
    error_text = getattr(context, "error_text", None) or \
                 _login_page(context).get_error_message()

    allure.attach(
        f"Expected : {expected_text}\nActual   : {error_text}",
        name="Error Message Comparison",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert expected_text in error_text, (
        f"Expected '{expected_text}' in error, got: '{error_text}'"
    )
    logger.info(f"✅ Error matches: '{expected_text}' ⊆ '{error_text}'")


@then('the user should be redirected back to the login page')
@allure.step("Then: User is back on the login page")
def step_verify_back_on_login(context):
    """After logout, confirm we are back on the login page."""
    page = _login_page(context)
    assert page.is_on_login_page(), "Username field not visible — not on login page."
    assert "login" in context.driver.current_url.lower(), (
        f"Expected login URL, got: {context.driver.current_url}"
    )
    logger.info(f"✅ Back on login page: {context.driver.current_url}")
