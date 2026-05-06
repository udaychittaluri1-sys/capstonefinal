# ============================================
# TEST CASES - Step by Step
# Notes Application
# ============================================

## TC-01: Valid Login

| Field             | Details                                          |
|-------------------|--------------------------------------------------|
| Test Case ID      | TC-01                                            |
| Test Scenario     | TS-01: User Authentication                       |
| Title             | Verify user can login with valid credentials     |
| Priority          | Critical                                         |
| Type              | Positive / Smoke                                 |
| Automated         | Yes → test_login.py::TestLogin::test_valid_login |

**Preconditions:** User account exists. App is accessible.

| Step | Action                                      | Expected Result                              |
|------|---------------------------------------------|----------------------------------------------|
| 1    | Navigate to /notes/app/login                | Login page loads with email & password fields |
| 2    | Enter valid email address                   | Email field populated                        |
| 3    | Enter valid password                        | Password field populated (masked)            |
| 4    | Click Login button                          | Form submitted                               |
| 5    | Observe redirect                            | Redirected to /notes/app (dashboard)         |

**Expected Result:** User is logged in and directed to Notes dashboard.

---

## TC-02: Login with Invalid Email

| Field             | Details                                            |
|-------------------|----------------------------------------------------|
| Test Case ID      | TC-02                                              |
| Test Scenario     | TS-02: Invalid Authentication                      |
| Title             | Verify login fails with unregistered email         |
| Priority          | High                                               |
| Type              | Negative                                           |
| Automated         | Yes → test_login.py::TestLogin::test_invalid_email |

**Preconditions:** App is accessible.

| Step | Action                              | Expected Result                        |
|------|-------------------------------------|----------------------------------------|
| 1    | Navigate to /notes/app/login        | Login page loads                       |
| 2    | Enter invalid@wrong.com             | Email field populated                  |
| 3    | Enter any password                  | Password field populated               |
| 4    | Click Login button                  | Form submitted                         |
| 5    | Observe page behavior               | Error shown OR still on login page     |

**Expected Result:** Login fails. User remains on login page.

---

## TC-03: Login with Wrong Password

| Field             | Details                                               |
|-------------------|-------------------------------------------------------|
| Test Case ID      | TC-03                                                 |
| Title             | Verify login fails with incorrect password            |
| Type              | Negative                                              |
| Automated         | Yes → test_login.py::TestLogin::test_invalid_password |

| Step | Action                              | Expected Result                        |
|------|-------------------------------------|----------------------------------------|
| 1    | Navigate to /notes/app/login        | Login page loads                       |
| 2    | Enter valid registered email         | Email field populated                  |
| 3    | Enter wrong password                | Password masked                        |
| 4    | Click Login button                  | Request sent                           |
| 5    | Observe result                      | Login fails, error shown               |

---

## TC-04: Create Note via UI (Home Category)

| Field             | Details                                                       |
|-------------------|---------------------------------------------------------------|
| Test Case ID      | TC-04                                                         |
| Test Scenario     | TS-06                                                         |
| Title             | Create note with Home category and verify appears in dashboard|
| Priority          | Critical                                                      |
| Type              | Positive / Smoke                                              |
| Automated         | Yes → test_notes_ui.py::test_create_note_home_category        |

**Preconditions:** User is logged in.

| Step | Action                              | Expected Result                              |
|------|-------------------------------------|----------------------------------------------|
| 1    | Click "Add New Note" button          | Note creation form opens                    |
| 2    | Select category "Home"              | Home selected in dropdown                    |
| 3    | Enter note title                    | Title field populated                        |
| 4    | Enter note description              | Description field populated                  |
| 5    | Click Create/Save button            | Form submitted, note created                 |
| 6    | Observe dashboard                   | New note card appears immediately            |

**Expected Result:** Note appears on dashboard with correct title.

---

## TC-05: Note Count Increases After Creation

| Field             | Details                                                          |
|-------------------|------------------------------------------------------------------|
| Test Case ID      | TC-05                                                            |
| Title             | Verify note count increases by 1 after creating note             |
| Type              | Positive / Regression                                            |
| Automated         | Yes → test_notes_ui.py::test_note_appears_instantly_after_creation|

| Step | Action                              | Expected Result                              |
|------|-------------------------------------|----------------------------------------------|
| 1    | Record current note count           | Count N captured                             |
| 2    | Create one new note                 | Note submitted                               |
| 3    | Count notes on dashboard            | Count is now N+1                             |

---

## TC-06: GET /notes API Returns 200

