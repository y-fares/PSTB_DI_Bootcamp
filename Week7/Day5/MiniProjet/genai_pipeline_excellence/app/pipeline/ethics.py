import re, yaml
from pathlib import Path
from typing import Dict, Any, List
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

TOXIC_KEYWORDS = [
    r"\bidiot(e)?\b", r"\bstupide\b", r"\bhaine\b", r"\bmenace\b",
    r"\bviolence\b", r"\binsulte\b"
]

class EthicsFilter:
    def __init__(self, cfg_path="app/configs/default.yaml"):
        self.cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.th = self.cfg["ethics"]["toxicity_threshold"]
        self.pii_patterns = [re.compile(p, re.IGNORECASE) for p in self.cfg["ethics"]["pii_patterns"]]
        self.embedder = SentenceTransformer(self.cfg["models"]["embedder"])
        self.clf = LogisticRegression()  # Placeholder: à entraîner si besoin

    def _rule_flags(self, text: str) -> List[Dict[str, Any]]:
        flags = []
        for pat in TOXIC_KEYWORDS:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                flags.append({"type":"toxicity_rule","rule":pat,"span_start":m.start(),"span_end":m.end(),"snippet":text[m.start():m.end()]})
        for pat in self.pii_patterns:
            for m in pat.finditer(text):
                flags.append({"type":"pii","rule":pat.pattern,"span_start":m.start(),"span_end":m.end(),"snippet":text[m.start():m.end()]})
        return flags

    def _tox_score(self, text: str) -> float:
        score = 0.1
        if re.search(r"\b(haine|menace|violence|insulte)\b", text, re.IGNORECASE):
            score += 0.6
        if len(text) > 400: score += 0.1
        return min(1.0, score)

    def evaluate(self, text: str) -> Dict[str, Any]:
        flags = self._rule_flags(text)
        tox = self._tox_score(text)
        verdict = "SAFE"
        if flags or tox >= self.th: verdict = "FLAG"
        redacted = text
        for f in flags:
            if f["type"] == "pii":
                s, e = f["span_start"], f["span_end"]
                redacted = redacted[:s] + "[REDACTED]" + redacted[e:]
        return {"verdict": verdict, "tox_score": float(tox), "flags": flags, "redacted_text": redacted}
