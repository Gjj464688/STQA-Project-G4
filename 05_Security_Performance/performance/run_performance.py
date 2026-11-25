r"""Week 5 performance test: one command runs every load level and analyses it.

Examples (PowerShell, in this folder):
    python run_performance.py --quick                  # 2-minute setup check
    python run_performance.py --label "Ahmad-PC"       # full experiment (about 50 min)
    python run_performance.py --analyse ..\evidence\perf_<folder>   # redo tables/charts only

What one full run does:
  * For each load level (default 1, 5, 10, 25, 50, 100, 200, 400, 800 virtual users) and
    each repeat (default 3): start a fresh isolated server with an empty
    database (run_perf_server.py, port 5015), run the JMeter plan
    (pytodo_load_test.jmx) in non-GUI mode, then stop the server.
  * Recovery check: on one server, run the highest level and then 1 user
    straight after, to see whether response times return to normal.
  * Analyse: only the steady-state window is measured (ramp-up excluded);
    registration (once per user, deliberately slow password hashing) is
    reported separately from the page/API workload.

Everything is saved in ..\evidence\perf_<date-time>_<label>\ :
    results.md            tables for the report (by load level, by page, per run)
    summary_by_level.csv, summary_by_page.csv, summary_by_run.csv
    charts\               response time, throughput and error rate vs users
    environment.json      computer, versions, app hashes, workload settings
    runs\*.jtl.gz         raw JMeter results (CSV, gzip) for every run
    runs\*_server_errors.txt  exception summary, only for runs where the server logged errors
"""
import argparse
import csv
import gzip
import hashlib
import json
import math
import os
import platform
import shutil
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = HERE / "pytodo_load_test.jmx"
SERVER = HERE / "run_perf_server.py"
EVIDENCE = HERE.parent / "evidence"
REGISTER_LABEL = "01 Register (once per user)"

# Proposed targets, fixed BEFORE execution (the brief gives none).
TARGET_P95_MS = 1000
TARGET_ERROR_PCT = 1.0
EXPECTED_LOAD_MAX_USERS = 25  # levels up to this are the "load test"; above = "stress test"


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

def find_jmeter(explicit):
    names = ["jmeter.bat"] if os.name == "nt" else ["jmeter"]
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("JMETER_HOME"):
        candidates.append(Path(os.environ["JMETER_HOME"]) / "bin")
    for base in (HERE.parents[2], Path.home() / "Downloads", Path.home()):
        candidates += sorted(base.glob("apache-jmeter-*/bin"), reverse=True)
        candidates += sorted(base.glob("apache-jmeter-*/apache-jmeter-*/bin"), reverse=True)
    for folder in candidates:
        if folder.is_file():
            return folder
        for name in names:
            if (folder / name).exists():
                return folder / name
    found = shutil.which(names[0])
    if found:
        return Path(found)
    raise SystemExit("JMeter not found. Extract apache-jmeter-5.6.3.zip into Downloads, "
                     "or pass --jmeter C:\\path\\to\\apache-jmeter-5.6.3\\bin\\jmeter.bat")


def run_quiet(command):
    try:
        out = subprocess.run(command, capture_output=True, text=True, timeout=60)
        return (out.stdout + out.stderr).strip()
    except Exception as error:  # noqa: BLE001 - environment info is best effort
        return f"unavailable ({error})"


def cpu_name():
    if os.name == "nt":
        name = run_quiet(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).Name"])
        return name.splitlines()[0] if name else platform.processor()
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def ram_gb():
    try:
        if os.name == "nt":
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return round(status.ullTotalPhys / 1024 ** 3, 1)
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                return round(int(line.split()[1]) / 1024 ** 2, 1)
    except Exception:  # noqa: BLE001
        pass
    return None


def package_version(name):
    from importlib import metadata
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def source_dir():
    value = os.environ.get("PYTODO_SOURCE_DIR") or os.environ.get("PYTODO_APP_DIR") or HERE.parents[2] / "pytodo_pro_student"
    return Path(value).resolve()


