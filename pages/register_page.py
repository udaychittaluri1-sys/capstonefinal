"""
============================================
Register Page Object
============================================
Page Object for the Notes Application Registration page.
URL: https://practice.expandtesting.com/notes/app/register
"""

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class RegisterPage(BasePage):
    """Page Object for user registration."""

    # Locators
    NAME_INPUT = (By.XPATH, "//input[@name='name' or @data-testid='register-name']")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email' or @data-testid='register-email']")
    PASSWORD_INPUT = (By.XPATH, "(//input[@type='password'])[1]")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "(//input[@type='password'])[2]")
    REGISTER_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[data-testid='alert-message']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/notes/app/login']")

    @allure.step("Navigate to Registration page")
    def navigate_to_register(self):
        self.navigate_to("https://practice.expandtesting.com/notes/app/register")

    @allure.step("Register new user: {name} / {email}")
    def register_user(self, name, email, password):
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.REGISTER_BUTTON)
        logger.info(f"Registration submitted for: {email}")

    def is_registration_successful(self):
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            return "success" in msg.lower() or "created" in msg.lower()
        except Exception:
            return "/login" in self.get_current_url()
