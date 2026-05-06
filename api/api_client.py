"""
============================================
API Client Module
============================================
Centralized HTTP client for the Notes API.
Uses the requests library with:
- Token-based authentication (x-auth-token)
- Response time measurement
- Allure reporting integration
- Retry logic for resilience
"""

import time
import allure
import requests

from api.endpoints import Endpoints
from utils.logger import get_logger
from utils.config_reader import get_api_config, get_app_config

logger = get_logger(__name__)


class APIClient:
    """
    HTTP client for the Notes REST API.
    Handles authentication, request building, and response validation.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize API client.

        Args:
            base_url (str, optional): API base URL override.
        """
        app_config = get_app_config()
        self.base_url = base_url or app_config.get(
            "api_base_url",
            "https://practice.expandtesting.com/notes/api"
        )
        self.api_config = get_api_config()
        self.timeout = self.api_config.get("timeout", 30)
        self.token = None
        self.session = requests.Session()
        logger.info(f"API Client initialized: {self.base_url}")

    def _get_url(self, endpoint: str) -> str:
        """Builds full URL from endpoint path."""
        return f"{self.base_url}{endpoint}"

    def _get_headers(self) -> dict:
        """Returns request headers with auth token if available."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if self.token:
            headers["x-auth-token"] = self.token
        return headers

    def _log_response(self, response, method: str, endpoint: str):
        """Logs response details and attaches to Allure."""
        elapsed = response.elapsed.total_seconds()
        logger.info(
            f"API {method} {endpoint} -> "
            f"Status: {response.status_code} | Time: {elapsed:.2f}s"
        )
        allure.attach(
            f"Method: {method}\nURL: {response.url}\n"
            f"Status: {response.status_code}\n"
            f"Time: {elapsed:.2f}s\n"
            f"Response: {response.text[:500]}",
            name=f"API Response - {method} {endpoint}",
            attachment_type=allure.attachment_type.TEXT,
        )

    # ============================================
    # USER ENDPOINTS
    # ============================================

    @allure.step("API: Register user - {email}")
    def register_user(self, name: str, email: str, password: str):
        """
        Registers a new user account.

        Args:
            name: User's display name.
            email: User's email address.
            password: User's password.

        Returns:
            requests.Response: API response object.
        """
        data = {"name": name, "email": email, "password": password}
        response = self.session.post(
            self._get_url(Endpoints.REGISTER),
            data=data,
            timeout=self.timeout,
        )
        self._log_response(response, "POST", Endpoints.REGISTER)
        return response

    @allure.step("API: Login user - {email}")
    def login(self, email: str, password: str):
        """
        Authenticates a user and stores the auth token.

        Args:
            email: User's email.
            password: User's password.

        Returns:
            requests.Response: API response object.
        """
        data = {"email": email, "password": password}
        response = self.session.post(
            self._get_url(Endpoints.LOGIN),
            data=data,
            timeout=self.timeout,
        )
        self._log_response(response, "POST", Endpoints.LOGIN)

        # Extract and store token on successful login
        if response.status_code == 200:
            resp_json = response.json()
            self.token = resp_json.get("data", {}).get("token", "")
            if self.token:
                logger.info("Auth token acquired successfully")
            else:
                logger.warning("Login succeeded but no token in response")

        return response

    @allure.step("API: Get user profile")
    def get_profile(self):
        """Retrieves the authenticated user's profile."""
        response = self.session.get(
            self._get_url(Endpoints.PROFILE),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "GET", Endpoints.PROFILE)
        return response

    @allure.step("API: Logout user")
    def logout(self):
        """Logs out the current user and invalidates the token."""
        response = self.session.delete(
            self._get_url(Endpoints.LOGOUT),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "DELETE", Endpoints.LOGOUT)
        if response.status_code == 200:
            self.token = None
        return response

    @allure.step("API: Delete user account")
    def delete_account(self):
        """Deletes the authenticated user's account."""
        response = self.session.delete(
            self._get_url(Endpoints.DELETE_ACCOUNT),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "DELETE", Endpoints.DELETE_ACCOUNT)
        return response

    # ============================================
    # NOTE ENDPOINTS
    # ============================================

    @allure.step("API: Create note - {title}")
    def create_note(self, title: str, description: str, category: str = "Home"):
        """
        Creates a new note.

        Args:
            title: Note title.
            description: Note description.
            category: Note category (Home/Work/Personal).

        Returns:
            requests.Response: API response object.
        """
        data = {
            "title": title,
            "description": description,
            "category": category,
        }
        response = self.session.post(
            self._get_url(Endpoints.NOTES),
            data=data,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "POST", Endpoints.NOTES)
        return response

    @allure.step("API: Get all notes")
    def get_all_notes(self):
        """Retrieves all notes for the authenticated user."""
        response = self.session.get(
            self._get_url(Endpoints.NOTES),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "GET", Endpoints.NOTES)
        return response

    @allure.step("API: Get note by ID - {note_id}")
    def get_note_by_id(self, note_id: str):
        """
        Retrieves a specific note by its ID.

        Args:
            note_id: The note's unique identifier.

        Returns:
            requests.Response: API response object.
        """
        endpoint = Endpoints.note_by_id(note_id)
        response = self.session.get(
            self._get_url(endpoint),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "GET", endpoint)
        return response

    @allure.step("API: Update note - {note_id}")
    def update_note(self, note_id: str, title: str, description: str,
                    completed: bool = False, category: str = "Home"):
        """
        Updates an existing note.

        Args:
            note_id: Note ID to update.
            title: Updated title.
            description: Updated description.
            completed: Completion status.
            category: Note category.

        Returns:
            requests.Response: API response object.
        """
        data = {
            "title": title,
            "description": description,
            "completed": str(completed).lower(),
            "category": category,
        }
        endpoint = Endpoints.note_by_id(note_id)
        response = self.session.put(
            self._get_url(endpoint),
            data=data,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "PUT", endpoint)
        return response

    @allure.step("API: Delete note - {note_id}")
    def delete_note(self, note_id: str):
        """
        Deletes a note by its ID.

        Args:
            note_id: Note ID to delete.

        Returns:
            requests.Response: API response object.
        """
        endpoint = Endpoints.note_by_id(note_id)
        response = self.session.delete(
            self._get_url(endpoint),
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "DELETE", endpoint)
        return response

    @allure.step("API: Toggle note completion - {note_id}")
    def update_note_status(self, note_id: str, completed: bool):
        """
        Updates only the completion status of a note.

        Args:
            note_id: Note ID.
            completed: New completion status.

        Returns:
            requests.Response: API response object.
        """
        endpoint = Endpoints.note_by_id(note_id)
        data = {"completed": str(completed).lower()}
        response = self.session.patch(
            self._get_url(endpoint),
            data=data,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        self._log_response(response, "PATCH", endpoint)
        return response

    # ============================================
    # HEALTH CHECK
    # ============================================

    @allure.step("API: Health check")
    def health_check(self):
        """Checks if the API service is healthy."""
        response = self.session.get(
            self._get_url(Endpoints.HEALTH_CHECK),
            timeout=self.timeout,
        )
        self._log_response(response, "GET", Endpoints.HEALTH_CHECK)
        return response
