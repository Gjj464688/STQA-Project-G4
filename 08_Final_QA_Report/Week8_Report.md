# PyTodo Pro - Week 8 SQA Metrics and Final Quality Evaluation

**Course:** TEB3433 / TFB3433 Software Testing and Quality Assurance  
**Project:** PyTodo Pro quality evaluation  
**Prepared from:** Week 1–6 reports, test evidence and Week 7 consolidation
**Reconciled:** 26 November 2026; group review pending

## 1. Overall evaluation

The test results show that many of the selected main workflows work under the conditions we tested. However, there are still issues with access control, validation, date handling, accessibility, API behaviour and database writes under load. The most serious finding is that a signed-in user was able to delete another user's task through an API request during an isolated check.

The results only represent the cases, functions, environments and workloads covered by our testing.

## 2. Test execution metrics

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

### Metrics charts

![Test pass rate by execution population](metrics_charts/test_pass_rate_by_phase.png)

![Test execution counts by population](metrics_charts/test_execution_counts.png)

The charts separate ordinary Fail, XFAIL and Not Run. The pass-rate chart excludes the four unexecuted review cases. Week 6 smoke is a subset of the full suite and Week 3 usability is user-reported manual evidence.

## 3. What the results tell us

- **Week 1:** Each of the two separately recorded executions (manual and automated) has 26 out of 29 black-box cases passed. The failures were related to the password minimum, due-today urgency and a whitespace-only title. The title expectation still needs confirmation.
- **Week 2:** 36 out of 41 helper tests passed. The selected helper module reached 100% statement and branch coverage, but five assertions still failed. Coverage shows which code was exercised; it does not guarantee correct behaviour.
- **Week 3:** 35 out of 37 checks/observations passed. The two accessibility findings are recorded in the defect log. Manual usability observations are different from automated browser checks.
- **Week 4:** 18/20 web checks passed. For API, 36/53 passed. The 17 failures include ownership/robustness checks and checks based on assumptions/design expectations. They should not all be reported as confirmed defects.
- **Week 6:** Full regression runs recorded 88 PASS and 16 XFAIL, with matching outcomes on the reference Linux and Windows runs. This gives us repeatability for the selected tests. The XFAIL marker is broad, so the reason for each expected failure still needs to be reviewed.
- **Week 5:** Eight source-review findings are documented. All four additional control reviews remain Not Run; no new execution is claimed. The performance results are limited to the recorded workloads. High-concurrency results were affected by connection failures and database contention.

### Selected evidence from earlier testing weeks

The screenshots below are selected from the evidence folders in the project repository. They are examples of the recorded testing evidence.

![Week 3 GUI dashboard summary](../03_GUI_Compatibility_Usability_Accessibility/evidence/gui_screenshots/GUI-TC-013_Dashboard_Summary.png)

*Figure: Dashboard summary captured during Week 3 GUI testing.*

![Week 6 regression task creation](../06_Automation_Regression/evidence/20261126-024054_full_Ahmad-PC/screenshots/test_create_task_with_category_and_due_date.png)

*Figure: Task creation with category and due date during a Week 6 regression run.*

![Week 6 regression login check](../06_Automation_Regression/evidence/20261126-024054_full_Ahmad-PC/screenshots/test_login_correct_then_wrong_password.png)

*Figure: Login behaviour check from the Week 6 regression run.*

![Week 6 regression mark done and reopen](../06_Automation_Regression/evidence/20261126-024054_full_Ahmad-PC/screenshots/test_mark_done_and_reopen.png)

*Figure: Marking a task done and reopening it during regression testing.*


## 4. Coverage and automation

### 4.1 Coverage

Week 2 recorded **100% statement coverage and 100% branch coverage** for the selected helper module/four functions. This is not coverage of the full application. Baseline statement coverage was 22/31 (70.97%); branch outcomes were 9/18 (50%). Final coverage was 31/31 statements and 18/18 branch outcomes. Routes, database behaviour, ownership checks, GUI, API, security, compatibility and performance were outside that measured scope. The five failing assertions also show why coverage should not be treated as a correctness score.

### 4.2 Regression automation

