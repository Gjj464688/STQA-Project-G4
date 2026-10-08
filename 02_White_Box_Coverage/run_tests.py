"""Run baseline/final PyTest suites in fresh processes and save real coverage."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ResultRecorder:
    def __init__(self):
        self.results = []

    def pytest_runtest_logreport(self, report):
        # A failed setup is an execution problem, not a functional result.
        if report.when == "setup" and report.failed:
            self.results.append(dict(node_id=report.nodeid, status="Error",
                                     detail=str(report.longrepr)))

    def pytest_runtest_makereport(self, item, call):
        if call.when != "call":
            return
        result = getattr(item, "week2_result", dict(case_id=item.nodeid))
        result = dict(result, node_id=item.nodeid,
                      status="Fail" if call.excinfo else "Pass")
        self.results.append(result)


def run_phase(phase):
    import coverage
    import pytest

    os.chdir(ROOT)
    EVIDENCE.mkdir(exist_ok=True)
    manifest = json.loads((EVIDENCE / "source_manifest.json").read_text())
    target = ROOT / "target" / "helpers.py"
    expected_hash = manifest["helpers_sha256"]
    if sha256(target) != expected_hash:
        raise RuntimeError("Source snapshot differs from its recorded original hash")

    cov = coverage.Coverage(config_file=str(ROOT / ".coveragerc"),
                            data_file=str(EVIDENCE / f".coverage.{phase}"))
    recorder = ResultRecorder()
    started = datetime.now(timezone.utc).isoformat()
    target_test = "tests/baseline_helpers.py" if phase == "baseline" else "tests/test_helpers.py"
    cov.start()
    try:
        status = pytest.main([target_test, "-v", "--tb=short",
                              f"--junitxml=evidence/{phase}_junit.xml"], plugins=[recorder])
    finally:
        cov.stop()
        cov.save()
    with (EVIDENCE / f"{phase}_coverage.txt").open("w", encoding="utf-8") as stream:
        cov.report(file=stream)
    cov.json_report(outfile=str(EVIDENCE / f"{phase}_coverage.json"))
    cov.xml_report(outfile=str(EVIDENCE / f"{phase}_coverage.xml"))
    html_directory = EVIDENCE / f"{phase}_html"
    cov.html_report(directory=str(html_directory))
    # Coverage creates an ignore-all file; retain the report as submission evidence.
    generated_ignore = html_directory / ".gitignore"
    if generated_ignore.is_file():
        generated_ignore.unlink()
    summary = dict(
        phase=phase, started_utc=started, python=platform.python_version(),
        platform=platform.platform(), pytest=pytest.__version__, coverage=coverage.__version__,
        source_sha256=sha256(target), pytest_exit_code=int(status),
        counts={key: sum(r["status"] == key for r in recorder.results)
                for key in ["Pass", "Fail", "Error"]},
        results=recorder.results,
    )
    if summary["source_sha256"] != expected_hash:
        raise RuntimeError("Source snapshot changed during tests")
    (EVIDENCE / f"{phase}_results.json").write_text(
        json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print("RECORDED SUMMARY:", json.dumps(summary["counts"]))
    print("PyTest exit code:", int(status), "(1 means assertion failures are recorded)")
    return int(status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["baseline", "final"])
    args = parser.parse_args()
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    if args.phase:
        return run_phase(args.phase)
    EVIDENCE.mkdir(exist_ok=True)
    final_status = 0
    for phase in ["baseline", "final"]:
        log_path = EVIDENCE / f"{phase}_pytest.txt"
        with log_path.open("w", encoding="utf-8") as log:
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                     "--phase", phase], cwd=ROOT, stdout=log,
                                    stderr=subprocess.STDOUT)
        print(log_path.read_text(encoding="utf-8"))
        if result.returncode not in [0, 1]:
            return result.returncode
        if phase == "baseline" and result.returncode:
            return result.returncode
        final_status = result.returncode
    return final_status


if __name__ == "__main__":
    sys.exit(main())
