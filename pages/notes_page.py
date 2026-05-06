"""
============================================
Notes Page Object
============================================
Page Object for the Notes dashboard page.
Handles note creation, viewing, deletion, and verification.
"""

import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class NotesPage(BasePage):
    """Page Object for the Notes dashboard after login."""

    # ============================================
    # LOCATORS
    # ============================================

    # Navigation & Header
    ADD_NOTE_BUTTON = (By.CSS_SELECTOR, "[data-testid='add-new-note']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='logout']")
    HOME_LINK = (By.CSS_SELECTOR, "a[href='/notes/app']")

    # Create/Edit Note Form
    NOTE_CATEGORY_SELECT = (By.CSS_SELECTOR, "[data-testid='note-category']")
    NOTE_COMPLETED_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='note-completed']")
    NOTE_TITLE_INPUT = (By.CSS_SELECTOR, "[data-testid='note-title']")
    NOTE_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='note-description']")
    CREATE_NOTE_BUTTON = (By.CSS_SELECTOR, "[data-testid='note-submit']")

    # Note Cards on Dashboard
    NOTE_CARDS = (By.CSS_SELECTOR, "[data-testid='note-card']")
    NOTE_CARD_TITLE = (By.CSS_SELECTOR, "[data-testid='note-card-title']")
    NOTE_CARD_DESCRIPTION = (By.CSS_SELECTOR, "[data-testid='note-card-description']")
    NOTE_DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='note-delete']")
    NOTE_EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='note-edit']")
    NOTE_VIEW_BUTTON = (By.CSS_SELECTOR, "[data-testid='note-view']")
    NOTE_CARD_CATEGORY = (By.CSS_SELECTOR, "[data-testid='note-card-category']")
    NOTE_COMPLETED_STATUS = (By.CSS_SELECTOR, "[data-testid='toggle-note-switch']")

    # Progress Bar / No notes message
    NO_NOTES_MESSAGE = (By.XPATH, "//*[contains(text(), 'No notes') or contains(text(), 'no notes')]")

    # Fallback Locators
    ADD_NOTE_FALLBACK = (By.XPATH, "//button[contains(text(), 'Add') or contains(text(), 'New') or contains(@class, 'add')]")
    TITLE_INPUT_FALLBACK = (By.XPATH, "//input[@name='title' or @placeholder='Title']")
    DESC_INPUT_FALLBACK = (By.XPATH, "//textarea[@name='description' or @placeholder='Description']")
    SUBMIT_FALLBACK = (By.XPATH, "//button[@type='submit' or contains(text(), 'Create') or contains(text(), 'Save')]")

    # ============================================
    # NAVIGATION
    # ============================================

    @allure.step("Navigate to Notes dashboard")
    def navigate_to_notes(self):
        """Opens the notes dashboard page."""
        self.navigate_to("https://practice.expandtesting.com/notes/app")
        logger.info("Navigated to Notes dashboard")

    @allure.step("Click Add New Note button")
    def click_add_note(self):
        """Clicks the button to add a new note."""
        try:
            self.click(self.ADD_NOTE_BUTTON)
        except Exception:
            self.click(self.ADD_NOTE_FALLBACK)
        logger.info("Clicked Add New Note")

    # ============================================
    # NOTE CREATION
    # ============================================

    @allure.step("Create note: {title}")
    def create_note(self, title: str, description: str, category: str = "Home"):
        """
        Creates a new note with the given details.

        Args:
            title (str): Note title.
            description (str): Note description.
            category (str): Note category (Home/Work/Personal).
        """
        self.click_add_note()
        time.sleep(1)  # Wait for form to appear

        # Select category
        try:
            cat_element = self.find_element(self.NOTE_CATEGORY_SELECT)
            select = Select(cat_element)
            select.select_by_visible_text(category)
        except Exception:
            logger.warning("Category select failed, trying alternate approach")
            try:
                self.click(self.NOTE_CATEGORY_SELECT)
                cat_option = (By.XPATH, f"//option[text()='{category}']")
                self.click(cat_option)
            except Exception:
                logger.warning(f"Could not set category to {category}")

        # Enter title
        try:
            self.type_text(self.NOTE_TITLE_INPUT, title)
        except Exception:
            self.type_text(self.TITLE_INPUT_FALLBACK, title)

        # Enter description
        try:
            self.type_text(self.NOTE_DESCRIPTION_INPUT, description)
        except Exception:
            self.type_text(self.DESC_INPUT_FALLBACK, description)

        # Submit
        try:
            self.click(self.CREATE_NOTE_BUTTON)
        except Exception:
            self.click(self.SUBMIT_FALLBACK)

        logger.info(f"Note created: '{title}' [{category}]")
        time.sleep(2)  # Wait for note to appear in list

    # ============================================
    # NOTE VERIFICATION
    # ============================================

    @allure.step("Get all note titles from dashboard")
    def get_all_note_titles(self) -> list:
        """
        Returns a list of all note titles visible on the dashboard.

        Returns:
            list: List of note title strings.
        """
        titles = []
        elements = self.find_elements(self.NOTE_CARD_TITLE, timeout=10)
        for el in elements:
            titles.append(el.text)
        logger.info(f"Found {len(titles)} notes on dashboard")
        return titles

    @allure.step("Verify note exists: {title}")
    def is_note_displayed(self, title: str) -> bool:
        """
        Checks if a note with the given title is visible.

        Args:
            title (str): Note title to search for.

        Returns:
            bool: True if note is found on the dashboard.
        """
        titles = self.get_all_note_titles()
        found = title in titles
        logger.info(f"Note '{title}' displayed: {found}")
        return found

    @allure.step("Get note count")
    def get_note_count(self) -> int:
        """Returns the number of notes on the dashboard."""
        cards = self.find_elements(self.NOTE_CARDS, timeout=10)
        count = len(cards)
        logger.info(f"Note count: {count}")
        return count

    @allure.step("Get note details for: {title}")
    def get_note_details(self, title: str) -> dict:
        """
        Retrieves full details of a note by its title.

        Args:
            title (str): Title of the note.

        Returns:
            dict: Note details (title, description, category).
        """
        cards = self.find_elements(self.NOTE_CARDS, timeout=10)
        for card in cards:
            try:
                card_title = card.find_element(*self.NOTE_CARD_TITLE).text
                if card_title == title:
                    desc = card.find_element(*self.NOTE_CARD_DESCRIPTION).text
                    return {"title": card_title, "description": desc}
            except Exception:
                continue
        logger.warning(f"Note not found: {title}")
        return {}

    # ============================================
    # NOTE DELETION
    # ============================================

    @allure.step("Delete note: {title}")
    def delete_note_by_title(self, title: str) -> bool:
        """
        Deletes a note by its title from the dashboard.

        Args:
            title (str): Title of the note to delete.

        Returns:
            bool: True if note was found and deleted.
        """
        # Build a safe XPath literal for the note title
        if "'" in title:
            title_literal = f'"{title}"'
        else:
            title_literal = f"'{title}'"

        card_locator = (
            By.XPATH,
            f"//*[@data-testid='note-card' and .//*[@data-testid='note-card-title' and normalize-space()={title_literal}]]"
        )

        try:
            note_card = self.find_element(card_locator, timeout=10)
            delete_button_locator = (
                By.XPATH,
                f"//*[@data-testid='note-card' and .//*[@data-testid='note-card-title' and normalize-space()={title_literal}]]//*[@data-testid='note-delete']"
            )
            delete_note=(
                    By.XPATH,
                    f"//button[@data-testid='note-delete-confirm']"
            )
            self.scroll_to_element(delete_button_locator)
            self.click(delete_button_locator)
            self.click(delete_note)
            if not self.wait_for_element_invisible(card_locator, timeout=10):
                logger.warning(f"Note card still visible after delete click: '{title}'")
                return False
            logger.info(f"Deleted note: '{title}'")
            return True
        except Exception as exc:
            logger.warning(f"Could not delete note '{title}': {exc}")
            return False

    # ============================================
    # LOGOUT
    # ============================================

    @allure.step("Logout from application")
    def logout(self):
        """Clicks the logout button/link."""
        try:
            self.click(self.LOGOUT_BUTTON)
        except Exception:
            logout_fallback = (By.XPATH, "//button[contains(text(),'Logout')] | //a[contains(text(),'Logout')]")
            self.click(logout_fallback)
        logger.info("Logged out from application")
