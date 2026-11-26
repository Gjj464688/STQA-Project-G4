# PyTodo Pro - Week 7 Requirements Traceability Matrix

The matrix connects the feature requirements with the test work completed in earlier weeks.

| Req ID | Feature / expected behaviour | Test evidence | Result / defect reference |
|---|---|---|---|
| R-01 | Registration and password validation | TC-BB-001–007, Week 2 helpers, Week 4 web/API, Week 6 | DEF-W1-001 password boundary; duplicate username expectation not confirmed |
| R-02 | Login, invalid credentials and logout | TC-BB-008–010, Week 3/4 and regression | Selected cases passed |
| R-03 | Task ownership and access control | TC-BB-010/018, API-25, P-08/P-09, Week 5 | DEF-W1-003 confirmed in isolated API probe; local retest pending |
| R-04 | Task creation and validation | TC-BB-011–014, API-32/42/49/50, regression | DEF-W1-004 proposed; DEF-W4-001/002/003 |
| R-05 | Edit and delete the correct task | TC-BB-015/017, API and regression | Selected UI checks passed; ownership issue linked to DEF-W1-003 |
| R-06 | Completion state | TC-BB-016 and regression | Selected checks passed |
| R-07 | Due-date urgency | TC-BB-019–023, helper tests and regression | DEF-W1-002 and DEF-W2-001 |
| R-08 | Search and filters | TC-BB-024–028, GUI/web/API | Selected browser checks passed; CR-02 source-review concern |
| R-09 | Dashboard counts | TC-BB-016/029 and helper tests | Selected checks passed; historical boundary needs more coverage |
| R-10 | API validation and response behaviour | Week 4 API suite, P-01–P-09, Week 6 | API failures include confirmed and assumption-based cases |
| R-11 | GUI, compatibility, usability and accessibility | Week 3 37 checks/observations | 35 pass, 2 fail; DEF-W3-001/002; mobile device testing not established |
| R-12 | Security and performance | Week 5 security reviews and performance runs | DEF-W1-003, DEF-W5-001; four reviews completed with findings documented |