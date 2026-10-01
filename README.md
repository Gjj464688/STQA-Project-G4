# STQA group project - PyTodo Pro quality assessment

This workspace contains QA artefacts for the supplied PyTodo Pro task manager. The application source is in `C:\Users\Admin\Downloads\pytodo_pro_student`; it is the test target and has not been changed for this assessment. The assignment brief is `C:\Users\Admin\Downloads\pytodo_pro_student\Group Project.pdf`. Files under this project's `sources/` directory are read-only synced references.

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
| Weeks 2-8 | To be completed as the relevant course topics are covered |
| Week 12 integration/presentation | To be completed after the evidence from all phases is available |

## Week 1 submission documents

Keep these three documents together with `evidence/` and the reproduction scripts:

| Document | Contents |
|---|---|
| [Week1_Report.md](01_Black_Box/Week1_Report.md) | Overview, feature/scope/risk matrix, technique justification, results summary, limitations, RTM |
| [Master_Test_Repository.md](01_Black_Box/Master_Test_Repository.md) | All 29 designs, test data, steps, expected/actual results, manual and automated statuses, case assignments, observations, screenshot links |
| [Defect_Log.md](01_Black_Box/Defect_Log.md) | Four reproducible defect records and the initial API probe evidence |

Original screenshots, their filename manifest, raw browser results and API logs remain in `01_Black_Box/evidence/`. The files support the recorded results. Student IDs belong above; tester/date details belong in the existing case records, and the manual browser/version belongs in the test repository's introductory environment paragraph.

## Running the application on Windows

Use the starter application's README and its `requirements.txt`. In PowerShell:

```powershell
cd C:\Users\Admin\Downloads\pytodo_pro_student
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

The brief sets the final deadline at the end of course Week 12; it gives no calendar date. Continue the shared repository as each phase is completed.

| Stage | Required deliverables from the brief | Current state / location |
|---|---|---|
| Week 2 - White-box | Selected units and rationale, control flow, statement/branch tests, PyTest files, coverage report and interpretation | Pending. Suggested units: `compute_urgency`, password/username validation, completed-in-last-N-days, and selected access decisions. Do not claim coverage until measured. |
| Week 3 - GUI/compatibility/usability/accessibility | GUI checklist/results, browser/configuration matrix, usability notes, WCAG-based findings, screenshots and recommendations | Pending. Week 1 Edge screenshots are supporting material, not a structured Week 3 assessment. |
| Week 4 - Web/API | Web scenarios, API suite, requests/data, expected versus actual status/content, evidence and defects | Pending. Week 1 `01_Black_Box/Defect_Log.md` contains exploratory API observations only; build a formal endpoint suite. |
| Week 5 - Security/performance | STRIDE table, safe security cases/findings, controlled workload/environment, timing/throughput/error results, limitations | Pending. Carry DEF-W1-003 into the ownership threat analysis. No performance claim yet. |
| Week 6 - Automation/regression | Candidate justification, automated scripts, manual-to-automated links, execution logs, regression suite and reflection | Pending. The Week 1 browser runner is a candidate to review, document, and refine for regression use. |
| Week 7 - Test management | Formal test plan/strategy, updated RTM, master test repository, consolidated defect log, execution/regression status | Pending final consolidation. Week 1 versions exist in `01_Black_Box/` and should be revised with later evidence. |
| Week 8 - Final QA evaluation | Integrated report, metrics/charts, residual risks, quality findings/limits, prioritized recommendations | Pending. Use complete evidence from earlier stages; keep automated and manual denominators distinct. |
| Week 12 integration/presentation | ISO/IEC 25010 and process context, CI/CD discussion, Agile/DevOps improvements, presentation and live demo | Pending after the testing phases. The brief calls this Week 9 integration work in course Week 12. |

For final submission, maintain unique case IDs, consistent expected/actual/evidence fields, a current RTM, matching defect statuses, reproducible scripts, interpreted metrics, stated limitations, and a prepared presentation/live demo.
