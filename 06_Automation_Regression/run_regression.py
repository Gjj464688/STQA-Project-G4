"""Run the PyTodo Pro regression suite and save evidence in one step.

Examples (PowerShell, from this folder):
    python run_regression.py                      # full suite, all four layers
    python run_regression.py --suite smoke        # fast smoke subset
    python run_regression.py --skip-ui            # no browser (unit, API, web)
    python run_regression.py --browser edge --label "Ahmad PC run 2"

Each run creates a new folder evidence/<date-time>_<suite>[_label]/ with:
    console.log     everything printed by PyTest
    junit.xml       machine-readable results (for CI tools)
    report.html     readable report with screenshots of the browser tests
    results.jsonl   one line per test, with its AUTO/manual/requirement links
    results.md      the same results as a table for the Week 6 report
    summary.json    counts, verdict, environment and app file hashes
    screenshots/    one image per browser test
Earlier runs are never overwritten.

Result meanings:
    PASS / FAIL   ordinary test outcome
    XFAIL         a known open defect was observed again (expected)
    XPASS         a known-defect test passed: the defect may be fixed, so
                  retest it and update the defect log (counts as a failure)
"""
import argparse
import importlib.metadata as metadata
import json
import os
import platform
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from conftest import APP_DIR, app_version_info  # noqa: E402


def package_version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def build_marker_expression(suite, skip_ui):
    parts = []
    if suite == "smoke":
        parts.append("smoke")
    if skip_ui:
        parts.append("not ui")
    return " and ".join(parts)


def run_pytest(args, evidence, env):
    command = [sys.executable, "-m", "pytest", "-p", "no:logging",
               f"--junitxml={evidence / 'junit.xml'}",
               f"--html={evidence / 'report.html'}", "--self-contained-html"]
    if args.marker:
        command += ["-m", args.marker]
    print("Running:", " ".join(command), flush=True)
    with open(evidence / "console.log", "w", encoding="utf-8") as log:
        process = subprocess.Popen(command, cwd=HERE, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        for line in process.stdout:
            print(line, end="")
            log.write(line)
        return process.wait()


def load_results(evidence):
    path = evidence / "results.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_results_table(evidence, results):
    lines = ["| AUTO ID | Layer | Smoke | Manual case(s) | Requirement(s) | Known defect | Result | Time (s) |",
             "|---|---|---|---|---|---|---|---:|"]
    for r in sorted(results, key=lambda r: (r["layer"] or "", r["auto_id"] or r["nodeid"])):
        lines.append("| {auto} | {layer} | {smoke} | {manual} | {req} | {defect} | {result} | {time:.3f} |".format(
            auto=r["auto_id"] or r["nodeid"], layer=r["layer"], smoke="Yes" if r["smoke"] else "",
            manual=", ".join(r["manual"]) or "-", req=", ".join(r["req"]) or "-",
            defect=r["known_defect"] or "", result=r["result"], time=r["duration_s"]))
    (evidence / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--suite", choices=["smoke", "full"], default="full")
    parser.add_argument("--skip-ui", action="store_true", help="skip the Selenium browser layer")
    parser.add_argument("--browser", choices=["chrome", "edge"], default="chrome")
    parser.add_argument("--headed", action="store_true", help="show the browser window")
    parser.add_argument("--label", default="", help="short note saved with the run, e.g. who ran it")
    args = parser.parse_args()
    args.marker = build_marker_expression(args.suite, args.skip_ui)

    started = datetime.now().astimezone()
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", args.label).strip("-")
    name = f"{started:%Y%m%d-%H%M%S}_{args.suite}{'_noui' if args.skip_ui else ''}{'_' + slug if slug else ''}"
    evidence = HERE / "evidence" / name
    evidence.mkdir(parents=True)

    env = dict(os.environ, REGRESSION_EVIDENCE_DIR=str(evidence), PYTODO_BROWSER=args.browser,
               PYTODO_SOURCE_DIR=str(APP_DIR))
    if args.headed:
        env["PYTODO_HEADED"] = "1"

    exit_code = run_pytest(args, evidence, env)
    finished = datetime.now().astimezone()
    results = load_results(evidence)
    write_results_table(evidence, results)

    counts = Counter(r["result"] for r in results)
    by_layer = {}
    for r in results:
        by_layer.setdefault(r["layer"], Counter())[r["result"]] += 1
    new_failures = [r for r in results if r["result"] in ("FAIL", "ERROR")]
    maybe_fixed = [r for r in results if r["result"] == "XPASS"]
    confirmed = sorted({r["known_defect"] for r in results if r["result"] == "XFAIL"})

    if new_failures or maybe_fixed:
        verdict = "ATTENTION"
    elif results:
        verdict = "PASSED (no new failures)"
    else:
        verdict = "NOT RUN"

    browser_file = evidence / "browser.json"
    summary = {
        "label": args.label, "suite": args.suite, "ui_included": not args.skip_ui,
        "marker_expression": args.marker or "(all tests)",
        "started": started.isoformat(timespec="seconds"), "finished": finished.isoformat(timespec="seconds"),
        "duration_s": round((finished - started).total_seconds(), 1),
        "pytest_exit_code": exit_code, "verdict": verdict,
        "counts": dict(counts), "total": len(results),
        "counts_by_layer": {k: dict(v) for k, v in by_layer.items()},
        "known_defects_still_present": confirmed,
        "new_failures": [{"test": r["auto_id"] or r["nodeid"], "message": r.get("message")} for r in new_failures],
        "known_defect_tests_now_passing": [{"test": r["auto_id"], "defect": r["known_defect"]} for r in maybe_fixed],
        "environment": {
            "os": platform.platform(), "python": platform.python_version(),
            "pytest": package_version("pytest"), "selenium": package_version("selenium"),
            "flask": package_version("flask"), "werkzeug": package_version("werkzeug"),
            "browser": json.loads(browser_file.read_text()) if browser_file.exists() else None,
            "timezone": str(started.tzinfo), "utc_offset": started.strftime("%z"),
        },
        "app_under_test": app_version_info(),
    }
    (evidence / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print(f"Regression {args.suite} run: {verdict}")
    print("Results: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f" (total {len(results)})")
    print("Known defects still present: " + (", ".join(confirmed) or "none"))
    for r in new_failures:
        print(f"  NEW FAILURE: {r['auto_id'] or r['nodeid']}: {r.get('message')}")
    for r in maybe_fixed:
        print(f"  POSSIBLY FIXED: {r['auto_id']} ({r['known_defect']}) passed - retest and update the defect log")
    if not summary["app_under_test"]["matches_week1_baseline"]:
        print("  NOTE: app files differ from the Week 1/2 baseline hashes (a changed version is being tested).")
    print(f"Evidence saved in: {evidence}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
