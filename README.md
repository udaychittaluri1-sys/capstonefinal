# ============================================================
# UI + API Hybrid Automation Framework
# Notes Application — Complete Execution Guide
# ============================================================

## 📁 Project Structure

```
capstone/
├── tests/
│   ├── test_login.py          # UI login tests (8 tests)
│   ├── test_notes_ui.py       # UI note CRUD tests (6 tests)
│   ├── test_notes_api.py      # API tests (12 tests)
│   └── test_e2e.py            # Hybrid E2E tests (4 tests)
├── pages/
│   ├── base_page.py           # Base POM with waits + self-healing
│   ├── login_page.py          # Login page object
│   ├── register_page.py       # Register page object
│   └── notes_page.py          # Notes dashboard page object
├── api/
│   ├── api_client.py          # Full REST API client
│   └── endpoints.py           # API endpoint constants
├── utils/
│   ├── logger.py              # Color console + file logger
│   ├── config_reader.py       # YAML config reader (singleton)
│   └── helpers.py             # Test data, screenshots, AI helpers
├── fixtures/
│   ├── driver_fixture.py      # WebDriver factory (Chrome/FF/Edge)
│   ├── api_fixture.py         # API client setup/teardown
│   └── conftest.py            # Central pytest fixtures
├── config/
│   ├── config.yaml            # All framework settings
│   └── environment.py         # Multi-environment support
├── docs/
│   ├── test_plan.md           # Test Plan
│   ├── test_scenarios.md      # Test Scenarios (TS-01 to TS-26)
│   ├── test_cases.md          # Step-by-step Test Cases
│   └── rtm.md                 # Requirement Traceability Matrix
├── reports/                   # Auto-created on first run
│   ├── allure-results/
│   ├── screenshots/
│   └── logs/
├── conftest.py                # Root conftest
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── Jenkinsfile                # CI/CD pipeline
└── README.md
```

---

## ⚙️ Prerequisites

| Requirement         | Version    |
|---------------------|------------|
| Python              | 3.10+      |
| Google Chrome       | Latest     |
| Git                 | Any        |
| Java (for Allure)   | 8+         |
| Allure CLI          | 2.x        |

---

## 🚀 Step-by-Step Setup

### Step 1 — Open Terminal in Project Folder

```powershell
cd "C:\Users\meera\OneDrive\Documents\Attachments\Desktop\capstone"
```

### Step 2 — Create Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Install Allure CLI (One-time)

Using Scoop (recommended for Windows):
```powershell
scoop install allure
```

Or download from: https://github.com/allure-framework/allure2/releases

---

## ▶️ Running Tests

### Run ALL Tests
```powershell
pytest tests/ -v
```

### Run Smoke Tests Only
```powershell
pytest tests/ -m smoke -v
```

### Run API Tests Only
```powershell
pytest tests/test_notes_api.py -v
```

### Run UI Tests Only
```powershell
pytest tests/test_login.py tests/test_notes_ui.py -v
```

### Run E2E Hybrid Tests Only
```powershell
pytest tests/test_e2e.py -v
```

### Run with Allure Reporting
```powershell
pytest tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Run in Parallel (4 workers)
```powershell
pytest tests/ -n 4 -v
```

### Run with Auto-retry (for flaky tests)
```powershell
pytest tests/ --reruns=2 --reruns-delay=2 -v
```

### Run Negative Tests Only
```powershell
pytest tests/ -m negative -v
```

### Run Performance Tests Only
```powershell
pytest tests/ -m performance -v
```

### Run in Headless Mode (edit config.yaml)
Set `headless: true` in `config/config.yaml`, then:
```powershell
pytest tests/ -v
```

---

## 📊 Allure Report Setup

```powershell
# Generate results
pytest tests/ --alluredir=reports/allure-results

# Open live report in browser
allure serve reports/allure-results

# Generate static HTML report
allure generate reports/allure-results -o reports/allure-html --clean
```

---

## 🔧 Configuration (config/config.yaml)

```yaml
browser:
  name: "chrome"        # chrome / firefox / edge
  headless: false        # true for CI/CD
  explicit_wait: 15      # seconds

api:
  max_response_time: 2.0 # SLA threshold in seconds

test_user:
  password: "TestPass@123"
```

---

## 🏷️ Pytest Markers

| Marker        | Description                          |
|---------------|--------------------------------------|
| `smoke`       | Critical path tests (fast feedback)  |
| `regression`  | Full regression suite                |
| `ui`          | Selenium UI tests                    |
| `api`         | REST API tests                       |
| `e2e`         | Hybrid UI + API tests                |
| `negative`    | Negative/boundary tests              |
| `performance` | Response time validation tests       |

---

## 🔁 CI/CD (Jenkins)

The `Jenkinsfile` provides a full parameterized pipeline:
- **BROWSER**: chrome / firefox / edge
- **ENV**: dev / staging / production
- **HEADLESS**: true/false
- **MARKERS**: smoke / regression / e2e / all
- **PARALLEL_WORKERS**: number of parallel jobs

Pipeline Stages:
1. Checkout → Setup Env → API Health Check
2. Smoke / API / UI / E2E (based on marker param)
3. Allure Report Generation
4. Archive artifacts

---

## 🧩 Framework Features

| Feature               | Implementation                          |
|-----------------------|-----------------------------------------|
| Page Object Model     | `pages/` with BasePage inheritance      |
| Explicit Waits        | WebDriverWait + EC throughout           |
| Self-Healing Locators | `_self_heal_locator()` in BasePage      |
| Retry Logic           | `pytest-rerunfailures` + click retries  |
| Screenshot on Failure | `capture_screenshot()` in conftest hook |
| Allure Reporting      | `@allure.step`, `@allure.story`, etc.   |
| Parallel Execution    | `pytest-xdist` with `-n N` flag         |
| Custom Logger         | `colorlog` + rotating file handler      |
| API Client            | `requests.Session` with token auth      |
| Test Data Generation  | `Faker` + random helpers                |
| AI Failure Analysis   | `ai_analyze_failure()` in helpers.py    |
| Multi-environment     | `config/environment.py` + env vars      |
| CI/CD                 | Jenkins declarative pipeline            |

---

## 📝 Test Count Summary

| Module              | Tests | Markers              |
|---------------------|-------|----------------------|
| test_login.py       | 8     | smoke, ui, negative  |
| test_notes_ui.py    | 6     | smoke, ui, regression|
| test_notes_api.py   | 12    | smoke, api, perf, neg|
| test_e2e.py         | 4     | smoke, e2e, perf     |
| **TOTAL**           | **30**|                      |

---

## ❓ Troubleshooting

| Issue                        | Solution                                          |
|------------------------------|---------------------------------------------------|
| ChromeDriver not found       | `webdriver-manager` auto-downloads it             |
| ModuleNotFoundError          | Run `pip install -r requirements.txt`             |
| Tests fail with timeout      | Increase `explicit_wait` in config.yaml           |
| Allure not found             | Install Allure CLI via Scoop or manually          |
| Tests slow on OneDrive path  | Move project to `C:\capstone` outside OneDrive    |
| Port already in use          | Close other browser sessions                      |
