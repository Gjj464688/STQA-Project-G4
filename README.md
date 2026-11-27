# STQA Project Group 4

Software Testing and Quality Assurance assessment of **PyTodo Pro**, the supplied Flask and SQLite task manager. This repository contains test designs, scripts, execution evidence, and quality reports. Application defects are documented as findings and recommendations; the supplied application code remains unchanged.

## Final submission

Group 4's integrated submission package (27 November 2026):

| Deliverable | File | Description |
|---|---|---|
| Final QA report (PDF) | [STQA Group 4 Final QA Report](08_Final_QA_Report/STQA_Group4_Final_QA_Report.pdf) | 38-page integrated report, including Weeks 1–8, standards integration, risks and recommendations. |
| Presentation (PowerPoint) | [PyTodo Pro QA Presentation](09_Presentation/PyTodo_Pro_QA_Presentation.pptx) | 14-slide presentation for the group quality evaluation. |
| Demonstration video (MP4) | [STQA PyTodo Pro Demo](09_Presentation/STQA_PyTodoPro_Demo.mp4) | 3-minute recorded demonstration with audio, selected live checks and saved evidence. Download the MP4 to play it locally. |

The weekly reports, test cases, scripts and execution evidence below support these three submission deliverables.

## Team

| Member | Student ID | Proposed coordination role |
|---|---|---|
| Gan Jeng Jie | 22003737 | QA and test lead |
| Wan Qistina Binti Wan Abdullah | 22003159 | Test design |
| Ahmad Adam Ali bin Wahid Ali | 24000180 | Automation and tools |
| Sathineswary Saravanesvaran | 20001344 | Defects and metrics |

Student IDs follow the supplied Group 4 Lab 3 cover sheet. Planned assignments do not establish who performed a particular execution; execution provenance is recorded in the relevant report.

## Progress

Updated **27 November 2026**. Week 3 and Week 4 verification was executed on 12 November; Week 5 and Week 6 execution evidence includes Linux and Windows laptop runs on 25–26 November. The final PDF, presentation and edited demonstration video are now included in the repository.

| Stage | Recorded results | Status |
|---|---|---|
| Week 1 black-box testing | 29 manual cases and 29 separate automated cases; each execution records 26 Pass / 3 Fail | Execution complete within selected scope |
| Week 2 white-box testing | 41 unit cases: 36 Pass / 5 Fail; four selected helpers | Execution complete within selected scope |
| Week 3 GUI, compatibility, usability, accessibility | 37 cases: 35 Pass / 2 Fail; includes 30 automated checks and 7 user-reported manual usability observations | Complete within selected scope; two accessibility defects open |
| Week 4 web testing | 20 browser cases: 18 Pass / 2 Fail | Complete within selected scope |
| Week 4 API testing | 53 cases: 36 Pass / 17 Fail; no setup errors | Complete within selected scope; confirmed defects and unconfirmed policy assumptions distinguished |
| Week 5 security and performance | 17 STRIDE entries, eight source-review findings; performance measured in two environments | Performance execution and four static control reviews complete (1 Pass / 3 Fail) |
| Week 6 automation and regression | 104 full-suite tests: 88 Pass / 16 XFAIL; 29-test smoke suite | Execution complete; matching Linux and Windows reference outcomes |
| Week 7 test management | Test plan/strategy, case-level registry (288 IDs), RTM and defect log | Consolidated |
| Week 8 final QA evaluation | Integrated metrics, charts, 11 open defect records, risk assessment and recommendations | Integrated report and metrics complete |
| Standards integration and presentation | Integrated PDF with ISO/IEC 25010, ISO 9001, CMMI, Agile/DevOps and CI/CD discussion; presentation slides and recorded demonstration | Submission artefacts prepared |

Week 2 achieved **100% statement and branch coverage for the selected helper module**, not the whole application. Failed assertions remain visible. Their presence does not make an executed test incomplete, and a failed assumption is not automatically a confirmed product defect. Manual and automated executions are counted separately.

## Reports and evidence

