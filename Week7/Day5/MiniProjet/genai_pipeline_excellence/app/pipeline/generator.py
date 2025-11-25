import time, hashlib, yaml
from typing import Dict, Any
from pathlib import Path

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch

class Generator:
    def __init__(self, cfg_path="app/configs/default.yaml"):
        self.cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.model_name = self.cfg["models"]["generator"]
        self.decoding = self.cfg["decoding"]
        self._load()

    def _load(self):
        if "t5" in self.model_name:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.is_t5 = True
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.is_t5 = False

    def generate(self, prompt: str, seed: int = 42) -> Dict[str, Any]:
        t0 = time.time()
        torch.manual_seed(seed)
        params = dict(
            max_new_tokens=self.decoding["max_new_tokens"],
            do_sample=True,
            top_k=self.decoding["top_k"],
            top_p=self.decoding["top_p"],
            temperature=self.decoding["temperature"],
            early_stopping=True
        )
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        output_ids = self.model.generate(input_ids, **params)
        text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        latency_ms = (time.time() - t0) * 1000
        h = hashlib.sha256((prompt + str(self.model_name)).encode()).hexdigest()[:16]
        return {"text": text, "latency_ms": latency_ms, "prompt_hash": h, "model": self.model_name}
