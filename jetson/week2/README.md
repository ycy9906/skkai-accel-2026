# Week 2 — 양자화 기초

**목표**: 비트를 줄이면 얼마나 빨라지고, 얼마나 망가지나
**산출물**: 1.5B 포맷 8개(F16~Q2_K)의 크기·속도·perplexity 표 + 파레토 그래프 1장

## 세션장 사전 준비

- [ ] `download.bat` 실행 → `../models/`에 파일 받기 (총 약 9.5 GB)
- [ ] `to_jetson.bat` 실행 → Jetson `~/models/`로 복사 (USB 2.0 젠더면 15분 이상)
- [ ] **7B 기준선 측정** (Jetson): 아래 명령 결과를 `results.csv`에 추가
- [ ] 리허설: Q4_0 하나 만들어 bench + perplexity 끝까지 (소요 시간 기록)
- [ ] `../models/`의 F16과 `wikitext-2-raw/`를 USB로 팀원에게 배포

```bash
cd ~/llama.cpp-b11946
# 7B 기준선 (분할 파일이면 첫 번째 파일만 지정)
./build/bin/llama-bench -m ~/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf -ngl 99 -p 512 -n 128 -r 3
```

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–10 | Memory Wall 발표 |
| 10–25 | 양자화: 각자 노트북에서 맡은 포맷, Jetson 운영자는 7개 전부 |
| 25–60 | Jetson bench(한 번에) / 노트북 perplexity(각자) |
| 60–75 | `results/results.csv` 채우기, 효율 계산 |
| 75–90 | 토론 |

| 담당 | perplexity 포맷 |
|---|---|
| A | F16, Q8_0 |
| B | Q6_K, Q5_K_M |
| C | Q4_K_M, Q4_0 |
| D | Q3_K_M, Q2_K |
| E (Jetson 운영) | 7개 양자화 + bench |

### 명령어

```bash
# 양자화 (노트북·Jetson 공통, 포맷당 1분 내외)
llama-quantize qwen2.5-1.5b-instruct-fp16.gguf q5_k_m.gguf Q5_K_M

# 속도 (Jetson, ~/models에서)
for f in Q8_0 Q6_K Q5_K_M Q4_K_M Q4_0 Q3_K_M Q2_K; do
  ~/llama.cpp-b11946/build/bin/llama-quantize qwen2.5-1.5b-instruct-fp16.gguf ${f,,}.gguf $f
done
~/llama.cpp-b11946/build/bin/llama-bench -m qwen2.5-1.5b-instruct-fp16.gguf -m q8_0.gguf -m q6_k.gguf \
  -m q5_k_m.gguf -m q4_k_m.gguf -m q4_0.gguf -m q3_k_m.gguf -m q2_k.gguf \
  -ngl 99 -p 512 -n 128 -r 3 -o csv > w2_bench.csv

# 정확도 (노트북은 -ngl 없이, Mac·Jetson은 -ngl 99)
llama-perplexity -m q5_k_m.gguf -f wiki.test.raw -c 512 --chunks 40
```

perplexity는 마지막 줄 `Final estimate: PPL = ...` 값을 기록.

## 토론 질문

1. 크기가 절반이면 속도도 2배인가? 어긋나는 포맷은?
2. Q4_0과 Q4_K_M은 크기가 비슷한데 속도·perplexity는?
3. perplexity가 급격히 튀는 지점은 몇 비트?

## 활동 후

- [ ] 기록 담당: `python scripts/plot_pareto.py 2` 로 그래프 → `results/week2_pareto.png`
- [ ] 전원: 토론 질문 해석 한 문단 → `assignments/{이름}/week2/`
