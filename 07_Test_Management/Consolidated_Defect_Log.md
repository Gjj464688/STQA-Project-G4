# Consolidated defect log

**26 November 2026.** Eleven open records: ten confirmed in their stated scopes and one reproduced observation with an unconfirmed requirement (DEF-W1-004). Detailed environment, preconditions, expected/actual, evidence and original status are maintained in the linked phase records. Severity and priority retain their original assessments. No source fixes or closures are claimed.

| Defect ID | Summary | Req. | Feature/module | Severity | Priority | Status | Case / evidence IDs | Detailed record |
|---|---|---|---|---|---|---|---|---|
| DEF-W1-001 | Password minimum boundary | R-01 | Registration | Moderate | Medium | Confirmed; Open | TC-BB-007; TC-WB-005; WEB-05 | [Original record](../01_Black_Box/Defect_Log.md#def-w1-001---exactly-8-characters-rejected-as-a-password) |
| DEF-W1-002 | Due-today urgency label | R-07 | Date logic | Moderate | Medium | Confirmed; Open | TC-BB-020; TC-WB-021 | [Original record](../01_Black_Box/Defect_Log.md#def-w1-002---due-today-task-marked-overdue) |
| DEF-W1-003 | Task ownership enforcement | R-03/R-05/R-10/R-12 | Access control | Major | High | Confirmed in Weeks 1 and 4; Open; named group review pending | P-08/P-09; API-25 | [Original record](../01_Black_Box/Defect_Log.md#def-w1-003---one-user-can-delete-another-users-task-through-the-api) |
| DEF-W1-004 | Blank task title | R-04 | Input validation | Moderate | Medium | Observed; requirement confirmation pending; Open | TC-BB-014 | [Original record](../01_Black_Box/Defect_Log.md#def-w1-004---whitespace-only-title-creates-an-unnamed-task) |
| DEF-W2-001 | Inclusive completion limit | R-09 | Date logic | Moderate | Medium | Confirmed at unit level; Open; UI/API boundary coverage pending | TC-WB-034/039; 032 associated interpretation | [Original record](../02_White_Box_Coverage/Week2_Report.md#new-defect-def-w2-001) |
| DEF-W3-001 | Completed-title readability contrast | R-11 | Accessibility | Moderate | Medium | Confirmed; Open | ACC-TC-002 | [Original record](../03_GUI_Compatibility_Usability_Accessibility/Week3_Report.md#def-w3-001-completed-task-titles-have-insufficient-text-contrast) |
| DEF-W3-002 | Programmatic labels | R-11 | Accessibility | Moderate | Medium | Confirmed; Open | ACC-TC-008 | [Original record](../03_GUI_Compatibility_Usability_Accessibility/Week3_Report.md#def-w3-002-new-task-fields-lack-programmatic-label-associations) |
| DEF-W4-001 | Task creation validation exception | R-04/R-10 | Input validation | Moderate | Medium | Confirmed; Open | API-32 | [Original record](../04_Web_API/Week4_Report.md#def-w4-001-integer-task-title-causes-an-unhandled-exception) |
| DEF-W4-002 | Task update validation exception | R-05/R-10 | Input validation | Moderate | Medium | Confirmed; Open | API-42 | [Original record](../04_Web_API/Week4_Report.md#def-w4-002-null-update-title-causes-a-database-constraint-exception) |
| DEF-W4-003 | Invalid-date persistence and listing impact | R-04/R-10 | Input validation | Major | High | Confirmed; Open | API-49/50 | [Original record](../04_Web_API/Week4_Report.md#def-w4-003-invalid-due-date-persists-and-prevents-task-listing) |
| DEF-W5-001 | Concurrent-write database errors | R-01/R-04/R-12 | Performance/reliability | Moderate | Low | Confirmed in controlled experiments; Open | Week 5 performance evidence | [Original record](../05_Security_Performance/Week5_Report.md#56-new-defect) |

## Source-review findings and outstanding checks

The eight separately tracked Week 5 findings CR-01–CR-08 are documented in [Week 5 security review](../05_Security_Performance/Week5_Report.md#3-security-test-cases-and-findings). They are not counted as eight new runtime defects. Four static security control reviews TC-SEC-001–004 are complete (1 Pass, 3 Fail); the failures confirm existing CR findings only, not new runtime defects. The Week 4 assumption failures, duplicate username observation, and Week 2 exact-current-time interpretation remain distinct from confirmed defects.

## Lifecycle

The defect coordinator maintains IDs, severity, priority, evidence, status and reviewer. A reproduced failure remains open until a maintainer-provided changed version is tested and the group confirms the result. An expected failure or unexpected pass alone does not close a defect. A proposed expectation must be agreed or retained as an observation. Record a dated review decision before changing status.
