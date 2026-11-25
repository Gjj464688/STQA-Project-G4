# PyTodo Pro - Week 6 test automation and regression

**Course:** TEB3433 / TFB3433 Software Testing and Quality Assurance, September 2026
**Assignment stage:** Week 6 - Test automation and regression
**Report date:** 2026-11-25 (Asia/Kuala_Lumpur, UTC+08:00)
**Team:** see the project README. Automation/Tool Coordinator: Ahmad Adam Ali.
**Execution provenance:** Suite written by Ahmad Adam Ali for the Automation/Tool Coordinator; development runs executed in a Linux workspace. Group runs on Windows: run 1 by Ahmad Adam Ali, 2026-11-26 (section 6.2); run 2: teammate `_____`, date `_____`. Group reviewer: `_____`.

## 1. Objective and scope

The brief asks the group to review earlier manual tests, select automation candidates by repetition, stability, criticality and regression value, map automated tests to the original cases, build and run automated tests with approved tools (PyTest/Selenium), create a focused regression suite, and analyse automation benefits and limitations.

This suite automates the **functional** behaviour tested in Week 1 (29 black-box cases) and Week 2 (41 white-box cases). It also adds **one regression check for every open defect found in Weeks 3 and 4**, so a single run reports the status of every open defect. The application is not changed: every run checks the SHA-256 of `app.py` (`050b4ee4...`) and `helpers.py` (`bf914033...`) against the Week 1-4 values and saves the result.

Not in this suite, by design:
- **The full Week 4 API suite (53 cases) and the Week 3/4 browser checks.** They are already automated with their own runners (`04_Web_API/run_api_tests.py`, `03_.../run_browser_checks.mjs`). Copying them here would duplicate them. A full regression pass runs this suite plus those runners.
- **Security tests.** Week 5's planned security checks will be added once the team has run them. DEF-W1-003 (cross-user delete) is already checked on every Week 4 run by API-25.
- **Performance.** Measured with JMeter in Week 5. A load test is not a pass/fail regression check.

## 2. Review of earlier tests

| Source | What exists | Automation status before Week 6 |
|---|---|---|
| Week 1 black-box | 29 cases (EP, BVA, decision table, state transition), manual + a Playwright script | Manual; the script only runs on one machine |
| Week 2 white-box | 41 PyTest cases, fixed clocks | Automated, but against a copied snapshot of `helpers.py` |
| Week 3 GUI/compatibility/accessibility | 37 cases: 30 automated browser checks (Playwright), 7 manual usability observations | Browser checks automated; usability manual |
| Week 4 web and API | 20 browser checks (Playwright), 53 API cases (PyTest) | Automated |
| Open defects | DEF-W1-001 to 004, DEF-W2-001, DEF-W3-001/002, DEF-W4-001 to 003 | Each week's runner checks only its own defects |

**The Week 1 Playwright script** (`01_Black_Box/run_browser_cases.mjs`) was reviewed and not extended. It loads Playwright from one computer's AI-tool cache, uses a hard-coded Edge path and needs a manual database reset. It also runs all 29 cases in the browser, the slowest and most fragile layer. The brief and Lab 5 name PyTest and Selenium for this stage. The script stays as Week 1 evidence, and its 29 cases are moved to the cheapest layer that can check each rule.

## 3. Automation candidate selection

Each group of cases was rated on the brief's four criteria. Criticality uses the Week 1 risk scores (impact × likelihood).

