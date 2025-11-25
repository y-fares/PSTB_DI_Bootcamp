import json, yaml
from pathlib import Path
from app.pipeline.orchestrator import run_once

CFG = "app/configs/default.yaml"
PROMPTS = "app/data/prompts.jsonl"

def main():
    results = []
    with open(PROMPTS, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)["prompt"]
            res = run_once(p, CFG)
            results.append({"prompt": p, **res})
    out = "app/data/eval_results.jsonl"
    with open(out, "w", encoding="utf-8") as w:
        for r in results:
            w.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Écrit: {out}. Résumés des statuts:", {r["status"] for r in results})

if __name__ == "__main__":
    main()
