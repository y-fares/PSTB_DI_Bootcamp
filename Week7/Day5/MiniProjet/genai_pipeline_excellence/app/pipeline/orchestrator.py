import argparse, json, time, yaml
from pathlib import Path
from app.pipeline.generator import Generator
from app.pipeline.qc import QualityChecker
from app.pipeline.ethics import EthicsFilter
from app.pipeline.storage import Storage

def run_once(prompt: str, cfg_path="app/configs/default.yaml"):
    cfg = yaml.safe_load(Path(cfg_path).read_text())
    store = Storage(cfg["storage"]["sqlite_path"])
    gen = Generator(cfg_path)
    qc = QualityChecker(cfg_path)
    et = EthicsFilter(cfg_path)

    g = gen.generate(prompt, seed=cfg.get("seed", 42))
    q = qc.score(g["text"], prompt)
    e = et.evaluate(g["text"])

    Q = q["Q"]
    verdict = e["verdict"]
    record = {
        "prompt_hash": g["prompt_hash"],
        "prompt": prompt,
        "seed": cfg.get("seed", 42),
        "gen_model": g["model"],
        "qc_model": cfg["models"]["summarizer"],
        "ethics_verdict": verdict,
        "Q": Q,
        "sim": q["sim"],
        "len_util": q["len_util"],
        "readability": q["readability"],
        "latency_ms": g["latency_ms"],
        "config_version": "default",
        "flags": e["flags"]
    }
    run_id = store.insert_run(record)

    thresholds = cfg["quality_score"]["thresholds"]
    status = "PASS" if (Q >= thresholds["pass"] and verdict == "SAFE") else "WARN" if (Q >= thresholds["warn"] and verdict == "SAFE") else "FAIL"
    return {
        "run_id": run_id,
        "status": status,
        "verdict": verdict,
        "Q": Q,
        "components": {k: record[k] for k in ["sim", "len_util", "readability"]},
        "text": g["text"] if verdict == "SAFE" else e["redacted_text"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=False, default="Explique l'importance des sauvegardes de données en 120 mots.")
    parser.add_argument("--config", default="app/configs/default.yaml")
    args = parser.parse_args()
    res = run_once(args.prompt, args.config)
    print(json.dumps(res, ensure_ascii=False, indent=2))
