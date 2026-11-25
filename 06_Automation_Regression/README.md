# Week 6 regression suite - how to run it on Windows

This folder automates the Week 1 and Week 2 tests of PyTodo Pro with PyTest and Selenium. It never changes the app and never uses its real database.

## 1. One-time setup

**a. Put the app next to this project.** Extract `pytodo_pro_student.zip` so the folders look like this:

```
working-folder\              (e.g. Downloads, or the folder holding the group repo)
  pytodo_pro_student\        <- app.py, helpers.py, templates\ ...
  STQA-Project-G4\  (or STQA_Week5_6\)
    06_Automation_Regression\   <- this folder
```

This is the same layout the group README uses.

If the app is somewhere else, tell the suite where before running: `$env:PYTODO_SOURCE_DIR = "C:\path\to\pytodo_pro_student"` (the same variable the Week 3/4 runners use)

**b. Create a virtual environment and install the tools.** In PowerShell, in this folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\..\pytodo_pro_student\requirements.txt -r requirements-regression.txt
```

If PowerShell blocks `Activate.ps1`, run `Set-ExecutionPolicy -Scope Process Bypass` first, then activate again.

**c. Browser.** Google Chrome must be installed, as in Lab 5. The first browser run downloads the matching driver automatically (Selenium Manager), so it needs internet once. To use Microsoft Edge instead, add `--browser edge`.

## 2. Run the suite

```powershell
python run_regression.py --suite smoke --label "Ahmad-PC-run-1"   # 29 key tests, about 10 s
python run_regression.py --label "Ahmad-PC-run-1"                 # all 104 tests
python run_regression.py --browser edge --label "Ahmad-PC-edge"   # browser tests in Edge
python run_regression.py --skip-ui                                # no browser (96 tests)
python run_regression.py --headed                                 # watch the browser
```

Use `--label` to record who ran it and where, for example your name and PC.

The last lines print a verdict:

| Verdict | Meaning |
|---|---|
| `PASSED (no new failures)` | Everything passed except the known open defects, which were seen again (XFAIL). This is the expected result for the current app. |
| `ATTENTION` + `NEW FAILURE` | Something that used to work now fails. Investigate and log a defect if it is the app's fault. |
| `ATTENTION` + `POSSIBLY FIXED` | A known-defect test passed (XPASS). Retest that defect by hand and update its status in the defect log. |

Expected result for the unchanged app: **PASS 88, XFAIL 16 (total 104)**. The 16 XFAILs are the nine open defects from Weeks 1-4.

## 3. Where the evidence goes

Each run creates a new folder, so nothing is overwritten:

```
evidence\<date-time>_<suite>_<label>\
  report.html     open in a browser: every test, with screenshots of the browser tests
  results.md      table of results with AUTO IDs, manual case IDs and requirements
  summary.json    counts, verdict, environment, app file hashes
  console.log     full PyTest output
  junit.xml       for CI tools
  screenshots\    one PNG per browser test
```

## 4. Run one layer or one test

```powershell
python -m pytest -m unit          # or: -m api, -m web, -m ui, -m smoke
python -m pytest -k dashboard     # tests whose name contains "dashboard"
python -m pytest --runxfail -m "not ui"   # show the real failure behind each known defect
```

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| `PyTodo Pro source not found` | Check step 1a, or set `$env:PYTODO_SOURCE_DIR`. |
| Browser tests error with a driver or session message | Update Chrome, check your internet for the first run, or use `--browser edge`. |
| `address already in use` on port 5002 | `$env:PYTODO_UI_PORT = "5003"`, then run again. |
| Many tests fail at once right after midnight | Rerun. Some tests use today's date, and a run that crosses midnight can mismatch. |

## 6. What is in this folder

| Path | Contents |
|---|---|
| `Week6_Report.md` | Week 6 report: candidate selection, design, results, experiments, reflection |
| `Regression_Test_Repository.md` | Every automated test with its objective, data, expected result, linked manual case and result |
| `run_regression.py` | One-command runner that saves evidence |
| `conftest.py`, `pytest.ini` | Shared setup: finds the app, isolates the database, known-defect and traceability markers |
| `tests/unit/` | Week 2's 41 white-box cases, re-run against the app's `helpers.py` |
| `tests/api/` | JSON API tests, plus one check per Week 4 defect |
| `tests/web/` | Page and form tests without a browser, plus the DEF-W3-002 label check |
| `tests/ui/` | Selenium tests and page objects, plus the DEF-W3-001 contrast check |
| `ci/github-actions-regression.yml` | Example CI workflow (not active) |
| `evidence/` | Recorded runs |