The Week 6 full suite contained 104 tests: 41 unit, 34 API, 21 web and 8 Selenium browser tests. The recorded full results were 88 PASS and 16 XFAIL. Linux runs took 17.8 and 18.9 seconds, while the Windows run took 49.4 seconds and had the same case outcomes. The fast/no-browser run had 82 PASS and 14 XFAIL out of 96 tests. The smoke suite had 18 PASS and 11 XFAIL out of 29 in the later run.

The automation helped us repeat boundary checks, run tests across different layers and check whether changes affect known defects. The simulated fix experiment for the password issue produced four XPASS signals, while the simulated regression experiment produced three failures. These were optional sensitivity demonstrations in a temporary copy, subject to the lecturer’s agreed scope; they are excluded from the unchanged-source baseline results.

## 5. Defect summary

The [consolidated log](../07_Test_Management/Consolidated_Defect_Log.md) contains 11 open defect records from Weeks 1–5: ten confirmed in the stated scopes and one reproduced observation with an unconfirmed requirement. The eight CR findings are separate. They cover the following areas:

| Area | Related defects / findings | What it means |
|---|---|---|
| Password validation | DEF-W1-001 | Minimum password boundary does not behave as expected |
| Date logic | DEF-W1-002, DEF-W2-001 | Due-today and exact completion-age boundaries need correction/confirmation |
| Access control | DEF-W1-003 | Another user's task can be deleted through the API; high impact |
| Input validation/API robustness | DEF-W1-004, DEF-W4-001–003 | Blank/invalid inputs and API edge cases require handling; some expectations need confirmation |
| Accessibility | DEF-W3-001/002 | Contrast and label association findings remain |
| Performance/reliability | DEF-W5-001 | Concurrent writes can produce database-lock errors |
| Security source review | CR-01–CR-08 | Source-review findings are tracked separately from runtime defects |

The 17 Week 4 API failures are not automatically 17 defects. Some assertions depend on assumptions that still need to be agreed. Duplicate usernames and whitespace-only titles also need formal requirement confirmation.

### Defect counts

| Severity | Open records |
|---|---|
| Critical | 0 |
| Major | 2 |
| Moderate | 9 |
| Minor | 0 |
| Total | 11 |

| Priority | Open records |
|---|---|
| High | 2 |
| Medium | 8 |
| Low | 1 |
| Total | 11 |

| Primary feature/module | Open records |
|---|---|
| Registration | 1 |
| Date logic | 2 |
| Access control | 1 |
| Input validation | 4 |
| Accessibility | 2 |
| Performance/reliability | 1 |
| Total | 11 |

Each record is counted once in its primary feature group. DEF-W1-004 is included in the Moderate/Medium counts as an observed issue pending requirement confirmation; this is not a claim of eleven independently confirmed defects.

## 6. Remaining risks

| Risk | Evidence | Risk/action |
|---|---|---|
| Cross-user task deletion | DEF-W1-003 isolated API evidence | High priority: retest ownership enforcement across API operations |
| Password minimum mismatch | DEF-W1-001 | Retest the boundary after any change |
| Date classification/boundary | DEF-W1-002 and DEF-W2-001 | Confirm inclusive/exclusive rules and retest with fixed dates |
| Blank/invalid input | DEF-W1-004 and DEF-W4 findings | Confirm expectations and validate server-side behaviour |
| Accessibility | DEF-W3-001/002 | Improve contrast and label associations; broaden checks |
| Concurrent database writes | DEF-W5-001 | Investigate locking and error handling; repeat controlled tests |
| Security source-review findings | CR-01–CR-08 | Address findings and add runtime checks where needed |
| Browser/device coverage | Week 3 test scope | More browser versions, physical mobile and assistive-technology testing |
| Application coverage | Week 2 measured scope | Coverage is limited to the selected helpers; additional structural testing may be useful |

### Performance evidence charts

These charts are taken from the combined Week 5 performance evidence run in the project repository. They are included as visual evidence of the recorded workload results; the limitations described above still apply.

![Performance response time chart](../05_Security_Performance/evidence/perf_20261125-agent-run-combined/charts/response_time_vs_users.png)

*Figure: Response time versus concurrent users.*

![Performance throughput chart](../05_Security_Performance/evidence/perf_20261125-agent-run-combined/charts/throughput_vs_users.png)

*Figure: Throughput versus concurrent users.*

