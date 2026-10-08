# Week 2 master test-case repository

## Scope, environment and procedure

All 41 cases call the unchanged [helpers.py snapshot](target/helpers.py). Selection rationale, control-flow diagrams, condition analysis, coverage, and defects are in [Week2_Report.md](Week2_Report.md). These are executed unit tests; actual group tester/reviewer identities remain unconfirmed. The agent executed the suites on 2026-10-07. A teammate review is still required before describing this as group-reviewed work.

Common preconditions: Python and the pinned test tools installed; source hash matches [source_manifest.json](evidence/source_manifest.json); no app server or database is needed. Reference date D = 2026-10-07. Reference time T = 2026-10-07 12:00:00. These are fixed test data independent of the computer clock. For tests of omitted clocks, the fixture temporarily supplies that fixed clock in memory and restores the original dependency afterwards.

Common steps for each row: (1) load the preserved helper module; (2) supply the recorded inputs, applying the fixed clock only where indicated; (3) call the named function once; (4) compare the return value or exception type with the expected result; (5) record the actual result and status. Inputs and expectations are defined in [cases.py](tests/cases.py). Every row maps to `tests/test_helpers.py::test_helper_case[<Case ID>]`, implemented in [test_helpers.py](tests/test_helpers.py) with the recording fixture in [conftest.py](tests/conftest.py).

Evidence for every row: [PyTest output](evidence/final_pytest.txt), [structured results](evidence/final_results.json), and [JUnit XML](evidence/final_junit.xml). Baseline cases 006, 010, 024, and 031 were executed separately in [baseline_helpers.py](tests/baseline_helpers.py). The final suite includes those same inputs plus the added cases.

## Expected-result basis and counts

| Basis | Executed | Pass | Fail | Interpretation |
|---|---:|---:|---:|---|
| Explicit helper specification | 35 | 31 | 4 | Failures: 005, 021, 034, 039 |
| Specification interpretation (I) | 2 | 1 | 1 | 032 includes the current instant; 037 excludes future timestamps; confirm these interpretations if needed |
| Robustness characterization (C) | 4 | 4 | 0 | 027, 028, 040, 041 document ValueError propagation; invalid-date policy is unspecified |
| Total | 41 | 36 | 5 | Zero errors, skips, or expected-failure markers |

Characterization passes describe observed behavior and do not establish acceptable user-facing error handling. Decision labels G/P/U/C correspond to the control-flow analysis in the report. Same-line Boolean return expressions are also traced, although coverage.py does not count them as additional `if` branches in this run.

## Password validation

Function: `is_valid_password`.

| Case ID | Objective | Input | Expected | Actual | Status | Target path / condition | Defect |
|---|---|---|---|---|---|---|---|
| TC-WB-001 | Reject None | `password=None` | `False` | `False` | Pass | P1 True -> return False | - |
| TC-WB-002 | Reject an integer | `password=123` | `False` | `False` | Pass | P1 True -> return False | - |
| TC-WB-003 | Reject an empty string | `password=''` | `False` | `False` | Pass | P1 False -> length expression False | - |
| TC-WB-004 | Reject seven characters | `password='abcdefg'` | `False` | `False` | Pass | P1 False -> length expression False | - |
| TC-WB-005 | Accept the stated minimum of eight | `password='abcdefgh'` | `True` | `False` | Fail | P1 False -> length expression; required True | DEF-W1-001 |
| TC-WB-006 | Accept nine characters | `password='abcdefghi'` | `True` | `True` | Pass | P1 False -> length expression True | - |

## Username validation

Function: `is_valid_username`.

