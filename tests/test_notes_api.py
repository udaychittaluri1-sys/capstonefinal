"""
============================================
Notes API Test Module
============================================
Tests for Notes REST API endpoints.
Covers: CRUD operations, response validation, performance.
"""

import pytest
import allure

from utils.logger import get_logger
from utils.helpers import generate_note_title, generate_note_description

logger = get_logger(__name__)


@allure.epic("Notes Application")
@allure.feature("Notes Management - API")
class TestNotesAPI:
    """Test suite for Notes API endpoints."""

    # ----- HEALTH CHECK -----

    @allure.story("Health Check")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_api_health_check(self, api_client):
        """TC-15: Verify API health check returns 200."""
        response = api_client.health_check()
        assert response.status_code == 200, \
            f"Health check should return 200, got {response.status_code}"
        logger.info("✅ TC-15: API health check PASSED")

    # ----- GET NOTES -----

    @allure.story("Get Notes")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_notes(self, authenticated_api):
        """TC-16: Verify GET /notes returns user's notes."""
        api, user_info = authenticated_api
        response = api.get_all_notes()

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        logger.info("✅ TC-16: GET all notes PASSED")

    @allure.story("Get Notes")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_notes_returns_list(self, authenticated_api):
        """TC-17: Verify GET /notes returns a list."""
        api, user_info = authenticated_api
        response = api.get_all_notes()

        data = response.json()
        assert isinstance(data["data"], list), \
            "Notes data should be a list"
        logger.info("✅ TC-17: Notes list format PASSED")

    # ----- CREATE NOTE VIA API -----

    @allure.story("Create Note")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_note_api(self, authenticated_api):
        """TC-18: Create a note via POST /notes."""
        api, user_info = authenticated_api
        title = generate_note_title()
        desc = generate_note_description()

        response = api.create_note(title, desc, "Work")

        assert response.status_code == 200, \
            f"Create note should return 200, got {response.status_code}"
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == title
        assert data["data"]["category"] == "Work"
        logger.info("✅ TC-18: Create note API PASSED")

    # ----- GET NOTE BY ID -----

    @allure.story("Get Note By ID")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_note_by_id(self, authenticated_api):
        """TC-19: Retrieve a specific note by ID."""
        api, user_info = authenticated_api

        # Create a note first
        title = generate_note_title()
        create_resp = api.create_note(title, "Test description", "Home")
        note_id = create_resp.json()["data"]["id"]

        # Get by ID
        response = api.get_note_by_id(note_id)
        assert response.status_code == 200
        assert response.json()["data"]["title"] == title
        logger.info("✅ TC-19: Get note by ID PASSED")

    # ----- DELETE NOTE -----

    @allure.story("Delete Note")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_delete_note_api(self, authenticated_api):
        """TC-20: Delete a note via DELETE /notes/{id}."""
        api, user_info = authenticated_api

        # Create then delete
        create_resp = api.create_note("Delete Me", "To be deleted", "Home")
        note_id = create_resp.json()["data"]["id"]

        del_response = api.delete_note(note_id)
        assert del_response.status_code == 200

        # Verify deletion
        get_resp = api.get_note_by_id(note_id)
        assert get_resp.status_code != 200, \
            "Deleted note should not be retrievable"
        logger.info("✅ TC-20: Delete note API PASSED")

    # ----- UPDATE NOTE -----

    @allure.story("Update Note")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_note_api(self, authenticated_api):
        """TC-21: Update a note via PUT /notes/{id}."""
        api, user_info = authenticated_api

        create_resp = api.create_note("Original Title", "Original Desc", "Home")
        note_id = create_resp.json()["data"]["id"]

        update_resp = api.update_note(
            note_id, "Updated Title", "Updated Desc", False, "Work"
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["data"]["title"] == "Updated Title"
        logger.info("✅ TC-21: Update note API PASSED")

    # ----- PERFORMANCE TESTS -----

    @allure.story("Performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.performance
    def test_get_notes_response_time(self, authenticated_api):
        """TC-22: Verify GET /notes response time < 2 seconds."""
        api, user_info = authenticated_api
        response = api.get_all_notes()

        elapsed = response.elapsed.total_seconds()
        assert elapsed < 2.0, \
            f"Response time {elapsed:.2f}s exceeds 2s threshold"
        logger.info(f"✅ TC-22: Response time {elapsed:.2f}s PASSED")

    @allure.story("Performance")
    @pytest.mark.api
    @pytest.mark.performance
    def test_create_note_response_time(self, authenticated_api):
        """TC-23: Verify POST /notes response time < 2 seconds."""
        api, user_info = authenticated_api
        response = api.create_note("Perf Test", "Performance check", "Home")

        elapsed = response.elapsed.total_seconds()
        assert elapsed < 2.0, \
            f"Response time {elapsed:.2f}s exceeds 2s threshold"
        logger.info(f"✅ TC-23: Create note time {elapsed:.2f}s PASSED")

    # ----- NEGATIVE / AUTH TESTS -----

    @allure.story("Negative Scenarios")
    @pytest.mark.api
    @pytest.mark.negative
    def test_get_notes_without_auth(self, api_client):
        """TC-24: Verify 401 when accessing notes without auth."""
        response = api_client.get_all_notes()
        assert response.status_code == 401, \
            f"Should return 401 without auth, got {response.status_code}"
        logger.info("✅ TC-24: Unauthorized access PASSED")

    @allure.story("Negative Scenarios")
    @pytest.mark.api
    @pytest.mark.negative
    def test_delete_nonexistent_note(self, authenticated_api):
        """TC-25: Verify error when deleting non-existent note."""
        api, user_info = authenticated_api
        response = api.delete_note("000000000000000000000000")
        assert response.status_code != 200, \
            "Should fail for non-existent note ID"
        logger.info("✅ TC-25: Delete non-existent note PASSED")

    @allure.story("Response Validation")
    @pytest.mark.api
    @pytest.mark.regression
    def test_note_response_schema(self, authenticated_api):
        """TC-26: Verify note response contains required fields."""
        api, user_info = authenticated_api
        create_resp = api.create_note("Schema Test", "Schema check", "Personal")

        data = create_resp.json()["data"]
        required_fields = ["id", "title", "description", "category",
                           "completed", "created_at", "updated_at"]
        for field in required_fields:
            assert field in data, f"Field '{field}' missing from response"
        logger.info("✅ TC-26: Response schema PASSED")
