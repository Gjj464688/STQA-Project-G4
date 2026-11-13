# Week 4 web and API assessment

## Scope and conclusion

The scoped Week 4 cases, reproducible execution, comparison records, and defect documentation are complete. The supplied application remains unchanged. Current results come from a dated independent verification on **2026-11-12**, not reconstruction of a missing historical test file.

| Execution | Planned / executed | Pass | Fail | Error / Blocked / Not Run |
|---|---:|---:|---:|---|
| Browser web checks, WEB-01 to WEB-20 | 20 / 20 | 18 | 2 | 0 |
| Isolated API checks, API-01 to API-53 | 53 / 53 | 36 | 17 | 0 |

The 17 API failures comprise five failures against ownership/robustness expectations and twelve failures against explicitly unconfirmed validation/design assumptions. They do not represent seventeen distinct confirmed defects. WEB-02 is an unconfirmed uniqueness expectation; WEB-05 reproduces the confirmed password defect DEF-W1-001. Failed assertions remain visible.

## Environment and source identity

Python 3.12.14; Flask 3.0.3; pytest 9.1.1; Windows 11 build 26200. Exact versions, timestamps, loaded source folder and source hashes are in [api_results.json](Evidence/verified/api_results.json). App SHA-256: `050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f`, matching the unchanged Week 1/2 target. API tests use a new temporary SQLite database per case. Browser checks use Edge 157.0.4341.42, 1280 x 900 CSS pixels, a dedicated account and a disposable database on localhost port 5014. No ordinary application database is used.

Executor: agent-executed verification. Original manual tester identity/date and the historical Python 3.14.8 environment were not independently established. They are not relabelled as this run's environment. Authentication uses session cookies; the API client fixture registers qa_user with dummy TestPass123 credentials; ownership checks create a second independent session.

## Repositories and traceability

| Artifact | Purpose |
|---|---|
| [Web scenarios](Web_Test_Scenarios.xlsx) | Twenty original web designs with freshly observed results and screenshot links |
| [API suite](API_Test_Suite.xlsx) | Fifty-three case IDs, exact executable node IDs, expectations, actuals, basis and defect links |
| [API data](API_Request_Test_Data.xlsx) | Exact ordered request data for the verification suite |
| [Expected versus actual](Expected_vs_Actual.xlsx) | Status/body comparisons for all current API and web cases |
| [test_api.py](tests/test_api.py), [fixtures](tests/conftest.py) | Executable API assertions and fresh database setup |
| [Full API log](Evidence/verified/api_pytest.txt), [JUnit](Evidence/verified/api_junit.xml) | Complete 53-case execution and ordinary failing assertions |
| [API results](Evidence/verified/api_results.json), [route map](Evidence/verified/route_map.json) | Machine-readable requests/responses, propagated exceptions, source identity and actual registered routes |
| [Web results](Evidence/verified/browser_results.json) | Twenty browser results and screenshot references |

IDs API-01 to API-36 retain the original scenario numbering. API-37 to API-53 make the original manual follow-ups and cross-user GET/PUT cases reproducible. The newly supplied executable file was authored for this verification; it is not falsely represented as the missing original tests/test_api.py. The original 27 manual request records and original workbook contents are preserved in [original_records.json](Evidence/original_records.json). They are not counted as additional current automated executions.

### Resolving the earlier inconsistencies

The registered [route map](Evidence/verified/route_map.json) contains DELETE `/api/tasks/<int:task_id>`. API-24 now verifies successful deletion. The earlier 405 screenshots have unverified source/import provenance and are retained as legacy evidence only; they do not establish that DELETE is missing from this supplied app. The reason for the historical mismatch is unknown.

The former API-OBS-04_Invalid_Description image actually shows update-title failures. It is retained as `Evidence/API-OBS-04_Actually_Update_Title_Legacy.png`, with no claim that it evidences description validation. Description cases now have exact recorded API responses. The earlier web duplicate-username Pass is superseded: WEB-02 observes duplicate acceptance and fails the original uniqueness assumption. A uniqueness requirement has not been confirmed.

The legacy password alias WEB-DEF-01 maps to **DEF-W1-001**. It is not a new defect. Original Week 1 findings remain open; an independent reproduction does not imply the app was fixed or regressed.

## UI and server comparison

| Concern | UI evidence | API evidence | Interpretation |
|---|---|---|---|
| Empty task title | Week 3 GUI-TC-001 native validation blocks empty form | API-09/22/23 reject missing/null/whitespace title with 400 | Client and API creation validation both checked; UI server-side whitespace behaviour was a separate Week 1 finding |
| Duplicate username | WEB-02 accepts duplicate registration | API-37 accepts duplicate registration | Consistent observed acceptance; uniqueness policy remains unconfirmed |
| Password minimum | WEB-05 rejects exactly 8 characters; WEB-06 accepts 9 | Registration API negative/positive cases check invalid/valid examples; Week 1/2 already reproduce the exact boundary | DEF-W1-001 is linked across phases |
| Ownership | WEB-20 redirects another user away from edit page | API-52/53 deny other-user GET/PUT; API-25 allows other-user deletion | UI/GET/PUT protection does not establish DELETE protection; DEF-W1-003 reproduced |
| Deletion | WEB-15 uses confirmation and removes selected task | API-24 deletes; API-26 returns 200 for missing task | Missing-task 404 expectation is an assumption about deletion semantics, separate from the confirmed ownership defect |

