# Week 1 master test-case repository

This is the single record for all 29 case designs, input data, expected results, manual and automated actual results, evidence, and defect IDs. Expectations were defined before execution. Manual and automated outcomes are recorded separately. Both runs contain 26 Pass and 3 Fail (007, 014, 020). The API probe is outside these 29 cases and is recorded in [Defect_Log.md](Defect_Log.md#api-probe-evidence).

The executor, partner, and dates in each case remain **planned assignments** until the group confirms who performed the tests. Record confirmed execution details in those existing case records. Manual browser/version: `_____`; database reset/reuse method: `_____`. The manual app ran on port 5000 using the supplied download, Python 3.12.10, Flask 3.0.3, and Asia/Singapore time.

Automated run started 2026-09-30T06:20:42.178Z: Windows NT build 26200, Edge 154.0.4258.37 via Playwright, Python 3.12.10, Flask 3.0.3, isolated SQLite database on port 5001. Raw results: [browser_results.json](evidence/browser_results.json). Method, scope, risks, and RTM: [Week1_Report.md](Week1_Report.md).

`D` is the local calendar date on the test day. Use fresh usernames for registration. For ownership checks, use two distinct accounts. For filter/dashboard cases, use a fresh account with only the four tasks specified below; the manual fixture used `filteruser1`. Preserve submitted inputs and expected results when reporting a failure.

## Decision table and shared filter data

Prepare four tasks under one account: `Work open A`, `Work done B`, `Personal open C`, `Personal done D`. The decision rules are: a selected category must match, a selected status must match, and both conditions apply together. `Any` means no category filter.

| Rule / case | Category | Status | Expected visible titles |
|---|---|---|---|
| TC-BB-024 | Work | Open | Work open A only |
| TC-BB-025 | Work | Done | Work done B only |
| TC-BB-026 | Personal | Open | Personal open C only |
| TC-BB-027 | Any | Done | Work done B and Personal done D only |

## State transition model

Session: signed out -> signed in -> signed out (008-010). Task: created/open -> edited (015) -> done -> reopened (016) -> deleted (017). Verify the selected task, the unaffected comparison task, and the dashboard counts where specified.

## TC-BB-001 - valid minimum username

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Confirm a 3-character username is accepted.
- **Preconditions:** Signed out; username unused.
- **Test Data:** Username `abc`; password `abcdefghi` (9 characters).
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Account is created and the task list opens under `abc`.
- **Automated Actual Result:** Registration opened My Tasks with abc shown in navigation.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-001.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** After the user submitted `abc` with a 9-character test password, the browser showed `My Tasks` and `abc` in the navigation; no tasks yet.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (retest)
- **Manual Status:** Pass
- **Manual Evidence:** [Original user screenshot](evidence/TC-BB-001-success.png)
- **Defect ID:** —

## TC-BB-002 - username below minimum

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Reject a 2-character username.
- **Preconditions:** Signed out.
- **Test Data:** Username `ab`; password `abcdefghi`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Registration is rejected with a useful validation message; no account is created.
- **Automated Actual Result:** Registration rejected ab: Username must be 3-20 characters (letters, numbers, underscore).
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-002.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Registration showed `Username must be 3-20 characters (letters, numbers, underscore).`; no `ab` account was found in the active app database after the attempt.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [Original user screenshot](evidence/manual_screenshots/TC-BB-002.png); image captured 2026-10-01.
- **Defect ID:** —
- **Evidence limitation:** Rejected input is cleared by the form. The username is corroborated by the user's recheck sequence and the recorded database check; the screenshot alone does not display the submitted username.

## TC-BB-003 - maximum username length

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Accept 20 valid characters.
- **Preconditions:** Signed out; username unused.
- **Test Data:** Username `abcdefghijklmnopqrst`; password `abcdefghi`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Account is created and the task list opens.
- **Automated Actual Result:** 20-character username accepted.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-003.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** My Tasks opened under `abcdefghijklmnopqrst` (exactly 20 characters); a read-only database check found one matching account.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [Original user screenshot](evidence/manual_screenshots/TC-BB-003.png); image captured 2026-10-01.
- **Defect ID:** —

## TC-BB-004 - username above maximum

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Reject 21 characters.
- **Preconditions:** Signed out.
- **Test Data:** Username `abcdefghijklmnopqrstu`; password `abcdefghi`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Registration is rejected; no account is created.
- **Automated Actual Result:** 21-character username rejected: Username must be 3-20 characters (letters, numbers, underscore).
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-004.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Registration showed `Username must be 3-20 characters (letters, numbers, underscore).`; a read-only database check found no `abcdefghijklmnopqrstu` account after the attempt.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [Original user screenshot](evidence/manual_screenshots/TC-BB-004.png); image captured 2026-10-01.
- **Defect ID:** —
- **Evidence limitation:** Rejected input is cleared by the form. The username is corroborated by the user's recheck sequence and the recorded database check; the screenshot alone does not display the submitted username.

## TC-BB-005 - invalid username character

- **Feature/Requirement:** R-01
- **Technique/Test Type:** EP
- **Objective:** Reject characters outside letters, digits, and underscore.
- **Preconditions:** Signed out.
- **Test Data:** Username `abc-1`; password `abcdefghi`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Registration is rejected with a useful validation message.
- **Automated Actual Result:** Username with hyphen rejected: Username must be 3-20 characters (letters, numbers, underscore).
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-005.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** User identified a manual TC-BB-005 screenshot showing `Username must be 3-20 characters (letters, numbers, underscore).`; a read-only database check found no `abc-1` account after the attempt.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-005.png)
- **Defect ID:** —

