# STQA group project - PyTodo Pro quality assessment

This workspace contains QA artefacts for the supplied PyTodo Pro task manager. The application source is currently in `C:\Users\Admin\Downloads\STQA\pytodo_pro_student`; it is the test target and has not been changed for this assessment. The assignment brief is `C:\Users\Admin\Downloads\STQA\pytodo_pro_student\Group Project.pdf`. Week 1 records retain the original pre-relocation environment. Files under this project's `sources/` directory are read-only synced references.

## Team and status

Team members: Gan Jeng Jie; Wan Qistina; Ahmad Adam Ali; Sathineswary Saravanesvaran  
Student IDs: `_____`  
Proposed QA/Test Lead: Gan Jeng Jie  
Proposed Test Design Coordinator: Wan Qistina  
Proposed Automation/Tool Coordinator: Ahmad Adam Ali  
Proposed Defect & Metrics Coordinator: Sathineswary Saravanesvaran

Planned case executors, partners and dates are recorded with each case in `01_Black_Box/Master_Test_Repository.md`. These assignments do not establish who actually performed the tests.

| Project stage | Current status |
|---|---|
| Week 1 application analysis and black-box testing | 29 automated browser cases executed (26 Pass, 3 Fail); 29 manual cases observed (26 Pass, 3 Fail); original images stored for every manual case; actual tester names and some execution metadata still needed |
| Week 2 white-box testing and coverage | Four helpers; 41 executed unit cases (36 Pass, 5 Fail); selected-module statement/branch coverage 100%; baseline and final evidence saved; group review pending |
| Weeks 3-8 | To be completed as the relevant course topics are covered |
| Combined submission and feedback | Submission around Week 10; feedback in Week 11; possible resubmission for evaluation in Week 12; exact dates pending |

## Week 1 documents for the combined submission

Keep these three documents together with `evidence/` and the reproduction scripts:

| Document | Contents |
|---|---|
| [Week1_Report.md](01_Black_Box/Week1_Report.md) | Overview, feature/scope/risk matrix, technique justification, results summary, limitations, RTM |
| [Master_Test_Repository.md](01_Black_Box/Master_Test_Repository.md) | All 29 designs, test data, steps, expected/actual results, manual and automated statuses, case assignments, observations, screenshot links |
| [Defect_Log.md](01_Black_Box/Defect_Log.md) | Four reproducible defect records and the initial API probe evidence |

Original screenshots, their filename manifest, raw browser results and API logs remain in `01_Black_Box/evidence/`. The files support the recorded results. Student IDs belong above; tester/date details belong in the existing case records, and the manual browser/version belongs in the test repository's introductory environment paragraph.

## Week 2 documents and execution

| Document / artifact | Contents |
|---|---|
| [Week2_Report.md](02_White_Box_Coverage/Week2_Report.md) | Selected units, rationale, control-flow diagrams, branch/condition/data-flow analysis, coverage comparison, findings and reproduction instructions |
| [Master_Test_Repository.md](02_White_Box_Coverage/Master_Test_Repository.md) | All 41 unit cases with inputs, expected/actual results, paths, statuses and defect links |
| `02_White_Box_Coverage/tests/` | Baseline and final PyTest tests with fixed clocks |
| `02_White_Box_Coverage/evidence/` | Test logs, JUnit, structured results, before/after coverage in text/JSON/XML/HTML, source hashes |

From the repository root, use Python 3.12 and run:

```powershell
python -m pip install -r .\02_White_Box_Coverage\requirements-test.txt
python .\02_White_Box_Coverage\run_tests.py
```

The runner checks an unchanged helper snapshot, runs both suites, and saves evidence. It returns exit code 1 for the five documented failing assertions. Coverage increased from 70.97% of statements / 50% of branch outcomes to 100% / 100% **for the selected helper module**, with no claim of whole-app coverage. Two existing defects were reproduced; a new inclusive completion-window defect is recorded in the Week 2 report. Review the interpreted zero-age expectation separately. Archive evidence before rerunning if retaining the saved execution is needed.

## Running the application on Windows

Use the starter application's README and its `requirements.txt`. In PowerShell:

```powershell
cd C:\Users\Admin\Downloads\STQA\pytodo_pro_student
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000/`. The app creates `pytodo_pro.db` and has no preset account, so register a test user. Record the Python/Flask/browser versions and use dummy credentials. Keep one app server on port 5000 to avoid mixing test databases.

