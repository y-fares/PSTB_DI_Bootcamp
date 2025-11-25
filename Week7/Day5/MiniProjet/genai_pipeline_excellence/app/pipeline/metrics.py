from typing import Dict, Any, List
from rouge_score import rouge_scorer
import sacrebleu
import math

def compute_metrics(refs: List[str], hyps: List[str]) -> Dict[str, Any]:
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_vals = [scorer.score(r, h)['rougeL'].fmeasure for r, h in zip(refs, hyps)]
    bleu = sacrebleu.corpus_bleu(hyps, [refs]).score
    ppl = math.nan
    return {"rougeL_avg": sum(rouge_vals)/len(rouge_vals), "bleu": bleu, "perplexity": ppl}
