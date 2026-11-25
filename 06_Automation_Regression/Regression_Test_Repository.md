# Week 6 automated regression test repository

One row per automated test in the regression suite (104 tests). Each row links the automated test to the original manual or white-box case (`TC-BB-*` from Week 1, `TC-WB-*` from Week 2) and to the Week 1 requirement IDs. The *Result* column is copied from the recorded full run `20261125-185829_full_agent-run-3` (`results.jsonl`); later runs are in `evidence/`.

Common preconditions: PyTodo Pro source unchanged (hashes checked and recorded by every run); each unit/API/web test starts from an empty temporary SQLite database; browser tests share one throwaway database served on 127.0.0.1:5002 and use a unique username per test. `D` is the computer's current date when the test runs. Default valid password: `abcdefghi` (9 characters). Steps are the test code itself: open the listed file and find the test by its AUTO ID in the `trace` marker.

Result meanings: **PASS**; **FAIL**; **XFAIL** = the linked open defect was observed again (expected while the defect is open); **XPASS** = a known-defect test passed, so the defect may be fixed and must be retested.

Four-task fixture (from Week 1 TC-BB-024 to 029): one user with `Work open A`, `Work done B` (done), `Personal open C`, `Personal done D` (done).


## Unit layer (Week 2 cases re-run): 41 tests

Test type: Unit / white-box (PyTest). Script: `tests/unit/test_unit_regression.py`.

