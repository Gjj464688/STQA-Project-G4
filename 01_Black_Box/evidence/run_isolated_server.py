"""Serve the supplied app for isolated Week 1 browser checks, without editing it."""

import sys
from pathlib import Path

SOURCE = Path(r"C:\Users\Admin\Downloads\pytodo_pro_student")
EVIDENCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE))

import app  # noqa: E402

app.DATABASE = str(EVIDENCE / "week1_browser_test.db")
app.init_db()
app.app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
