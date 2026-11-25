# Performance results: perf_20261126-024531_Ahmad-PC

Computer: AMD Ryzen 7 7730U with Radeon Graphics, 16 logical CPUs, 15.4 GB RAM, Windows-11-10.0.26300-SP0. Python 3.13.15, Flask 3.0.3, apache-jmeter-5.6.3, Java: openjdk version "17.0.21" 2026-10-20.

Each run: 60 s measured after ramp-up, fresh server and empty database (runs per level in the table). Targets (proposed before execution): p95 <= 1000 ms and errors <= 1.0%.

## By load level (page and API requests; registration shown separately)

| Users | Type | Runs | Requests measured | Median (ms) | p95 (ms) | p95 range across runs | Max (ms) | Throughput (req/s) | Errors (%) | Meets targets | Register median / p95 (ms) |
|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| 1 | Load | 3 | 173 | 5 | 16.3 | 16-17 | 18 | 0.9 | 0.0 | Yes | 158 / 160 |
| 5 | Load | 3 | 844 | 4.7 | 264.3 | 15-759 | 1805 | 4.7 | 0.0 | Yes | 137 / 168 |
| 10 | Load | 3 | 1511 | 5 | 1433.3 | 1357-1477 | 1997 | 8.4 | 0.0 | No | 139 / 1556 |
| 25 | Load | 3 | 4406 | 4 | 8.3 | 8-9 | 50 | 24.5 | 0.0 | Yes | 131 / 145 |
| 50 | Stress | 3 | 8720 | 4 | 8.3 | 8-9 | 2383 | 48.5 | 0.0 | Yes | 131 / 154 |
| 100 | Stress | 3 | 17611 | 4 | 17 | 16-18 | 113 | 97.9 | 0.0 | Yes | 132 / 150 |
| 200 | Stress | 3 | 34578 | 4.3 | 55.3 | 38-81 | 6140 | 192.1 | 19.2 | No | 133 / 161 |
| 400 | Stress | 3 | 67586 | 23 | 84.7 | 78-89 | 6074 | 375.5 | 80.9 | No | 140 / 4245 |
| 800 | Stress | 3 | 123323 | 102.3 | 454.3 | 423-492 | 2633 | 685.1 | 87.1 | No | 133 / 505 |

## By page (mean of runs)

| Users | Page / request | Median (ms) | p95 (ms) | Errors (%) |
|---:|---|---:|---:|---:|
| 1 | 02 Task list page | 6 | 7 | 0.0 |
| 1 | 03 Dashboard page | 4 | 6.3 | 0.0 |
| 1 | 04 API list tasks | 4 | 5 | 0.0 |
| 1 | 05 API create task | 10.7 | 17 | 0.0 |
| 5 | 02 Task list page | 4.7 | 259.3 | 0.0 |
| 5 | 03 Dashboard page | 4 | 20 | 0.0 |
| 5 | 04 API list tasks | 3.7 | 87.7 | 0.0 |
| 5 | 05 API create task | 8.7 | 485 | 0.0 |
| 10 | 02 Task list page | 4.7 | 1102.3 | 0.0 |
| 10 | 03 Dashboard page | 4 | 1321.7 | 0.0 |
| 10 | 04 API list tasks | 4 | 1406 | 0.0 |
| 10 | 05 API create task | 9 | 1557 | 0.0 |
| 25 | 02 Task list page | 4 | 6 | 0.0 |
| 25 | 03 Dashboard page | 4 | 5.3 | 0.0 |
| 25 | 04 API list tasks | 4 | 5 | 0.0 |
| 25 | 05 API create task | 7 | 14 | 0.0 |
| 50 | 02 Task list page | 4 | 6.3 | 0.0 |
| 50 | 03 Dashboard page | 3.3 | 5.3 | 0.0 |
| 50 | 04 API list tasks | 3 | 5 | 0.0 |
| 50 | 05 API create task | 6 | 18.3 | 0.0 |
| 100 | 02 Task list page | 4 | 12 | 0.0 |
| 100 | 03 Dashboard page | 3 | 6 | 0.0 |
| 100 | 04 API list tasks | 3 | 5.7 | 0.0 |
| 100 | 05 API create task | 5 | 23.7 | 0.0 |
| 200 | 02 Task list page | 4.3 | 59 | 19.57 |
| 200 | 03 Dashboard page | 3.7 | 34 | 18.79 |
| 200 | 04 API list tasks | 3.3 | 34.3 | 18.87 |
| 200 | 05 API create task | 6.7 | 127 | 19.49 |
| 400 | 02 Task list page | 23.7 | 82.3 | 80.88 |
| 400 | 03 Dashboard page | 22.3 | 72.7 | 81.06 |
| 400 | 04 API list tasks | 22.3 | 72.3 | 80.64 |
| 400 | 05 API create task | 24.3 | 170.7 | 81.02 |
| 800 | 02 Task list page | 105.7 | 437.7 | 87.23 |
| 800 | 03 Dashboard page | 94.7 | 430.3 | 86.91 |
| 800 | 04 API list tasks | 94.7 | 432 | 87.01 |
| 800 | 05 API create task | 115.7 | 529 | 87.21 |

