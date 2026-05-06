# ============================================
# TEST PLAN
# UI + API Hybrid Automation Framework
# Notes Application
# ============================================

## 1. INTRODUCTION

### 1.1 Project Overview
This test plan covers the UI and API testing of the Notes Application
(https://practice.expandtesting.com/notes/app) using a hybrid Selenium + Python + Pytest
automation framework.

### 1.2 Objectives
- Validate UI login functionality with positive and negative scenarios
- Verify note CRUD operations via both UI and API
- Ensure data consistency between UI and API layers
- Validate API response times meet SLA (< 2 seconds)
- Test error handling and edge cases

### 1.3 Scope
**In Scope:**
- User authentication (login/register)
- Note creation, reading, updating, and deletion
- UI-API data consistency (hybrid E2E tests)
- API response validation (status codes, schema, timing)
- Negative testing (invalid inputs, unauthorized access)

**Out of Scope:**
- Password reset flows (requires email verification)
- Browser compatibility testing (beyond Chrome, Firefox, Edge)
- Load/stress testing at scale
- Mobile responsiveness testing

---

## 2. TEST ENVIRONMENT

| Component       | Details                                                |
|-----------------|--------------------------------------------------------|
| Application URL | https://practice.expandtesting.com/notes/app           |
| API Base URL    | https://practice.expandtesting.com/notes/api           |
| Browsers        | Chrome (primary), Firefox, Edge                        |
| OS              | Windows 10/11                                          |
| Framework       | Python 3.10+ / Selenium 4.x / Pytest 7.x              |
| Reporting       | Allure Reports                                         |

---

## 3. TEST STRATEGY

### 3.1 Test Types
| Type        | Tool/Method              | Coverage                      |
|-------------|--------------------------|-------------------------------|
| UI Tests    | Selenium WebDriver + POM | Login, Note CRUD via browser  |
| API Tests   | Requests library         | REST API CRUD, auth, perf     |
| E2E Hybrid  | Selenium + Requests      | Cross-layer data consistency  |
| Performance | Response time assertions | API < 2s, UI load < 5s       |

### 3.2 Test Levels
- **Smoke Tests**: Critical path (login + create note + API health)
- **Regression Tests**: Full test suite across all modules
- **Negative Tests**: Invalid inputs, unauthorized access, edge cases

### 3.3 Test Execution
- **Local**: `pytest tests/ -v`
- **Parallel**: `pytest tests/ -n 4`
- **CI/CD**: Jenkins pipeline with Allure reporting

---

## 4. ENTRY/EXIT CRITERIA

### Entry Criteria
- Application deployed and accessible
- API health check returns 200
- Test environment configured
- Test data requirements documented

### Exit Criteria
- All smoke tests pass (100%)
- Regression pass rate >= 95%
- No critical/blocker defects open
- All test artifacts archived

---

## 5. RISKS AND MITIGATIONS

| Risk                          | Impact | Mitigation                          |
|-------------------------------|--------|-------------------------------------|
| Flaky UI elements             | Medium | Self-healing locators + retry logic |
| Network latency               | Medium | Configurable timeouts + retries    |
| Test data pollution            | Low    | Unique data per test + cleanup     |
| API breaking changes           | High   | Schema validation + monitoring     |

---

## 6. DELIVERABLES
- Test Plan (this document)
- Test Scenarios and Test Cases
- Requirement Traceability Matrix (RTM)
- Automation framework with full code
- Allure test execution reports
- Jenkins CI/CD pipeline configuration