| AUTO ID | Smoke | Linked case(s) | Req. | Objective / test data | Expected result | Known defect | Result (run 3) |
|---|---|---|---|---|---|---|---|
| AUTO-UNIT-001 |  | TC-WB-001 | R-01 | `is_valid_password(password=None)` | False |  | PASS |
| AUTO-UNIT-002 |  | TC-WB-002 | R-01 | `is_valid_password(password=123)` | False |  | PASS |
| AUTO-UNIT-003 |  | TC-WB-003 | R-01 | `is_valid_password(password='')` | False |  | PASS |
| AUTO-UNIT-004 |  | TC-WB-004, TC-BB-006 | R-01 | `is_valid_password(password='abcdefg')` | False |  | PASS |
| AUTO-UNIT-005 | Yes | TC-WB-005, TC-BB-007 | R-01 | `is_valid_password(password='abcdefgh')` | True | DEF-W1-001 | XFAIL |
| AUTO-UNIT-006 | Yes | TC-WB-006, TC-BB-007 | R-01 | `is_valid_password(password='abcdefghi')` | True |  | PASS |
| AUTO-UNIT-007 |  | TC-WB-007 | R-01 | `is_valid_username(username=None)` | False |  | PASS |
| AUTO-UNIT-008 |  | TC-WB-008 | R-01 | `is_valid_username(username=123)` | False |  | PASS |
| AUTO-UNIT-009 |  | TC-WB-009, TC-BB-002 | R-01 | `is_valid_username(username='ab')` | False |  | PASS |
| AUTO-UNIT-010 | Yes | TC-WB-010, TC-BB-001 | R-01 | `is_valid_username(username='abc')` | True |  | PASS |
| AUTO-UNIT-011 |  | TC-WB-011, TC-BB-003 | R-01 | `is_valid_username(username='abcdefghijklmnopqrst')` | True |  | PASS |
| AUTO-UNIT-012 |  | TC-WB-012, TC-BB-004 | R-01 | `is_valid_username(username='abcdefghijklmnopqrstu')` | False |  | PASS |
| AUTO-UNIT-013 |  | TC-WB-013 | R-01 | `is_valid_username(username='abc_1')` | True |  | PASS |
| AUTO-UNIT-014 |  | TC-WB-014, TC-BB-005 | R-01 | `is_valid_username(username='abc-1')` | False |  | PASS |
| AUTO-UNIT-015 |  | TC-WB-015 | R-01 | `is_valid_username(username='abc 1')` | False |  | PASS |
| AUTO-UNIT-016 |  | TC-WB-016 | R-01 | `is_valid_username(username='')` | False |  | PASS |
| AUTO-UNIT-017 |  | TC-WB-017 | R-01 | `is_valid_username(username='A1b')` | True |  | PASS |
| AUTO-UNIT-018 |  | TC-WB-018 | R-07 | `compute_urgency(due_date_str=None, today=date(2026, 10, 7))` | 'No due date' |  | PASS |
| AUTO-UNIT-019 |  | TC-WB-019 | R-07 | `compute_urgency(due_date_str='', today=date(2026, 10, 7))` | 'No due date' |  | PASS |
| AUTO-UNIT-020 |  | TC-WB-020, TC-BB-019 | R-07 | `compute_urgency(due_date_str='2026-10-06', today=date(2026, 10, 7))` | 'Overdue' |  | PASS |
| AUTO-UNIT-021 | Yes | TC-WB-021, TC-BB-020 | R-07 | `compute_urgency(due_date_str='2026-10-07', today=date(2026, 10, 7))` | 'Due Today' | DEF-W1-002 | XFAIL |
| AUTO-UNIT-022 |  | TC-WB-022, TC-BB-021 | R-07 | `compute_urgency(due_date_str='2026-10-08', today=date(2026, 10, 7))` | 'Due Soon' |  | PASS |
| AUTO-UNIT-023 |  | TC-WB-023, TC-BB-022 | R-07 | `compute_urgency(due_date_str='2026-10-09', today=date(2026, 10, 7))` | 'Due Soon' |  | PASS |
| AUTO-UNIT-024 | Yes | TC-WB-024, TC-BB-023 | R-07 | `compute_urgency(due_date_str='2026-10-10', today=date(2026, 10, 7))` | 'Upcoming' |  | PASS |
| AUTO-UNIT-025 |  | TC-WB-025 | R-07 | `compute_urgency(due_date_str=None)` (fixed clock) | 'No due date' |  | PASS |
| AUTO-UNIT-026 |  | TC-WB-026 | R-07 | `compute_urgency(due_date_str='2026-10-08')` (fixed clock) | 'Due Soon' |  | PASS |
| AUTO-UNIT-027 |  | TC-WB-027 | R-07 | `compute_urgency(due_date_str='not-a-date', today=date(2026, 10, 7))` | raises ValueError |  | PASS |
| AUTO-UNIT-028 |  | TC-WB-028 | R-07 | `compute_urgency(due_date_str='2026-02-30', today=date(2026, 10, 7))` | raises ValueError |  | PASS |
| AUTO-UNIT-029 |  | TC-WB-029 | R-09 | `completed_in_last_n_days(completed_at_str=None, now=datetime(2026, 10, 7, 12, 0))` | False |  | PASS |
| AUTO-UNIT-030 |  | TC-WB-030 | R-09 | `completed_in_last_n_days(completed_at_str='', now=datetime(2026, 10, 7, 12, 0))` | False |  | PASS |
| AUTO-UNIT-031 | Yes | TC-WB-031 | R-09 | `completed_in_last_n_days(completed_at_str='2026-10-06 12:00:00', now=datetime(2026, 10, 7, 12, 0))` | True |  | PASS |
| AUTO-UNIT-032 |  | TC-WB-032 | R-09 | `completed_in_last_n_days(completed_at_str='2026-10-07 12:00:00', now=datetime(2026, 10, 7, 12, 0))` | True | DEF-W2-001 | XFAIL |
| AUTO-UNIT-033 |  | TC-WB-033 | R-09 | `completed_in_last_n_days(completed_at_str='2026-09-30 12:00:01', now=datetime(2026, 10, 7, 12, 0))` | True |  | PASS |
| AUTO-UNIT-034 | Yes | TC-WB-034 | R-09 | `completed_in_last_n_days(completed_at_str='2026-09-30 12:00:00', now=datetime(2026, 10, 7, 12, 0))` | True | DEF-W2-001 | XFAIL |
| AUTO-UNIT-035 |  | TC-WB-035 | R-09 | `completed_in_last_n_days(completed_at_str='2026-09-30 11:59:59', now=datetime(2026, 10, 7, 12, 0))` | False |  | PASS |
| AUTO-UNIT-036 |  | TC-WB-036 | R-09 | `completed_in_last_n_days(completed_at_str='2026-09-29 12:00:00', now=datetime(2026, 10, 7, 12, 0))` | False |  | PASS |
| AUTO-UNIT-037 |  | TC-WB-037 | R-09 | `completed_in_last_n_days(completed_at_str='2026-10-07 12:00:01', now=datetime(2026, 10, 7, 12, 0))` | False |  | PASS |
| AUTO-UNIT-038 |  | TC-WB-038 | R-09 | `completed_in_last_n_days(completed_at_str='2026-10-06 12:00:00')` (fixed clock) | True |  | PASS |
| AUTO-UNIT-039 |  | TC-WB-039 | R-09 | `completed_in_last_n_days(completed_at_str='2026-10-06 12:00:00', n=1, now=datetime(2026, 10, 7, 12, 0))` | True | DEF-W2-001 | XFAIL |
| AUTO-UNIT-040 |  | TC-WB-040 | R-09 | `completed_in_last_n_days(completed_at_str='not-a-timestamp', now=datetime(2026, 10, 7, 12, 0))` | raises ValueError |  | PASS |
| AUTO-UNIT-041 |  | TC-WB-041 | R-09 | `completed_in_last_n_days(completed_at_str='2026-02-30 12:00:00', now=datetime(2026, 10, 7, 12, 0))` | raises ValueError |  | PASS |

