# Week 5 - Security and performance

| File / folder | What it is |
|---|---|
| `Week5_Report.md` | The Week 5 report: STRIDE table, security findings, performance test and results, limitations, recommendations |
| `performance/pytodo_load_test.jmx` | JMeter plan (open it in the JMeter GUI to look at it; run it with the script below) |
| `performance/run_perf_server.py` | Starts the unchanged app on port 5015 with an empty test database |
| `performance/run_performance.py` | One command: runs every load level, then makes the tables and charts |
| `evidence/perf_<date-time>_<label>/` | One folder per experiment: `results.md`, `charts/`, CSV summaries, raw JMeter results (`.jtl.gz`, open with 7-Zip), `environment.json` |

## Run the performance test on your PC

**1. Folders.** Keep the app beside the project, and extract JMeter into Downloads (or anywhere, then use `--jmeter`):

```
Downloads\
  pytodo_pro_student\          <- extracted app (app.py, helpers.py ...)
  apache-jmeter-5.6.3\         <- extracted JMeter
  STQA_Week5_6\05_Security_Performance\performance\   <- run from here
```

If the app is elsewhere: `$env:PYTODO_SOURCE_DIR = "C:\path\to\pytodo_pro_student"`

**2. Python packages** (in your virtual environment): the app's `requirements.txt`, plus `matplotlib` for the charts.

```powershell
pip install -r ..\..\..\pytodo_pro_student\requirements.txt matplotlib
```

JMeter needs Java (you have the JDK installer in Downloads). Check with `java -version`.

**3. Quick check (about 2 minutes):**

```powershell
python run_performance.py --quick
```

**4. Full experiment (about 50 minutes).** Close other programs first, plug in the charger, and leave the PC alone while it runs:

```powershell
python run_performance.py --label "Ahmad-PC"
```

It prints a summary at the end. Copy the tables from the new `evidence\perf_...\results.md` and the three charts into the report's results section (section 5), replacing the agent-run numbers, and update the environment table (section 4.4) from `environment.json`.

**Options:** `--levels 1,5,10,25` (choose user counts), `--repeats 3`, `--steady 60` (seconds measured per run), `--no-recovery`, `--port 5016`, `--jmeter C:\...\apache-jmeter-5.6.3\bin\jmeter.bat`. To redo only the tables and charts for an existing folder: `python run_performance.py --analyse ..\evidence\perf_<folder>`.