## TC-BB-006 - password below minimum

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Reject 7 characters.
- **Preconditions:** Signed out; username unused.
- **Test Data:** Username `pw7user`; password `abcdefg`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Registration is rejected; no account is created.
- **Automated Actual Result:** 7-character password rejected: Password must be at least 8 characters.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-006.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Registration showed `Password must be at least 8 characters.`; a read-only database check found no `pw7user` account after the attempt.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-006.png)
- **Defect ID:** —

## TC-BB-007 - password at stated minimum

- **Feature/Requirement:** R-01
- **Technique/Test Type:** BVA
- **Objective:** Accept exactly 8 characters as stated on the registration form and in `helpers.py`.
- **Preconditions:** Signed out; username unused.
- **Test Data:** Username `pw8user`; password `abcdefgh`.
- **Steps:** 1. Open Register. 2. Enter the data. 3. Submit.
- **Expected Result:** Account is created and the task list opens.
- **Automated Actual Result:** Expected 8-character password accepted; got http://127.0.0.1:5001/register, Password must be at least 8 characters.
- **Automated Status:** Fail
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-007.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Registration rejected the exactly eight-character password with `Password must be at least 8 characters.`; a read-only database check found no `pw8user` account after the attempt.
- **Planned Manual Executor:** Gan Jeng Jie
- **Planned Partner/Reviewer:** Wan Qistina
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Fail
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-007.png)
- **Defect ID:** DEF-W1-001

## TC-BB-008 - correct login

- **Feature/Requirement:** R-02
- **Technique/Test Type:** EP
- **Objective:** Confirm a registered user can sign in.
- **Preconditions:** `login_user` exists with password `abcdefghi`; signed out.
- **Test Data:** Correct username and password.
- **Steps:** 1. Open Login. 2. Enter credentials. 3. Submit.
- **Expected Result:** Task list opens with the correct account shown.
- **Automated Actual Result:** Correct credentials opened My Tasks under login_user.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-008.png); raw result in `evidence/browser_results.json`
- **Manual Test Data:** Existing username `abc`, password `abcdefghi` (case instruction; different account name from the isolated automated run).
- **Manual Actual Result:** The user-provided screenshot showed **My Tasks** with `abc` in the navigation and a **Log out** link after the login instruction.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-008.png)
- **Defect ID:** —

## TC-BB-009 - wrong password

- **Feature/Requirement:** R-02
- **Technique/Test Type:** EP
- **Objective:** Reject incorrect credentials.
- **Preconditions:** `login_user` exists; signed out.
- **Test Data:** Username `login_user`; password `wrongpass`.
- **Steps:** 1. Open Login. 2. Enter credentials. 3. Submit.
- **Expected Result:** Login is rejected and protected task data is not shown.
- **Automated Actual Result:** Wrong password rejected: Invalid username or password.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-009.png); raw result in `evidence/browser_results.json`
- **Manual Test Data:** Existing username `abc`, incorrect password `wrongpass` (case instruction; different account name from the isolated automated run).
- **Manual Actual Result:** The user-provided screenshot showed `Invalid username or password.` on the login page, with no protected task list.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-009.png)
- **Defect ID:** —

## TC-BB-010 - logout and protected page

