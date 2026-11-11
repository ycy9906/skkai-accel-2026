# SKKAI AI Accelerator — Week 2

## Q3_K_M Quantization Experiment

**Member:** seyoung  
**Date:** 2026-11-04  
**Model:** Qwen2.5-1.5B-Instruct

### Experiment Environment

- Google Colab CPU
- llama.cpp commit: `8ca4060`
- Quantization: Q3_K_M
- Dataset: WikiText-2 test
- Perplexity options: `-c 512 --chunks 40`

### Results

| Metric | Result |
|---|---|
| GGUF file size | 0.8242 GB |
| Perplexity (PPL) | 10.9884 ± 0.29607 |
| Quantization time | 108.14 seconds |
| pp512 | Pending Jetson measurement |
| tg128 | Pending Jetson measurement |

### Analysis

Q3_K_M quantization reduced the model size substantially compared to F16, producing a GGUF file of approximately 0.8242 GB. The measured perplexity on WikiText-2 was 10.9884. Further comparison with the F16 perplexity and Jetson decoding throughput is required to determine the trade-off between compression, prediction quality, and inference speed.

### Files

- `ppl_Q3_K_M.csv` — Quantization result
- `ppl_Q3_K_M.log` — Perplexity measurement log
- GGUF model — Team Google Drive (`skkai_w2/gguf/qwen1.5b-q3_k_m.gguf`)
