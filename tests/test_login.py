import pytest
import allure

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from api.api_client import APIClient
from utils.logger import get_logger
from utils.helpers import generate_random_email
from utils.config_reader import get_test_user

logger = get_logger(__name__)


@allure.epic("Notes Application")
@allure.feature("Authentication")
class TestLogin:
    """Test suite for login functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup: create test user via API before each test."""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.api = APIClient()
        self.user_config = get_test_user()

        # Create unique test user via API
        self.email = generate_random_email("login_test")
        self.password = self.user_config.get("password", "TestPass@123")
        self.name = self.user_config.get("name", "Test Automation User")

        reg_resp = self.api.register_user(self.name, self.email, self.password)
        logger.info(f"Test user setup: {self.email} (status: {reg_resp.status_code})")

        yield

        # Cleanup: delete test user
        try:
            self.api.login(self.email, self.password)
            self.api.delete_account()
        except Exception:
            pass

    # ----- POSITIVE TESTS -----

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_valid_login(self):
        """TC-01: Verify user can login with valid credentials."""
        self.login_page.full_login(self.email, self.password)
        assert self.login_page.is_login_successful(), \
            "Login should succeed with valid credentials"
        logger.info("✅ TC-01: Valid login PASSED")

    @allure.story("Valid Login")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_redirects_to_notes(self):
        """TC-02: Verify successful login redirects to notes page."""
        self.login_page.full_login(self.email, self.password)
        self.login_page.is_login_successful()
        current_url = self.driver.current_url
        assert "/notes/app" in current_url, \
            f"Should redirect to notes page, got: {current_url}"
        logger.info("✅ TC-02: Login redirect PASSED")

    # ----- NEGATIVE TESTS -----

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_email(self):
        """TC-03: Verify login fails with invalid email."""
        self.login_page.full_login("invalid@wrong.com", self.password)
        assert not self.login_page.is_login_successful(), \
            "Login should fail with invalid email"
        logger.info("✅ TC-03: Invalid email login PASSED")

    @allure.story("Invalid Login")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_invalid_password(self):
        """TC-04: Verify login fails with wrong password."""
        self.login_page.full_login(self.email, "WrongPassword@999")
        assert not self.login_page.is_login_successful(), \
            "Login should fail with wrong password"
        logger.info("✅ TC-04: Invalid password PASSED")

    @allure.story("Invalid Login")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_empty_email(self):
        """TC-05: Verify login fails with empty email."""
        self.login_page.navigate_to_login()
        self.login_page.enter_password(self.password)
        self.login_page.click_login()
        assert not self.login_page.is_login_successful(), \
            "Login should fail with empty email"
        logger.info("✅ TC-05: Empty email PASSED")

    @allure.story("Invalid Login")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_empty_password(self):
        """TC-06: Verify login fails with empty password."""
        self.login_page.navigate_to_login()
        self.login_page.enter_email(self.email)
        self.login_page.click_login()
        assert not self.login_page.is_login_successful(), \
            "Login should fail with empty password"
        logger.info("✅ TC-06: Empty password PASSED")

    @allure.story("Invalid Login")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_both_fields_empty(self):
        """TC-07: Verify login fails with both fields empty."""
        self.login_page.navigate_to_login()
        self.login_page.click_login()
        assert not self.login_page.is_login_successful(), \
            "Login should fail with both fields empty"
        logger.info("✅ TC-07: Both fields empty PASSED")

    # ----- UI VERIFICATION -----

    @allure.story("Login Page UI")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_login_page_elements_displayed(self):
        """TC-08: Verify all login page elements are present."""
        self.login_page.navigate_to_login()
        assert self.login_page.is_login_page_displayed(), \
            "Login page should display email and password fields"
        logger.info("✅ TC-08: Login page elements PASSED")