## Every run

| Run | Kind | Users | Requests | Median (ms) | p95 (ms) | Throughput (req/s) | Errors (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| u001_r1 | level | 1 | 57 | 5 | 16 | 0.9 | 0.0 |
| u001_r2 | level | 1 | 57 | 5 | 16 | 0.9 | 0.0 |
| u001_r3 | level | 1 | 59 | 5 | 17 | 1.0 | 0.0 |
| u005_r1 | level | 5 | 283 | 5 | 15 | 4.7 | 0.0 |
| u005_r2 | level | 5 | 268 | 5 | 759 | 4.5 | 0.0 |
| u005_r3 | level | 5 | 293 | 4 | 19 | 4.9 | 0.0 |
| u010_r1 | level | 10 | 507 | 5 | 1477 | 8.4 | 0.0 |
| u010_r2 | level | 10 | 508 | 5 | 1357 | 8.5 | 0.0 |
| u010_r3 | level | 10 | 496 | 5 | 1466 | 8.3 | 0.0 |
| u025_r1 | level | 25 | 1486 | 4 | 8 | 24.8 | 0.0 |
| u025_r2 | level | 25 | 1465 | 4 | 9 | 24.4 | 0.0 |
| u025_r3 | level | 25 | 1455 | 4 | 8 | 24.2 | 0.0 |
| u050_r1 | level | 50 | 2950 | 4 | 8 | 49.2 | 0.0 |
| u050_r2 | level | 50 | 2837 | 4 | 9 | 47.3 | 0.0 |
| u050_r3 | level | 50 | 2933 | 4 | 8 | 48.9 | 0.0 |
| u100_r1 | level | 100 | 5877 | 4 | 17 | 98.0 | 0.0 |
| u100_r2 | level | 100 | 5908 | 4 | 18 | 98.5 | 0.0 |
| u100_r3 | level | 100 | 5826 | 4 | 16 | 97.1 | 0.0 |
| u200_r1 | level | 200 | 11483 | 5 | 81 | 191.4 | 8.1 |
| u200_r2 | level | 200 | 11683 | 4 | 38 | 194.7 | 20.4 |
| u200_r3 | level | 200 | 11412 | 4 | 47 | 190.2 | 29.05 |
| u400_r1 | level | 400 | 22803 | 21 | 87 | 380.1 | 75.92 |
| u400_r2 | level | 400 | 22751 | 24 | 89 | 379.2 | 83.04 |
| u400_r3 | level | 400 | 22032 | 24 | 78 | 367.2 | 83.74 |
| u800_r1 | level | 800 | 40503 | 120 | 492 | 675.0 | 85.65 |
| u800_r2 | level | 800 | 41338 | 96 | 448 | 689.0 | 85.75 |
| u800_r3 | level | 800 | 41482 | 91 | 423 | 691.4 | 89.88 |
| recovery_u800 | recovery | 800 | 40410 | 126 | 494 | 673.5 | 89.85 |
| recovery_u001_after | recovery | 1 | 57 | 5 | 16 | 0.9 | 0.0 |
