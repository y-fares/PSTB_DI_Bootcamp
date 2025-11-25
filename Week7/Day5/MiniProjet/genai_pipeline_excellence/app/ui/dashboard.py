import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd
import yaml
import json, subprocess, sys

CFG = "app/configs/default.yaml"

def load_runs(db_path):
    con = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM runs ORDER BY id DESC LIMIT 500", con)
    con.close()
    return df

st.set_page_config(page_title="GenAI Pipeline Dashboard", layout="wide")
st.title("GenAI Pipeline — Dashboard")

cfg = yaml.safe_load(Path(CFG).read_text())
db_path = cfg["storage"]["sqlite_path"]

col1, col2 = st.columns(2)
with col1:
    prompt = st.text_area("Prompt", "Explique l'importance des sauvegardes de données en 120 mots.")
with col2:
    if st.button("Générer"):
        res = subprocess.check_output([sys.executable, "app/pipeline/orchestrator.py", "--prompt", prompt]).decode("utf-8")
        st.code(res, language="json")

st.markdown("---")
st.subheader("Derniers runs")
if Path(db_path).exists():
    df = load_runs(db_path)
    st.dataframe(df, use_container_width=True)
    st.metric("PASS (Q ≥ pass & SAFE)", int(((df["Q"] >= cfg["quality_score"]["thresholds"]["pass"]) & (df["ethics_verdict"]=="SAFE")).sum()))
    st.metric("WARN", int(((df["Q"] >= cfg["quality_score"]["thresholds"]["warn"]) & (df["Q"] < cfg["quality_score"]["thresholds"]["pass"]) & (df["ethics_verdict"]=="SAFE")).sum()))
    st.metric("FLAG/FAIL", int(((df["ethics_verdict"]!="SAFE") | (df["Q"] < cfg["quality_score"]["thresholds"]["warn"])).sum()))
else:
    st.info("Aucun run enregistré pour l’instant.")
