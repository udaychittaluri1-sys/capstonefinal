"""
============================================
API Fixture Module
============================================
Pytest fixtures for API client lifecycle management.
Handles user registration, login, and cleanup.
"""

import pytest
from api.api_client import APIClient
from utils.logger import get_logger
from utils.config_reader import get_test_user
from utils.helpers import generate_random_email

logger = get_logger(__name__)


def create_api_client() -> APIClient:
    """
    Factory function to create an authenticated API client.

    Returns:
        APIClient: Configured and ready-to-use API client.
    """
    client = APIClient()
    logger.info("API client created")
    return client


def setup_test_user(client: APIClient) -> dict:
    """
    Creates a test user via API and logs in to get auth token.

    Args:
        client: API client instance.

    Returns:
        dict: User details (name, email, password, token).
    """
    user_config = get_test_user()
    email = generate_random_email("capstone")
    name = user_config.get("name", "Test Automation User")
    password = user_config.get("password", "TestPass@123")

    # Register user
    reg_response = client.register_user(name, email, password)
    if reg_response.status_code == 201:
        logger.info(f"Test user registered: {email}")
    else:
        logger.warning(f"Registration response: {reg_response.status_code}")

    # Login to get token
    login_response = client.login(email, password)
    if login_response.status_code == 200:
        logger.info("Test user logged in successfully")
    else:
        logger.error(f"Login failed: {login_response.status_code}")

    return {
        "name": name,
        "email": email,
        "password": password,
        "token": client.token,
    }


def cleanup_test_user(client: APIClient):
    """
    Cleans up by deleting the test user account.

    Args:
        client: Authenticated API client.
    """
    try:
        response = client.delete_account()
        if response.status_code == 200:
            logger.info("Test user account deleted")
        else:
            logger.warning(f"Account cleanup status: {response.status_code}")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
