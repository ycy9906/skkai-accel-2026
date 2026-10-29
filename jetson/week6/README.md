# Week 6 — 7B 적용과 최종 발표

**목표**: Week 2~5에서 찾은 조합을 **Qwen2.5-7B**에 적용해 Jetson에 올리고, 7B Q4_K_M 기준선 대비 1.5배 달성 여부 발표
**산출물**: 최종 결과표, 발표, 라이브 데모

7B는 무거워서 **활동 전 1주 동안** 세션장이 **4090 서버**에서 미리 만든다 (Colab 무료로는 메모리 부족). 서버 스크립트는 `server/` 폴더에 있다.

처음 한 번: 서버에 이 레포를 클론하고 `cd jetson/week6/server && bash server_setup.sh` (venv, llama.cpp 빌드, 원본 모델 다운로드). 이후 명령은 그 작업 폴더(`~/skkai-jetson`)에서 실행하며, `server/`의 `.py`·`.sh`를 그 폴더로 복사해 둔다.

## 사전 준비 (Week 5 직후 ~ 활동 전날)

7B는 F16(15 GB)·Q8_0(8.1 GB)이 Jetson에 안 올라간다. **perplexity는 서버에서** 잰다.

```bash
cd ~/skkai-jetson && source .venv/bin/activate
# 1) 레이어 제거 (Week 5에서 정한 층 수 비율대로, 예: 28층 중 6)
python prune_layers.py models/Qwen2.5-7B-Instruct 6
# 2) QLoRA 회복 (4bit 로드, 병합은 bf16)
python lora_recover.py models/Qwen2.5-7B-Instruct-drop6 8000 16 --4bit
# 3) GGUF 변환 → imatrix → 양자화 (Week 3 확정 포맷)
python llama.cpp/convert_hf_to_gguf.py models/Qwen2.5-7B-Instruct-drop6-lora-8000-r16 --outfile gguf/7b-final-f16.gguf --outtype f16
llama.cpp/build/bin/llama-imatrix -m gguf/7b-final-f16.gguf -f wiki.train.raw -o gguf/7b-final.imatrix -ngl 99 -c 512 --chunks 100
llama.cpp/build/bin/llama-quantize --imatrix gguf/7b-final.imatrix gguf/7b-final-f16.gguf gguf/7b-final-q.gguf <포맷>
# 4) perplexity (서버): 기준선과 최종 모델 모두
llama.cpp/build/bin/llama-perplexity -m gguf/7b-final-q.gguf -f wiki.test.raw -c 512 --chunks 40 -ngl 99
```

- [ ] 최종 7B 모델을 Jetson `~/models/final/`로 (서버 → 노트북 → Jetson)
- [ ] Jetson에서 실행 중 `free -h` 확인, 부족하면 `-c 2048`
- [ ] 발표 파트 취합 (활동 전날까지)

## 활동 (90분)

| 시간 | 내용 |
|---|---|
| 0–20 | 최종 측정: 7B 기준 vs 7B 최종, `-r 5` |
| 20–35 | 라이브 데모: 1.5B / 7B 원본 / 7B 최종에 같은 질문, tegrastats |
| 35–70 | 발표 리허설 (1인 1파트, 5–7분) |
| 70–90 | 회고, 다음 학기 방향 |

## 최종 결과표

| 모델 | 크기 (GB) | tg128 (tok/s) | 효율 | perplexity | 비고 |
|---|---|---|---|---|---|
| 1.5B Q4_K_M | 1.12 | 43.6 | 48% |  | 연습 기준 |
| 7B Q4_K_M | 약 4.7 |  |  |  | 최종 기준 |
| 7B 최종 |  |  |  |  | 목표: 기준 × 1.5 |

## 활동 후

- [ ] 레포 `jetson/README.md`에 최종 결과와 그래프 추가
- [ ] 보드 반납 협의: 전원 모드 MAXN_SUPER 확인, 설치한 패키지·`skkaiaccel` 계정 처리, GS308·공유기 분리