| Field             | Details                                             |
|-------------------|-----------------------------------------------------|
| Test Case ID      | TC-06                                               |
| Title             | GET /notes returns 200 with user's note list        |
| Priority          | Critical                                            |
| Type              | API / Smoke                                         |
| Automated         | Yes → test_notes_api.py::TestNotesAPI::test_get_all_notes |

**Preconditions:** User is authenticated (token available).

| Step | Action                                      | Expected Result                    |
|------|---------------------------------------------|------------------------------------|
| 1    | Register and login via API                  | Token obtained                     |
| 2    | Send GET /notes with x-auth-token header    | Request sent                       |
| 3    | Check response status code                  | 200 OK                             |
| 4    | Check response body                         | success=true, data=array           |

---

## TC-07: DELETE /notes/{id} Removes Note

| Field             | Details                                             |
|-------------------|-----------------------------------------------------|
| Test Case ID      | TC-07                                               |
| Title             | Delete note via API and verify it no longer exists  |
| Priority          | Critical                                            |
| Type              | API / Smoke                                         |
| Automated         | Yes → test_notes_api.py::TestNotesAPI::test_delete_note_api |

| Step | Action                                      | Expected Result                    |
|------|---------------------------------------------|------------------------------------|
| 1    | Create note via POST /notes                 | Note created, ID captured          |
| 2    | Send DELETE /notes/{id}                     | 200 OK returned                    |
| 3    | Send GET /notes/{id}                        | 404 or error response              |

---

## TC-08: API Response Time < 2 Seconds

| Field             | Details                                                |
|-------------------|--------------------------------------------------------|
| Test Case ID      | TC-08                                                  |
| Title             | Verify GET /notes response time is under 2 seconds     |
| Type              | Performance                                            |
| Automated         | Yes → test_notes_api.py::test_get_notes_response_time  |

| Step | Action                         | Expected Result              |
|------|--------------------------------|------------------------------|
| 1    | Login via API                  | Token obtained               |
| 2    | Record timestamp               | Start time captured          |
| 3    | Send GET /notes                | Response received            |
| 4    | Measure elapsed time           | elapsed < 2.0 seconds        |

---

## TC-09: UI → API Data Consistency (E2E Scenario 1)

| Field             | Details                                                     |
|-------------------|-------------------------------------------------------------|
| Test Case ID      | TC-09                                                       |
| Title             | Note created in UI matches data fetched via API             |
| Priority          | Critical                                                    |
| Type              | E2E / Smoke                                                 |
| Automated         | Yes → test_e2e.py::TestE2E::test_ui_create_api_verify       |

| Step | Action                                | Expected Result                         |
|------|---------------------------------------|-----------------------------------------|
| 1    | Login to app (UI + API)               | Both sessions authenticated             |
| 2    | Create note via UI with known title   | Note appears on UI dashboard            |
| 3    | Call GET /notes via API               | 200 response with notes list            |
| 4    | Find note by title in API response    | Note found in API data                  |
| 5    | Compare title, description, category  | All fields match between UI and API     |

---

## TC-10: API Delete Removes Note from UI (E2E Scenario 2)

| Field             | Details                                                     |
|-------------------|-------------------------------------------------------------|
| Test Case ID      | TC-10                                                       |
| Title             | Note deleted via API disappears from UI after refresh       |
| Priority          | Critical                                                    |
| Type              | E2E / Smoke                                                 |
| Automated         | Yes → test_e2e.py::TestE2E::test_api_delete_ui_verify       |

| Step | Action                                | Expected Result                         |
|------|---------------------------------------|-----------------------------------------|
| 1    | Create note via API                   | Note created, ID captured               |
| 2    | Refresh browser                       | Note appears in UI dashboard            |
| 3    | Delete note via DELETE /notes/{id}    | 200 OK response                         |
| 4    | Refresh UI page                       | Note list reloads                       |
| 5    | Search for deleted note title         | Note NOT found in UI                    |

---

## TC-11: Unauthorized Access Returns 401

| Field             | Details                                                     |
|-------------------|-------------------------------------------------------------|
| Test Case ID      | TC-11                                                       |
| Title             | Accessing /notes without token returns 401                  |
| Type              | Negative / API                                              |
| Automated         | Yes → test_notes_api.py::test_get_notes_without_auth        |

| Step | Action                              | Expected Result              |
|------|-------------------------------------|------------------------------|
| 1    | Do NOT login (no token)             | No x-auth-token header       |
| 2    | Send GET /notes                     | Request sent without auth    |
| 3    | Check status code                   | 401 Unauthorized             |
