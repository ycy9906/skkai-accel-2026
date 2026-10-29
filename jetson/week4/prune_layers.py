"""레이어 pruning (ShortGPT 방식): 입력·출력이 비슷한 레이어 = 하는 일이 적은 레이어를 제거
사용: python prune_layers.py <모델 폴더> <제거할 층 수>
예)   python prune_layers.py models/Qwen2.5-1.5B-Instruct 4   ->  models/Qwen2.5-1.5B-Instruct-drop4/
"""
import sys, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

src, n_drop = sys.argv[1].rstrip("/"), int(sys.argv[2])
out = f"{src}-drop{n_drop}"
tok = AutoTokenizer.from_pretrained(src)
model = AutoModelForCausalLM.from_pretrained(src, torch_dtype=torch.float16, device_map="cuda")

# calibration: wikitext train 32 x 512 토큰 (평가용 test와 겹치지 않음)
text = "\n".join(t for t in load_dataset("wikitext", "wikitext-2-raw-v1", split="train")["text"] if t.strip())
ids = tok(text[:400000], return_tensors="pt").input_ids[:, :32 * 512].view(32, 512).cuda()

L = model.config.num_hidden_layers
sim = torch.zeros(L)
with torch.no_grad():
    for b in ids.split(4):
        hs = model(b, output_hidden_states=True).hidden_states
        for i in range(L):
            sim[i] += torch.nn.functional.cosine_similarity(hs[i].float(), hs[i + 1].float(), dim=-1).mean().cpu()
sim /= 8
print("layer similarity (높을수록 제거 후보):")
for i, s in enumerate(sim.tolist()):
    print(f"  {i:2d}: {s:.4f}")
sim[0] = sim[-1] = -1e9  # 첫·마지막 레이어는 남김

drop = sorted(sim.topk(n_drop).indices.tolist())
print("drop layers:", drop)
keep = [l for i, l in enumerate(model.model.layers) if i not in drop]
model.model.layers = torch.nn.ModuleList(keep)
for i, l in enumerate(model.model.layers):
    l.self_attn.layer_idx = i
if getattr(model.config, "layer_types", None):
    model.config.layer_types = [t for i, t in enumerate(model.config.layer_types) if i not in drop]
model.config.num_hidden_layers = len(keep)
model.save_pretrained(out)
tok.save_pretrained(out)
print("saved", out, f"({L} -> {len(keep)} layers)")
