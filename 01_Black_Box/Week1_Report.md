# PyTodo Pro - Week 1 QA report

**Course:** TEB3433 / TFB3433 Software Testing and Quality Assurance, September 2026  
**Assignment stage:** Week 1 - application analysis and black-box testing  
**Report updated:** 2026-10-01 (Asia/Singapore)  
**Team:** See the project [README](../README.md) for names, student IDs, and coordination roles.
**Manual test assignments:** Planned executors, partners and dates are retained within each case in `Master_Test_Repository.md`. Actual tester/date confirmation is still pending.

## 1. Purpose and application overview

The group is assessing the quality of the supplied PyTodo Pro application, not developing it. PyTodo Pro is a Flask and SQLite task manager with account registration/login, task creation/editing/deletion, completion state, categories, due-date urgency, filters/search, dashboard counts, and a JSON API. Its seeded categories are Work, Personal, Study, and Urgent. The main user is a signed-in person managing their own tasks. Relevant assets are user accounts and task data.

The Week 1 scope covered core browser workflows and selected input/date boundaries. The feature/risk matrix and RTM are included below. The greatest current risks are task ownership (R-03), registration validation (R-01), task validation (R-04), and urgency classification (R-07). R-04's estimated risk score rose from 4 to 6 after the whitespace-title finding; this is a qualitative reassessment, not a measured failure probability.

### Feature inventory, scope and risk matrix

Risk ratings are QA judgments (impact x likelihood, each 1-3), updated after the isolated checks. They are prioritization aids, not measured probabilities. `Later` means deeper testing is planned in another project week.

| Req ID | Feature / expected behavior | Impact | Likelihood | Score | Week 1 evidence / follow-up |
|---|---|---:|---:|---:|---|
| R-01 | Register with valid username and password; reject invalid input | 2 | 3 | 6 | Automated: 6 Pass, 1 Fail; manual: 6 Pass, 1 Fail; DEF-W1-001 reproduced manually |
| R-02 | Authenticate, reject wrong credentials, log out | 3 | 2 | 6 | Automated and manual: 3 Pass |
| R-03 | Restrict tasks to their owner | 3 | 3 | 9 | UI isolation passed; API deletion failed; DEF-W1-003; Week 5 follow-up |
| R-04 | Create tasks with title, description, category, optional due date | 2 | 3 | 6 | Automated and manual: 3 Pass, 1 Fail; whitespace title DEF-W1-004; requirement confirmation pending |
| R-05 | Edit and delete the correct task | 2 | 2 | 4 | UI edit/delete passed; API ownership issue DEF-W1-003 |
| R-06 | Mark tasks done and reopen them | 2 | 2 | 4 | State transition passed in browser |
| R-07 | Show correct urgency for no date, past, today, +1/+2, +3 days | 2 | 3 | 6 | Automated: 5 Pass, 1 Fail; manual due-today failure reproduced as DEF-W1-002 |
| R-08 | Combine category/status filters and title search | 2 | 2 | 4 | 5 Pass in browser |
| R-09 | Show accurate dashboard counts | 2 | 2 | 4 | Selected counters passed with controlled data |
| R-10 | API validation and status codes | 2 | 3 | 6 | Exploratory probe only; full suite Week 4 |
| R-11 | GUI, compatibility, usability, accessibility | 2 | 2 | 4 | Screenshots collected; structured review Week 3 |
| R-12 | Security and performance under load | 3 | 2 | 6 | Ownership issue observed; controlled testing Week 5; performance untested |

The initial pre-execution scores used the same scale. R-04 was initially 2 x 2 = 4 and was raised to 2 x 3 = 6 after the whitespace-title failure. Other scores are unchanged. Keep these ratings under review as later phases add evidence.

## 2. Requirements and test design

Expectations came from the assignment brief, the starter README, registration form, and `helpers.py` specifications. Where a behavior was not stated precisely, the report identifies it as a proposed quality expectation. In particular, rejecting a whitespace-only title and enforcing unique usernames need specification confirmation. User ownership is supported by the per-user task list and the ownership checks in most task routes.

| Technique | Case IDs | Why it fits | Key test data |
|---|---|---|---|
| Equivalence partitioning | 005, 008-009, 011-014, 018, 028 | Representative valid/invalid credentials, task input, ownership, and search | Hyphen in username; wrong password; empty and spaces-only title; two accounts |
| Boundary value analysis | 001-004, 006-007, 019-023 | Inputs and date labels change at clear boundaries | Username lengths 2/3/20/21; password 7/8/9; due dates D-1 through D+3 |
| Decision table | 024-027 | Category and status combine to decide which tasks appear | Work/Personal/All crossed with Open/Done |
| State transition | 010, 015-017 | Session and task state change over time | Signed in -> signed out; open -> done -> open; existing -> deleted |

The 29 cases, test data, preconditions, numbered/procedural steps, expected results, automated actual results, evidence, and defects are in `Master_Test_Repository.md`. The same repository includes the decision table and state transition model.

