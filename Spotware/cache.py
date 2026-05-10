"""
cache.py  —  SpotWare persistent submission cache (SQLite-backed)
Place this file alongside app.py (inside Spotware/).

Public API
----------
save_submission(perception, decision, image_b64, timestamp) -> int  (row id)
load_submissions(limit=200)  -> list[dict]
clear_cache()
submission_count() -> int
"""

import json
import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).resolve().parent / "spotware_cache.db"


# ── Internal helpers ──────────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at     TEXT    NOT NULL,
                device_class   TEXT,
                manufacturer   TEXT,
                model          TEXT,
                condition      TEXT,
                confidence     REAL,
                completeness   TEXT,
                action_label   TEXT,
                action_color   TEXT,
                co2_avoided_kg REAL,
                value_usd      REAL,
                metals_total_g REAL,
                perception_json    TEXT,
                sustainability_json TEXT,
                decision_json      TEXT,
                image_b64          TEXT
            )
        """)
        conn.commit()


_ensure_table()


# ── Public API ────────────────────────────────────────────────────────────────

def save_submission(
    perception: dict,
    decision: dict,
    image_b64: str = "",
    timestamp: str = "",
    sustainability: dict | None = None,
) -> int:
    """Persist one analysis result. Returns the new row id."""
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO submissions (
                created_at, device_class, manufacturer, model,
                condition, confidence, completeness,
                action_label, action_color,
                co2_avoided_kg, value_usd, metals_total_g,
                perception_json, sustainability_json, decision_json, image_b64
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                timestamp,
                perception.get("device_class"),
                perception.get("manufacturer"),
                perception.get("model"),
                perception.get("condition"),
                perception.get("confidence"),
                perception.get("completeness"),
                decision.get("label"),
                decision.get("color"),
                decision.get("co2_avoided_kg", 0),
                decision.get("value_usd", 0),
                decision.get("metals_total_g", 0),
                json.dumps(perception),
                json.dumps(sustainability or {}),
                json.dumps(decision),
                image_b64,
            ),
        )
        conn.commit()
        rowid = cur.lastrowid
        assert rowid is not None
        return rowid


def load_submissions(limit: int = 200) -> list[dict]:
    """
    Return up to *limit* most-recent submissions as plain dicts.
    JSON columns are automatically decoded.
    """
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM submissions ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()

    results = []
    for row in rows:
        d = dict(row)
        for col in ("perception_json", "sustainability_json", "decision_json"):
            raw = d.pop(col, None)
            key = col.replace("_json", "")
            try:
                d[key] = json.loads(raw) if raw else {}
            except Exception:
                d[key] = {}
        results.append(d)
    return results


def clear_cache():
    """Delete all rows from the submissions table."""
    with _connect() as conn:
        conn.execute("DELETE FROM submissions")
        conn.commit()


def submission_count() -> int:
    """Total number of persisted submissions."""
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]