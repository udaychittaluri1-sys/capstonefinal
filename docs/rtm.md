# ============================================
# REQUIREMENT TRACEABILITY MATRIX (RTM)
# Notes Application - UI + API Hybrid Framework
# ============================================

## Legend
- REQ = Functional Requirement
- TS  = Test Scenario ID
- TC  = Test Case ID (in code)
- Status: ✅ Automated | 🔧 Manual | ⏳ Planned

---

## RTM Table

| REQ ID | Requirement Description                          | TS ID | TC / Test Method                                    | Type        | Status |
|--------|--------------------------------------------------|-------|-----------------------------------------------------|-------------|--------|
| REQ-01 | User can login with valid credentials            | TS-01 | test_login.py::test_valid_login                     | UI Positive | ✅     |
| REQ-02 | Login redirects to notes dashboard               | TS-05 | test_login.py::test_login_redirects_to_notes        | UI Positive | ✅     |
| REQ-03 | Login fails with invalid email                   | TS-02 | test_login.py::test_invalid_email                   | UI Negative | ✅     |
| REQ-04 | Login fails with wrong password                  | TS-03 | test_login.py::test_invalid_password                | UI Negative | ✅     |
| REQ-05 | Login fails with empty email field               | TS-04 | test_login.py::test_empty_email                     | UI Negative | ✅     |
| REQ-06 | Login fails with empty password field            | TS-04 | test_login.py::test_empty_password                  | UI Negative | ✅     |
| REQ-07 | Login fails with both fields empty               | TS-04 | test_login.py::test_both_fields_empty               | UI Negative | ✅     |
| REQ-08 | Login page displays all required elements        | TS-01 | test_login.py::test_login_page_elements_displayed   | UI Positive | ✅     |
| REQ-09 | User can create note with Home category          | TS-06 | test_notes_ui.py::test_create_note_home_category    | UI Positive | ✅     |
| REQ-10 | User can create note with Work category          | TS-07 | test_notes_ui.py::test_create_note_work_category    | UI Positive | ✅     |
| REQ-11 | User can create note with Personal category      | TS-08 | test_notes_ui.py::test_create_note_personal_category| UI Positive | ✅     |
| REQ-12 | Note appears in list immediately after creation  | TS-09 | test_notes_ui.py::test_note_appears_instantly       | UI Positive | ✅     |
| REQ-13 | Multiple notes can be created and all shown      | TS-10 | test_notes_ui.py::test_multiple_notes_creation      | UI Positive | ✅     |
| REQ-14 | Note can be deleted via UI                       | TS-10 | test_notes_ui.py::test_delete_note_via_ui           | UI Positive | ✅     |
| REQ-15 | API health check returns 200                     | TS-26 | test_notes_api.py::test_api_health_check            | API Smoke   | ✅     |
| REQ-16 | GET /notes returns 200 with authenticated user   | TS-11 | test_notes_api.py::test_get_all_notes               | API Positive| ✅     |
| REQ-17 | GET /notes returns list of notes                 | TS-11 | test_notes_api.py::test_get_notes_returns_list      | API Positive| ✅     |
| REQ-18 | POST /notes creates note successfully            | TS-12 | test_notes_api.py::test_create_note_api             | API Positive| ✅     |
| REQ-19 | GET /notes/{id} retrieves specific note          | TS-13 | test_notes_api.py::test_get_note_by_id              | API Positive| ✅     |
| REQ-20 | DELETE /notes/{id} removes note                  | TS-15 | test_notes_api.py::test_delete_note_api             | API Positive| ✅     |
| REQ-21 | PUT /notes/{id} updates note fields              | TS-14 | test_notes_api.py::test_update_note_api             | API Positive| ✅     |
| REQ-22 | GET /notes returns 401 without token             | TS-16 | test_notes_api.py::test_get_notes_without_auth      | API Negative| ✅     |
| REQ-23 | Delete non-existent note returns error           | TS-17 | test_notes_api.py::test_delete_nonexistent_note     | API Negative| ✅     |
| REQ-24 | Note response contains required schema fields    | TS-25 | test_notes_api.py::test_note_response_schema        | API Positive| ✅     |
| REQ-25 | GET /notes response time < 2 seconds             | TS-22 | test_notes_api.py::test_get_notes_response_time     | Perf        | ✅     |
| REQ-26 | POST /notes response time < 2 seconds            | TS-23 | test_notes_api.py::test_create_note_response_time   | Perf        | ✅     |
| REQ-27 | Note created in UI matches data in API           | TS-18 | test_e2e.py::test_ui_create_api_verify              | E2E         | ✅     |
| REQ-28 | Note title/desc consistent between UI and API    | TS-19 | test_e2e.py::test_ui_create_api_verify              | E2E         | ✅     |
| REQ-29 | Note deleted via API disappears from UI          | TS-20 | test_e2e.py::test_api_delete_ui_verify              | E2E         | ✅     |
| REQ-30 | API-created note appears in UI after refresh     | TS-21 | test_e2e.py::test_api_delete_ui_verify              | E2E         | ✅     |
| REQ-31 | Full CRUD cycle works across UI and API          | TS-18-21 | test_e2e.py::test_full_crud_hybrid               | E2E         | ✅     |
| REQ-32 | UI notes page loads within 5 seconds             | TS-24 | test_e2e.py::test_ui_page_load_performance          | Perf        | ✅     |

---

## Summary

| Category    | Total Requirements | Automated | Manual | Coverage |
|-------------|-------------------|-----------|--------|----------|
| UI Login    | 8                 | 8         | 0      | 100%     |
| UI Notes    | 6                 | 6         | 0      | 100%     |
| API CRUD    | 7                 | 7         | 0      | 100%     |
| API Neg     | 2                 | 2         | 0      | 100%     |
| API Schema  | 1                 | 1         | 0      | 100%     |
| Performance | 3                 | 3         | 0      | 100%     |
| E2E Hybrid  | 5                 | 5         | 0      | 100%     |
| **TOTAL**   | **32**            | **32**    | **0**  | **100%** |
