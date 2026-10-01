# Week 1 defect log

Four initial defects are recorded below. Browser failures 007, 014, and 020 were reproduced manually. DEF-W1-003 comes from the separate API probe; its group retest is pending. The complete case execution record is [Master_Test_Repository.md](Master_Test_Repository.md). Keep these defect IDs stable across later phases.

### DEF-W1-001 - exactly 8 characters rejected as a password

- **Affected feature:** Registration / password validation (R-01).
- **Environment:** Python 3.12.10, Flask 3.0.3, app from supplied download, isolated in-memory SQLite database, local date 2026-09-30 (+08:00).
- **Preconditions:** New, unused username; not signed in.
- **Steps to reproduce:** In the browser, open Register while signed out, enter unused username `pw8user` and exactly eight-character password `abcdefgh`, then submit. The original isolated API check also submitted `POST /api/register` with an eight-character password and compared it with a nine-character password.
- **Expected result:** An 8-character password is accepted because the form and helper specification say minimum 8; a 9-character password is also accepted.
- **Actual result:** The manual browser registration showed `Password must be at least 8 characters.` and did not create `pw8user`. In the isolated API check, eight characters returned HTTP 400 `invalid password`, while nine characters returned HTTP 201.
- **Severity / priority:** Moderate / Medium.
- **Evidence:** Original manual screenshot `evidence/manual_screenshots/TC-BB-007.png` and [case observation](Master_Test_Repository.md#tc-bb-007---password-at-stated-minimum); the API probe evidence section below, observations P-01 and P-02; raw log `evidence/isolated_api_probe_2026-09-30.txt`; automated browser result TC-BB-007 and `evidence/browser_screenshots/TC-BB-007.png`; source reference `helpers.py`, `is_valid_password`.
- **Status:** Confirmed by isolated API, automated browser, and user-performed manual browser checks. The original manual screenshot is stored; actual manual tester/date remain unconfirmed.

### DEF-W1-002 - due-today task marked overdue

- **Affected feature:** Task urgency (R-07).
- **Environment:** Isolated checks: Python 3.12.10, Flask 3.0.3, Edge 154, separate SQLite database on port 5001; user-performed browser check: downloaded app on port 5000. Local date 2026-09-30 (+08:00).
- **Preconditions:** Signed-in account; fresh open task.
- **Steps to reproduce:** 1. Create a task whose due date equals the local date. 2. Inspect its `urgency` value and compare with tasks due yesterday, tomorrow, +2, and +3 days.
- **Expected result:** Due today is `Due Today`, according to the helper specification; yesterday is `Overdue`.
- **Actual result:** The due-today task displayed `Overdue` in the user-performed browser test on 2026-09-30; the isolated browser/API checks also returned `Overdue`.
- **Severity / priority:** Moderate / Medium.
- **Evidence:** Original manual screenshot `evidence/manual_screenshots/TC-BB-020.png` and [case observation](Master_Test_Repository.md#tc-bb-020---due-today); the API probe evidence section below, observations P-04 through P-07; raw log `evidence/isolated_api_probe_2026-09-30.txt`; automated browser result TC-BB-020 and `evidence/browser_screenshots/TC-BB-020.png`; source reference `helpers.py`, `compute_urgency`.
- **Status:** Confirmed by isolated API, automated browser, and user-performed manual browser checks. The original manual screenshot is stored; actual manual tester/date remain unconfirmed.

### DEF-W1-003 - one user can delete another user's task through the API

- **Affected feature:** Task ownership and deletion (R-03/R-05).
- **Environment:** Same isolated check environment; two distinct signed-in clients/accounts.
- **Preconditions:** Account A owns a task; account B has no permission to manage it.
- **Steps to reproduce:** 1. Sign in as A and create a task; record its ID. 2. Sign in as B in a separate session. 3. Send `DELETE /api/tasks/<A-task-ID>` as B. 4. Try to fetch the task again as A.
- **Expected result:** B's deletion is denied and A's task remains accessible.
- **Actual result:** B received HTTP 200 `{"result":"ok"}`; A then received HTTP 404 for the task.
- **Severity / priority:** Major / High.
- **Evidence:** the API probe evidence section below, observations P-08 and P-09; raw log `evidence/isolated_api_probe_2026-09-30.txt`; source reference `app.py`, `api_delete_task`.
- **Status:** Confirmed by isolated API check; group retest in its local environment pending. Revisit in Week 5 threat analysis.

### DEF-W1-004 - whitespace-only title creates an unnamed task

- **Affected feature:** Task creation / title validation (R-04).
- **Environment:** Microsoft Edge headless browser through Playwright, Python 3.12.10, Flask 3.0.3, supplied app with isolated SQLite database, 2026-09-30 (+08:00).
- **Preconditions:** Signed in; task list accessible.
- **Steps to reproduce:** 1. Open New Task. 2. Type three spaces in Title. 3. Click Create Task. 4. Inspect the task list.
- **Expected result:** A whitespace-only title is rejected with a clear validation message because it identifies no task. This is a proposed quality expectation; confirm it with the group/lecturer if a formal requirement is needed.
- **Actual result:** The app redirected to My Tasks and created a new row whose title displays as blank. A read-only check of the live app database found the stored title was the empty string after the three-space input.
- **Severity / priority:** Moderate / Medium.
- **Evidence:** Original manual screenshot `evidence/manual_screenshots/TC-BB-014.png` and [case observation](Master_Test_Repository.md#tc-bb-014---whitespace-only-title); automated browser result TC-BB-014 and `evidence/browser_screenshots/TC-BB-014.png`; source reference `app.py`, `new_task`.
- **Status:** Reproduced in isolated automated and user-performed manual browser checks; formal whitespace-title requirement confirmation pending.

## Open requirement question, not yet a confirmed defect

An isolated API check accepted a second account with an identical username (observation P-03). The brief and starter README do not explicitly define username uniqueness. Ask the lecturer/group to agree on the expected behavior; if usernames should identify one account, add a test case and defect report with evidence. Until then, record it as a risk to authentication rather than asserting a formal requirement violation.

## API probe evidence

Date/time: 2026-09-30, Asia/Singapore (+08:00). Environment: Windows, Python 3.12.10, Flask 3.0.3, supplied `pytodo_pro_student` source. The app was imported without changing its files. Flask's local test client used separate signed-in sessions (`account_a` and `account_b`) and a shared **in-memory** SQLite database; no server was exposed and no downloaded database was modified. The raw output is in `evidence/isolated_api_probe_2026-09-30.txt`. These results are supporting evidence for test design and initial defects. They do not satisfy the Week 1 requirement to execute cases manually in the browser.

| Observation | Controlled input/action | Expected from stated behavior or ownership rule | Observed result |
|---|---|---|---|
| P-01 | Register valid username with 8-character password | Accepted; minimum stated as 8 | HTTP 400, `{"error":"invalid password"}` |
| P-02 | Register valid username with 9-character password | Accepted | HTTP 201 |
| P-03 | Register a second account using the same username | Requirement needs confirmation | HTTP 201 for second account |
| P-04 | Create open task due 2026-09-30 (D) | `Due Today` | HTTP 201, urgency `Overdue` |
| P-05 | Create open task due D+1 | `Due Soon` | HTTP 201, urgency `Due Soon` |
| P-06 | Create open task due D+2 | `Due Soon` | HTTP 201, urgency `Due Soon` |
| P-07 | Create open task due D+3 | `Upcoming` | HTTP 201, urgency `Upcoming` |
| P-08 | Account B deletes account A's task via its task ID | Denied; A's task remains | HTTP 200, `{"result":"ok"}` |
| P-09 | Account A fetches that task after B's request | Task still available | HTTP 404, `{"error":"not found"}` |

Code inspection indicates that a 7-character password would be rejected; that specific input was not executed in this API probe, but TC-BB-006 subsequently passed in the isolated browser run. Password and due-date expectations come from the registration form and `helpers.py` docstrings. Task ownership is inferred from the per-user task list and the ownership checks on other task routes. Keep this distinction clear in the final report.