## API layer: 34 tests

Test type: API (PyTest + Flask test client). Script: `tests/api/test_api_regression.py`.

| AUTO ID | Smoke | Linked case(s) | Req. | Objective / test data | Expected result | Known defect | Result (run 3) |
|---|---|---|---|---|---|---|---|
| AUTO-API-001 | Yes | TC-BB-001 | R-01 | Register `abc` / 9-char password | HTTP 201 with new id and username |  | PASS |
| AUTO-API-002a |  | TC-BB-002 | R-01 | Register 2-char username `ab` | HTTP 400 `invalid username` |  | PASS |
| AUTO-API-002b |  | TC-BB-003 | R-01 | Register 20-char username | HTTP 201 |  | PASS |
| AUTO-API-002c |  | TC-BB-004 | R-01 | Register 21-char username | HTTP 400 `invalid username` |  | PASS |
| AUTO-API-002d |  | TC-BB-005 | R-01 | Register `abc-1` (hyphen) | HTTP 400 `invalid username` |  | PASS |
| AUTO-API-003 |  | TC-BB-006 | R-01 | Register with 7-char password | HTTP 400 `invalid password` |  | PASS |
| AUTO-API-004 | Yes | TC-BB-007 | R-01 | Register with exactly 8-char password | HTTP 201 (stated minimum is 8) | DEF-W1-001 | XFAIL |
| AUTO-API-005 | Yes | TC-BB-008 | R-02 | Log in with correct password from a fresh session | HTTP 200; task list then reachable |  | PASS |
| AUTO-API-006 |  | TC-BB-009 | R-02 | Log in with wrong password | HTTP 401 `invalid credentials` |  | PASS |
| AUTO-API-007 | Yes | TC-BB-010 | R-02 | Request task list with no session | HTTP 401 `authentication required` |  | PASS |
| AUTO-API-008 |  | - | R-04 | List categories | Personal, Study, Urgent, Work |  | PASS |
| AUTO-API-009 | Yes | TC-BB-011 | R-04 | Create task with title, description, Study, due D+5 | HTTP 201; fields echoed; urgency Upcoming |  | PASS |
| AUTO-API-010 |  | TC-BB-012 | R-04 | Create task with title only | No category, no due date, urgency `No due date` |  | PASS |
| AUTO-API-011a |  | TC-BB-013 | R-04 | Create task with empty title | HTTP 400 `title is required` (server-side counterpart of the browser check) |  | PASS |
| AUTO-API-011b |  | TC-BB-014 | R-04 | Create task with three spaces as title | HTTP 400 `title is required` (API strips spaces; compare AUTO-WEB-007) |  | PASS |
| AUTO-API-012 |  | TC-BB-015 | R-05 | Update first of two tasks: title, Study, D+2 | First task changed; second unchanged |  | PASS |
| AUTO-API-013 | Yes | TC-BB-016 | R-06 | Mark done, then reopen (due D+1) | Done: urgency Done + completed_at; reopened: completed_at null, Due Soon |  | PASS |
| AUTO-API-014 | Yes | TC-BB-017 | R-05 | Delete one of two own tasks | `{result: ok}`; deleted task 404; other task still 200 |  | PASS |
| AUTO-API-015 |  | TC-BB-018 | R-03 | Two users each create a task; B lists tasks | B sees only B's task |  | PASS |
| AUTO-API-016a |  | TC-BB-012 | R-07 | Task without due date | `No due date` |  | PASS |
| AUTO-API-016b |  | TC-BB-019 | R-07 | Task due D-1 | `Overdue` |  | PASS |
| AUTO-API-016c | Yes | TC-BB-020 | R-07 | Task due today (D) | `Due Today` | DEF-W1-002 | XFAIL |
| AUTO-API-016d |  | TC-BB-021 | R-07 | Task due D+1 | `Due Soon` |  | PASS |
| AUTO-API-016e |  | TC-BB-022 | R-07 | Task due D+2 | `Due Soon` |  | PASS |
| AUTO-API-016f |  | TC-BB-023 | R-07 | Task due D+3 | `Upcoming` |  | PASS |
| AUTO-API-017a |  | TC-BB-024 | R-08 | Four-task fixture; category=Work, status=open | Work open A only |  | PASS |
| AUTO-API-017b |  | TC-BB-025 | R-08 | Four-task fixture; category=Work, status=done | Work done B only |  | PASS |
| AUTO-API-017c |  | TC-BB-026 | R-08 | Four-task fixture; category=Personal, status=open | Personal open C only |  | PASS |
| AUTO-API-017d |  | TC-BB-027 | R-08 | Four-task fixture; status=done, any category | Personal done D, Work done B |  | PASS |
| AUTO-API-017e |  | TC-BB-028 | R-08 | Four-task fixture; search q=open | Personal open C, Work open A |  | PASS |
| AUTO-API-018 | Yes | TC-BB-029 | R-09 | Four-task fixture; GET /api/dashboard | total 4, open 2, overdue 0, due_soon 0, completed_this_week 2 |  | PASS |
| AUTO-API-019 | Yes | API-32 | R-04, R-10 | Create task with a number as title (`123`) | HTTP 400, no crash (DEF-W4-001) | DEF-W4-001 | XFAIL |
| AUTO-API-020 | Yes | API-42 | R-05, R-10 | Update a task's title to null | HTTP 400; original title kept (DEF-W4-002) | DEF-W4-002 | XFAIL |
| AUTO-API-021 | Yes | API-49, API-50 | R-04, R-10 | Create task with due date `not-a-date`, then list tasks | HTTP 400; task list still returns 200 (DEF-W4-003) | DEF-W4-003 | XFAIL |