| Case ID | Objective | Input | Expected | Actual | Status | Target path / condition | Defect |
|---|---|---|---|---|---|---|---|
| TC-WB-007 | Reject None | `username=None` | `False` | `False` | Pass | U1 True -> return False | - |
| TC-WB-008 | Reject an integer | `username=123` | `False` | `False` | Pass | U1 True -> return False | - |
| TC-WB-009 | Reject length two | `username='ab'` | `False` | `False` | Pass | U1 False -> U2 True (below minimum) | - |
| TC-WB-010 | Accept length three | `username='abc'` | `True` | `True` | Pass | U1 False -> U2 False -> all valid letters | - |
| TC-WB-011 | Accept length twenty | `username='abcdefghijklmnopqrst'` | `True` | `True` | Pass | U1 False -> U2 False -> all valid letters | - |
| TC-WB-012 | Reject length twenty-one | `username='abcdefghijklmnopqrstu'` | `False` | `False` | Pass | U1 False -> U2 True (above maximum) | - |
| TC-WB-013 | Accept underscore and digit | `username='abc_1'` | `True` | `True` | Pass | U1 False -> U2 False -> character OR takes both alternatives | - |
| TC-WB-014 | Reject a hyphen | `username='abc-1'` | `False` | `False` | Pass | U1 False -> U2 False -> all stops at invalid character | - |
| TC-WB-015 | Reject a space | `username='abc 1'` | `False` | `False` | Pass | U1 False -> U2 False -> all stops at invalid character | - |
| TC-WB-016 | Reject an empty username | `username=''` | `False` | `False` | Pass | U1 False -> U2 True (below minimum) | - |
| TC-WB-017 | Accept uppercase letters and digits | `username='A1b'` | `True` | `True` | Pass | U1 False -> U2 False -> all valid characters | - |

## Urgency classification

Function: `compute_urgency`.

| Case ID | Objective | Input | Expected | Actual | Status | Target path / condition | Defect |
|---|---|---|---|---|---|---|---|
| TC-WB-018 | Handle None due date | `due_date_str=None, today=2026-10-07` | `'No due date'` | `'No due date'` | Pass | G1 False -> G2 True | - |
| TC-WB-019 | Handle empty due date | `due_date_str='', today=2026-10-07` | `'No due date'` | `'No due date'` | Pass | G1 False -> G2 True | - |
| TC-WB-020 | Classify yesterday | `due_date_str='2026-10-06', today=2026-10-07` | `'Overdue'` | `'Overdue'` | Pass | G1 False -> G2 False -> G3 True | - |
| TC-WB-021 | Classify today per docstring | `due_date_str='2026-10-07', today=2026-10-07` | `'Due Today'` | `'Overdue'` | Fail | G1 False -> G2 False -> G3 True; label mismatch | DEF-W1-002 |
| TC-WB-022 | Classify tomorrow | `due_date_str='2026-10-08', today=2026-10-07` | `'Due Soon'` | `'Due Soon'` | Pass | G1 False -> G2 False -> G3 False -> G4 True | - |
| TC-WB-023 | Classify two days away | `due_date_str='2026-10-09', today=2026-10-07` | `'Due Soon'` | `'Due Soon'` | Pass | G1 False -> G2 False -> G3 False -> G4 True | - |
| TC-WB-024 | Classify three days away | `due_date_str='2026-10-10', today=2026-10-07` | `'Upcoming'` | `'Upcoming'` | Pass | G1 False -> G2 False -> G3 False -> G4 False | - |
| TC-WB-025 | Use default today before no-date return | `due_date_str=None; frozen date default` | `'No due date'` | `'No due date'` | Pass | G1 True -> G2 True | - |
| TC-WB-026 | Use default today for dated task | `due_date_str='2026-10-08'; frozen date default` | `'Due Soon'` | `'Due Soon'` | Pass | G1 True -> G2 False -> G3 False -> G4 True | - |
| TC-WB-027 | Characterize malformed date handling | `due_date_str='not-a-date', today=2026-10-07` | `ValueError` [C] | `ValueError` | Pass | G1 False -> G2 False -> parser raises | - |
| TC-WB-028 | Characterize impossible calendar date | `due_date_str='2026-02-30', today=2026-10-07` | `ValueError` [C] | `ValueError` | Pass | G1 False -> G2 False -> parser raises | - |

## Recent completion window

Function: `completed_in_last_n_days`.

