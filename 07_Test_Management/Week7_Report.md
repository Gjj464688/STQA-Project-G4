# PyTodo Pro - Week 7 Test Management Report

**Course:** TEB3433 / TFB3433 Software Testing and Quality Assurance  
**Project:** PyTodo Pro quality evaluation  
**Prepared using:** Week 1–6 reports, test repositories and evidence
**Reconciled:** 26 November 2026, using saved evidence; group review pending

## 1. Purpose

For Week 7, we brought together the testing work from the previous weeks so the team can see what was tested, which requirements have test evidence, and what defects are still open. This report is a summary of the existing work. The original test cases, screenshots, logs and reports are still the main evidence.

## 2. Test plan

### 2.1 Scope

We are testing the supplied PyTodo Pro Flask and SQLite task manager. The project is a quality evaluation, so we did not change the application to make the test results pass. The main areas covered are registration and login, task ownership, creating/editing/deleting tasks, completion, due dates, search and filters, dashboard counts, GUI and usability, accessibility, web/API behaviour, security review, performance and regression automation.

Testing all application code and all possible inputs is outside our scope. We also did not conduct uncontrolled penetration testing or make production-capacity claims. Behaviours that are not clearly stated in the requirements are kept as assumptions or questions instead of confirmed defects.

### 2.2 Test objectives

- Check the main user workflows and important input/date boundaries.
- Test the selected helper functions using statement and branch coverage.
- Review the GUI, compatibility, usability and selected accessibility checks.
- Check web and API responses, including invalid input and ownership cases.
- Review security controls and run controlled performance tests.
- Use automation for repeatable regression checks.
- Keep the test evidence, defects and risks organised.

### 2.3 Test approach

| Testing activity | What we covered | Evidence kept |
|---|---|---|
| Week 1 black-box | 29 cases using equivalence partitioning, boundary values, decision tables and state transitions | Master test repository, screenshots and results |
| Week 2 white-box | 41 tests for selected helper functions and statement/branch coverage | PyTest results and coverage reports |
| Week 3 GUI/compatibility/usability/accessibility | 30 browser checks and 7 manual usability observations | Week 3 report, case records and evidence |
| Week 4 web/API | 20 web checks and 53 API cases | Report, test records, runner and evidence |
| Week 5 security | STRIDE-oriented source review and four planned follow-up control reviews (Not Run) | Week 5 report and findings |
| Week 5 performance | Controlled workload tests on selected pages/endpoints | Performance report and recorded runs |
| Week 6 automation | 104-case full regression and 29-case smoke suite | Regression repository, report and execution results |

### 2.4 Test environment and tools

The environment was different for each phase, so we have not treated the runs as if they were done on one setup. The reports record Windows/Python for Week 2, browser testing with Playwright and Chrome/Edge for Week 3, Flask test-client checks for Week 4, JMeter experiments for Week 5, and Linux and Windows regression runs in Week 6. Tools used include PyTest, coverage.py, Flask test client, Playwright, Selenium, JMeter, Python and spreadsheets/Markdown for records. Exact versions and commands are in the original phase reports.

### 2.5 Test data

Test data was made up of dummy accounts and tasks. It included valid and invalid usernames/passwords, title and description values, categories, due dates, open/done states, search terms, filter combinations, separate accounts for ownership checks and API payloads. No production or personal data was used.

### 2.6 Entry and exit criteria

**Entry:** the supplied application and environment are available, test data is prepared, and the test cases have IDs, preconditions and expected results.  
**Exit:** test cases have a recorded status, failures have evidence or are labelled as assumptions, defects have IDs and status, and the RTM/repositories are updated. These criteria do not mean the application is defect-free.

### 2.7 Team responsibilities

| Member (proposed role) | Responsibility |
|---|---|
| Gan Jeng Jie — QA/test lead | Scope, entry/exit criteria, consolidation and review coordination |
| Wan Qistina — Test design | Requirements, case designs, RTM and manual record review |
| Ahmad Adam Ali — Automation/tools | Tools, regression evidence and environment documentation |
| Sathineswary Saravanesvaran — Defects/metrics | Defect status, execution metrics and residual risk review |

These roles are proposed in the project README; they do not establish actual historical execution identities. The team must confirm named reviewers and missing execution metadata.

### 2.8 Main limitations

Some test populations overlap between weeks. Some Week 4 failures depend on expectations that still need confirmation. Week 2 coverage is limited to the selected helper functions. The Week 6 XFAIL marker needs its failure reason checked because it can hide unrelated errors. Performance results only represent the recorded workload and machine. Some tester/date and group-review details also need confirmation. Week 5 includes eight source-review findings and four independently planned control reviews, all Not Run. Existing evidence is retained; no additional runtime result is claimed.

## 3. Test prioritisation

We prioritised the features that could have the biggest effect on users or their data: ownership/access control, registration and password validation, task input validation, date logic, task lifecycle, API robustness and database behaviour under concurrent writes. Regression automation is used for repeatable checks, while manual review is still needed for usability and accessibility.