## Web form layer: 21 tests

Test type: Web form (PyTest + Flask test client). Script: `tests/web/test_web_regression.py`.

| AUTO ID | Smoke | Linked case(s) | Req. | Objective / test data | Expected result | Known defect | Result (run 3) |
|---|---|---|---|---|---|---|---|
| AUTO-WEB-001 | Yes | TC-BB-001 | R-01 | Register form: `abc` / 9-char password | Redirect to task list; `My Tasks` and `abc` in navigation |  | PASS |
| AUTO-WEB-002 |  | TC-BB-005 | R-01 | Register form: `abc-1` | Username rule message shown |  | PASS |
| AUTO-WEB-003 |  | TC-BB-007 | R-01 | Register form: exactly 8-char password | Account created (redirect), no error | DEF-W1-001 | XFAIL |
| AUTO-WEB-004 |  | TC-BB-009 | R-02 | Login form: wrong password | `Invalid username or password.` |  | PASS |
| AUTO-WEB-005 | Yes | TC-BB-010 | R-02 | Log out, then open /, /dashboard, /tasks/new | Each redirects to /login |  | PASS |
| AUTO-WEB-006 |  | TC-BB-012 | R-04 | New-task form with title only | Task listed with `No due date` |  | PASS |
| AUTO-WEB-007 | Yes | TC-BB-014 | R-04 | New-task form with three spaces as title | No task created (proposed quality expectation) | DEF-W1-004 | XFAIL |
| AUTO-WEB-008 |  | TC-BB-015 | R-05 | Edit first of two tasks: `Updated lab`, Study, D+2 | Edited task changed; other unchanged |  | PASS |
| AUTO-WEB-009 | Yes | TC-BB-016 | R-06, R-09 | Toggle a task done, then open again | Dashboard completed 1 / open 0, then completed 0 / open 1 |  | PASS |
| AUTO-WEB-010 |  | TC-BB-017 | R-05 | Delete one of two tasks via form | Only the other task remains |  | PASS |
| AUTO-WEB-011 |  | TC-BB-018 | R-03 | Two users; A creates a task; view B's list | B's list empty; A's list shows A's task |  | PASS |
| AUTO-WEB-012a |  | TC-BB-019 | R-07 | Task due D-1 in list | Badge `Overdue` |  | PASS |
| AUTO-WEB-012b |  | TC-BB-020 | R-07 | Task due today in list | Badge `Due Today` | DEF-W1-002 | XFAIL |
| AUTO-WEB-012c |  | TC-BB-023 | R-07 | Task due D+3 in list | Badge `Upcoming` |  | PASS |
| AUTO-WEB-013a |  | TC-BB-024 | R-08 | Four-task fixture; Work + Open filter | Work open A only |  | PASS |
| AUTO-WEB-013b |  | TC-BB-025 | R-08 | Four-task fixture; Work + Done filter | Work done B only |  | PASS |
| AUTO-WEB-013c |  | TC-BB-026 | R-08 | Four-task fixture; Personal + Open filter | Personal open C only |  | PASS |
| AUTO-WEB-013d |  | TC-BB-027 | R-08 | Four-task fixture; All categories + Done | Personal done D, Work done B |  | PASS |
| AUTO-WEB-013e |  | TC-BB-028 | R-08 | Four-task fixture; search `Personal` | Personal done D, Personal open C |  | PASS |
| AUTO-WEB-014 | Yes | TC-BB-029 | R-09 | Four-task fixture; Dashboard page | Total 4, Open 2, Overdue 0, Due Soon 0, Completed 2 |  | PASS |
| AUTO-WEB-015 | Yes | ACC-TC-008 | R-11 | New Task form: Title, Description, Category, Due Date | Each control has an id and a matching `<label for>` (DEF-W3-002) | DEF-W3-002 | XFAIL |