| Phase | Main documents | Other deliverables |
|---|---|---|
| Week 1 | [Report](01_Black_Box/Week1_Report.md), [test repository](01_Black_Box/Master_Test_Repository.md), [defect log](01_Black_Box/Defect_Log.md) | [Original screenshots, browser results, and API probe evidence](01_Black_Box/evidence) |
| Week 2 | [Report](02_White_Box_Coverage/Week2_Report.md), [test repository](02_White_Box_Coverage/Master_Test_Repository.md) | [Unit tests](02_White_Box_Coverage/tests), [coverage and execution evidence](02_White_Box_Coverage/evidence) |
| Week 3 | [Report](03_GUI_Compatibility_Usability_Accessibility/Week3_Report.md) and four Excel workbooks in the [phase folder](03_GUI_Compatibility_Usability_Accessibility) | [Original and verification evidence](03_GUI_Compatibility_Usability_Accessibility/evidence), browser scripts |
| Week 4 | [Report](04_Web_API/Week4_Report.md) and four Excel workbooks in the [phase folder](04_Web_API) | [API tests](04_Web_API/tests), [logs, JUnit, JSON, route map, and screenshots](04_Web_API/Evidence) |
| Week 5 | [Report](05_Security_Performance/Week5_Report.md), [setup and evidence index](05_Security_Performance/README.md) | [Performance evidence](05_Security_Performance/evidence), [static control review evidence](05_Security_Performance/evidence/static_control_review_20261126.json) |
| Week 6 | [Report](06_Automation_Regression/Week6_Report.md), [regression test repository](06_Automation_Regression/Regression_Test_Repository.md), [setup](06_Automation_Regression/README.md) | [Tests](06_Automation_Regression/tests), [execution evidence](06_Automation_Regression/evidence), illustrative CI workflow |
| Week 7 | [Test Management Report](07_Test_Management/Week7_Report.md) | [Consolidated Test Plan](07_Test_Management/Week7_Report.md), [Master Test Case Repository](07_Test_Management/Master_Test_Case_Repository.md), [Requirements Traceability Matrix](07_Test_Management/Requirements_Traceability_Matrix.md), [Consolidated Defect Log](07_Test_Management/Consolidated_Defect_Log.md) |
| Week 8 | [Final QA Report](08_Final_QA_Report/Week8_Report.md) | Final quality assessment, [metrics charts](08_Final_QA_Report/metrics_charts), defect summary, risk assessment, recommendations, and selected testing evidence |
| Week 9 / integration | [Integrated final QA report (PDF)](08_Final_QA_Report/STQA_Group4_Final_QA_Report.pdf) | [Presentation and demonstration](09_Presentation) |

Each report explains scope, environment, findings, recommendations, and limitations. Week 3's Markdown report supersedes its earlier Word summary. Original Week 3/4 workbook observations are retained in each phase's evidence as `original_records.json`; superseded records are excluded from current execution totals. Existing defect IDs are reused across phases to avoid duplicate defect counts.

## Portable setup

Use Python 3.12, Node.js with npm, and the installed desktop versions of Microsoft Edge and Google Chrome. The recent verification used Python 3.12.14, pytest 9.1.1, Flask 3.0.3, and Playwright 1.62.1. Exact browser versions and tested viewports are recorded in the Week 3 report.

Obtain the original supplied application separately and arrange the folders as follows:

```text
working-folder/
  STQA-Project-G4/
  pytodo_pro_student/
    app.py
    helpers.py
    requirements.txt
    Group Project.pdf
```

Run the following PowerShell commands from the **repository root**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\02_White_Box_Coverage\requirements-test.txt -r .\04_Web_API\requirements-test.txt
```

For tests that use the original app, resolve its location in that terminal:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
```

This example uses a sibling folder and does not depend on a particular username or drive. If your app is stored elsewhere, set `PYTODO_SOURCE_DIR` to that folder instead. Week 2's helper tests use the included unchanged snapshot and do not require a running app.

## Run the tests

Archive saved evidence before rerunning: the runners replace their current output files. The recorded runs include failing assertions, so **exit code 1 is expected when those assertions fail**. Inspect logs and case counts to distinguish findings from setup or execution errors.

### Week 2 unit tests and coverage

From the repository root:

```powershell
.\.venv\Scripts\python.exe .\02_White_Box_Coverage\run_tests.py
```

Recorded result: 36 Pass / 5 Fail in the final suite. The runner saves baseline and final coverage and checks the helper snapshot's integrity. After cloning, open [baseline HTML](02_White_Box_Coverage/evidence/baseline_html/index.html) or [final HTML](02_White_Box_Coverage/evidence/final_html/index.html) in a browser; GitHub does not host these files as an interactive coverage site.

### Week 3 checks and Week 4 web checks

Install the pinned browser-test dependency once:

```powershell
Push-Location .\03_GUI_Compatibility_Usability_Accessibility
npm install
Pop-Location
```

In the first terminal, from the repository root:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
.\.venv\Scripts\python.exe .\03_GUI_Compatibility_Usability_Accessibility\run_isolated_server.py
```

In a second terminal, from the repository root:

```powershell
Push-Location .\03_GUI_Compatibility_Usability_Accessibility
npm test
Pop-Location
```

The default test server is `http://127.0.0.1:5013`. It uses a temporary database. The browser runner produces both Week 3 automated evidence and Week 4 web evidence. Recorded results are 28 Pass / 2 Fail for the 30 Week 3 browser checks, and 18 Pass / 2 Fail for the 20 Week 4 web checks. The seven manual usability observations are a separate population.

