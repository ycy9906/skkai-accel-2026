# Week 4 — Pruning (Colab)

**목표**: 레이어를 빼면 빨라지고, 0으로 만들면 안 빨라진다는 걸 숫자로 확인
**산출물**: 2·4·6·8층 제거 모델 + magnitude 50% 모델의 크기·속도·perplexity

팀원 전원이 **각자 구글 계정의 Colab(T4 GPU)**에서 동시에 실험한다. 서버 계정·설치 필요 없음.

## 세션장 사전 준비

- [ ] `week4_colab.ipynb`를 Colab에서 열어 `N_DROP=2`로 끝까지 리허설 (약 10분)
- [ ] 나온 `.gguf`를 Jetson에 옮겨 bench까지 확인
- [ ] 팀원 공지: 구글 계정 로그인, Drive 여유 공간 5GB 이상

**Colab에서 여는 법**: colab.research.google.com → 파일 → 노트북 열기 → GitHub 탭 → `ycy9906/skkai-accel-2026` → `jetson/week4/week4_colab.ipynb`
→ 런타임 → 런타임 유형 변경 → **T4 GPU** → 위에서부터 셀 실행

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–10 | LUT-GEMM 발표 |
| 10–35 | 각자 Colab 실행 (맡은 설정만 바꾸고 셀 실행) |
| 35–45 | Drive에서 `.gguf` 받기 → Jetson 운영자에게 전달 (`scp`) |
| 45–70 | Jetson bench + 노트북 perplexity |
| 70–90 | 그래프 갱신, Week 5 회복 대상 선정 |

| 담당 | 노트북 설정 |
|---|---|
| A | `MODE="layers"`, `N_DROP=2` (26층) |
| B | `MODE="layers"`, `N_DROP=4` (24층) |
| C | `MODE="layers"`, `N_DROP=6` (22층) |
| D | `MODE="layers"`, `N_DROP=8` (20층) |
| E (Jetson 운영) | `MODE="magnitude"` + 전체 bench |

```bash
# Jetson으로 옮기기 (노트북 cmd, 내려받은 폴더에서)
scp qwen1p5b-drop4-q4_k_m.gguf skkaiaccel@192.168.0.250:~/models/
# 속도 (Jetson)
~/llama.cpp-b11946/build/bin/llama-bench -m ~/models/qwen1p5b-drop4-q4_k_m.gguf -ngl 99 -p 512 -n 128 -r 3
# 정확도 (각자 노트북)
llama-perplexity -m qwen1p5b-drop4-q4_k_m.gguf -f wiki.test.raw -c 512 --chunks 40
```

Colab 노트북에서는 imatrix가 필요한 포맷(IQ 계열)을 못 만든다. Week 3에서 IQ 포맷으로 확정했다면 `SAVE_F16=True`로 F16을 받아 Jetson에서 imatrix를 만들고 양자화한다.

## 토론 질문

1. 레이어를 25% 뺐는데 파일은 왜 25%보다 덜 줄었나? (힌트: 임베딩·출력층)
2. magnitude 50%는 크기도 속도도 그대로다. 무엇이 있어야 빨라지나? (힌트: Ampere 2:4 sparsity)
3. 제거된 레이어는 앞쪽인가 뒤쪽인가? (노트북 출력의 `drop layers` 확인)

## 활동 후

- [ ] 전원: 해석 한 문단 → `assignments/{이름}/week4/`
- [ ] 세션장: Week 5 회복 대상 확정 (보통 drop 4, drop 6), `week5_colab.ipynb` 리허설