- **Feature/Requirement:** R-02/R-03
- **Technique/Test Type:** state transition
- **Objective:** End a session.
- **Preconditions:** Signed in; at least one task exists.
- **Test Data:** Task-list URL `/`.
- **Steps:** 1. Click Log out. 2. Then browse directly to `/`.
- **Expected Result:** Login page appears; the old task list is inaccessible until login.
- **Automated Actual Result:** Logout cleared access; direct visit to / redirected to Login.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-010.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** After the logout/direct-navigation instruction, the screenshot showed the Log in page and no task list. A read-only database check found a `Logout check` task owned by `abc`, meeting the task precondition.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-010.png)
- **Defect ID:** —

## TC-BB-011 - create complete task

- **Feature/Requirement:** R-04
- **Technique/Test Type:** EP
- **Objective:** Create a task with all main fields.
- **Preconditions:** Signed in; Work category available.
- **Test Data:** Title `Submit lab`; description `Draft report`; category Work; due date D+3.
- **Steps:** 1. Open New Task. 2. Enter data. 3. Submit. 4. Inspect task list and edit form.
- **Expected Result:** One new open task appears with saved title, description, category, and due date.
- **Automated Actual Result:** Task saved; title/category visible and description/due date persisted in edit form.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-011.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** The task list showed `Submit lab`, Work, and due date `2026-10-03`; the edit form showed saved description `Draft report` and the same title, category, and due date. A read-only database check corroborated these values.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [list](evidence/manual_screenshots/TC-BB-011-list.png); [edit-form](evidence/manual_screenshots/TC-BB-011-edit-form.png)
- **Defect ID:** —

## TC-BB-012 - create without optional fields

- **Feature/Requirement:** R-04/R-07
- **Technique/Test Type:** EP
- **Objective:** Create a task without description, category, or date.
- **Preconditions:** Signed in.
- **Test Data:** Title `Undated task`; other fields blank.
- **Steps:** 1. Create task. 2. Inspect list.
- **Expected Result:** Task is saved; urgency reads `No due date`.
- **Automated Actual Result:** Task without optional fields saved; urgency No due date.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-012.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** The list showed `Undated task` with no category, no due date, and `No due date` urgency. A read-only database check found an empty description and null category/due date.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-012.png)
- **Defect ID:** —

## TC-BB-013 - blank title in browser

- **Feature/Requirement:** R-04
- **Technique/Test Type:** EP
- **Objective:** Prevent an empty required title.
- **Preconditions:** Signed in.
- **Test Data:** Empty title; other fields arbitrary.
- **Steps:** 1. Open New Task. 2. Leave title empty. 3. Submit.
- **Expected Result:** Task is not created and the user is prompted to provide a title.
- **Automated Actual Result:** Browser required-field validation blocked an empty title.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-013.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Browser showed `Please fill out this field.` on the empty Title input; a read-only database check found no task with an empty-string title.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-013.png)
- **Defect ID:** —

## TC-BB-014 - whitespace-only title

- **Feature/Requirement:** R-04
- **Technique/Test Type:** EP
- **Objective:** Check server validation after trimming.
- **Preconditions:** Signed in.
- **Test Data:** Three spaces as title.
- **Steps:** 1. Open New Task. 2. Enter spaces in title. 3. Submit. 4. Inspect list.
- **Expected Result:** Task is not created; a clear validation message is shown. This is a proposed quality expectation because a blank title cannot identify a task.
- **Automated Actual Result:** Whitespace title was accepted: redirected to http://127.0.0.1:5001/, task rows=1, error=
- **Automated Status:** Fail
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-014.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** After the three-space-title instruction, the task list showed a new row with no visible title. A read-only database check found the saved task's title is the empty string after trimming.
- **Planned Manual Executor:** Ahmad Adam Ali
- **Planned Partner/Reviewer:** Sathineswary Saravanesvaran
- **Planned Date:** Thu 2026-10-01 (evidence review/retest)
- **Manual Status:** Fail
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-014.png)
- **Defect ID:** DEF-W1-004

## TC-BB-015 - edit existing task

