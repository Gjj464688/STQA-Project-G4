# PyTodo Pro - Week 7 Test Management Report

**Course:** TEB3433 / TFB3433 Software Testing and Quality Assurance  
**Project:** PyTodo Pro quality evaluation  
**Prepared using:** Week 1–6 reports, test repositories and evidence  

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
| Week 5 security | STRIDE-oriented checks and four documented source/control reviews | Week 5 report and findings |
| Week 5 performance | Controlled workload tests on selected pages/endpoints | Performance report and recorded runs |
| Week 6 automation | 104-case full regression and 29-case smoke suite | Regression repository, report and execution results |

### 2.4 Test environment and tools

The environment was different for each phase, so we have not treated the runs as if they were done on one setup. The reports record Windows/Python for Week 2, browser testing with Playwright and Chrome/Edge for Week 3, Flask test-client checks for Week 4, JMeter experiments for Week 5, and Linux and Windows regression runs in Week 6. Tools used include PyTest, coverage.py, Flask test client, Playwright, Selenium, JMeter, Python and spreadsheets/Markdown for records. Exact versions and commands are in the original phase reports.

### 2.5 Test data

Test data was made up of dummy accounts and tasks. It included valid and invalid usernames/passwords, title and description values, categories, due dates, open/done states, search terms, filter combinations, separate accounts for ownership checks and API payloads. No production or personal data was used.

### 2.6 Entry and exit criteria

**Entry:** the supplied application and environment are available, test data is prepared, and the test cases have IDs, preconditions and expected results.  
**Exit:** test cases have a recorded status, failures have evidence or are labelled as assumptions, defects have IDs and status, and the RTM/repositories are updated. These criteria do not mean the application is defect-free.

### 2.7 Main limitations

Some test populations overlap between weeks. Some Week 4 failures depend on expectations that still need confirmation. Week 2 coverage is limited to the selected helper functions. The Week 6 XFAIL marker needs its failure reason checked because it can hide unrelated errors. Performance results only represent the recorded workload and machine. Some tester/date and group-review details also need confirmation. Week 5 included four completed security-control/source reviews, with the review results and findings documented in the Week 5 report.

## 3. Test prioritisation

We prioritised the features that could have the biggest effect on users or their data: ownership/access control, registration and password validation, task input validation, date logic, task lifecycle, API robustness and database behaviour under concurrent writes. Regression automation is used for repeatable checks, while manual review is still needed for usability and accessibility.

## 4. Consolidated execution summary

The numbers below are from the individual phases.

| Phase | Cases/run | Executed | Pass | Fail / XFAIL | Notes |
|---|---:|---:|---:|---:|---|
| Week 1 black-box | 29 | 29 | 26 | 3 Fail | API probe P-01–P-09 is separate |
| Week 2 white-box | 41 | 41 | 36 | 5 Fail | Selected helper functions only |
| Week 3 GUI/compatibility/accessibility | 37 | 37 | 35 | 2 Fail | 30 browser checks + 7 manual observations |
| Week 4 web | 20 | 20 | 18 | 2 Fail | Browser checks |
| Week 4 API | 53 | 53 | 36 | 17 Fail | Some failures are based on assumptions; not all are confirmed defects |
| Week 5 security-control reviews | 4 | 4 reviewed | — | Findings recorded | Completed based on documented source-review evidence |
| Week 6 full regression | 104 | 104 | 88 | 16 XFAIL | Recorded full runs were consistent |
| Week 6 smoke | 29 | 29 | 18 | 11 XFAIL | Later recorded smoke run |

Week 5 performance runs are reported separately because they were workload experiments rather than a simple pass/fail case list.

## 5. Requirements Traceability Matrix

The RTM below links the main requirements to the test evidence and findings.

