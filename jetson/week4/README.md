# Week 4 — Pruning

**목표**: 레이어를 빼면 빨라지고, 0으로 만들면 안 빨라진다는 걸 숫자로 확인
**산출물**: 2·4·6·8층 제거 모델 + magnitude 50% 모델의 크기·속도·perplexity

모든 생성 작업은 **4090 서버**에서 한다. Jetson은 인터넷이 없어서 결과 파일은 **서버 → 노트북 → Jetson** 순서로 옮긴다.

## 세션장 사전 준비 (Week 3 직후부터)

- [ ] 서버에서 `bash server_setup.sh` (venv, llama.cpp 빌드, 1.5B·7B 원본 다운로드)
- [ ] 이 폴더의 `.py`, `.sh`를 서버 작업 폴더(`~/skkai-jetson`)에 복사
- [ ] 리허설: drop 2 하나를 끝까지 (생성 → 변환 → 양자화 → Jetson bench)
- [ ] 팀원 4명 서버 계정·SSH 접속 확인

```bash
cd ~/skkai-jetson && source .venv/bin/activate
python prune_layers.py models/Qwen2.5-1.5B-Instruct 4
bash to_gguf.sh models/Qwen2.5-1.5B-Instruct-drop4 Q4_K_M   # Week 3 확정 포맷으로 바꿔서
```

pruning한 모델은 원본 `imatrix.dat`과 층 수가 달라서 그대로는 못 쓴다. imatrix가 필요한 포맷이면 그 모델의 F16으로 imatrix를 새로 만든다.

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–10 | LUT-GEMM 발표 |
| 10–40 | 각자 서버에서 맡은 모델 생성 → 변환 → 양자화 → 노트북으로 받기 |
| 40–70 | Jetson bench + 노트북 perplexity |
| 70–90 | 그래프 갱신, Week 5 회복 대상 선정 |

| 담당 | 모델 |
|---|---|
| A | drop 2 (26층) |
| B | drop 4 (24층) |
| C | drop 6 (22층) |
| D | drop 8 (20층) |
| E (Jetson 운영) | magnitude 50% + 전체 bench |

## 토론 질문

1. 레이어를 25% 뺐는데 파일은 왜 25%보다 덜 줄었나? (힌트: 임베딩·출력층)
2. magnitude 50%는 크기도 속도도 그대로다. 무엇이 있어야 빨라지나? (힌트: Ampere 2:4 sparsity)
3. 제거된 레이어는 앞쪽인가 뒤쪽인가?

## 활동 후

- [ ] 전원: 해석 한 문단 → `assignments/{이름}/week4/`
- [ ] 세션장: Week 5 회복 대상 2개 확정 (보통 drop 4, drop 6)
- [ ] 세션장: `week5/lora_recover.py` 리허설 1회