def environment(jmeter, settings):
    src = source_dir()
    java = run_quiet(["java", "-version"]).splitlines()
    java = next((l for l in java if "version" in l), java[0] if java else "unknown")
    return {
        "computer": {"os": platform.platform(), "cpu": cpu_name(), "logical_cpus": os.cpu_count(), "ram_gb": ram_gb()},
        "software": {"python": platform.python_version(), "flask": package_version("flask"),
                     "werkzeug": package_version("werkzeug"), "jmeter": jmeter.parent.parent.name, "java": java},
        "server": "Flask built-in server, threaded, debug off, 127.0.0.1 (same server type as 'python app.py')",
        "app_under_test": {"source": str(src), **{
            name: hashlib.sha256((src / name).read_bytes()).hexdigest() for name in ("app.py", "helpers.py")}},
        "note": "JMeter and the app run on the same computer and share its CPU.",
        "workload": settings,
    }


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------

def port_free(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def start_server(port, log_path):
    env = dict(os.environ, PERF_PORT=str(port), PYTHONUNBUFFERED="1")
    log = open(log_path, "w", encoding="utf-8")
    process = subprocess.Popen([sys.executable, str(SERVER)], env=env, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(100):
        time.sleep(0.2)
        if process.poll() is not None:
            log.close()
            raise SystemExit(f"Test server stopped at start-up; see {log_path}")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/login", timeout=2) as response:
                if response.status == 200:
                    return process, log
        except OSError:
            continue
    process.terminate()
    raise SystemExit("Test server did not start within 20 s")


def stop_server(process, log):
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    log.close()


def rampup_for(users):
    return max(5, math.ceil(users / 5))


def run_jmeter(jmeter, users, steady, port, jtl, jmeter_log):
    rampup = rampup_for(users)
    command = [str(jmeter), "-n", "-t", str(PLAN), "-l", str(jtl), "-j", str(jmeter_log),
               f"-Jusers={users}", f"-Jrampup={rampup}", f"-Jduration={rampup + steady}",
               f"-Jport={port}", "-Jhost=127.0.0.1",
               "-Jjmeter.save.saveservice.subresults=false", "-Jjmeter.save.saveservice.output_format=csv"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=rampup + steady + 180, check=False)
    return rampup


def one_run(args, jmeter, out, levels_users, tag, results):
    """Fresh server; run one or more levels back to back on it (more than one = recovery check)."""
    server_log = Path(tempfile.gettempdir()) / f"pytodo_perf_server_{os.getpid()}.log"
    process, log = start_server(args.port, server_log)
    try:
        for users, run_id in levels_users:
            jtl = out / "runs" / f"{run_id}.jtl"
            print(f"  {run_id}: {users} user(s) ...", end="", flush=True)
            rampup = run_jmeter(jmeter, users, args.steady, args.port, jtl, out / "runs" / f"{run_id}_jmeter.log")
            results.append({"run_id": run_id, "users": users, "rampup_s": rampup, "steady_s": args.steady,
                            "kind": tag, "jtl": jtl.name + ".gz"})
            stats = analyse_jtl(jtl, rampup, args.steady)
            compress(jtl)
            print(f" median {stats['median_ms']} ms, p95 {stats['p95_ms']} ms, "
                  f"{stats['throughput_rps']} req/s, errors {stats['error_pct']}%")
    finally:
        stop_server(process, log)
    text = server_log.read_text(encoding="utf-8", errors="replace")
    if "Traceback" in text or '" 500 ' in text:
        (out / "runs" / f"{levels_users[0][1]}_server_errors.txt").write_text(summarise_server_errors(text), encoding="utf-8")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def percentile(values, pct):
    if not values:
        return None
    ordered = sorted(values)
    rank = max(0, math.ceil(pct / 100 * len(ordered)) - 1)  # nearest-rank, as JMeter
    return ordered[rank]


def read_jtl(jtl):
    jtl = Path(jtl)
    if not jtl.exists() and Path(str(jtl) + ".gz").exists():
        jtl = Path(str(jtl) + ".gz")
    opener = gzip.open if jtl.suffix == ".gz" else open
    with opener(jtl, "rt", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def compress(jtl):
    """Store raw results as .jtl.gz (about 10x smaller; open with 7-Zip to get the CSV back)."""
    with open(jtl, "rb") as src, gzip.open(str(jtl) + ".gz", "wb") as dst:
        shutil.copyfileobj(src, dst)
    jtl.unlink()


def summarise_server_errors(text):
    """Count exception types and keep the first two tracebacks, instead of the whole server log."""
    lines = text.splitlines()
    counts = {}
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("File ", "Traceback", "^", "~")) and (
                stripped.split(":")[0].endswith(("Error", "Exception")) or stripped.startswith("sqlite3.")):
            key = stripped[:120]
            counts[key] = counts.get(key, 0) + 1
    tracebacks, current = [], None
    for line in lines:
        if line.startswith("Traceback"):
            current = [line]
        elif current is not None:
            current.append(line)
            if line and not line.startswith(" "):
                tracebacks.append("\n".join(current))
                current = None
                if len(tracebacks) == 2:
                    break
    status_500 = sum(1 for line in lines if '" 500 ' in line)
    out = [f"HTTP 500 responses logged: {status_500}", "", "Exception lines (count, text):"]
    out += [f"{n:>7}  {k}" for k, n in sorted(counts.items(), key=lambda kv: -kv[1])]
    out += ["", "First tracebacks:", ""] + tracebacks
    return "\n".join(out) + "\n"


def describe(samples, window_s):
    elapsed = [int(s["elapsed"]) for s in samples]
    errors = sum(1 for s in samples if s["success"] != "true")
    if not samples:
        return {"samples": 0, "avg_ms": None, "median_ms": None, "p90_ms": None, "p95_ms": None,
                "max_ms": None, "throughput_rps": 0.0, "error_pct": 0.0}
    return {
        "samples": len(samples),
        "avg_ms": round(statistics.mean(elapsed)),
        "median_ms": percentile(elapsed, 50),
        "p90_ms": percentile(elapsed, 90),
        "p95_ms": percentile(elapsed, 95),
        "max_ms": max(elapsed),
        "throughput_rps": round(len(samples) / window_s, 1) if window_s else None,
        "error_pct": round(100 * errors / len(samples), 2),
    }


def steady_samples(rows, rampup, steady):
    if not rows:
        return []
    t0 = min(int(r["timeStamp"]) for r in rows)
    start, end = t0 + rampup * 1000, t0 + (rampup + steady) * 1000
    return [r for r in rows if r["label"] != REGISTER_LABEL and start <= int(r["timeStamp"]) < end]


def analyse_jtl(jtl, rampup, steady):
    return describe(steady_samples(read_jtl(jtl), rampup, steady), steady)


def analyse_folder(out):
    meta = json.loads((out / "runs.json").read_text(encoding="utf-8"))
    runs = meta["runs"]
    per_run, per_page, register = [], defaultdict(list), defaultdict(list)
    for run in runs:
        rows = read_jtl(out / "runs" / run["jtl"])
        steady = steady_samples(rows, run["rampup_s"], run["steady_s"])
        stats = describe(steady, run["steady_s"])
        per_run.append({**{k: run[k] for k in ("run_id", "kind", "users", "rampup_s", "steady_s")}, **stats})
        if run["kind"] == "level":
            for label in sorted({s["label"] for s in steady}):
                per_page[(run["users"], label)].append(describe([s for s in steady if s["label"] == label], run["steady_s"]))
            register[run["users"]] += [s for s in rows if s["label"] == REGISTER_LABEL]

    # Average the repeats of each level.
    by_level = []
    for users in sorted({r["users"] for r in per_run if r["kind"] == "level"}):
        reps = [r for r in per_run if r["kind"] == "level" and r["users"] == users]
        mean = lambda key: round(statistics.mean(r[key] for r in reps if r[key] is not None), 1)  # noqa: E731
        p95s = [r["p95_ms"] for r in reps if r["p95_ms"] is not None]
        reg = describe(register[users], None)
        level = {
            "users": users, "test_type": "Load" if users <= EXPECTED_LOAD_MAX_USERS else "Stress",
            "runs": len(reps), "samples": sum(r["samples"] for r in reps),
            "median_ms": mean("median_ms"), "p95_ms": mean("p95_ms"),
            "p95_range_ms": f"{min(p95s)}-{max(p95s)}" if p95s else "-",
            "max_ms": max(r["max_ms"] for r in reps if r["max_ms"] is not None),
            "throughput_rps": mean("throughput_rps"), "error_pct": mean("error_pct"),
            "register_median_ms": reg["median_ms"], "register_p95_ms": reg["p95_ms"],
            "register_error_pct": reg["error_pct"],
        }
        level["meets_targets"] = "Yes" if (level["p95_ms"] <= TARGET_P95_MS and level["error_pct"] <= TARGET_ERROR_PCT) else "No"
        by_level.append(level)

    pages = []
    for (users, label), stats_list in sorted(per_page.items()):
        pages.append({"users": users, "page": label,
                      "median_ms": round(statistics.mean(s["median_ms"] for s in stats_list), 1),
                      "p95_ms": round(statistics.mean(s["p95_ms"] for s in stats_list), 1),
                      "error_pct": round(statistics.mean(s["error_pct"] for s in stats_list), 2)})

    write_csv(out / "summary_by_run.csv", per_run)
    write_csv(out / "summary_by_level.csv", by_level)
    write_csv(out / "summary_by_page.csv", pages)
    write_markdown(out, meta, by_level, pages, per_run)
    draw_charts(out, by_level)
    return by_level


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(out, meta, by_level, pages, per_run):
    env = meta["environment"]
    lines = [f"# Performance results: {out.name}", "",
             f"Computer: {env['computer']['cpu']}, {env['computer']['logical_cpus']} logical CPUs, "
             f"{env['computer']['ram_gb']} GB RAM, {env['computer']['os']}. "
             f"Python {env['software']['python']}, Flask {env['software']['flask']}, {env['software']['jmeter']}, "
             f"Java: {env['software']['java']}.", "",
             f"Each run: {meta['settings']['steady_s']} s measured after ramp-up, fresh server and empty database "
             f"(runs per level in the table). Targets (proposed before execution): "
             f"p95 <= {TARGET_P95_MS} ms and errors <= {TARGET_ERROR_PCT}%.", "",
             "## By load level (page and API requests; registration shown separately)", "",
             "| Users | Type | Runs | Requests measured | Median (ms) | p95 (ms) | p95 range across runs | Max (ms) | Throughput (req/s) | Errors (%) | Meets targets | Register median / p95 (ms) |",
             "|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|"]
    for l in by_level:
        lines.append(f"| {l['users']} | {l['test_type']} | {l['runs']} | {l['samples']} | {l['median_ms']} | {l['p95_ms']} | "
                     f"{l['p95_range_ms']} | {l['max_ms']} | {l['throughput_rps']} | {l['error_pct']} | {l['meets_targets']} | "
                     f"{l['register_median_ms']} / {l['register_p95_ms']} |")
    lines += ["", "## By page (mean of runs)", "", "| Users | Page / request | Median (ms) | p95 (ms) | Errors (%) |", "|---:|---|---:|---:|---:|"]
    lines += [f"| {p['users']} | {p['page']} | {p['median_ms']} | {p['p95_ms']} | {p['error_pct']} |" for p in pages]
    lines += ["", "## Every run", "", "| Run | Kind | Users | Requests | Median (ms) | p95 (ms) | Throughput (req/s) | Errors (%) |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    lines += [f"| {r['run_id']} | {r['kind']} | {r['users']} | {r['samples']} | {r['median_ms']} | {r['p95_ms']} | {r['throughput_rps']} | {r['error_pct']} |" for r in per_run]
    (out / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_charts(out, by_level):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed: skipping charts (pip install matplotlib)")
        return
    folder = out / "charts"
    folder.mkdir(exist_ok=True)
    blue, orange, text, muted, grid = "#257de0", "#f47230", "#191919", "#666666", "#e6e6e6"
    users = [str(l["users"]) for l in by_level]
    x = list(range(len(users)))

    def frame(title, ylabel):
        fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
        ax.set_title(title, loc="left", fontsize=12, color=text, pad=12)
        ax.set_xlabel("Concurrent virtual users", color=muted)
        ax.set_ylabel(ylabel, color=muted)
        ax.set_xticks(x, users)
        ax.grid(axis="y", color=grid, linewidth=1)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        ax.tick_params(colors=muted)
        return fig, ax

    def line(ax, values, color, label, end_label=True):
        ax.plot(x, values, color=color, linewidth=2, solid_capstyle="round", solid_joinstyle="round",
                marker="o", markersize=8, markerfacecolor=color, markeredgecolor="white", markeredgewidth=2, label=label)
        if end_label:
            ax.annotate(f"{label}: {values[-1]:g}", (x[-1], values[-1]), xytext=(8, 0), textcoords="offset points",
                        va="center", fontsize=9, color=text)

    p95 = [l["p95_ms"] for l in by_level]
    median = [l["median_ms"] for l in by_level]
    top = max(p95)
    show_target = top >= 0.3 * TARGET_P95_MS
    fig, ax = frame("Response time as load increases", "Milliseconds")
    ymax = max(top * 1.25, TARGET_P95_MS * 1.1 if show_target else 0, 10)
    # Label line ends only when they are far enough apart not to collide; the legend always names them.
    apart = abs(p95[-1] - median[-1]) > 0.08 * ymax
    line(ax, p95, orange, "p95", end_label=apart)
    line(ax, median, blue, "median", end_label=apart)
    ax.set_ylim(0, ymax)
    if show_target:
        ax.axhline(TARGET_P95_MS, color=muted, linewidth=1)
        ax.annotate(f"p95 target {TARGET_P95_MS} ms", (x[0], TARGET_P95_MS), xytext=(0, 4),
                    textcoords="offset points", ha="left", fontsize=8, color=muted)
    else:
        ax.text(0, 1.0, f"p95 target ({TARGET_P95_MS} ms) is far above every value, so it is not drawn",
                transform=ax.transAxes, fontsize=8, color=muted, va="bottom")
    ax.legend(frameon=False, loc="upper left", labelcolor=text, bbox_to_anchor=(0, 0.95))
    ax.set_xlim(-0.3, len(x) - 0.2 + (0.9 if apart else 0.3))
    fig.tight_layout()
    fig.savefig(folder / "response_time_vs_users.png")
    plt.close(fig)

    fig, ax = frame("Throughput as load increases", "Requests per second")
    line(ax, [l["throughput_rps"] for l in by_level], blue, "req/s")
    ax.set_xlim(-0.3, len(x) - 0.2 + 0.9)
    fig.tight_layout()
    fig.savefig(folder / "throughput_vs_users.png")
    plt.close(fig)

    fig, ax = frame("Error rate as load increases", "Errors (% of requests)")
    errors = [l["error_pct"] for l in by_level]
    bars = ax.bar(x, errors, width=0.22, color=blue)
    for bar, value in zip(bars, errors):
        if value > 0:  # label only the bars that have errors; zero bars are explained below the title
            ax.annotate(f"{value:g}%", (bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=8, color=text)
    ax.axhline(TARGET_ERROR_PCT, color=muted, linewidth=1)
    top = max(max(errors) * 1.25, TARGET_ERROR_PCT * 3)
    ax.set_ylim(0, top)
    ax.annotate(f"target {TARGET_ERROR_PCT:g}%", (x[0], TARGET_ERROR_PCT), xytext=(0, 3),
                textcoords="offset points", ha="left", fontsize=8, color=muted)
    zero = [users[i] for i, v in enumerate(errors) if v == 0]
    if zero:
        ax.text(0, 1.0, f"0% errors at {', '.join(zero)} users", transform=ax.transAxes,
                fontsize=8, color=muted, va="bottom")
    fig.tight_layout()
    fig.savefig(folder / "error_rate_vs_users.png")
    plt.close(fig)


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--levels", default="1,5,10,25,50,100,200,400,800", help="comma-separated virtual-user counts")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--steady", type=int, default=60, help="seconds measured after ramp-up, per run")
    parser.add_argument("--no-recovery", action="store_true", help="skip the recovery check")
    parser.add_argument("--quick", action="store_true", help="setup check: 1 and 5 users, 1 run, 20 s")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PERF_PORT", "5015")))
    parser.add_argument("--jmeter", help="path to jmeter.bat (Windows) or jmeter")
    parser.add_argument("--label", default="", help="who ran it / which computer")
    parser.add_argument("--analyse", help="re-analyse an existing evidence folder and exit")
    args = parser.parse_args()

    if args.analyse:
        analyse_folder(Path(args.analyse).resolve())
        print(f"Re-analysed {args.analyse}")
        return
    if args.quick:
        args.levels, args.repeats, args.steady, args.no_recovery = "1,5", 1, 20, True

    levels = [int(v) for v in args.levels.split(",")]
    jmeter = find_jmeter(args.jmeter)
    if not port_free(args.port):
        raise SystemExit(f"Port {args.port} is already in use. Stop that program or use --port.")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    label = "".join(c if c.isalnum() or c in "-_" else "-" for c in args.label).strip("-")
    out = EVIDENCE / f"perf_{stamp}{'_quick' if args.quick else ''}{'_' + label if label else ''}"
    (out / "runs").mkdir(parents=True)
    settings = {"levels_users": levels, "repeats": args.repeats, "steady_s": args.steady,
                "rampup_rule": "max(5 s, users / 5 s)", "think_time": "uniform random 0.5-1.5 s before each request",
                "per_user_flow": "register once; then loop: task list page, dashboard page, API task list, API create task",
                "recovery_check": not args.no_recovery,
                "targets": {"p95_ms": TARGET_P95_MS, "error_pct": TARGET_ERROR_PCT}, "label": args.label}
    env = environment(jmeter, settings)
    print(f"Evidence folder: {out}\nJMeter: {jmeter}\n")

    runs = []
    started = datetime.now().astimezone()
    for users in levels:
        for rep in range(1, args.repeats + 1):
            one_run(args, jmeter, out, [(users, f"u{users:03d}_r{rep}")], "level", runs)
    if not args.no_recovery:
        top = max(levels)
        print("Recovery check (highest level, then 1 user on the same server):")
        one_run(args, jmeter, out, [(top, f"recovery_u{top:03d}"), (1, "recovery_u001_after")], "recovery", runs)

    meta = {"started": started.isoformat(timespec="seconds"),
            "finished": datetime.now().astimezone().isoformat(timespec="seconds"),
            "settings": settings, "environment": env, "runs": runs}
    (out / "runs.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out / "environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
    by_level = analyse_folder(out)

    print("\nUsers  Median  p95    req/s   Errors  Meets targets")
    for l in by_level:
        print(f"{l['users']:>5}  {l['median_ms']:>6}  {l['p95_ms']:>5}  {l['throughput_rps']:>6}  {l['error_pct']:>5}%  {l['meets_targets']}")
    print(f"\nTables: {out / 'results.md'}\nCharts: {out / 'charts'}")


if __name__ == "__main__":
    main()