## 3. Environment, execution, and evidence

The isolated automated run used the supplied app code unchanged, Windows NT build 26200, Python 3.12.10, Flask 3.0.3, Microsoft Edge 154.0.4258.37 through Playwright, a separate SQLite database, and local date 2026-09-30 in Asia/Singapore. The temporary test server ran on port 5001 and was stopped after execution. The group's visible app on port 5000 and its `abc` account were not changed by this run. The app source files used for the isolated run had SHA-256 prefixes `050B4EE4` (`app.py`) and `BF914033` (`helpers.py`).

The browser filled forms, clicked controls, followed redirects, inspected visible results, and saved one screenshot per case. Raw structured results are in `evidence/browser_results.json`; screenshots are in `evidence/browser_screenshots/`. A separate in-memory API probe is documented in the API probe appendix of `Defect_Log.md` and its raw log. The user supplied a screenshot of successful TC-BB-001 registration, saved as `evidence/TC-BB-001-success.png`, plus screenshots for TC-BB-002 through TC-BB-029. Thirty-seven original screenshot files covering TC-BB-002 through TC-BB-029 were copied unchanged from the user's OneDrive Screenshots folder into `evidence/manual_screenshots/`; `manifest.csv` records their original filenames and case mapping. The new TC-BB-002 through TC-BB-004 files were captured on 2026-10-01 during the user's recheck. The manifest separately labels setup images for TC-BB-027/028 and final result images. Observation notes and available database checks are included under each case in `Master_Test_Repository.md`. TC-BB-011 has list and edit screenshots; TC-BB-016 has a done-list image and two Dashboard images; TC-BB-017 has list and Dashboard screenshots.

| Execution type | Planned | Executed | Passed | Failed | Blocked | Not Run | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Isolated automated browser | 29 | 29 | 26 | 3 | 0 | 0 | 89.7% passed; 10.3% failed in this selected suite |
| Group manual browser | 29 | 29 | 26 | 3 | 0 | 0 | 100% observed; original images stored, actual tester metadata pending |

The API probe's P-01-P-09 observations are **not** added to the 29-case counts. Its cross-user deletion finding is an additional defect. Counts from RTM rows overlap because some cases support more than one requirement.

All 29 manual cases have user-provided observations. Individual case records document variations in task titles, deletion targets, and completion dates; the expected outcomes are preserved.

## 4. Findings and defect status

| Defect | Finding | Severity / priority | Evidence | Current status |
|---|---|---|---|---|
| DEF-W1-001 | An exactly 8-character password is rejected despite the stated minimum of 8 | Moderate / Medium | Manual TC-BB-007 screenshot; automated TC-BB-007; API P-01/P-02 | Confirmed in manual browser, isolated browser, and API checks |
| DEF-W1-002 | A task due today is labeled `Overdue` instead of `Due Today` | Moderate / Medium | Manual TC-BB-020 screenshot and database check; automated TC-BB-020; API P-04-P-07 | Confirmed in manual browser, isolated browser, and API checks |
| DEF-W1-003 | One signed-in account can delete another account's task via the API | Major / High | API P-08/P-09 raw log | Confirmed in isolated API check; team retest pending |
| DEF-W1-004 | A whitespace-only title creates a task with no visible title | Moderate / Medium | Manual TC-BB-014 screenshot and database check; automated TC-BB-014 | Reproduced manually and in isolated browser; formal requirement confirmation pending |

Detailed reproducible reports, environments, expected/actual results, severity, priority, evidence, and lifecycle status are in `Defect_Log.md`. An additional observation is that duplicate usernames were accepted through the API. Username uniqueness has not been established as a formal requirement, so it remains an open question rather than a confirmed defect.

The browser correctly kept account A's task out of account B's list and edit page (TC-BB-018), while the API deletion check failed. This difference shows why the later API and security phases must cover ownership independently from the UI.

## 5. Quality assessment, limits, and next actions

The selected common workflows for login, task lifecycle, filters, and current dashboard counts worked in the isolated Edge run. Three browser cases failed at defined input/date boundaries, and an additional API check found unauthorized deletion. The evidence does not establish overall product quality or absence of other defects.

The main limits are: actual tester names and browser version metadata remain unconfirmed; only one browser/version was used for the automated suite; the API probe was small rather than a full endpoint suite; historical 7-day dashboard boundaries, accessibility, compatibility, performance, and broader security behavior remain untested. The whitespace-title expectation and duplicate-username policy need confirmation. The group should record student IDs before submission. Capture timestamps in screenshot filenames establish when the images were saved, but do not identify the person who tested or independently prove the execution time. The TC-BB-002 and TC-BB-004 forms clear submitted values, so those images alone do not show the rejected usernames; case mapping follows the user's recheck sequence.

Prioritize these actions: (1) prevent cross-user API deletion and add owner-scope regression cases; (2) align password and due-today behavior with their stated rules; (3) reject whitespace-only task titles in both UI and server validation; (4) confirm actual tester names, dates, and browser versions for the completed manual log; (5) carry the observed risks into Weeks 2-5 and revise the RTM as evidence grows.

