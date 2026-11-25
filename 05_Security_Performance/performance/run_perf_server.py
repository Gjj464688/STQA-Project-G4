"""Serve the unchanged PyTodo Pro app for the Week 5 performance test.

Same approach as the Week 3/4 isolated server: the original app is loaded
without changes (hash checked), it uses a new temporary database, debug is
off, and it listens only on 127.0.0.1. Port 5015 by default, so it does
not clash with the app (5000) or the Week 3/4 (5013/5014) and Week 6 (5002)
test servers.

run_performance.py starts and stops this server for every test run, so a
run always begins with an empty database. You can also start it by hand:
    python run_perf_server.py
"""
import hashlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL_APP_SHA256 = "050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f"
DEFAULT_SOURCE = HERE.parents[2] / "pytodo_pro_student"


def source_dir():
    value = os.environ.get("PYTODO_SOURCE_DIR") or os.environ.get("PYTODO_APP_DIR") or DEFAULT_SOURCE
    return Path(value).resolve()


def main():
    source = source_dir()
    app_file = source / "app.py"
    if not app_file.exists():
        raise SystemExit(f"PyTodo Pro source not found at {source}. Set PYTODO_SOURCE_DIR.")
    if hashlib.sha256(app_file.read_bytes()).hexdigest() != ORIGINAL_APP_SHA256:
        raise SystemExit("app.py differs from the recorded original; refusing to test a changed app.")

    sys.path.insert(0, str(source))
    spec = importlib.util.spec_from_file_location("week5_target", app_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    port = int(os.environ.get("PERF_PORT", "5015"))
    with tempfile.TemporaryDirectory(prefix="pytodo-week5-") as work:
        module.DATABASE = str(Path(work) / "perf.sqlite3")
        module.init_db()
        # Flask's built-in server, threaded (its default) - the same server
        # the supplied app uses when started with "python app.py".
        module.app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
