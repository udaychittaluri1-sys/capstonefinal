# ============================================
# TEST SCENARIOS
# Notes Application
# ============================================

## SC-01: User Authentication
| ID    | Scenario                                        | Type     |
|-------|-------------------------------------------------|----------|
| TS-01 | Verify user can login with valid credentials     | Positive |
| TS-02 | Verify login fails with invalid email            | Negative |
| TS-03 | Verify login fails with wrong password           | Negative |
| TS-04 | Verify login fails with empty fields             | Negative |
| TS-05 | Verify successful login redirects to notes page  | Positive |

## TS-02: Note Creation (UI)
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-06 | Create note with Home category                   | Positive |
| TS-07 | Create note with Work category                   | Positive |
| TS-08 | Create note with Personal category               | Positive |
| TS-09 | Verify note appears instantly after creation      | Positive |
| TS-10 | Create multiple notes and verify all displayed    | Positive |

## TS-03: Note Operations (API)
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-11 | GET /notes returns user's notes                  | Positive |
| TS-12 | POST /notes creates a new note                   | Positive |
| TS-13 | GET /notes/{id} retrieves specific note          | Positive |
| TS-14 | PUT /notes/{id} updates a note                   | Positive |
| TS-15 | DELETE /notes/{id} deletes a note                | Positive |
| TS-16 | Verify 401 without authentication                | Negative |
| TS-17 | Delete non-existent note returns error           | Negative |

## TS-04: UI → API Data Consistency
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-18 | Note created in UI exists in API response        | E2E      |
| TS-19 | Note title/description match between UI and API  | E2E      |

## TS-05: API → UI Sync
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-20 | Note deleted via API disappears from UI          | E2E      |
| TS-21 | Note created via API appears in UI after refresh | E2E      |

## TS-06: Performance
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-22 | GET /notes response time < 2 seconds             | Perf     |
| TS-23 | POST /notes response time < 2 seconds            | Perf     |
| TS-24 | UI page load time < 5 seconds                    | Perf     |

## TS-07: Response Validation
| ID    | Scenario                                         | Type     |
|-------|--------------------------------------------------|----------|
| TS-25 | Note API response contains all required fields   | Positive |
| TS-26 | API health check returns 200                     | Positive |