### 3.1 Risk management and exit decision

| Risk | Priority / impact | Control and owner role |
|---|---|---|
| Ownership and validation defects | High | Track open findings and maintainer recommendations; QA lead and defect coordinator |
| Inconsistent expected requirements | Medium | Record assumptions and obtain agreement; test design coordinator |
| Incomplete security reviews | High | Record Not Run separately and review source evidence; QA lead |
| Broad expected-failure classification | Medium | Review underlying failure reason; automation coordinator |
| Unconfirmed manual evidence provenance | Medium | Obtain dates/tester/reviewer confirmation; QA lead |
| Environment-dependent performance | Medium | Interpret by environment and distinguish client errors; metrics coordinator |

Exit decision: planned functional executions and consolidation are recorded; four Week 5 follow-ups, original metadata and named group reviews remain outstanding. The project can report open defects and pending checks without claiming all tests passed.

## 4. Consolidated execution summary

| Population | Planned | Executed | Pass | Fail | XFAIL | Blocked | Not Run | Pass rate | Basis |
|---|---|---|---|---|---|---|---|---|---|
| W1 manual | 29 | 29 | 26 | 3 | 0 | 0 | 0 | 89.66% | Original manual observations |
| W1 automated | 29 | 29 | 26 | 3 | 0 | 0 | 0 | 89.66% | Separate automated browser run |
| W2 unit | 41 | 41 | 36 | 5 | 0 | 0 | 0 | 87.80% | Final suite; four-case baseline excluded |
| W3 browser | 30 | 30 | 28 | 2 | 0 | 0 | 0 | 93.33% | Current browser verification |
| W3 usability | 7 | 7 | 7 | 0 | 0 | 0 | 0 | 100.00% | Reported manual observations |
| W4 web | 20 | 20 | 18 | 2 | 0 | 0 | 0 | 90.00% | Current browser verification |
| W4 API | 53 | 53 | 36 | 17 | 0 | 0 | 0 | 67.92% | Current API verification |
| W5 follow-ups | 4 | 0 | 0 | 0 | 0 | 0 | 4 | N/A | Pending independent control reviews |
| W6 full | 104 | 104 | 88 | 0 | 16 | 0 | 0 | 84.62% | One full Windows reference run; Linux agreement |
| W6 smoke | 29 | 29 | 18 | 0 | 11 | 0 | 0 | 62.07% | Subset of full suite; separate run |

Pass rate = Pass / Executed. XFAIL is an expected-failure classification, separate from ordinary failures. Setup errors and XPASS are zero in the selected runs above. The earlier Week 6 smoke run with one setup error and both simulated-change runs remain in historical evidence; they are not baseline rows. Week 1 manual and automated results correspond to the same 29 designs, and the Week 6 smoke suite is a subset. Do not sum these populations as unique tests. Week 5 performance experiments, nine Week 1 API probe observations and eight Week 5 source-review findings are reported separately.

## 5. Requirements traceability

[Requirements Traceability Matrix](Requirements_Traceability_Matrix.md) maps all twelve requirement IDs to the actual case IDs and known gaps. [Master Test Case Repository](Master_Test_Case_Repository.md) holds 288 unique design/regression/review IDs with statuses and links; original steps and evidence remain in the phase repositories.

## 6. Consolidated defect management

[Consolidated Defect Log](Consolidated_Defect_Log.md) records 11 open entries (10 scope-confirmed, one observed pending requirement confirmation), with severity, priority, source references and lifecycle. The eight Week 5 CR findings are tracked separately; the four follow-up reviews are Not Run.

## 7. Week 6 regression status

- Full regression: 104 tests, 88 PASS and 16 XFAIL. Recorded Linux and Windows full runs had matching case outcomes.
- Smoke suite: 29 tests, 18 PASS and 11 XFAIL in the later recorded run.
- The XFAILs are linked to known defect IDs, but the marker is broad. The failure message/reason should still be checked before accepting an XFAIL as the expected defect.
- Week 6 covers selected earlier test cases and does not cover every Week 5 performance or source-review finding.

## 8. Remaining work

1. Confirm the expected behaviour for duplicate usernames and spaces-only task titles.
2. Confirm tester names, dates and group review details where they are missing.
3. Retain the Week 1 and Week 4 ownership finding evidence and confirm group review and remediation recommendations.
4. Complete the four outstanding security control reviews and record evidence and reviewer status.
5. Check defect severity, priority and status against the original reports before submission.
6. Keep the RTM and master repositories aligned, and avoid combining overlapping test counts.
7. Save the current evidence before rerunning scripts that replace evidence files.

## 9. Conclusion

This week we consolidated the testing work from Weeks 1–6 into the test plan, RTM, defect log and case-level master repository. The main workflows have some good results, but there are still confirmed defects and areas that were not covered. The reports should be reviewed by the group before final submission, especially the open defects and the assumptions that still need confirmation.
