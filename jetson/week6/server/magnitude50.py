"""비정형 pruning 50% (magnitude, Wanda의 단순판): 행마다 절댓값이 작은 절반을 0으로
사용: python magnitude50.py models/Qwen2.5-1.5B-Instruct   ->  models/Qwen2.5-1.5B-Instruct-mag50/
"""
import sys, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

src = sys.argv[1].rstrip("/")
out = f"{src}-mag50"
model = AutoModelForCausalLM.from_pretrained(src, torch_dtype=torch.float16, device_map="cuda")
with torch.no_grad():
    for layer in model.model.layers:
        for m in layer.modules():
            if isinstance(m, torch.nn.Linear):
                w = m.weight
                idx = w.abs().argsort(dim=1)[:, : w.shape[1] // 2]
                w.scatter_(1, idx, 0)
model.save_pretrained(out)
AutoTokenizer.from_pretrained(src).save_pretrained(out)
print("saved", out)