## 6. Requirements traceability matrix (RTM)

The requirement IDs are working testable statements derived from the supplied app's README, forms, and helper specifications. R-03 (ownership) and whitespace rejection under R-04 are justified quality expectations; confirm them with the group/lecturer if a formal specification is required. Manual and automated results are recorded in `Master_Test_Repository.md`; API observations and defect details are in `Defect_Log.md`. One case may support more than one requirement, so counts in different rows must **not** be added together.

| Requirement / feature | Test scenario | Test case ID(s) | Type / technique | Automated result | Manual result | Defect ID / gap |
|---|---|---|---|---|---|---|
| R-01 Registration | Username and password valid/invalid classes and length boundaries | TC-BB-001-007 | EP, BVA, functional | 6 Pass, 1 Fail (007) | 001-006 Pass; 007 Fail | DEF-W1-001; duplicate-username rule unresolved |
| R-02 Authentication | Correct and wrong login; logout | TC-BB-008-010 | EP, state transition | 3 Pass | 008-010 Pass | None observed |
| R-03 User task ownership | Logged-out access and another user's task list/edit URL | TC-BB-010, TC-BB-018; API probe P-08/P-09 | Functional, access control | Browser 2 Pass; API ownership check failed | 010 and 018 Pass | DEF-W1-003; API ownership needs full Week 4/5 suite |
| R-04 Task creation and validation | Full task, optional fields, empty title, spaces-only title | TC-BB-011-014 | EP, functional | 3 Pass, 1 Fail (014) | 011-013 Pass; 014 Fail | DEF-W1-004; whitespace-title expectation proposed |
| R-05 Task edit and deletion | Edit selected task; delete selected task | TC-BB-015, TC-BB-017; API probe P-08/P-09 | State transition, functional | Browser 2 Pass; API delete ownership failed | 015 and 017 Pass with documented data variations | DEF-W1-003 |
| R-06 Completion state | Open -> done -> open | TC-BB-016 | State transition | 1 Pass | 016 Pass | None observed |
| R-07 Urgency classification | No date, yesterday, today, +1, +2, +3 | TC-BB-012, TC-BB-019-023 | BVA, state | 5 Pass, 1 Fail (020) | 012, 019, 021-023 Pass; 020 Fail | DEF-W1-002 |
| R-08 Filters and search | Category/status combinations and title search | TC-BB-024-028 | Decision table, EP | 5 Pass | 024-028 Pass | None observed |
| R-09 Dashboard counts | Completion transition and known four-task totals | TC-BB-016, TC-BB-029 | Functional, state | 2 Pass | 016 and 029 Pass | Historical 7-day boundary untested; Week 2 follow-up |
| R-10 API validation/status | Registration, task creation/list/get/delete spot checks | P-01-P-09 (observations, not formal cases) | Exploratory API | Three confirmed issue categories plus duplicate-username observation | Not Run | DEF-W1-001/002/003; formal API suite Week 4 |
| R-11 GUI, compatibility, accessibility | Forms and pages visible in Edge | Browser screenshots only | Visual evidence, not structured Week 3 checks | No formal result | Not Run | Browser/device matrix and WCAG checks pending |
| R-12 Security and performance | Task ownership and controlled load | P-08/P-09 for ownership only | Exploratory security | Ownership deletion failed; performance untested | Not Run | DEF-W1-003; STRIDE/performance Week 5 |

### Traceability checks

- All 29 `TC-BB` case IDs appear in at least one RTM row and have a design record in `Master_Test_Repository.md`.
- Every automated failure (TC-BB-007, 014, 020) links to a defect report and screenshot.
- DEF-W1-003 arose from the separate API probe and is linked to R-03/R-05/R-10/R-12; it is not counted as one of the 29 automated browser cases.
- Manual status remains distinct: TC-BB-001 through TC-BB-029 have original user-provided browser images in the repository. TC-BB-002 through TC-BB-004 were recaptured on 2026-10-01.

## 7. Guideline coverage

| Required Week 1 content (brief, page 2) | Location |
|---|---|
| Application overview and feature inventory | This report, section 1 |
| Initial scope/risk matrix | This report, section 1; initial and revised risk scores retained |
| Black-box scenarios and cases | `Master_Test_Repository.md`: all 29 cases |
| Test data and technique justification | This report, section 2; per-case inputs and decision/state models in the test repository |
| Execution evidence and initial defects | Per-case results and linked screenshots; `Defect_Log.md` |

The brief specifies deliverable contents rather than a separate file for each content type. Its RTM requirement is met by section 6. Setup, tools, team details and automated-run instructions are in the root `README.md`.

**Source:** `Group Project.pdf`, pages 1-2 and 5-7, supplied at `C:\Users\Admin\Downloads\pytodo_pro_student\Group Project.pdf`; starter README, application forms and helper specifications. No application code was changed.