## Browser (UI) layer: 8 tests

Test type: UI end-to-end (Selenium + PyTest). Script: `tests/ui/test_ui_regression.py`.

| AUTO ID | Smoke | Linked case(s) | Req. | Objective / test data | Expected result | Known defect | Result (run 3) |
|---|---|---|---|---|---|---|---|
| AUTO-UI-001 | Yes | TC-BB-001 | R-01 | Browser: register a new user | Heading `My Tasks`; username in navigation |  | PASS |
| AUTO-UI-002 |  | TC-BB-007 | R-01 | Browser: register with 8-char password | No error; task list shown | DEF-W1-001 | XFAIL |
| AUTO-UI-003 |  | TC-BB-008, TC-BB-009 | R-02 | Browser: log out, wrong password, then correct password | Error message, then signed in |  | PASS |
| AUTO-UI-004 | Yes | TC-BB-011 | R-04, R-07 | Browser: create task, Study, due D+5, description | Task listed with badge Upcoming |  | PASS |
| AUTO-UI-005 | Yes | TC-BB-016 | R-06, R-09 | Browser: mark done, check dashboard, reopen | Row marked done/Done; completed 1, then 0 |  | PASS |
| AUTO-UI-006 |  | TC-BB-017 | R-05 | Browser: delete one of two tasks, accept confirmation dialog | Only the kept task remains |  | PASS |
| AUTO-UI-007 |  | TC-BB-010 | R-02 | Browser: log out, open /dashboard | Redirected to Log in page |  | PASS |
| AUTO-UI-008 | Yes | ACC-TC-002 | R-11 | Browser: complete a task, read title colour and background | Contrast at least 4.5:1 (DEF-W3-001) | DEF-W3-001 | XFAIL |

## Regression checks for open defects found in Weeks 3 and 4

One automated test per open defect, so a single regression run reports every open defect. The full Week 4 API suite (53 cases) and Week 3/4 browser checks keep their own runners; DEF-W1-003 is checked by Week 4 API-25.

