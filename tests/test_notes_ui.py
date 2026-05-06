"""
============================================
Notes UI Test Module
============================================
Tests for note CRUD operations via the UI.
Covers: create note, verify display, note details.
"""

import pytest
import allure

from pages.notes_page import NotesPage
from utils.logger import get_logger
from utils.helpers import generate_note_title, generate_note_description, get_random_category

logger = get_logger(__name__)


@allure.epic("Notes Application")
@allure.feature("Notes Management - UI")
class TestNotesUI:
    """Test suite for notes UI operations."""

    # ----- CREATE NOTE TESTS -----

    @allure.story("Create Note")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_create_note_home_category(self, logged_in_ui):
        """TC-09: Create a note with Home category via UI."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        title = generate_note_title()
        description = generate_note_description()

        notes_page.create_note(title, description, "Home")
        assert notes_page.is_note_displayed(title), \
            f"Note '{title}' should appear on dashboard after creation"
        logger.info("✅ TC-09: Create Home note PASSED")

    @allure.story("Create Note")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_note_work_category(self, logged_in_ui):
        """TC-10: Create a note with Work category via UI."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        title = generate_note_title()
        description = generate_note_description()

        notes_page.create_note(title, description, "Work")
        assert notes_page.is_note_displayed(title), \
            f"Note '{title}' should appear on dashboard"
        logger.info("✅ TC-10: Create Work note PASSED")

    @allure.story("Create Note")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_note_personal_category(self, logged_in_ui):
        """TC-11: Create a note with Personal category via UI."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        title = generate_note_title()
        description = generate_note_description()

        notes_page.create_note(title, description, "Personal")
        assert notes_page.is_note_displayed(title), \
            f"Note '{title}' should appear on dashboard"
        logger.info("✅ TC-11: Create Personal note PASSED")

    # ----- NOTE LIST TESTS -----

    @allure.story("Note List")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_note_appears_instantly_after_creation(self, logged_in_ui):
        """TC-12: Verify note appears in list immediately after creation."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        initial_count = notes_page.get_note_count()
        title = generate_note_title()

        notes_page.create_note(title, generate_note_description(), "Home")

        new_count = notes_page.get_note_count()
        assert new_count == initial_count + 1, \
            f"Note count should increase by 1: was {initial_count}, now {new_count}"
        logger.info("✅ TC-12: Instant note display PASSED")

    @allure.story("Note List")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_multiple_notes_creation(self, logged_in_ui):
        """TC-13: Create multiple notes and verify all are displayed."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        titles = []
        for i in range(3):
            title = generate_note_title()
            titles.append(title)
            notes_page.create_note(title, generate_note_description(), get_random_category())

        displayed_titles = notes_page.get_all_note_titles()
        for title in titles:
            assert title in displayed_titles, \
                f"Note '{title}' should be in the list"
        logger.info("✅ TC-13: Multiple notes creation PASSED")

    # ----- DELETE NOTE TESTS -----

    @allure.story("Delete Note")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.delete
    def test_delete_note_via_ui(self, logged_in_ui):
        """TC-14: Delete a note via UI and verify removal."""
        driver, login_page, notes_page, user_info, api = logged_in_ui

        title = generate_note_title()
        notes_page.create_note(title, generate_note_description(), "Home")
        assert notes_page.is_note_displayed(title)

        notes_page.delete_note_by_title(title)
        assert not notes_page.is_note_displayed(title), \
            f"Note '{title}' should be removed after deletion"
        logger.info("✅ TC-14: Delete note via UI PASSED")