| Case ID | Objective | Input | Expected | Actual | Status | Target path / condition | Defect |
|---|---|---|---|---|---|---|---|
| TC-WB-029 | Handle absent completion | `completed_at_str=None, now=2026-10-07 12:00:00` | `False` | `False` | Pass | C1 True -> return False | - |
| TC-WB-030 | Handle empty completion | `completed_at_str='', now=2026-10-07 12:00:00` | `False` | `False` | Pass | C1 True -> return False | - |
| TC-WB-031 | Include a completion one day ago | `completed_at_str='2026-10-06 12:00:00', now=2026-10-07 12:00:00` | `True` | `True` | Pass | C1 False -> C2 False -> age positive and within limit | - |
| TC-WB-032 | Include a completion at the reference instant | `completed_at_str='2026-10-07 12:00:00', now=2026-10-07 12:00:00` | `True` [I] | `False` | Fail | C1 False -> C2 False -> age positive operand False | DEF-W2-001 |
| TC-WB-033 | Include one second inside seven-day limit | `completed_at_str='2026-09-30 12:00:01', now=2026-10-07 12:00:00` | `True` | `True` | Pass | C1 False -> C2 False -> both age operands True | - |
| TC-WB-034 | Include exactly seven days ago | `completed_at_str='2026-09-30 12:00:00', now=2026-10-07 12:00:00` | `True` | `False` | Fail | C1 False -> C2 False -> day-limit operand False | DEF-W2-001 |
| TC-WB-035 | Exclude one second beyond seven days | `completed_at_str='2026-09-30 11:59:59', now=2026-10-07 12:00:00` | `False` | `False` | Pass | C1 False -> C2 False -> day-limit operand False | - |
| TC-WB-036 | Exclude eight days ago | `completed_at_str='2026-09-29 12:00:00', now=2026-10-07 12:00:00` | `False` | `False` | Pass | C1 False -> C2 False -> day-limit operand False | - |
| TC-WB-037 | Exclude a future completion | `completed_at_str='2026-10-07 12:00:01', now=2026-10-07 12:00:00` | `False` [I] | `False` | Pass | C1 False -> C2 False -> age positive operand False | - |
| TC-WB-038 | Exercise default now with a recent completion | `completed_at_str='2026-10-06 12:00:00'; frozen datetime default` | `True` | `True` | Pass | C1 False -> C2 True -> both age operands True | - |
| TC-WB-039 | Include exactly N days when N is one | `completed_at_str='2026-10-06 12:00:00', n=1, now=2026-10-07 12:00:00` | `True` | `False` | Fail | C1 False -> C2 False -> day-limit operand False | DEF-W2-001 |
| TC-WB-040 | Characterize malformed completion timestamp | `completed_at_str='not-a-timestamp', now=2026-10-07 12:00:00` | `ValueError` [C] | `ValueError` | Pass | C1 False -> C2 False -> parser raises | - |
| TC-WB-041 | Characterize impossible completion date | `completed_at_str='2026-02-30 12:00:00', now=2026-10-07 12:00:00` | `ValueError` [C] | `ValueError` | Pass | C1 False -> C2 False -> parser raises | - |

## Defect and requirement links

- R-01 registration: 001-017. TC-WB-005 reproduces [DEF-W1-001](../01_Black_Box/Defect_Log.md#def-w1-001---exactly-8-characters-rejected-as-a-password).
- R-07 urgency: 018-028. TC-WB-021 reproduces [DEF-W1-002](../01_Black_Box/Defect_Log.md#def-w1-002---due-today-task-marked-overdue).
- R-09 dashboard recent completions: 029-041. TC-WB-034 and 039 confirm DEF-W2-001 in the [Week 2 report](Week2_Report.md#new-defect-def-w2-001). TC-WB-032 is an associated zero-age observation with an interpreted expectation.

The tests exercise helper logic only. Dashboard rendering, Flask integration, APIs, and account ownership are outside this coverage denominator. The original Week 1 counts remain unchanged.