## Reproducing the isolated Week 1 browser run

The saved run used Windows NT build 26200, Python 3.12.10, Flask 3.0.3, Node.js, Microsoft Edge 154.0.4258.37, and Playwright from the local Codex runtime. It served the unmodified app with a separate SQLite database on port 5001. The reproducible scripts are `01_Black_Box/evidence/run_isolated_server.py` and `01_Black_Box/run_browser_cases.mjs`.

Run the isolated server first, then run the browser script in a second terminal from this workspace root:

```powershell
python .\01_Black_Box\evidence\run_isolated_server.py
node .\01_Black_Box\run_browser_cases.mjs
```

Use a fresh isolated database for each rerun by archiving or renaming the existing `01_Black_Box/evidence/week1_browser_test.db` **while the test server is stopped**. Archive the old screenshots/results first because a rerun replaces files with the same names. The browser script uses the Playwright path from this machine's Codex runtime; a teammate running it elsewhere must point that import to their Playwright installation. These automated checks support the Week 1 evidence but do not replace the brief's manual-execution requirement.

## Later project stages

Updated course guidance supplied by the user on 2026-10-07 sets a single combined submission around Week 10, feedback in Week 11, and a possible resubmission for evaluation in Week 12. Use this schedule for planning; exact dates and the resubmission requirement remain to be confirmed. The brief's Week 12 reference is retained below as its original integration/presentation timing. Weekly stages organize the work; the shared message does not require weekly project submissions.

Lab tasks and the project carry separate course marks. A TA may have a specific arrangement to evaluate project progress during labs; confirm any such arrangement with that TA. Lab results establish performance on the lab code; project evidence must assess PyTodo itself.

The project scope is to inspect PyTodo and develop a clear, proportionate QA plan and documentation using the course techniques. Keep the supplied application code and features unchanged. Record observed defects, evidence, severity, risks, and recommendations; implementation of application fixes is outside this assessment scope. Test scripts and QA documents are project deliverables.

| Stage | Required deliverables from the brief | Current state / location |
|---|---|---|
| Week 2 - White-box | Selected units and rationale, control flow, statement/branch tests, PyTest files, coverage report and interpretation | Executed in `02_White_Box_Coverage/`: four helpers, 41 cases (36 Pass/5 Fail), full measured statement/branch coverage for the selected module. Group review pending. |
| Week 3 - GUI/compatibility/usability/accessibility | GUI checklist/results, browser/configuration matrix, usability notes, WCAG-based findings, screenshots and recommendations | Pending. Week 1 Edge screenshots are supporting material, not a structured Week 3 assessment. |
| Week 4 - Web/API | Web scenarios, API suite, requests/data, expected versus actual status/content, evidence and defects | Pending. Week 1 `01_Black_Box/Defect_Log.md` contains exploratory API observations only; build a formal endpoint suite. |
| Week 5 - Security/performance | STRIDE table, safe security cases/findings, controlled workload/environment, timing/throughput/error results, limitations | Pending. Carry DEF-W1-003 into the ownership threat analysis. No performance claim yet. |
| Week 6 - Automation/regression | Candidate justification, automated scripts, manual-to-automated links, execution logs, regression suite and reflection | Pending. The Week 1 browser runner is a candidate to review, document, and refine for regression use. |
| Week 7 - Test management | Formal test plan/strategy, updated RTM, master test repository, consolidated defect log, execution/regression status | Pending final consolidation. Week 1 versions exist in `01_Black_Box/` and should be revised with later evidence. |
| Week 8 - Final QA evaluation | Integrated report, metrics/charts, residual risks, quality findings/limits, prioritized recommendations | Pending. Use complete evidence from earlier stages; keep automated and manual denominators distinct. |
| Week 12 integration/presentation | ISO/IEC 25010 and process context, CI/CD discussion, Agile/DevOps improvements, presentation and live demo | Pending after the testing phases. The brief calls this Week 9 integration work in course Week 12. |

For final submission, maintain unique case IDs, consistent expected/actual/evidence fields, a current RTM, matching defect statuses, reproducible scripts, interpreted metrics, stated limitations, and a prepared presentation/live demo.