Stop the test server with Ctrl+C after the run. Restart it before another browser execution to obtain a fresh database. For an alternative port, use matching `QA_PORT` in the server terminal and `QA_BASE_URL` in the browser terminal. The saved verification used port 5014.

### Week 4 API checks

From the repository root:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
.\.venv\Scripts\python.exe .\04_Web_API\run_api_tests.py
```

Recorded result: 36 Pass / 17 Fail, with no setup errors. Each API case uses its own temporary database through Flask's test client; no running server is required. The suite verifies source identity and records requests, responses, propagated exceptions, and registered routes. See the Week 4 report for the distinction between confirmed defects and assumption failures.

### Week 5 security and performance

The [Week 5 report](05_Security_Performance/Week5_Report.md) contains 17 STRIDE entries, links to existing evidence, eight source-review findings (CR-01 to CR-08), and four completed static security control reviews (1 Pass / 3 Fail). Source-review findings are tracked separately from runtime defects; the four reviews are counted in their own static-review population.

The performance test needs Apache JMeter 5.6.3 extracted beside the repository, Java, and `matplotlib`. From the repository root:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
.\.venv\Scripts\python.exe .\05_Security_Performance\performance\run_performance.py --quick
.\.venv\Scripts\python.exe .\05_Security_Performance\performance\run_performance.py --label "<name>-PC"
```

`--quick` is a two-minute setup check; the full experiment takes about 50 minutes. For each load level and repeat, the runner starts the unchanged app on port 5015 with a temporary database and debug off, runs the JMeter plan in non-GUI mode, and stops the server. Each run creates a new timestamped folder in `05_Security_Performance/evidence`; earlier results are not overwritten.

Recorded result: the two environments generally showed low median response times at the proposed small-team workload. Some laptop repeats missed the proposed latency target; the cause of the pauses was not established. At higher concurrency, the laptop results were substantially affected by test-client connection failures. Database contention was also observed in both environments and is recorded as DEF-W5-001. The reported limits describe these controlled experiments, not production capacity. See the report for the measurement windows, per-run variation, error classification and recovery results.

### Week 6 automation and regression

Install the regression-test dependencies once (pytest-html and Selenium). Google Chrome must be installed; Selenium downloads the matching driver on its first run. From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\06_Automation_Regression\requirements-regression.txt
```

Then run the suite:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
.\.venv\Scripts\python.exe .\06_Automation_Regression\run_regression.py --suite smoke
.\.venv\Scripts\python.exe .\06_Automation_Regression\run_regression.py --label "<name>-PC"
```

Recorded result: 104 tests (41 unit, 34 API, 21 web and 8 Selenium browser tests), 88 Pass / 16 XFAIL in each completed full baseline run. All 29 Week 1 cases (one partial) and all 41 Week 2 cases have automated counterparts. XFAIL is a marked expected failure; review its reason before confirming the associated defect. XPASS prompts retest and review. The standalone suite links to nine of the ten Week 1–4 defect IDs; the remaining ownership finding is separately tracked by Week 4, and the Week 5 performance finding remains outside this suite. The 29-test smoke set covers the subset represented in this suite. Ahmad's Windows run matched the Linux reference. The two simulated-change experiments are separate evidence and excluded from baseline totals.

### Historical Week 1 browser runner

The saved [server script](01_Black_Box/evidence/run_isolated_server.py) and [browser script](01_Black_Box/run_browser_cases.mjs) retain their original machine-specific source, Playwright import, and Edge executable settings. Adjust those settings for your environment before rerunning them on port 5001. Their original results remain in the Week 1 evidence; the current Week 3/4 browser runner does not replace the Week 1 case set or its manual execution evidence.

## Open the application for manual testing

Use the original application's README and requirements. From the repository root:

```powershell
Push-Location ..\pytodo_pro_student
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000/` and register a dummy test account; the starter app has no preset account. This starts the ordinary application and its database, separately from the isolated verification server. After stopping the app, use `Pop-Location` to return to the repository root.

## Submission scope

The integrated final report, presentation and edited demonstration are available in the [final submission section](#final-submission). The recording illustrates selected live functional checks and existing results; it is not a new full-suite execution or an additional aggregate test population.

The phase reports retain the documented execution provenance, assumptions, limitations, open defects and recommendations. The supplied application remains unchanged; implementation of application fixes is outside the agreed project scope.
