# Week 5 — LoRA 회복 학습

**목표**: 레이어를 뺀 모델을 짧게 추가 학습해서, 속도는 유지하고 perplexity를 되돌리기
**산출물**: 회복 전후 비교, **최종 조합 1개 확정** (몇 층 제거 + 어떤 학습 + 어떤 양자화)

LoRA = 원래 가중치는 고정하고 작은 행렬 2개(rank r)만 학습. 병합하면 원래 크기로 돌아가므로 Jetson 속도는 거의 그대로여야 정상.

## 세션장 사전 준비

- [ ] 이 폴더의 `lora_recover.py`를 서버 작업 폴더에 복사
- [ ] 리허설: drop4 + 2,000개 1회. 소요 시간과 `nvidia-smi` 메모리 기록 → 2개 동시 실행 가능한지 판단
- [ ] 서버가 안 되면 Colab(T4)용으로 `bf16=True`를 `fp16=True`로 바꾼 사본 준비

```bash
cd ~/skkai-jetson && source .venv/bin/activate
python lora_recover.py models/Qwen2.5-1.5B-Instruct-drop4 2000 16
bash to_gguf.sh models/Qwen2.5-1.5B-Instruct-drop4-lora-2000-r16 Q4_K_M
```

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–15 | LoRA 개념 설명 |
| 15–50 | 학습 4개 실행 (대기 중 품질 비교 준비) |
| 50–75 | 변환·양자화 → Jetson bench + 노트북 perplexity |
| 75–90 | 최종 조합 확정 |

| 담당 | 설정 |
|---|---|
| A | drop4, 2,000개, r16 |
| B | drop4, 8,000개, r16 |
| C | drop6, 8,000개, r16 |
| D | drop6, 8,000개, r64 |
| E (Jetson 운영) | 품질 비교: 같은 질문을 원본 / drop6 / drop6+LoRA에 |

```bash
~/llama.cpp-b11946/build/bin/llama-cli -m <모델>.gguf -ngl 99 -n 200 -no-cnv -p "Explain why the sky is blue in three sentences."
```

## 토론 질문

1. 데이터 4배 vs rank 4배, 어느 쪽이 회복에 더 효과적인가?
2. drop6+LoRA가 drop4(회복 없음)보다 나은가? 그렇다면 "더 깎고 회복"이 정답인가?
3. 지시문으로 학습했는데 wikitext perplexity가 오르는 이유는?

## 활동 후

- [ ] 전원: 해석 한 문단 → `assignments/{이름}/week5/`
- [ ] 세션장: 최종 조합 확정 → **바로 7B에 적용 시작** (`week6/README.md`)
- [ ] 발표 파트 배분: 도입·양자화·pruning·LoRA·결론, 1인 1파트
