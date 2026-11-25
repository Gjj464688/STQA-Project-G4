# Performance results: perf_20261125-182754_agent-run

Computer: Intel(R) Xeon(R) Processor @ 2.30GHz, 2 logical CPUs, 7.8 GB RAM, Linux-6.18.44-fc-v880-x86_64-with-glibc2.39. Python 3.13.18, Flask 3.0.3, apache-jmeter-5.6.3, Java: openjdk version "21.0.13.0.3" 2026-10-24.

Each run: 60 s measured after ramp-up, fresh server and empty database (runs per level in the table). Targets (proposed before execution): p95 <= 1000 ms and errors <= 1.0%.

## By load level (page and API requests; registration shown separately)

| Users | Type | Runs | Requests measured | Median (ms) | p95 (ms) | p95 range across runs | Max (ms) | Throughput (req/s) | Errors (%) | Meets targets | Register median / p95 (ms) |
|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| 1 | Load | 3 | 174 | 4 | 8 | 7-9 | 18 | 1.0 | 0.0 | Yes | 104 / 121 |
| 5 | Load | 3 | 870 | 3 | 6.3 | 6-7 | 42 | 4.8 | 0.0 | Yes | 68 / 116 |
| 10 | Load | 3 | 1769 | 2.7 | 5.7 | 5-6 | 26 | 9.8 | 0.0 | Yes | 71 / 114 |
| 25 | Load | 3 | 4416 | 2.3 | 5.3 | 5-6 | 17 | 24.5 | 0.0 | Yes | 74 / 100 |
| 50 | Stress | 3 | 8861 | 2 | 4.7 | 4-5 | 25 | 49.2 | 0.0 | Yes | 68 / 97 |
| 100 | Stress | 3 | 17814 | 2 | 4.3 | 4-5 | 32 | 99.0 | 0.0 | Yes | 68 / 103 |
| 200 | Stress | 3 | 35496 | 2 | 6.3 | 6-7 | 62 | 197.2 | 0.0 | Yes | 68 / 99 |

## By page (mean of runs)

| Users | Page / request | Median (ms) | p95 (ms) | Errors (%) |
|---:|---|---:|---:|---:|
| 1 | 02 Task list page | 3.7 | 5.3 | 0.0 |
| 1 | 03 Dashboard page | 3.7 | 5.3 | 0.0 |
| 1 | 04 API list tasks | 3 | 4.7 | 0.0 |
| 1 | 05 API create task | 6 | 14.3 | 0.0 |
| 5 | 02 Task list page | 3 | 4.7 | 0.0 |
| 5 | 03 Dashboard page | 3 | 4.3 | 0.0 |
| 5 | 04 API list tasks | 3 | 4.3 | 0.0 |
| 5 | 05 API create task | 5 | 8.3 | 0.0 |
| 10 | 02 Task list page | 2.7 | 4.7 | 0.0 |
| 10 | 03 Dashboard page | 2.3 | 4 | 0.0 |
| 10 | 04 API list tasks | 2.3 | 4 | 0.0 |
| 10 | 05 API create task | 4.3 | 6.7 | 0.0 |
| 25 | 02 Task list page | 2.3 | 3.7 | 0.0 |
| 25 | 03 Dashboard page | 2.3 | 3.3 | 0.0 |
| 25 | 04 API list tasks | 2 | 3.3 | 0.0 |
| 25 | 05 API create task | 4.3 | 6.7 | 0.0 |
| 50 | 02 Task list page | 2 | 4.3 | 0.0 |
| 50 | 03 Dashboard page | 2 | 3.3 | 0.0 |
| 50 | 04 API list tasks | 2 | 3.3 | 0.0 |
| 50 | 05 API create task | 3.3 | 6 | 0.0 |
| 100 | 02 Task list page | 2 | 4.3 | 0.0 |
| 100 | 03 Dashboard page | 1.7 | 3.3 | 0.0 |
| 100 | 04 API list tasks | 1.3 | 3.3 | 0.0 |
| 100 | 05 API create task | 3 | 6 | 0.0 |
| 200 | 02 Task list page | 2 | 7.3 | 0.0 |
| 200 | 03 Dashboard page | 2 | 5.3 | 0.0 |
| 200 | 04 API list tasks | 2 | 5 | 0.0 |
| 200 | 05 API create task | 3 | 7.3 | 0.0 |

## Every run

| Run | Kind | Users | Requests | Median (ms) | p95 (ms) | Throughput (req/s) | Errors (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| u001_r1 | level | 1 | 59 | 4 | 8 | 1.0 | 0.0 |
| u001_r2 | level | 1 | 59 | 4 | 9 | 1.0 | 0.0 |
| u001_r3 | level | 1 | 56 | 4 | 7 | 0.9 | 0.0 |
| u005_r1 | level | 5 | 291 | 3 | 6 | 4.8 | 0.0 |
| u005_r2 | level | 5 | 292 | 3 | 7 | 4.9 | 0.0 |
| u005_r3 | level | 5 | 287 | 3 | 6 | 4.8 | 0.0 |
| u010_r1 | level | 10 | 594 | 2 | 5 | 9.9 | 0.0 |
| u010_r2 | level | 10 | 592 | 3 | 6 | 9.9 | 0.0 |
| u010_r3 | level | 10 | 583 | 3 | 6 | 9.7 | 0.0 |
| u025_r1 | level | 25 | 1473 | 3 | 6 | 24.6 | 0.0 |
| u025_r2 | level | 25 | 1479 | 2 | 5 | 24.6 | 0.0 |
| u025_r3 | level | 25 | 1464 | 2 | 5 | 24.4 | 0.0 |
| u050_r1 | level | 50 | 2944 | 2 | 4 | 49.1 | 0.0 |
| u050_r2 | level | 50 | 2946 | 2 | 5 | 49.1 | 0.0 |
| u050_r3 | level | 50 | 2971 | 2 | 5 | 49.5 | 0.0 |
| u100_r1 | level | 100 | 5908 | 2 | 5 | 98.5 | 0.0 |
| u100_r2 | level | 100 | 5972 | 2 | 4 | 99.5 | 0.0 |
| u100_r3 | level | 100 | 5934 | 2 | 4 | 98.9 | 0.0 |
| u200_r1 | level | 200 | 11790 | 2 | 6 | 196.5 | 0.0 |
| u200_r2 | level | 200 | 11794 | 2 | 6 | 196.6 | 0.0 |
| u200_r3 | level | 200 | 11912 | 2 | 7 | 198.5 | 0.0 |
| recovery_u200 | recovery | 200 | 11777 | 2 | 6 | 196.3 | 0.0 |
| recovery_u001_after | recovery | 1 | 59 | 4 | 8 | 1.0 | 0.0 |
