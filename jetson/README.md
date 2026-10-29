# Jetson LLM 압축 프로젝트 (6주)

**목표**: Qwen2.5-7B-Instruct를 Jetson Orin Nano Super에서 돌리고, 압축으로 Q4_K_M 대비 decode 속도(tg128) **1.5배** 달성 (perplexity 증가 10% 이내)

Week 2~5는 1.5B로 기법을 빠르게 실험하고, Week 6에 찾은 조합을 7B에 적용한다.

| 주차 | 목표 | 산출물 |
|---|---|---|
| [1](week1/) | Jetson에 LLM 올리고 기준 속도 측정 | 1.5B Q4_K_M 43.6 tok/s (완료) |
| [2](week2/) | 비트를 줄이면 얼마나 빨라지고 망가지나 | 포맷 8개 속도·정확도 표 + 그래프 |
| [3](week3/) | 같은 비트에서 정확도를 덜 잃는 양자화(imatrix) | 최종 양자화 포맷 확정 |
| [4](week4/) | 레이어를 빼면 얼마나 빨라지고 망가지나 | 2·4·6·8층 제거 결과 |
| [5](week5/) | 레이어 뺀 모델을 LoRA로 회복 | 최종 조합 확정 |
| [6](week6/) | 최종 조합을 7B에 적용, 발표 | 최종 결과표 + 발표 + 데모 |

## 폴더

- `weekN/` : 주차별 안내(README), 다운로드·실험 스크립트
- `results/results.csv` : 팀 공용 결과표 (모든 주차 누적)
- `scripts/` : 공용 스크립트 (그래프)
- `models/` : 모델 파일 저장 위치. **git에 안 올라감** (용량 제한)

## Jetson 접속

| 누구 | 방법 |
|---|---|
| 팀원 | ipTIME 와이파이 → `ssh skkaiaccel@192.168.0.250` → `tmux attach -t lab` |
| 세션장 | 랜 젠더 유선 → `ssh skkaiaccel@10.110.1.3` |

Jetson 재부팅 후 팀원 주소가 사라지면 Jetson에서 `sudo ip addr add 192.168.0.250/24 dev enP8p1s0`

## 측정 규칙

1. 벤치 전 `sudo jetson_clocks` (전원 모드 MAXN_SUPER 유지)
2. 벤치 중에는 `llama-server` 끄고 다른 명령 금지
3. 속도: `llama-bench -ngl 99 -p 512 -n 128 -r 3`
4. 정확도: `llama-perplexity -f wiki.test.raw -c 512 --chunks 40` (모두 같은 설정)
5. 효율 = tg128 ÷ (102 GB/s ÷ 파일 크기 GB)

## 빌린 보드라서 절대 하지 말 것

`sudo apt upgrade`, `sudo apt autoremove`, 재플래시, `gl5-lidar` 네트워크 설정 변경, `skkai` 계정 파일 수정