| Req ID | Feature | Test evidence | Result / defect |
|---|---|---|---|
| R-01 | Registration and password validation | TC-BB-001–007, Week 2 helper tests, Week 4 and Week 6 | DEF-W1-001 password boundary; duplicate username expectation still needs confirmation |
| R-02 | Login, invalid credentials and logout | TC-BB-008–010 and Week 3/4/regression | Selected checks passed; no defect recorded in these selected cases |
| R-03 | Task ownership/access control | TC-BB-010/018, API-25, P-08/P-09 and Week 5 review | DEF-W1-003 cross-user API deletion confirmed in isolated probe; local retest pending |
| R-04 | Create task and input validation | TC-BB-011–014, API-32/42/49/50 and regression | DEF-W1-004 proposed blank-title expectation; DEF-W4-001/002/003 |
| R-05 | Edit and delete task | TC-BB-015/017, API and regression | Selected UI checks pass; ownership issue linked to DEF-W1-003 |
| R-06 | Complete/reopen task | TC-BB-016 and regression | Selected checks passed |
| R-07 | Due-date urgency | TC-BB-019–023, helper tests and regression | DEF-W1-002 due-today label; DEF-W2-001 exact boundary |
| R-08 | Search and filters | TC-BB-024–028 and GUI/web/API | Selected browser cases passed; source-review concern CR-02 |
| R-09 | Dashboard counts | TC-BB-016/029 and helper tests | Selected checks passed; historical 7-day boundary needs more testing |
| R-10 | API behaviour and validation | Week 4 API cases, P-01–P-09 and Week 6 | API failures include both confirmed issues and expectation-based cases |
| R-11 | GUI, compatibility, usability and accessibility | Week 3, 37 checks/observations | 35 passed, 2 failed; DEF-W3-001/002; physical mobile coverage not established |
| R-12 | Security and performance | Week 5 reviews and controlled experiments | Ownership issue and DB lock finding; four reviews completed with documented findings |

## 6. Consolidated defect log

| ID | Defect | Severity | Priority | Status/evidence |
|---|---|---|---|---|
| DEF-W1-001 | Exactly 8-character password rejected although minimum is stated as 8 | Moderate | Medium | Confirmed in manual browser, isolated browser and API; open |
| DEF-W1-002 | Due-today task shown as Overdue instead of Due Today | Moderate | Medium | Confirmed in browser/API checks; open |
| DEF-W1-003 | User can delete another user's task through API | Major | High | Confirmed in isolated API probe; group local retest pending; open |
| DEF-W1-004 | Whitespace-only title creates a blank task | Moderate | Medium | Reproduced; expectation needs formal confirmation; open |
| DEF-W2-001 | Exact N-day completion boundary not included | Moderate | Medium | Confirmed at unit level; open; further UI/API check pending |
| DEF-W3-001 | Completed-task text contrast is 2.85:1 | Moderate | Medium | Confirmed against 4.5:1 target; open |
| DEF-W3-002 | New Task controls lack programmatic label association | Moderate | Medium | Confirmed; open |
| DEF-W4-001 | Integer task title causes an unhandled exception | Moderate | Medium | Confirmed robustness issue; open |
| DEF-W4-002 | Null update title causes database constraint exception | Moderate | Medium | Confirmed robustness issue; open |
| DEF-W4-003 | Invalid due date is stored and breaks task listing | Major | High | Confirmed at isolated API level; open |
| DEF-W5-001 | Concurrent writes can return HTTP 500/database locked under heavy load | Moderate | Low | Observed during controlled performance run; open |

## 7. Week 5 source-review findings

Week 5 also contains source-review findings CR-01 to CR-08. These are kept separate from runtime defect counts. All four security-control reviews were completed, and the documented source-review findings are included in the Week 5 records. Recommendations include checking task ownership in API operations, safe search/query handling, server-side validation and safe handling of database lock conditions.

## 8. Week 6 regression status

- Full regression: 104 tests, 88 PASS and 16 XFAIL. Recorded Linux and Windows full runs had matching case outcomes.
- Smoke suite: 29 tests, 18 PASS and 11 XFAIL in the later recorded run.
- The XFAILs are linked to known defect IDs, but the marker is broad. The failure message/reason should still be checked before accepting an XFAIL as the expected defect.
- Week 6 covers selected earlier test cases and does not cover every Week 5 performance or source-review finding.

## 9. Remaining work

1. Confirm the expected behaviour for duplicate usernames and spaces-only task titles.
2. Confirm tester names, dates and group review details where they are missing.
3. Retest DEF-W1-003 locally if possible, while keeping the isolated API evidence.
4. Review the documented Week 5 security findings and decide which need additional runtime checks.
5. Check defect severity, priority and status against the original reports before submission.
6. Keep the RTM and master repositories aligned, and avoid combining overlapping test counts.
7. Save the current evidence before rerunning scripts that replace evidence files.

## 10. Conclusion

This week we consolidated the testing work from Weeks 1–6 into the test plan, RTM, defect log and repository index. The main workflows have some good results, but there are still confirmed defects and areas that were not covered. The reports should be reviewed by the group before final submission, especially the open defects and the assumptions that still need confirmation.