- **Feature/Requirement:** R-05
- **Technique/Test Type:** state transition
- **Objective:** Save changes to the selected task only.
- **Preconditions:** Signed in; two tasks exist.
- **Test Data:** Change first task title to `Updated lab`, category to Study, due date to D+2.
- **Steps:** 1. Edit the first task. 2. Save. 3. Inspect both tasks.
- **Expected Result:** First task shows changed values; second task is unchanged.
- **Automated Actual Result:** Selected task changed title/category/due date; second task stayed unchanged.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-015.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** The selected task saved as `Update lab`, category Study, due date `2026-10-02`; `Undated task` remained unchanged. The planned title was `Updated lab`; the saved title is recorded as a manual test-data variation pending any correction from the tester.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Note:** Saved title `Update lab` differs from planned `Updated lab`; see the observation for the documented data variation.
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-015.png)
- **Defect ID:** —
- **Evidence limitation:** If the tester confirms entering `Updated lab` exactly, investigate the saved `Update lab` title and reconsider the current data-variation classification.

## TC-BB-016 - mark done and reopen

- **Feature/Requirement:** R-06/R-09
- **Technique/Test Type:** state transition
- **Objective:** Open -> done -> open.
- **Preconditions:** Signed in; one known open task; record dashboard counts.
- **Test Data:** The known task.
- **Steps:** 1. Mark it done. 2. Inspect list/dashboard. 3. Mark it open again. 4. Inspect list/dashboard.
- **Expected Result:** Task and open count change in both directions; completed count rises when done and no longer includes the task after reopening.
- **Automated Actual Result:** Open -> done -> open; dashboard open 0 -> 1 and recent completion 1 -> 0.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-016.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** `Update lab` was shown Done; Dashboard while done: total 4, open 3, due soon 0, completed last 7 days 1. After reopening: total 4, open 4, due soon 1, completed last 7 days 0. A read-only database check confirmed the task ended open.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [done-list](evidence/manual_screenshots/TC-BB-016-done-list.png); [done-dashboard](evidence/manual_screenshots/TC-BB-016-done-dashboard.png); [reopened-dashboard](evidence/manual_screenshots/TC-BB-016-reopened-dashboard.png)
- **Defect ID:** —

## TC-BB-017 - delete one task

- **Feature/Requirement:** R-05
- **Technique/Test Type:** state transition
- **Objective:** Remove only the selected task.
- **Preconditions:** Signed in; two tasks exist.
- **Test Data:** First task ID/title.
- **Steps:** 1. Delete the first task and confirm. 2. Inspect list and dashboard.
- **Expected Result:** First task disappears, second remains, total count decreases by one.
- **Automated Actual Result:** Selected task deleted; other task remained; total became 1.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-017.png); raw result in `evidence/browser_results.json`
- **Manual Test Data:** Delete `Logout check` (labeled setup task; variation from the isolated case's first-task fixture).
- **Manual Actual Result:** `Logout check` disappeared while the other three tasks remained; Dashboard Total Tasks decreased from 4 to 3. A read-only database check found no `Logout check` task.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [list](evidence/manual_screenshots/TC-BB-017-list.png); [dashboard](evidence/manual_screenshots/TC-BB-017-dashboard.png)
- **Defect ID:** —

## TC-BB-018 - separate users' task lists

- **Feature/Requirement:** R-03
- **Technique/Test Type:** EP
- **Objective:** Protect a user's own tasks.
- **Preconditions:** Account A owns a task; account B exists.
- **Test Data:** Account A task title and edit URL; account B credentials.
- **Steps:** 1. Sign out A. 2. Sign in B. 3. Inspect task list. 4. Attempt A's known edit URL.
- **Expected Result:** B cannot see or edit A's task; A's task remains unchanged when A signs back in.
- **Automated Actual Result:** B could not list or edit A task; A still saw it after signing back in.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-018.png); raw result in `evidence/browser_results.json`
- **Manual Test Data:** Account A `abc`, account B `abcdefghijklmnopqrst`, A's task ID 2 (`Update lab`), edit URL `/tasks/2/edit`.
- **Manual Actual Result:** Under account B, the task list was empty and entering A's edit URL showed the same empty My Tasks page, not A's edit form. A read-only database check confirmed A's task remained unchanged.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [account-b-view-1](evidence/manual_screenshots/TC-BB-018-account-b-view-1.png); [account-b-view-2](evidence/manual_screenshots/TC-BB-018-account-b-view-2.png)
- **Defect ID:** —

## TC-BB-019 - past due date

