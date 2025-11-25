import sqlite3
from pathlib import Path
from typing import Dict, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  prompt_hash TEXT,
  prompt TEXT,
  seed INTEGER,
  gen_model TEXT,
  qc_model TEXT,
  ethics_verdict TEXT,
  Q REAL,
  sim REAL,
  len_util REAL,
  readability REAL,
  latency_ms REAL,
  config_version TEXT
);
CREATE TABLE IF NOT EXISTS flags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER,
  type TEXT,
  rule TEXT,
  span_start INTEGER,
  span_end INTEGER,
  snippet TEXT,
  FOREIGN KEY(run_id) REFERENCES runs(id)
);
"""

class Storage:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def insert_run(self, record: Dict[str, Any]) -> int:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("""
            INSERT INTO runs (prompt_hash, prompt, seed, gen_model, qc_model, ethics_verdict,
                              Q, sim, len_util, readability, latency_ms, config_version)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (record.get("prompt_hash"), record.get("prompt"), record.get("seed"),
                  record.get("gen_model"), record.get("qc_model"), record.get("ethics_verdict"),
                  record.get("Q"), record.get("sim"), record.get("len_util"),
                  record.get("readability"), record.get("latency_ms"),
                  record.get("config_version","default")))
            run_id = cur.lastrowid
            for f in record.get("flags", []):
                cur.execute("""
                INSERT INTO flags (run_id, type, rule, span_start, span_end, snippet)
                VALUES (?,?,?,?,?,?)
                """, (run_id, f.get("type"), f.get("rule"), f.get("span_start"),
                      f.get("span_end"), f.get("snippet")))
            con.commit()
            return run_id
