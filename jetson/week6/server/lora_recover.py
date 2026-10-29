"""LoRA 회복 학습: pruning으로 깎인 정확도를 짧은 추가 학습으로 되돌림
사용: python lora_recover.py <모델 폴더> <학습 샘플 수> <rank> [--4bit]
예)   python lora_recover.py models/Qwen2.5-1.5B-Instruct-drop4 2000 16
      python lora_recover.py models/Qwen2.5-7B-Instruct-drop6 8000 16 --4bit   # 7B는 QLoRA
결과: <모델 폴더>-lora-<n>-r<r>/ (병합된 모델, 바로 GGUF 변환 가능)
학습 데이터는 평가용 wikitext와 겹치지 않도록 지시문 데이터(alpaca-cleaned)를 쓴다.
"""
import sys, gc, torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig

base, n, r = sys.argv[1].rstrip("/"), int(sys.argv[2]), int(sys.argv[3])
use_4bit = "--4bit" in sys.argv
out = f"{base}-lora-{n}-r{r}"

ds = load_dataset("yahma/alpaca-cleaned", split=f"train[:{n}]")
ds = ds.map(lambda e: {"messages": [
    {"role": "user", "content": (e["instruction"] + "\n" + e["input"]).strip()},
    {"role": "assistant", "content": e["output"]}]}, remove_columns=ds.column_names)

tok = AutoTokenizer.from_pretrained(base)
kw = {"torch_dtype": torch.bfloat16}
if use_4bit:
    kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                   bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(base, device_map="cuda", **kw)

trainer = SFTTrainer(
    model=model,
    processing_class=tok,
    train_dataset=ds,
    args=SFTConfig(output_dir=out + "-ckpt", num_train_epochs=1, per_device_train_batch_size=4 if use_4bit else 8,
                   gradient_accumulation_steps=2 if use_4bit else 1, learning_rate=2e-4, bf16=True,
                   logging_steps=20, save_strategy="no", report_to="none"),
    peft_config=LoraConfig(r=r, lora_alpha=2 * r, target_modules="all-linear", task_type="CAUSAL_LM"),
)
trainer.train()
trainer.model.save_pretrained(out + "-adapter")

# 어댑터를 bf16 원본에 병합 (4bit로 학습했어도 병합은 bf16에서)
del trainer, model
gc.collect(); torch.cuda.empty_cache()
full = AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.bfloat16, device_map="cuda")
merged = PeftModel.from_pretrained(full, out + "-adapter").merge_and_unload()
merged.save_pretrained(out)
tok.save_pretrained(out)
print("saved", out)