| Cases | Feature (req., risk) | Repetition | Stability | Criticality | Regression value | Decision and layer(s) |
|---|---|---|---|---|---|---|
| TC-BB-001 to 005 | Username rules (R-01, 6) | High | High | Medium-high | High: boundary logic | **Automate** at unit + API; web for invalid character; one browser test |
| TC-BB-006, 007 | Password minimum (R-01, 6) | High | High | Medium-high | **Very high**: open DEF-W1-001 | **Automate at all four layers**, because users see the defect in the form |
| TC-BB-008 to 010 | Login, logout, protected pages (R-02, 6) | High | High | High | High | **Automate** at API, web and browser; smoke set |
| TC-BB-011, 012 | Create task (R-04, 6) | High | High | High | High | **Automate** at API and web; 011 also in the browser |
| TC-BB-013 | Blank title in browser (R-04) | Medium | Low-medium: browser's own prompt | Medium | Medium | **Partly automate**: server rule via API; the browser prompt stays manual |
| TC-BB-014 | Whitespace-only title (R-04) | High | High | Medium | **Very high**: open DEF-W1-004 | **Automate** at web (where the defect is) and API |
| TC-BB-015 to 017 | Edit, done/reopen, delete (R-05/R-06, 4) | High | High | Medium | High | **Automate** at API and web; 016, 017 also in the browser |
| TC-BB-018 | Separate users' lists (R-03, 9) | High | High | **Highest** | High | **Automate** list isolation at API and web |
| TC-BB-019 to 023 | Urgency boundaries (R-07, 6) | High | Medium: date-dependent | High | **Very high**: open DEF-W1-002 | **Automate**; unit tests use a fixed clock |
| TC-BB-024 to 028 | Filters and search (R-08, 4) | High | High | Medium | Medium | **Automate** at API and web as a parametrised decision table |
| TC-BB-029 | Dashboard counts (R-09, 4) | High | High | Medium | High | **Automate** at API and web |
| TC-WB-001 to 041 | Week 2 white-box cases | High | High | Medium-high | High: includes DEF-W2-001 | **Reuse unchanged**, now against the app's own `helpers.py` |
| ACC-TC-002, ACC-TC-008 | Week 3 accessibility defects (R-11) | Medium | High: measured values | Medium | High: open DEF-W3-001/002 | **One check each** (browser for contrast, web for labels) |
| API-32, API-42, API-49/50 | Week 4 robustness defects (R-04/R-10) | High | High | High | **Very high**: open DEF-W4-001 to 003 | **One API check each** |
| Other Week 3/4 cases | GUI, compatibility, web and API | High | High | Medium | Medium | **Already automated** in their own runners; not duplicated |

**Kept manual:** usability observations and visual consistency (Week 3), exploratory testing, the browser's own required-field prompt, and duplicate usernames (P-03). These need human judgement, and the STQA09/10 slides note that visually subjective and exploratory work suits manual testing. Duplicate usernames have no agreed expected behaviour yet, and a test needs an expected result. Week 4's 12 assumption failures are not added for the same reason.

## 4. Suite design

The suite follows the test pyramid from the STQA09/10 lecture: many fast low-level tests and few slow end-to-end tests.

| Layer | Tool | Tests | Smoke | What it exercises |
|---|---|---:|---:|---|
| Unit | PyTest | 41 | 7 | `helpers.py` functions directly, fixed clock |
| API | PyTest + Flask test client | 34 | 12 | JSON endpoints, status codes and bodies |
| Web | PyTest + Flask test client | 21 | 6 | Pages and form posts (the same fields a browser sends) |
| UI (browser) | Selenium + PyTest, page objects as in Lab 5 | 8 | 4 | Real Chrome/Edge against a live isolated server |
| **Total** | | **104** | **29** | |

1. **Isolation.** Each unit, API and web test uses a new empty SQLite file. Browser tests use one throwaway database on 127.0.0.1:5002 with unique usernames. The real `pytodo_pro.db` is never touched and no manual reset is needed.
2. **Known defects as strict expected failures.** A test linked to an open defect is marked `@known_defect("DEF-...")`. While the defect is present it reports **XFAIL**, so the run stays green but still checks the defect. If the defect is fixed the test reports **XPASS**, which counts as a failure and tells the team to retest and update the defect log. Expected results are never changed to match wrong behaviour.
3. **Traceability in code.** Every test carries `@trace("AUTO-...", manual=[...], req=[...])`, and the runner saves these links next to each result.
4. **Smoke set (29 tests, about 8 s):** one test per critical requirement plus one test for every open defect.
5. **Stable browser tests.** Page objects keep locators in one place. Every form-submitting click waits for the new page (section 6.3). Dates are set in ISO format, because typed dates follow the computer's locale.
6. **Evidence by default.** `run_regression.py` saves the console log, JUnit XML, an HTML report with screenshots, per-test results with traceability, and a summary with environment and app hashes, in a new timestamped folder for every run.

