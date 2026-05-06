"""
============================================
Base Page Object
============================================
Foundation class for all Page Objects in the framework.
Implements common Selenium operations with:
- Explicit waits (WebDriverWait)
- Self-healing locator strategy
- Screenshot on failure
- Allure step logging
"""

import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

from utils.logger import get_logger
from utils.helpers import capture_screenshot, ai_analyze_failure
from utils.config_reader import get_browser_config

logger = get_logger(__name__)


class BasePage:
    """
    Base Page Object providing reusable Selenium operations.

    All page objects inherit from this class to get:
    - Smart element finding with waits
    - Self-healing locators (fallback strategies)
    - Automatic screenshot on failure
    - Allure reporting integration
    """

    def __init__(self, driver):
        """
        Initialize BasePage with a WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
        """
        self.driver = driver
        self.browser_config = get_browser_config()
        self.timeout = self.browser_config.get("explicit_wait", 15)
        self.wait = WebDriverWait(
            driver,
            self.timeout,
            ignored_exceptions=[
                StaleElementReferenceException,
                NoSuchElementException,
            ],
        )

    # ============================================
    # CORE ELEMENT OPERATIONS
    # ============================================

    @allure.step("Finding element: {locator}")
    def find_element(self, locator: tuple, timeout: int = None):
        """
        Finds a single element with explicit wait.

        Args:
            locator (tuple): Locator tuple (By.XXX, "value").
            timeout (int, optional): Custom timeout override.

        Returns:
            WebElement: The found web element.

        Raises:
            TimeoutException: If element not found within timeout.
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element NOT found within {wait_time}s: {locator}")
            # Attempt self-healing
            healed = self._self_heal_locator(locator)
            if healed:
                return healed
            capture_screenshot(self.driver, f"element_not_found_{locator[1][:20]}")
            raise

    @allure.step("Finding elements: {locator}")
    def find_elements(self, locator: tuple, timeout: int = None) -> list:
        """
        Finds multiple elements with explicit wait.

        Args:
            locator (tuple): Locator tuple (By.XXX, "value").
            timeout (int, optional): Custom timeout override.

        Returns:
            list: List of found web elements (may be empty).
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found for: {locator}")
            return []

    # ============================================
    # INTERACTION METHODS
    # ============================================

    @allure.step("Clicking element: {locator}")
    def click(self, locator: tuple, timeout: int = None):
        """
        Clicks an element after waiting for it to be clickable.

        Implements retry logic for intercepted clicks.

        Args:
            locator (tuple): Locator tuple (By.XXX, "value").
            timeout (int, optional): Custom timeout override.
        """
        wait_time = timeout or self.timeout
        max_retries = 3

        for attempt in range(max_retries):
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                logger.info(f"Clicked element: {locator}")
                return
            except ElementClickInterceptedException:
                logger.warning(
                    f"Click intercepted on attempt {attempt + 1}, "
                    f"trying JavaScript click..."
                )
                try:
                    element = self.driver.find_element(*locator)
                    self.driver.execute_script("arguments[0].click();", element)
                    logger.info(f"JS-clicked element: {locator}")
                    return
                except Exception:
                    time.sleep(0.5)
            except TimeoutException:
                logger.error(f"Element not clickable: {locator}")
                capture_screenshot(self.driver, "click_failed")
                raise

    @allure.step("Typing '{text}' into element: {locator}")
    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        """
        Types text into an input element.

        Args:
            locator (tuple): Locator tuple.
            text (str): Text to type.
            clear_first (bool): Whether to clear the field first.
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
            # Double-clear using keyboard for React inputs
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
        element.send_keys(text)
        logger.info(f"Typed text into: {locator}")

    @allure.step("Getting text from element: {locator}")
    def get_text(self, locator: tuple) -> str:
        """
        Gets the visible text of an element.

        Args:
            locator (tuple): Locator tuple.

        Returns:
            str: Visible text of the element.
        """
        element = self.find_element(locator)
        text = element.text
        logger.debug(f"Got text '{text}' from: {locator}")
        return text

    @allure.step("Getting attribute '{attribute}' from element: {locator}")
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Gets a specific attribute value of an element.

        Args:
            locator (tuple): Locator tuple.
            attribute (str): Attribute name (e.g., 'value', 'href').

        Returns:
            str: Attribute value.
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    # ============================================
    # WAIT METHODS
    # ============================================

    @allure.step("Waiting for element to be visible: {locator}")
    def wait_for_element_visible(self, locator: tuple, timeout: int = None):
        """
        Waits until an element is visible on the page.

        Args:
            locator (tuple): Locator tuple.
            timeout (int, optional): Custom timeout.

        Returns:
            WebElement: The visible element.
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element is visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time}s: {locator}")
            capture_screenshot(self.driver, "element_not_visible")
            raise

    @allure.step("Waiting for element to disappear: {locator}")
    def wait_for_element_invisible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Waits until an element disappears from the page.

        Args:
            locator (tuple): Locator tuple.
            timeout (int, optional): Custom timeout.

        Returns:
            bool: True if element disappeared, False otherwise.
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.info(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element still visible after {wait_time}s: {locator}")
            return False

    def wait_for_url_contains(self, url_part: str, timeout: int = None):
        """
        Waits until the current URL contains the specified string.

        Args:
            url_part (str): Expected URL substring.
            timeout (int, optional): Custom timeout.
        """
        wait_time = timeout or self.timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.url_contains(url_part)
        )
        logger.info(f"URL contains: {url_part}")

    # ============================================
    # NAVIGATION METHODS
    # ============================================

    @allure.step("Navigating to: {url}")
    def navigate_to(self, url: str):
        """
        Navigates the browser to a URL.

        Args:
            url (str): Target URL.
        """
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Returns the current page title."""
        return self.driver.title

    def refresh_page(self):
        """Refreshes the current page."""
        self.driver.refresh()
        logger.info("Page refreshed")

    # ============================================
    # JAVASCRIPT EXECUTION
    # ============================================

    def execute_script(self, script: str, *args):
        """
        Executes JavaScript on the page.

        Args:
            script (str): JavaScript code to execute.
            *args: Arguments to pass to the script.

        Returns:
            The return value of the JavaScript execution.
        """
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator: tuple):
        """Scrolls the page to bring an element into view."""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )
        logger.debug(f"Scrolled to element: {locator}")

    # ============================================
    # VERIFICATION METHODS
    # ============================================

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Checks if an element is present on the page.

        Args:
            locator (tuple): Locator tuple.
            timeout (int): Wait timeout.

        Returns:
            bool: True if element is present.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Checks if an element is visible on the page.

        Args:
            locator (tuple): Locator tuple.
            timeout (int): Wait timeout.

        Returns:
            bool: True if element is visible.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ============================================
    # SELF-HEALING LOCATOR (AGENTIC AUTOMATION)
    # ============================================

    def _self_heal_locator(self, original_locator: tuple):
        """
        Attempts to find an element using alternative locator strategies.
        This implements the 'self-healing locator' pattern for agentic automation.

        The strategy tries multiple approaches:
        1. Partial text match via XPath
        2. CSS class name partial match
        3. Tag + attribute combination

        Args:
            original_locator (tuple): The original failing locator.

        Returns:
            WebElement or None: The healed element if found.
        """
        by, value = original_locator
        logger.warning(f"🔧 Self-healing: Attempting alternative locators for: {value}")

        # Strategy 1: Try by partial attribute match (XPath)
        healing_strategies = []

        if by == By.ID:
            healing_strategies.append(
                (By.XPATH, f"//*[contains(@id, '{value}')]")
            )
            healing_strategies.append(
                (By.CSS_SELECTOR, f"[id*='{value}']")
            )
        elif by == By.CSS_SELECTOR:
            # Try extracting key parts of the selector
            if "data-testid" in value:
                testid = value.split("data-testid=")[1].strip("\"']")
                healing_strategies.append(
                    (By.XPATH, f"//*[contains(@data-testid, '{testid}')]")
                )
        elif by == By.NAME:
            healing_strategies.append(
                (By.XPATH, f"//*[contains(@name, '{value}')]")
            )

        # Attempt each healing strategy
        for strategy in healing_strategies:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(strategy)
                )
                logger.info(f"✅ Self-healed! Found element with: {strategy}")
                allure.attach(
                    f"Original: {original_locator}\nHealed: {strategy}",
                    name="Self-Healing Locator",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return element
            except TimeoutException:
                continue

        logger.error(f"❌ Self-healing FAILED for: {original_locator}")
        return None

    # ============================================
    # PERFORMANCE TIMING
    # ============================================

    def get_page_load_time(self) -> float:
        """
        Measures the page load time using Navigation Timing API.

        Returns:
            float: Page load time in seconds.
        """
        load_time = self.driver.execute_script(
            "return (window.performance.timing.loadEventEnd - "
            "window.performance.timing.navigationStart) / 1000;"
        )
        logger.info(f"⏱ Page load time: {load_time:.2f} seconds")
        return load_time
