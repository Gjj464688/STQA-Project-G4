# Performance results: perf_20261125-185954_agent-run-stress-extension

Computer: Intel(R) Xeon(R) Processor @ 2.30GHz, 2 logical CPUs, 7.8 GB RAM, Linux-6.18.44-fc-v880-x86_64-with-glibc2.39. Python 3.13.18, Flask 3.0.3, apache-jmeter-5.6.3, Java: openjdk version "21.0.13.0.3" 2026-10-24.

Each run: 60 s measured after ramp-up, fresh server and empty database (runs per level in the table). Targets (proposed before execution): p95 <= 1000 ms and errors <= 1.0%.

## By load level (page and API requests; registration shown separately)

| Users | Type | Runs | Requests measured | Median (ms) | p95 (ms) | p95 range across runs | Max (ms) | Throughput (req/s) | Errors (%) | Meets targets | Register median / p95 (ms) |
|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| 400 | Stress | 2 | 46457 | 6 | 81.5 | 78-85 | 1149 | 387.1 | 0.0 | Yes | 76 / 187 |
| 800 | Stress | 2 | 47924 | 261 | 5123.5 | 5098-5149 | 9270 | 399.4 | 22.5 | No | 124 / 5290 |

## By page (mean of runs)

| Users | Page / request | Median (ms) | p95 (ms) | Errors (%) |
|---:|---|---:|---:|---:|
| 400 | 02 Task list page | 7 | 102.5 | 0.0 |
| 400 | 03 Dashboard page | 5 | 62 | 0.0 |
| 400 | 04 API list tasks | 5 | 58 | 0.0 |
| 400 | 05 API create task | 6 | 106 | 0.0 |
| 800 | 02 Task list page | 294.5 | 1898.5 | 14.8 |
| 800 | 03 Dashboard page | 178.5 | 1348.5 | 14.7 |
| 800 | 04 API list tasks | 175 | 1339 | 14.59 |
| 800 | 05 API create task | 2380.5 | 5402.5 | 45.77 |

## Every run

| Run | Kind | Users | Requests | Median (ms) | p95 (ms) | Throughput (req/s) | Errors (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| u400_r1 | level | 400 | 23214 | 6 | 85 | 386.9 | 0.0 |
| u400_r2 | level | 400 | 23243 | 6 | 78 | 387.4 | 0.0 |
| u800_r1 | level | 800 | 24445 | 242 | 5098 | 407.4 | 21.66 |
| u800_r2 | level | 800 | 23479 | 280 | 5149 | 391.3 | 23.28 |
| recovery_u800 | recovery | 800 | 23405 | 298 | 5109 | 390.1 | 14.92 |
| recovery_u001_after | recovery | 1 | 59 | 4 | 7 | 1.0 | 0.0 |