- **Feature/Requirement:** R-07
- **Technique/Test Type:** BVA
- **Objective:** Classify D-1.
- **Preconditions:** Signed in.
- **Test Data:** Due date D-1.
- **Steps:** 1. Create a task due D-1. 2. Inspect urgency.
- **Expected Result:** `Overdue`.
- **Automated Actual Result:** Due 2026-09-29: urgency Overdue.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-019.png); raw result in `evidence/browser_results.json`
- **Manual Test Data:** Account `abcdefghijklmnopqrst`; saved title `Pass due task` (suggested title was `Past due task`); due date `2026-09-29` (D-1 on 2026-09-30).
- **Manual Actual Result:** Task list labeled the task **Overdue**; a read-only database check confirmed the due date and account.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-019.png)
- **Defect ID:** —

## TC-BB-020 - due today

- **Feature/Requirement:** R-07
- **Technique/Test Type:** BVA
- **Objective:** Classify the exact today boundary.
- **Preconditions:** Signed in.
- **Test Data:** Due date D.
- **Steps:** 1. Create a task due D. 2. Inspect urgency.
- **Expected Result:** `Due Today`, as specified in `helpers.py`.
- **Automated Actual Result:** Due 2026-09-30: expected Due Today, observed Overdue
- **Automated Status:** Fail
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-020.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** On local date `2026-09-30`, the task due `2026-09-30` displayed **Overdue** instead of **Due Today**. A read-only database check confirmed the saved due date.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Fail
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-020.png)
- **Defect ID:** DEF-W1-002

## TC-BB-021 - due in one day

- **Feature/Requirement:** R-07
- **Technique/Test Type:** BVA
- **Objective:** Classify D+1.
- **Preconditions:** Signed in.
- **Test Data:** Due date D+1.
- **Steps:** 1. Create a task due D+1. 2. Inspect urgency.
- **Expected Result:** `Due Soon`.
- **Automated Actual Result:** Due 2026-10-01: urgency Due Soon.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-021.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** On local date `2026-09-30`, `Due tomorrow task` due `2026-10-01` displayed **Due Soon**. A read-only database check confirmed the saved due date.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-021.png)
- **Defect ID:** —

## TC-BB-022 - due in two days

- **Feature/Requirement:** R-07
- **Technique/Test Type:** BVA
- **Objective:** Classify D+2.
- **Preconditions:** Signed in.
- **Test Data:** Due date D+2.
- **Steps:** 1. Create a task due D+2. 2. Inspect urgency.
- **Expected Result:** `Due Soon`.
- **Automated Actual Result:** Due 2026-10-02: urgency Due Soon.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-022.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** On local date `2026-09-30`, `Due in two days task` due `2026-10-02` displayed **Due Soon**. A read-only database check confirmed the saved due date.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-022.png)
- **Defect ID:** —

## TC-BB-023 - due in three days

- **Feature/Requirement:** R-07
- **Technique/Test Type:** BVA
- **Objective:** Classify D+3.
- **Preconditions:** Signed in.
- **Test Data:** Due date D+3.
- **Steps:** 1. Create a task due D+3. 2. Inspect urgency.
- **Expected Result:** `Upcoming`.
- **Automated Actual Result:** Due 2026-10-03: urgency Upcoming.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-023.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** On local date `2026-09-30`, `Due in three days task` due `2026-10-03` displayed **Upcoming**. A read-only database check confirmed the saved due date.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02 (evidence review/retest)
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-023.png)
- **Defect ID:** —

## TC-BB-024 - Work and open

- **Feature/Requirement:** R-08
- **Technique/Test Type:** decision table
- **Objective:** Apply both filters.
- **Preconditions:** Four-task fixture above exists.
- **Test Data:** Category Work; status Open.
- **Steps:** 1. Set both filters. 2. Submit. 3. Record visible titles.
- **Expected Result:** `Work open A` only.
- **Automated Actual Result:** Category=Work, status=open; visible: Work open A.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-024.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** The Work + Open filter showed only `Work Open A` (Work, open). A read-only database check confirmed the four-task fixture and that this was its sole Work + Open task. The capital `Open` is a title data variation.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-024.png)
- **Defect ID:** —

## TC-BB-025 - Work and done

- **Feature/Requirement:** R-08
- **Technique/Test Type:** decision table
- **Objective:** Apply both filters.
- **Preconditions:** Four-task fixture above exists.
- **Test Data:** Category Work; status Done.
- **Steps:** 1. Set both filters. 2. Submit. 3. Record visible titles.
- **Expected Result:** `Work done B` only.
- **Automated Actual Result:** Category=Work, status=done; visible: Work done B.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-025.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** With Work + Done selected, the list showed only `Work done B`, marked complete with a check mark, struck-through title, and Done label.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-025.png)
- **Defect ID:** —