| Original case | Defect | Automated test | Layer |
|---|---|---|---|
| ACC-TC-002 | DEF-W3-001 | AUTO-UI-008 | ui |
| ACC-TC-008 | DEF-W3-002 | AUTO-WEB-015 | web |
| API-32 | DEF-W4-001 | AUTO-API-019 | api |
| API-42 | DEF-W4-002 | AUTO-API-020 | api |
| API-49, API-50 | DEF-W4-003 | AUTO-API-021 | api |

## Manual-to-automated traceability (Week 1 black-box cases)

All 29 Week 1 cases now have at least one automated counterpart. Most are automated at the API or web-form layer (fast, stable); the most important end-to-end flows are also checked in a real browser. All 41 Week 2 cases are re-run unchanged in the unit layer (`TC-WB-nnn` → `AUTO-UNIT-nnn`).

| Manual case | Title | Automated test(s) | Layers | Coverage note |
|---|---|---|---|---|
| TC-BB-001 | valid minimum username | AUTO-API-001, AUTO-UI-001, AUTO-UNIT-010, AUTO-WEB-001 | unit, api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-002 | username below minimum | AUTO-API-002a, AUTO-UNIT-009 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-003 | maximum username length | AUTO-API-002b, AUTO-UNIT-011 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-004 | username above maximum | AUTO-API-002c, AUTO-UNIT-012 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-005 | invalid username character | AUTO-API-002d, AUTO-UNIT-014, AUTO-WEB-002 | unit, api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-006 | password below minimum | AUTO-API-003, AUTO-UNIT-004 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-007 | password at stated minimum | AUTO-API-004, AUTO-UI-002, AUTO-UNIT-005, AUTO-UNIT-006, AUTO-WEB-003 | unit, api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-008 | correct login | AUTO-API-005, AUTO-UI-003 | api, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-009 | wrong password | AUTO-API-006, AUTO-UI-003, AUTO-WEB-004 | api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-010 | logout and protected page | AUTO-API-007, AUTO-UI-007, AUTO-WEB-005 | api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-011 | create complete task | AUTO-API-009, AUTO-UI-004 | api, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-012 | create without optional fields | AUTO-API-010, AUTO-API-016a, AUTO-WEB-006 | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-013 | blank title in browser | AUTO-API-011a | api | Partial: the server-side rule is automated (API rejects an empty title). The browser's own `required` prompt is a browser-native message and stays a manual GUI check; note the web form route itself has no server-side title check. |
| TC-BB-014 | whitespace-only title | AUTO-API-011b, AUTO-WEB-007 | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-015 | edit existing task | AUTO-API-012, AUTO-WEB-008 | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-016 | mark done and reopen | AUTO-API-013, AUTO-UI-005, AUTO-WEB-009 | api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-017 | delete one task | AUTO-API-014, AUTO-UI-006, AUTO-WEB-010 | api, web, ui | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-018 | separate users' task lists | AUTO-API-015, AUTO-WEB-011 | api, web | List isolation only (what Week 1 tested in the UI). Ownership checks on other operations belong to the Week 5 security cases. |
| TC-BB-019 | past due date | AUTO-API-016b, AUTO-UNIT-020, AUTO-WEB-012a | unit, api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-020 | due today | AUTO-API-016c, AUTO-UNIT-021, AUTO-WEB-012b | unit, api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-021 | due in one day | AUTO-API-016d, AUTO-UNIT-022 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-022 | due in two days | AUTO-API-016e, AUTO-UNIT-023 | unit, api | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-023 | due in three days | AUTO-API-016f, AUTO-UNIT-024, AUTO-WEB-012c | unit, api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-024 | Work and open | AUTO-API-017a, AUTO-WEB-013a | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-025 | Work and done | AUTO-API-017b, AUTO-WEB-013b | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-026 | Personal and open | AUTO-API-017c, AUTO-WEB-013c | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-027 | all categories and done | AUTO-API-017d, AUTO-WEB-013d | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-028 | title search | AUTO-API-017e, AUTO-WEB-013e | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
| TC-BB-029 | dashboard counts | AUTO-API-018, AUTO-WEB-014 | api, web | Same rule and expected result; test data may differ where uniqueness is needed |
