# PyTodo Pro - Week 7 Consolidated Defect Log

| ID | Summary | Severity | Priority | Status / evidence |
|---|---|---|---|---|
| DEF-W1-001 | Exactly 8-character password rejected despite stated minimum | Moderate | Medium | Confirmed in manual browser, isolated browser and API; open |
| DEF-W1-002 | Due-today task labelled Overdue instead of Due Today | Moderate | Medium | Confirmed in browser/API checks; open |
| DEF-W1-003 | Signed-in user can delete another user's task through API | Major | High | Confirmed in isolated API probe; local group retest pending; open |
| DEF-W1-004 | Whitespace-only title creates blank task | Moderate | Medium | Reproduced; expected behaviour still needs formal confirmation; open |
| DEF-W2-001 | Exact N-day completion boundary is not included | Moderate | Medium | Confirmed at unit level; further UI/API check pending; open |
| DEF-W3-001 | Completed-task title contrast is 2.85:1 | Moderate | Medium | Confirmed against 4.5:1 target; open |
| DEF-W3-002 | New Task controls do not have programmatic label associations | Moderate | Medium | Confirmed; open |
| DEF-W4-001 | Integer task title causes unhandled exception | Moderate | Medium | Confirmed robustness defect; open |
| DEF-W4-002 | Null update title causes database constraint exception | Moderate | Medium | Confirmed robustness defect; open |
| DEF-W4-003 | Invalid due date persists and breaks task listing | Major | High | Confirmed at isolated API level; open |
| DEF-W5-001 | Concurrent writes return HTTP 500/database locked under heavy load | Moderate | Low | Observed in controlled performance experiment; open |

The Week 4 API suite also contains failures based on assumptions/design expectations. Week 5 source-review findings CR-01–CR-08 are recorded separately from runtime defects.
