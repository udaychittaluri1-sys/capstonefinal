"""
============================================
API Endpoints Module
============================================
Centralized API endpoint definitions for the Notes API.
Base URL: https://practice.expandtesting.com/notes/api
"""


class Endpoints:
    """All API endpoint paths as class constants."""

    # Health
    HEALTH_CHECK = "/health-check"

    # User endpoints
    REGISTER = "/users/register"
    LOGIN = "/users/login"
    PROFILE = "/users/profile"
    FORGOT_PASSWORD = "/users/forgot-password"
    CHANGE_PASSWORD = "/users/change-password"
    LOGOUT = "/users/logout"
    DELETE_ACCOUNT = "/users/delete-account"

    # Note endpoints
    NOTES = "/notes"
    NOTE_BY_ID = "/notes/{note_id}"

    @staticmethod
    def note_by_id(note_id: str) -> str:
        """Returns the endpoint path for a specific note."""
        return f"/notes/{note_id}"