Per-test details are in [Regression_Test_Repository.md](Regression_Test_Repository.md).

## 5. Manual-to-automated traceability summary

- **All 29 Week 1 cases** have an automated counterpart (28 fully; TC-BB-013 partly).
- **All 41 Week 2 cases** are re-run unchanged (`TC-WB-nnn` → `AUTO-UNIT-nnn`).
- **Week 3/4 open defects:** ACC-TC-002 → AUTO-UI-008; ACC-TC-008 → AUTO-WEB-015; API-32 → AUTO-API-019; API-42 → AUTO-API-020; API-49/50 → AUTO-API-021.
- **Requirements:** R-01, R-02 and R-04 to R-09 are covered at two or more layers; R-03 (list isolation), R-10 and R-11 (open defects only) are covered in part. R-12 (security and performance) belongs to Week 5.
- **Open defects checked on every run (16 tests):** DEF-W1-001 (4), DEF-W1-002 (3), DEF-W1-004 (1), DEF-W2-001 (3), DEF-W3-001 (1), DEF-W3-002 (1), DEF-W4-001 (1), DEF-W4-002 (1), DEF-W4-003 (1). DEF-W1-003 is checked by Week 4 API-25.

## 6. Execution results

### 6.1 Environment (agent-executed runs)

Linux workspace (Ubuntu 24.04, x86_64, 2 CPUs); Python 3.13.18; Flask 3.0.3 (the app's pinned version); Werkzeug 3.1.9; pytest 9.1.1; pytest-html 4.2.0; Selenium 4.54.0; Chrome for Testing 153.0.8010.12, headless, 1280x900, with ChromeDriver 153.0.8010.52; UTC+08:00. App unchanged in every run except the two labelled experiments. A clean Python 3.12 setup was also checked and gave the same results.

**Ahmad's laptop run:** Windows 11 (build 26300), AMD Ryzen 7 7730U, Python 3.13.15, Flask 3.0.3, Werkzeug 3.1.9, pytest 9.1.1, Selenium 4.51.0, Chrome 157.0.8103.79 headless at 1280x900; UTC+08:00. App hashes matched the baseline.

### 6.2 Recorded runs

All runs are in `evidence/`, named `<date-time>_<suite>_<label>`. Durations are wall-clock, including PyTest start-up.

| Run | Suite | Result | Total | Duration | Notes |
|---|---|---|---:|---:|---|
| agent-run-1 | Smoke (earlier 24-test version) | ATTENTION: PASS 17, XFAIL 6, **ERROR 1** | 24 | 4.8 s | Flaky browser wait; see 6.3 |
| agent-run-2 | Smoke | PASSED: PASS 18, XFAIL 11 | 29 | 7.9 s | |
| agent-run-3 | Full | PASSED: PASS 88, XFAIL 16 | 104 | 17.8 s | Reference run for the test repository |
| agent-run-4 | Full | PASSED: PASS 88, XFAIL 16 | 104 | 18.9 s | Repeat: identical results |
| agent-run-5 | Full, no browser | PASSED: PASS 82, XFAIL 14 | 96 | 4.0 s | Fast layers only (the CI fast job) |
| experiment-A | Full, temporary copy | ATTENTION: PASS 88, XFAIL 12, **XPASS 4** | 104 | 19.7 s | Simulated fix; section 7 |
| experiment-B | Full, temporary copy | ATTENTION: PASS 85, XFAIL 16, **FAIL 3** | 104 | 16.2 s | Simulated regression; section 7 |
| **Ahmad-PC** | Full, on Windows | PASSED: PASS 88, XFAIL 16 | 104 | 49.4 s | Ahmad's laptop, Chrome 157 (`evidence/20261126-024054_full_Ahmad-PC`) |

On the unchanged app every run, on Linux and on Ahmad's Windows laptop, observed the same nine open defects again, with no new failures. The Windows run gave exactly the same result as the Linux runs.

**Per layer (agent-run-3, test-body time only):**

| Layer | Tests | PASS | XFAIL | Time | Average per test |
|---|---:|---:|---:|---:|---:|
| Unit | 41 | 36 | 5 | under 0.01 s | under 1 ms |
| API | 34 | 29 | 5 | 1.36 s | 0.04 s |
| Web | 21 | 17 | 4 | 0.95 s | 0.045 s |
| UI | 8 | 6 | 2 | 5.97 s | 0.75 s |

A browser test takes about 18 times longer than an API test, before counting browser start-up. Including start-up, the 8 browser tests add about 14 seconds to a full run (17.8 s with them, 4.0 s without). That cost is why the browser layer is kept small.

### 6.3 Flaky test found and fixed

In agent-run-1, `AUTO-UI-005` failed during setup with a WebDriver error ("Node with given id does not belong to the document"). The page objects waited for the old page to disappear using Selenium's `staleness_of`. While Chrome was mid-navigation it returned this internal error instead, so the result depended on timing. **Fix** (`tests/ui/pages/waits.py`): treat any error during navigation as "still loading", then wait for `document.readyState == "complete"`. The browser layer was then run 10 times in a row (70 browser test executions) with no errors. That console check was not saved as an evidence folder. This lowers the risk of flakiness but cannot prove there is none. The failing run is kept as evidence.

## 7. Does the suite detect change? Two controlled experiments

Each experiment used a **temporary copy** of the app with one line changed. The supplied files were not modified, and their hashes were unchanged afterwards.

- **Experiment A, simulated defect fix.** `is_valid_password` was changed from `> 8` to `>= 8`, a likely fix for DEF-W1-001. All 4 DEF-W1-001 tests (unit, API, web, browser) reported **XPASS**, and the runner printed "POSSIBLY FIXED ... retest and update the defect log". The other eight defects were still reported as present. A fix can't go unnoticed.
- **Experiment B, simulated regression.** The web route that marks a task done stopped saving the completion time. **Three tests failed:** AUTO-WEB-009, AUTO-WEB-014 and AUTO-UI-005, all reporting completed counts of 0 instead of 1. The API layer did **not** catch it, because the API marks tasks done through a different route. Web and API share rules but not code, so both layers need tests.

## 8. Reflection: benefits and limitations

> **DRAFT. Ahmad: rewrite this in your own words after your own runs, and add what you noticed (setup problems, time taken, anything surprising).**

**Benefits**
- **Speed:** all 104 checks run with one command in about 18 seconds, or about 4 seconds without the browser.
- **Repeatability:** two full runs gave identical results, and no manual database reset is needed.
- **Defect tracking:** every run confirms the nine open defects, and experiment A shows a fix gets flagged automatically.
- **Regression detection:** experiment B was caught at two layers, and it showed why both web and API tests are needed.
- **Evidence:** each run produces the reports, screenshots and traceability the final report needs.

**Limitations**
- **Browser tests are slow and fragile.** The only unexpected failure came from browser timing, not the app.
- **Automation checks only what it is told to.** Every assertion encodes an expected result someone decided; DEF-W1-004, for example, still needs its expectation confirmed. Automation can't judge usability or appearance.
- **The test client is not a real server.** The API and web layers skip the real HTTP server; only the 8 browser tests use it.
- **Date-dependent tests** could misbehave if a run crosses midnight. The unit layer avoids this with a fixed clock.
- **Environment:** the suite was developed on Linux. Ahmad's Windows run gave identical results; a second group computer is still to be tried (section 9).

## 9. Remaining actions

1. **Ahmad:** done on Windows with Chrome (88 Pass / 16 XFAIL). Optional: once more with `--browser edge`.
2. **A teammate:** run it on a second computer.
3. **Group:** review the tests and decisions; record the reviewer.
4. **After Week 5:** add the agreed security checks with `@trace` and `@known_defect` markers.
5. **Week 7:** copy the traceability links into the RTM and master test repository.
6. **Week 12 (CI/CD):** `ci/github-actions-regression.yml` shows the fast layers on every push and the browser layer nightly. It needs an agreed copy of the app in the repository.

## 10. How to run

See [README.md](README.md). Short version (PowerShell, in this folder):

```powershell
python run_regression.py --suite smoke     # 29 tests, about 10 s
python run_regression.py                   # all 104 tests
```