![Performance error rate chart](../05_Security_Performance/evidence/perf_20261125-agent-run-combined/charts/error_rate_vs_users.png)

*Figure: Error rate versus concurrent users.*

## 7. Quality assessment

| Quality area | Our assessment | Limitation |
|---|---|---|
| Functional suitability | Main selected workflows generally work, but date/password/input issues remain | Only selected cases were tested |
| Reliability | Regression outcomes were repeatable; database locking was observed under load | Does not represent production reliability |
| Security | Ownership issue is a significant concern; source-review findings are documented | No uncontrolled penetration testing |
| Usability | Some browser checks and seven manual observations were completed | Not a large user study |
| Accessibility | Two findings remain | Basic selected checks only, not full conformance testing |
| Performance | Some controlled runs showed low response times; high concurrency had client errors and DB locking | Limited workload and machine |
| Compatibility | Selected browser/viewport checks were performed | No full device/browser matrix |
| Maintainability/testability | Test repositories and runners help repeat the work | No full maintainability review |

## 8. Limitations of this evaluation

- Test cases from different weeks overlap and do not represent a unique combined population.
- Week 2 coverage only applies to the selected helper module and functions.
- Some Week 4 failures depend on assumptions that need confirmation.
- Duplicate usernames and spaces-only titles are not fully formalised requirements.
- The four Week 5 follow-up control reviews remain Not Run; the eight original source-review findings are separately documented.
- Performance results are limited to the recorded setup and workload; connection failures and DB locking affected some results.
- Physical mobile, broader browser versions, screen-reader testing and full WCAG evaluation were not established.
- Some manual tester/date details and group-review confirmations still need to be checked.
- XFAIL handling in Week 6 should be reviewed to avoid hiding unrelated errors.

## 9. QA process improvement and recommended next steps

| Preventive QA activity | Evidence motivating it | Proposed improvement |
|---|---|---|
| Requirement review before test design | Password/date rules and ambiguous input policies | Record explicit acceptance criteria and resolve assumptions with product owner/lecturer |
| Peer review of validation and authorization controls | Prior source-review and ownership/robustness findings | Require maintainer review of input handling and access-control policies |
| Automated regression and CI reporting | Repeatable Week 6 runs and temporary-copy experiments | Use stable checks, inspect unexpected outcomes and require review of expected-failure reasons |
| Accessibility review during UI design | Contrast and semantic-label findings | Include basic accessibility review in acceptance criteria |
| Controlled reliability measurement | Environment-dependent database errors | Set realistic workload targets, distinguish client/server outcomes and review recovery evidence |
| Test management review | Overlapping populations and missing original metadata | Maintain unique IDs, evidence links, explicit status and dated review |

Implementation of application changes is a recommendation for its maintainer; the group retains the supplied code for assessment.

1. **Priority 1 – Access control:** Prioritize maintainer review of the existing ownership finding and its authorization policy; preserve the documented evidence.
2. **Priority 1 – Security findings:** Review and address the documented Week 5 source-review findings. Complete the four outstanding control reviews and record their evidence.
3. **Priority 1 – Validation:** Retain the stated eight-character password minimum and confirm the blank-title expectation, then update tests and defect statuses.
4. **Priority 2 – Date logic:** Confirm date-boundary rules and retest the due-today and exact-N-day issues.
5. **Priority 2 – Accessibility:** Improve contrast and labels and expand the checks to keyboard/focus and assistive technology.
6. **Priority 2 – Performance:** Investigate database locking and repeat controlled tests with client-side connection errors separated from server errors.
7. **Priority 2 – Regression:** Narrow XFAIL handling so unrelated exceptions are not treated as expected.
8. **Priority 3 – Traceability and coverage:** Keep test IDs, defect IDs and RTM entries consistent; add more tests where risk justifies them.
9. **Priority 3 – Compatibility:** Extend browser and physical-device coverage.

## 10. Conclusion

Based on the testing we completed, PyTodo Pro can perform many of the selected core workflows, and the automated regression work gives us a repeatable way to check them. However, the access-control issue, other validation/date defects, accessibility findings, API failures and database-lock behaviour still affect confidence in the application. We therefore consider the quality to be **partially demonstrated for the tested scope, with significant risks remaining**. The main areas to address first are access control, the documented security findings, validation, date logic, accessibility and reliability under concurrent writes.
