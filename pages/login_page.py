"""
============================================
Login Page Object
============================================
Page Object for the Notes Application Login page.
URL: https://practice.expandtesting.com/notes/app/login

Handles:
- User login with email & password
- Login validation
- Error message extraction
- Navigation to registration page
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.config_reader import get_app_config

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for the Login page of the Notes application.
    Encapsulates all login-related UI interactions.
    """

    # ============================================
    # LOCATORS
    # ============================================
    # Using data-testid attributes where available, with CSS/XPath fallbacks

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-testid='login-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-testid='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-testid='login-submit']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/notes/app/register']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='alert-message']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "[data-testid='logout']")

    # Fallback locators for self-healing
    EMAIL_INPUT_FALLBACK = (By.XPATH, "//input[@type='email' or @name='email' or @placeholder='Email address']")
    PASSWORD_INPUT_FALLBACK = (By.XPATH, "//input[@type='password' or @name='password']")
    LOGIN_BUTTON_FALLBACK = (By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Log in')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.app_config = get_app_config()

    # ============================================
    # PAGE ACTIONS
    # ============================================

    @allure.step("Navigate to Login page")
    def navigate_to_login(self):
        """Opens the login page URL."""
        login_url = self.app_config.get("login_url", "https://practice.expandtesting.com/notes/app/login")
        self.navigate_to(login_url)
        logger.info("Navigated to Login page")

    @allure.step("Enter email: {email}")
    def enter_email(self, email: str):
        """
        Enters the email address in the login form.

        Args:
            email (str): User's email address.
        """
        try:
            self.type_text(self.EMAIL_INPUT, email)
        except Exception:
            logger.warning("Primary email locator failed, trying fallback")
            self.type_text(self.EMAIL_INPUT_FALLBACK, email)
        logger.info(f"Entered email: {email}")

    @allure.step("Enter password")
    def enter_password(self, password: str):
        """
        Enters the password in the login form.

        Args:
            password (str): User's password.
        """
        try:
            self.type_text(self.PASSWORD_INPUT, password)
        except Exception:
            logger.warning("Primary password locator failed, trying fallback")
            self.type_text(self.PASSWORD_INPUT_FALLBACK, password)
        logger.info("Entered password: ****")

    @allure.step("Click Login button")
    def click_login(self):
        """Clicks the Login submit button."""
        try:
            self.click(self.LOGIN_BUTTON)
        except Exception:
            logger.warning("Primary login button locator failed, trying fallback")
            self.click(self.LOGIN_BUTTON_FALLBACK)
        logger.info("Clicked Login button")

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str):
        """
        Performs complete login flow: enter email, password, click login.

        Args:
            email (str): User's email address.
            password (str): User's password.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        logger.info(f"Login attempted with email: {email}")

    @allure.step("Full login flow with navigation")
    def full_login(self, email: str, password: str):
        """
        Navigates to login page and performs login.

        Args:
            email (str): User's email.
            password (str): User's password.
        """
        self.navigate_to_login()
        self.login(email, password)

    # ============================================
    # VERIFICATION METHODS
    # ============================================

    @allure.step("Verify login page is displayed")
    def is_login_page_displayed(self) -> bool:
        """
        Checks if the login page is currently displayed.

        Returns:
            bool: True if login form elements are visible.
        """
        return (
            self.is_element_visible(self.EMAIL_INPUT, timeout=10)
            or self.is_element_visible(self.EMAIL_INPUT_FALLBACK, timeout=5)
        )

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """
        Retrieves the login error message text.

        Returns:
            str: Error message text, or empty string if not present.
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            logger.debug("No error message displayed")
            return ""

    @allure.step("Verify login was successful")
    def is_login_successful(self) -> bool:
        """
        Verifies that login was successful by checking URL redirect or dashboard visibility.

        Returns:
            bool: True if redirected away from login page.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/notes/app" in driver.current_url and "/login" not in driver.current_url
            )
            current_url = self.get_current_url()
            is_success = "/notes/app" in current_url and "/login" not in current_url
            logger.info(f"Login success check: {is_success} (URL: {current_url})")
            return is_success
        except TimeoutException:
            logger.warning("Login success check failed - still on login page")
            return False
        except Exception as exc:
            logger.warning(f"Unexpected error during login success check: {exc}")
            return False

    @allure.step("Click Register link")
    def click_register_link(self):
        """Clicks the 'Create an account' / Register link."""
        self.click(self.REGISTER_LINK)
        logger.info("Clicked Register link")
