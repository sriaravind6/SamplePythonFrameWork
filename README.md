# 🧪 Python BDD Automation Framework

A production-ready **Behave + Selenium + Allure** test automation framework with automatic per-step screenshot capture.

---

## 📁 Project Structure

```
SamplePythonFrameWork/
├── features/
│   ├── login.feature              # Gherkin scenarios
│   └── steps/
│       └── step_definitions.py   # Step implementations
├── utils/
│   ├── config.py                 # Central configuration
│   ├── driver_factory.py         # WebDriver initializer
│   └── screenshot_helper.py      # Screenshot + Allure attach
├── environment.py                # Behave hooks (before/after)
├── behave.ini                    # Behave settings
├── requirements.txt              # Python dependencies
├── screenshots/                  # Auto-created screenshot store
├── reports/                      # Allure raw JSON results
└── logs/                         # Execution logs
```

---

## ⚙️ Setup

### 1. Create & activate virtual environment (recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Install Allure CLI (Windows via Scoop)
```powershell
# Install Scoop (if not already installed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```
> **Alternative**: Download from https://github.com/allure-framework/allure2/releases and add `bin/` to PATH.

---

## 🚀 Running Tests

### Run ALL scenarios (with Allure output)
```powershell
python -m behave -f allure_behave.formatter:AllureFormatter -o reports/
```

### Run only SMOKE tagged scenarios
```powershell
python -m behave -f allure_behave.formatter:AllureFormatter -o reports/ --tags=smoke
```

### Run only NEGATIVE scenarios
```powershell
python -m behave -f allure_behave.formatter:AllureFormatter -o reports/ --tags=negative
```

### Run with plain console output (no Allure)
```powershell
python -m behave
```

---

## 📊 Viewing Allure Report

```powershell
allure serve reports/
```
> This starts a local web server and opens the report in your browser automatically.

### Generate static HTML report
```powershell
allure generate reports/ -o allure-report/ --clean
allure open allure-report/
```

---

## 🌍 Environment Variables

Override any setting without changing code:

| Variable            | Default                                              | Description               |
|---------------------|------------------------------------------------------|---------------------------|
| `BASE_URL`          | `https://practicetestautomation.com/...`             | URL to open before tests  |
| `BROWSER`           | `chrome`                                             | `chrome`, `firefox`, `edge` |
| `HEADLESS`          | `false`                                              | Run browser headlessly    |
| `IMPLICIT_WAIT`     | `10`                                                 | Implicit wait (seconds)   |
| `EXPLICIT_WAIT`     | `20`                                                 | Explicit wait (seconds)   |
| `TEST_USERNAME`     | `student`                                            | Login username            |
| `TEST_PASSWORD`     | `Password123`                                        | Login password            |

**Example – headless Chrome run:**
```powershell
$env:HEADLESS="true"; python -m behave -f allure_behave.formatter:AllureFormatter -o reports/
```

---

## 📸 Screenshot Behaviour

- A screenshot is captured **after every step** (pass or fail)
- Saved to `screenshots/` with a timestamp + step name
- Automatically attached to the **Allure report**

---

## 🏷️ Available Tags

| Tag         | Scenarios                              |
|-------------|----------------------------------------|
| `@smoke`    | Happy path + logout                    |
| `@positive` | Valid credentials login                |
| `@negative` | Invalid username / password tests      |
| `@logout`   | Logout flow                            |

---

## ✅ Tested With

- Python 3.11+
- Chrome 124+ (auto-managed via webdriver-manager)
- Allure 2.27+