Flask TESTING=True propagates AttributeError, IntegrityError and ValueError into the client. These are recorded as exceptions, not invented HTTP 500 responses. The suite is an in-process endpoint test; it does not measure real network transport or server performance.

## Defects and recommendations

### Existing DEF-W1-003 Cross-user task deletion

- Feature / requirement: API task ownership, R-03/R-05/R-10/R-12; API-25.
- Preconditions: account A owns a task; account B has an independent authenticated session.
- Steps: (1) Create a task as A. (2) Register/sign in as B. (3) DELETE A's captured task ID. (4) Inspect whether A's row remains.
- Expected: request denied and A's task preserved. The test asserts 404; preservation is the essential ownership requirement.
- Actual: HTTP 200 and A's task row is deleted; owner_record_exists is false in the structured result.
- Severity / priority / status: Major / High / Confirmed, open; canonical record remains in [Week 1 defect log](../01_Black_Box/Defect_Log.md).
- Evidence: API-25 in JSON/log/JUnit. Recommendation: maintainer should scope DELETE to authenticated owner and retest both owners. No application fix applied.

### DEF-W4-001 Integer task title causes an unhandled exception

- Feature / requirement: API creation validation, R-04/R-10; API-32.
- Preconditions: authenticated client, fresh database, TESTING=True.
- Steps: POST `/api/tasks` with `{"title":123}`.
- Expected: controlled client-error response for an invalid title type; test uses 400 as the proposed response.
- Actual: AttributeError because integer title has no strip method; no normal response is returned to the test client.
- Severity / priority / status: Moderate / Medium / Confirmed robustness defect, open.
- Evidence: API-32 JSON/log/JUnit; app.py line 405. Recommendation: maintainer should validate input type before string operations.

### DEF-W4-002 Null update title causes a database constraint exception

- Feature / requirement: API update validation, R-05/R-10; API-42.
- Preconditions: authenticated owner and existing valid task.
- Steps: (1) Create a valid task. (2) PUT its ID with `{"title":null}`.
- Expected: controlled validation rejection without an unhandled database exception; test uses 400 as proposed response.
- Actual: sqlite3.IntegrityError, NOT NULL constraint failed: tasks.title.
- Severity / priority / status: Moderate / Medium / Confirmed robustness defect, open.
- Evidence: API-42 JSON/log/JUnit. Recommendation: maintainer should reject null titles before database updates and preserve valid state.

### DEF-W4-003 Invalid due date persists and prevents task listing

- Feature / requirement: API creation and listing, R-04/R-10; API-49/50.
- Preconditions: authenticated client; fresh temporary database for each case.
- Steps: (1) POST `/api/tasks` with `{"title":"Invalid Date Test","due_date":"not-a-date"}`. (2) Inspect database for the invalid date. (3) GET `/api/tasks`.
- Expected: invalid date rejected before insertion; task listing remains available. Proposed creation response is 400; listing should return a JSON list with 200.
- Actual: POST commits the invalid record, then urgency parsing raises ValueError. The record count for invalid dates is 1. Subsequent GET raises ValueError too.
- Severity / priority / status: Major / High / Confirmed at isolated API level, open.
- Evidence: API-49/50 JSON/log/JUnit, including invalid_record_persisted. Recommendation: maintainer should validate dates before commit and verify failed creation leaves no invalid record.

### Assumptions and observations

The twelve assumption failures cover missing-task DELETE status, invalid/negative/zero/large pagination policy, numeric/null optional descriptions, numeric update titles and preservation, and empty/whitespace update titles. Their asserted policies are visible in the workbook and test file. Confirm these policies before reporting additional product defects. Characterization cases intentionally record duplicate acceptance, invalid path IDs and generic malformed/content-type rejection without claiming those behaviours fully satisfy an unspecified contract. Keep assertion outcomes distinct from defect classifications.

## Reproduction

Place the original supplied `pytodo_pro_student` folder beside the cloned repository. From the repository root, resolve that sibling folder and run the tests below. If your app is elsewhere, set `PYTODO_SOURCE_DIR` to that folder instead:

```powershell
$env:PYTODO_SOURCE_DIR = (Resolve-Path '..\pytodo_pro_student').Path
python -m pip install -r .\04_Web_API\requirements-test.txt
python .\04_Web_API\run_api_tests.py
```

Expected assertion outcome against the recorded source: 36 Pass, 17 Fail, 0 setup errors. Exit code 1 records failing assertions; inspect errors rather than treating all nonzero exits as product defects. The runner checks the original app hash before import and source hashes after execution. It replaces current API evidence, so archive saved evidence before a new run.

For the web checks, use [Week 3 browser instructions](../03_GUI_Compatibility_Usability_Accessibility/Week3_Report.md#reproduction-and-evidence); that runner emits WEB-01 to WEB-20 evidence here. Current browser outcomes are 18 Pass/2 Fail.

The brief's web scenarios, API suite, requests/data, expected-versus-actual status/body comparisons, and execution evidence/defects are present. Selected missing/invalid inputs, types, dates, methods, pagination and owner boundaries are covered. This does not establish exhaustive endpoint, category-type, payload-size, Unicode, security, performance or network coverage. Broader security/performance belong to later phases.
