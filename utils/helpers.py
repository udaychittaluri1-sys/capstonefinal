"""
============================================
Helper Utilities Module
============================================
Common helper functions used across the framework:
- Random test data generation
- Screenshot capture
- Wait utilities
- Timestamp generation
- AI-powered test data generation (MCP support)
"""

import os
import time
import string
import random
from datetime import datetime

import allure
from faker import Faker

from utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker()

# --- Screenshot directory ---
SCREENSHOT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports",
    "screenshots",
)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ============================================
# TEST DATA GENERATION
# ============================================

def generate_random_email(prefix: str = "testuser") -> str:
    """
    Generates a unique random email address.

    Args:
        prefix (str): Email prefix string.

    Returns:
        str: Unique email address.
    """
    timestamp = int(time.time() * 1000)
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=5))
    email = f"{prefix}_{timestamp}_{random_suffix}@expandtesting.com"
    logger.debug(f"Generated random email: {email}")
    return email


def generate_random_password(length: int = 12) -> str:
    """
    Generates a secure random password meeting common requirements.

    Args:
        length (int): Password length (minimum 8).

    Returns:
        str: Random password with mixed case, digits, and special chars.
    """
    if length < 8:
        length = 8

    # Ensure at least one of each required character type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*"),
    ]
    # Fill remaining length with random mix
    password += random.choices(
        string.ascii_letters + string.digits + "!@#$%^&*",
        k=length - 4,
    )
    random.shuffle(password)
    return ''.join(password)


def generate_note_title() -> str:
    """Generates a realistic note title using Faker."""
    title = f"AutoTest - {fake.catch_phrase()}"
    logger.debug(f"Generated note title: {title}")
    return title


def generate_note_description() -> str:
    """Generates a realistic note description using Faker."""
    description = fake.paragraph(nb_sentences=3)
    logger.debug(f"Generated note description: {description[:50]}...")
    return description


def get_random_category() -> str:
    """
    Returns a random note category from allowed values.

    Returns:
        str: One of 'Home', 'Work', or 'Personal'.
    """
    return random.choice(["Home", "Work", "Personal"])


# ============================================
# SCREENSHOT UTILITIES
# ============================================

def capture_screenshot(driver, test_name: str) -> str:
    """
    Captures a browser screenshot and attaches it to Allure report.

    Args:
        driver: Selenium WebDriver instance.
        test_name (str): Name of the test for file naming.

    Returns:
        str: Absolute path to the saved screenshot.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")

        # Attach to Allure report
        with open(filepath, "rb") as f:
            allure.attach(
                f.read(),
                name=f"Screenshot - {test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
        return filepath

    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return ""


# ============================================
# TIMING & PERFORMANCE UTILITIES
# ============================================

def get_timestamp() -> str:
    """Returns current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def measure_execution_time(func):
    """
    Decorator to measure and log function execution time.

    Usage:
        @measure_execution_time
        def my_test_function():
            ...
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"⏱ {func.__name__} executed in {elapsed:.2f} seconds")
        return result
    return wrapper


# ============================================
# AI / MCP SUPPORT UTILITIES
# ============================================

def ai_generate_test_data(data_type: str = "note") -> dict:
    """
    AI-powered test data generation (MCP support placeholder).
    Uses Faker as the intelligent data source.

    In production, this could be connected to an LLM via MCP protocol
    for context-aware test data generation.

    Args:
        data_type (str): Type of test data to generate.

    Returns:
        dict: Generated test data.
    """
    if data_type == "note":
        return {
            "title": generate_note_title(),
            "description": generate_note_description(),
            "category": get_random_category(),
        }
    elif data_type == "user":
        return {
            "name": fake.name(),
            "email": generate_random_email(),
            "password": generate_random_password(),
        }
    else:
        logger.warning(f"Unknown data type: {data_type}")
        return {}


def ai_analyze_failure(error_message: str, screenshot_path: str = "") -> dict:
    """
    AI-powered failure analysis (MCP support placeholder).

    In production, this would connect to an LLM to analyze failures,
    suggest fixes, and classify error types.

    Args:
        error_message (str): The error/exception message.
        screenshot_path (str): Path to failure screenshot.

    Returns:
        dict: Analysis results with suggested actions.
    """
    analysis = {
        "error_type": "unknown",
        "possible_cause": "",
        "suggested_action": "",
        "confidence": 0.0,
    }

    # Basic rule-based classification (would be LLM in production)
    error_lower = error_message.lower()
    if "timeout" in error_lower or "timed out" in error_lower:
        analysis["error_type"] = "timeout"
        analysis["possible_cause"] = "Element not found or page load too slow"
        analysis["suggested_action"] = "Increase wait time or check element locator"
        analysis["confidence"] = 0.85
    elif "nosuchelement" in error_lower or "no such element" in error_lower:
        analysis["error_type"] = "element_not_found"
        analysis["possible_cause"] = "Locator changed or element not rendered"
        analysis["suggested_action"] = "Update locator or add explicit wait"
        analysis["confidence"] = 0.90
    elif "stale" in error_lower:
        analysis["error_type"] = "stale_element"
        analysis["possible_cause"] = "DOM was refreshed after element was located"
        analysis["suggested_action"] = "Re-locate element before interaction"
        analysis["confidence"] = 0.88
    elif "401" in error_lower or "unauthorized" in error_lower:
        analysis["error_type"] = "authentication_failure"
        analysis["possible_cause"] = "Token expired or invalid credentials"
        analysis["suggested_action"] = "Re-authenticate and retry"
        analysis["confidence"] = 0.92
    else:
        analysis["possible_cause"] = "Unclassified failure - manual review needed"
        analysis["suggested_action"] = "Check logs and screenshot for details"
        analysis["confidence"] = 0.30

    logger.info(f"🤖 AI Failure Analysis: {analysis['error_type']} "
                f"(confidence: {analysis['confidence']:.0%})")
    return analysis