## TC-BB-026 - Personal and open

- **Feature/Requirement:** R-08
- **Technique/Test Type:** decision table
- **Objective:** Apply both filters.
- **Preconditions:** Four-task fixture above exists.
- **Test Data:** Category Personal; status Open.
- **Steps:** 1. Set both filters. 2. Submit. 3. Record visible titles.
- **Expected Result:** `Personal open C` only.
- **Automated Actual Result:** Category=Personal, status=open; visible: Personal open C.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-026.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** With Personal + Open selected, the list showed only `Personal open C`, with category Personal and an open-state circle.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-026.png)
- **Defect ID:** —

## TC-BB-027 - all categories and done

- **Feature/Requirement:** R-08
- **Technique/Test Type:** decision table
- **Objective:** Apply status without category restriction.
- **Preconditions:** Four-task fixture above exists.
- **Test Data:** Category All; status Done.
- **Steps:** 1. Set both filters. 2. Submit. 3. Record visible titles.
- **Expected Result:** `Work done B` and `Personal done D` only.
- **Automated Actual Result:** Category=All, status=done; visible: Personal done D, Work done B.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-027.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** All categories + Done showed exactly `Personal Open D` (Personal) and `Work done B` (Work), both visibly complete. The first title differs from planned `Personal done D`; its category and Done state match the decision rule.
- **Planned Manual Executor:** Sathineswary Saravanesvaran
- **Planned Partner/Reviewer:** Ahmad Adam Ali
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [setup-personal-done](evidence/manual_screenshots/TC-BB-027-setup-personal-done.png); [result](evidence/manual_screenshots/TC-BB-027.png)
- **Defect ID:** —

## TC-BB-028 - title search

- **Feature/Requirement:** R-08
- **Technique/Test Type:** EP
- **Objective:** Search title text.
- **Preconditions:** Four-task fixture above exists; clear other filters.
- **Test Data:** Search text `Personal`.
- **Steps:** 1. Enter search text. 2. Submit. 3. Record visible titles.
- **Expected Result:** Both Personal tasks appear; Work tasks do not.
- **Automated Actual Result:** Search Personal returned Personal done D, Personal open C only.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-028.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** With both dropdowns set to All and `Personal` entered in Search title, the list showed exactly `Personal Open D` and `Personal open C`; neither Work task appeared. The first title uses the documented fixture variation.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [setup-all-unfiltered](evidence/manual_screenshots/TC-BB-028-setup-all-unfiltered.png); [setup-personal-category](evidence/manual_screenshots/TC-BB-028-setup-personal-category.png); [setup-all-unfiltered-2](evidence/manual_screenshots/TC-BB-028-setup-all-unfiltered-2.png); [result](evidence/manual_screenshots/TC-BB-028.png)
- **Defect ID:** —

## TC-BB-029 - dashboard counts

- **Feature/Requirement:** R-09
- **Technique/Test Type:** functional
- **Objective:** Compare summary with known task state.
- **Preconditions:** Signed in; use the four-task fixture, with no other tasks in this account; no task has a due date.
- **Test Data:** Two open and two done tasks, both done tasks completed today.
- **Steps:** 1. Open Dashboard. 2. Record all five counters. 3. Compare with task list and dates.
- **Expected Result:** Total 4; Open 2; Overdue 0; Due Soon 0; Completed (last 7 days) 2.
- **Automated Actual Result:** Dashboard counts {"total":4,"open":2,"overdue":0,"soon":0,"completed":2}.
- **Automated Status:** Pass
- **Automated Evidence:** [Screenshot](evidence/browser_screenshots/TC-BB-029.png); raw result in `evidence/browser_results.json`
- **Manual Actual Result:** Dashboard showed Total 4, Open 2, Overdue 0, Due Soon 0, Completed (last 7 days) 2. A read-only database check confirmed four tasks, two open/two done, no due dates, and completion timestamps on 2026-09-30. On 2026-10-01 the completions were from yesterday rather than the planned today, but within the last seven days.
- **Planned Manual Executor:** Wan Qistina
- **Planned Partner/Reviewer:** Gan Jeng Jie
- **Planned Date:** Fri 2026-10-02
- **Manual Status:** Pass
- **Manual Evidence:** [result](evidence/manual_screenshots/TC-BB-029.png)
- **Defect ID:** —
