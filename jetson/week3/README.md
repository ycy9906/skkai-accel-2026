# Week 3 — 똑똑한 양자화 (imatrix)

**목표**: 같은 비트에서 중요한 가중치를 아끼면 정확도가 얼마나 회복되나 (AWQ 아이디어 체험)
**산출물**: imatrix 전후 비교표, **최종 양자화 포맷 1개 확정**

새로 받을 파일 없음 (Week 2 파일 + `wiki.train.raw` 사용).

## 세션장 사전 준비

- [ ] Jetson에서 중요도 행렬 생성 (수 분, 당일에 하지 않음)
- [ ] `imatrix.dat`(수 MB)를 팀원에게 배포
- [ ] 리허설: `IQ2_XS` 하나 만들어 Jetson 속도 확인

```bash
cd ~/models
~/llama.cpp-b11946/build/bin/llama-imatrix -m qwen2.5-1.5b-instruct-fp16.gguf -f wiki.train.raw \
  -o imatrix.dat -ngl 99 -c 512 --chunks 100
```

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–10 | AWQ 발표, Week 2 그래프 리뷰 |
| 10–45 | 실험 A: imatrix 양자화 vs 일반 양자화 |
| 45–70 | 실험 B: flash attention, 컨텍스트 길이 (Jetson) |
| 70–90 | 최종 포맷 확정 |

**실험 A** (노트북에서 만들고 perplexity, Jetson은 bench)

| 담당 | 모델 |
|---|---|
| A | Q4_K_M + imatrix |
| B | Q3_K_M + imatrix |
| C | Q2_K + imatrix |
| D | IQ3_XXS, IQ2_XS (imatrix 필수 포맷) |
| E (Jetson 운영) | 위 5개 bench |

```bash
llama-quantize --imatrix imatrix.dat qwen2.5-1.5b-instruct-fp16.gguf q3_k_m-imat.gguf Q3_K_M
```

관찰 포인트: IQ 포맷은 파일이 작지만 압축 해제 계산이 복잡하다. **바이트가 줄었는데 느려지는가?**

**실험 B** (Jetson, Q4_K_M)

```bash
~/llama.cpp-b11946/build/bin/llama-bench -m q4_k_m.gguf -ngl 99 -p 0 -n 128 -fa 0,1 -d 0,1024,4096 -r 3
```

컨텍스트가 길수록 느려지는 이유: 토큰마다 가중치 + **KV cache**도 읽어야 해서.

## 토론 질문

1. imatrix 효과가 가장 큰 비트는?
2. calibration도 wikitext, 평가도 wikitext. 과대평가 가능성은?
3. 최종 포맷은? (Week 4~5 pruning으로 perplexity가 더 오른다는 걸 감안)

## 활동 후

- [ ] 기록 담당: `python scripts/plot_pareto.py 3`
- [ ] 전원: 해석 한 문단 → `assignments/{이름}/week3/`
- [ ] 세션장: `week4/week4_colab.ipynb` 리허설 (Colab, T4)
