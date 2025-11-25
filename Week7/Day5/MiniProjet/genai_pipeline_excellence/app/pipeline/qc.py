import math, re, yaml
from pathlib import Path
from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util
import textstat

class QualityChecker:
    def __init__(self, cfg_path="app/configs/default.yaml"):
        self.cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.weights = self.cfg["quality_score"]["weights"]
        embedder_name = self.cfg["models"]["embedder"]
        self.embedder = SentenceTransformer(embedder_name)

    def _similarity(self, a: str, b: str) -> float:
        emb = self.embedder.encode([a, b], convert_to_tensor=True, normalize_embeddings=True)
        sim = float(util.cos_sim(emb[0], emb[1]).cpu().item())
        return max(0.0, min(1.0, sim))

    def _length_score(self, text: str) -> float:
        toks = len(re.findall(r"\w+", text))
        mn = self.cfg["quality_score"]["length"]["min_tokens"]
        mx = self.cfg["quality_score"]["length"]["max_tokens"]
        if toks < mn: return toks / mn
        if toks > mx: return mx / toks
        return 1.0

    def _readability(self, text: str) -> float:
        fk = textstat.flesch_kincaid_grade(text)
        score = 1.0 / (1.0 + math.exp((fk - 8) / 4.0))
        return float(score)

    def score(self, text: str, prompt: str) -> Dict[str, Any]:
        sim = self._similarity(prompt, text)
        length = self._length_score(text)
        read = self._readability(text)
        w = self.weights
        Q = w["sim"]*sim + w["length"]*length + w["readability"]*read
        return {"Q": float(Q), "sim": float(sim), "len_util": float(length), "readability": float(read)}
