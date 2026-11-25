# Performance results: perf_20261126-024152_quick_Ahmad-PC-check

Computer: AMD Ryzen 7 7730U with Radeon Graphics, 16 logical CPUs, 15.4 GB RAM, Windows-11-10.0.26300-SP0. Python 3.13.15, Flask 3.0.3, apache-jmeter-5.6.3, Java: openjdk version "17.0.21" 2026-10-20.

Each run: 20 s measured after ramp-up, fresh server and empty database (runs per level in the table). Targets (proposed before execution): p95 <= 1000 ms and errors <= 1.0%.

## By load level (page and API requests; registration shown separately)

| Users | Type | Runs | Requests measured | Median (ms) | p95 (ms) | p95 range across runs | Max (ms) | Throughput (req/s) | Errors (%) | Meets targets | Register median / p95 (ms) |
|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| 1 | Load | 1 | 21 | 6 | 21 | 21-21 | 22 | 1.1 | 0.0 | Yes | 231 / 231 |
| 5 | Load | 1 | 94 | 6 | 19 | 19-19 | 23 | 4.7 | 0.0 | Yes | 196 / 217 |

## By page (mean of runs)

| Users | Page / request | Median (ms) | p95 (ms) | Errors (%) |
|---:|---|---:|---:|---:|
| 1 | 02 Task list page | 7 | 8 | 0.0 |
| 1 | 03 Dashboard page | 5 | 6 | 0.0 |
| 1 | 04 API list tasks | 5 | 5 | 0.0 |
| 1 | 05 API create task | 21 | 22 | 0.0 |
| 5 | 02 Task list page | 5 | 8 | 0.0 |
| 5 | 03 Dashboard page | 5 | 7 | 0.0 |
| 5 | 04 API list tasks | 5 | 7 | 0.0 |
| 5 | 05 API create task | 18 | 21 | 0.0 |

## Every run

| Run | Kind | Users | Requests | Median (ms) | p95 (ms) | Throughput (req/s) | Errors (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| u001_r1 | level | 1 | 21 | 6 | 21 | 1.1 | 0.0 |
| u005_r1 | level | 5 | 94 | 6 | 19 | 4.7 | 0.0 |
