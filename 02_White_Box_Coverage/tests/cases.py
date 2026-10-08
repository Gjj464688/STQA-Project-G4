"""Specification-based input cases, with stable IDs for the Week 2 repository."""
from datetime import date, datetime, timedelta

TODAY = date(2026, 10, 7)
NOW = datetime(2026, 10, 7, 12, 0, 0)


def case(number, function, args, expected, objective, paths, *, clock=None,
         exception=None, defect=None, basis="Specification"):
    return dict(id=f"TC-WB-{number:03}", function=function, args=args,
                expected=expected, objective=objective, paths=paths, clock=clock,
                exception=exception, defect=defect, basis=basis)


def due(days):
    return (TODAY + timedelta(days=days)).isoformat()


def completed(age):
    return (NOW - age).strftime("%Y-%m-%d %H:%M:%S")


CASES = [
    case(1, "is_valid_password", {"password": None}, False,
         "Reject None", "P1 True -> return False"),
    case(2, "is_valid_password", {"password": 123}, False,
         "Reject an integer", "P1 True -> return False"),
    case(3, "is_valid_password", {"password": ""}, False,
         "Reject an empty string", "P1 False -> length expression False"),
    case(4, "is_valid_password", {"password": "abcdefg"}, False,
         "Reject seven characters", "P1 False -> length expression False"),
    case(5, "is_valid_password", {"password": "abcdefgh"}, True,
         "Accept the stated minimum of eight", "P1 False -> length expression; required True",
         defect="DEF-W1-001"),
    case(6, "is_valid_password", {"password": "abcdefghi"}, True,
         "Accept nine characters", "P1 False -> length expression True"),
    case(7, "is_valid_username", {"username": None}, False,
         "Reject None", "U1 True -> return False"),
    case(8, "is_valid_username", {"username": 123}, False,
         "Reject an integer", "U1 True -> return False"),
    case(9, "is_valid_username", {"username": "ab"}, False,
         "Reject length two", "U1 False -> U2 True (below minimum)"),
    case(10, "is_valid_username", {"username": "abc"}, True,
         "Accept length three", "U1 False -> U2 False -> all valid letters"),
    case(11, "is_valid_username", {"username": "abcdefghijklmnopqrst"}, True,
         "Accept length twenty", "U1 False -> U2 False -> all valid letters"),
    case(12, "is_valid_username", {"username": "abcdefghijklmnopqrstu"}, False,
         "Reject length twenty-one", "U1 False -> U2 True (above maximum)"),
    case(13, "is_valid_username", {"username": "abc_1"}, True,
         "Accept underscore and digit", "U1 False -> U2 False -> character OR takes both alternatives"),
    case(14, "is_valid_username", {"username": "abc-1"}, False,
         "Reject a hyphen", "U1 False -> U2 False -> all stops at invalid character"),
    case(15, "is_valid_username", {"username": "abc 1"}, False,
         "Reject a space", "U1 False -> U2 False -> all stops at invalid character"),
    case(16, "is_valid_username", {"username": ""}, False,
         "Reject an empty username", "U1 False -> U2 True (below minimum)"),
    case(17, "is_valid_username", {"username": "A1b"}, True,
         "Accept uppercase letters and digits", "U1 False -> U2 False -> all valid characters"),
    case(18, "compute_urgency", {"due_date_str": None, "today": TODAY}, "No due date",
         "Handle None due date", "G1 False -> G2 True"),
    case(19, "compute_urgency", {"due_date_str": "", "today": TODAY}, "No due date",
         "Handle empty due date", "G1 False -> G2 True"),
    case(20, "compute_urgency", {"due_date_str": due(-1), "today": TODAY}, "Overdue",
         "Classify yesterday", "G1 False -> G2 False -> G3 True"),
    case(21, "compute_urgency", {"due_date_str": due(0), "today": TODAY}, "Due Today",
         "Classify today per docstring", "G1 False -> G2 False -> G3 True; label mismatch",
         defect="DEF-W1-002"),
    case(22, "compute_urgency", {"due_date_str": due(1), "today": TODAY}, "Due Soon",
         "Classify tomorrow", "G1 False -> G2 False -> G3 False -> G4 True"),
    case(23, "compute_urgency", {"due_date_str": due(2), "today": TODAY}, "Due Soon",
         "Classify two days away", "G1 False -> G2 False -> G3 False -> G4 True"),
    case(24, "compute_urgency", {"due_date_str": due(3), "today": TODAY}, "Upcoming",
         "Classify three days away", "G1 False -> G2 False -> G3 False -> G4 False"),
    case(25, "compute_urgency", {"due_date_str": None}, "No due date",
         "Use default today before no-date return", "G1 True -> G2 True", clock="date"),
    case(26, "compute_urgency", {"due_date_str": due(1)}, "Due Soon",
         "Use default today for dated task", "G1 True -> G2 False -> G3 False -> G4 True", clock="date"),
    case(27, "compute_urgency", {"due_date_str": "not-a-date", "today": TODAY}, None,
         "Characterize malformed date handling", "G1 False -> G2 False -> parser raises",
         exception="ValueError", basis="Characterization; invalid-date policy unspecified"),
    case(28, "compute_urgency", {"due_date_str": "2026-02-30", "today": TODAY}, None,
         "Characterize impossible calendar date", "G1 False -> G2 False -> parser raises",
         exception="ValueError", basis="Characterization; invalid-date policy unspecified"),
    case(29, "completed_in_last_n_days", {"completed_at_str": None, "now": NOW}, False,
         "Handle absent completion", "C1 True -> return False"),
    case(30, "completed_in_last_n_days", {"completed_at_str": "", "now": NOW}, False,
         "Handle empty completion", "C1 True -> return False"),
    case(31, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=1)), "now": NOW}, True,
         "Include a completion one day ago", "C1 False -> C2 False -> age positive and within limit"),
    case(32, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(0)), "now": NOW}, True,
         "Include a completion at the reference instant", "C1 False -> C2 False -> age positive operand False",
         defect="DEF-W2-001", basis="Specification interpretation: within last N days includes now"),
    case(33, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=7)-timedelta(seconds=1)), "now": NOW}, True,
         "Include one second inside seven-day limit", "C1 False -> C2 False -> both age operands True"),
    case(34, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=7)), "now": NOW}, True,
         "Include exactly seven days ago", "C1 False -> C2 False -> day-limit operand False",
         defect="DEF-W2-001"),
    case(35, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=7,seconds=1)), "now": NOW}, False,
         "Exclude one second beyond seven days", "C1 False -> C2 False -> day-limit operand False"),
    case(36, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=8)), "now": NOW}, False,
         "Exclude eight days ago", "C1 False -> C2 False -> day-limit operand False"),
    case(37, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(seconds=-1)), "now": NOW}, False,
         "Exclude a future completion", "C1 False -> C2 False -> age positive operand False",
         basis="Specification interpretation: last N days excludes future timestamps"),
    case(38, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=1))}, True,
         "Exercise default now with a recent completion", "C1 False -> C2 True -> both age operands True", clock="datetime"),
    case(39, "completed_in_last_n_days", {"completed_at_str": completed(timedelta(days=1)), "n": 1, "now": NOW}, True,
         "Include exactly N days when N is one", "C1 False -> C2 False -> day-limit operand False",
         defect="DEF-W2-001"),
    case(40, "completed_in_last_n_days", {"completed_at_str": "not-a-timestamp", "now": NOW}, None,
         "Characterize malformed completion timestamp", "C1 False -> C2 False -> parser raises",
         exception="ValueError", basis="Characterization; invalid-timestamp policy unspecified"),
    case(41, "completed_in_last_n_days", {"completed_at_str": "2026-02-30 12:00:00", "now": NOW}, None,
         "Characterize impossible completion date", "C1 False -> C2 False -> parser raises",
         exception="ValueError", basis="Characterization; invalid-timestamp policy unspecified"),
]

BASELINE_IDS = {"TC-WB-006", "TC-WB-010", "TC-WB-024", "TC-WB-031"}
