# Week 5 — LoRA 회복 학습 (Colab)

**목표**: 레이어를 뺀 모델을 짧게 추가 학습해서, 속도는 유지하고 perplexity를 되돌리기
**산출물**: 회복 전후 비교, **최종 조합 1개 확정** (몇 층 제거 + 학습 설정 + 양자화 포맷)

LoRA = 원래 가중치는 고정하고 작은 행렬 2개(rank r)만 학습. 병합하면 원래 크기로 돌아가므로 Jetson 속도는 거의 그대로여야 정상.

## 세션장 사전 준비

- [ ] `week5_colab.ipynb`를 `N_SAMPLES=2000`으로 리허설 → **학습 셀 소요 시간 기록** (T4는 4090보다 3~4배 느림)
- [ ] 시간이 너무 길면 활동 표의 `N_SAMPLES`를 줄인다
- [ ] 품질 비교용 원본·drop6 `.gguf`를 Jetson에 미리 준비 (Week 4 결과)

열기: Week 4와 같은 방법으로 `jetson/week5/week5_colab.ipynb`, 런타임은 **T4 GPU**

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–10 | LoRA 개념 설명 → 바로 학습 셀 실행 |
| 10–45 | 학습 대기 중: Week 4 결과 토론, 품질 비교 데모 |
| 45–70 | Drive에서 받기 → Jetson bench + 노트북 perplexity |
| 70–90 | 최종 조합 확정 |

| 담당 | 노트북 설정 |
|---|---|
| A | `N_DROP=4, N_SAMPLES=2000, RANK=16` |
| B | `N_DROP=4, N_SAMPLES=4000, RANK=16` |
| C | `N_DROP=6, N_SAMPLES=4000, RANK=16` |
| D | `N_DROP=6, N_SAMPLES=4000, RANK=64` |
| E (Jetson 운영) | 품질 비교: 같은 질문을 원본 / drop6 / drop6+LoRA에 |

```bash
~/llama.cpp-b11946/build/bin/llama-cli -m <모델>.gguf -ngl 99 -n 200 -no-cnv -p "Explain why the sky is blue in three sentences."
```

## 토론 질문

1. 데이터 2배 vs rank 4배, 어느 쪽이 회복에 더 효과적인가?
2. drop6+LoRA가 drop4(회복 없음)보다 나은가? 그렇다면 "더 깎고 회복"이 정답인가?
3. 지시문으로 학습했는데 wikitext perplexity가 오르는 이유는?

## 활동 후

- [ ] 전원: 해석 한 문단 → `assignments/{이름}/week5/`
- [ ] 세션장: 최종 조합 확정 → **4090 서버에서 7B 적용 시작** (`week6/README.md`)
- [ ] 발표 파트 배분: 도입·양자화·pruning·LoRA·결론, 1인 1파트
