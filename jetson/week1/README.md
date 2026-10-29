# Week 1 — Jetson에 LLM 올리기 (완료, 2026-10-28)

| 항목 | 결과 |
|---|---|
| 보드 | Jetson Orin Nano (JetPack R36.5, MAXN_SUPER, 102 GB/s) |
| 모델 | Qwen2.5-1.5B-Instruct Q4_K_M (1.04 GiB = 1.12 GB) |
| tg128 (GPU) | **43.64 tok/s** → 이론 상한 91의 48% |
| tg128 (CPU, `-ngl 0`) | 23.68 tok/s → 26% |
| pp512 (GPU) | 1926 tok/s |

**결론**: decode는 메모리 대역폭이 천장이다. CPU와 GPU가 같은 메모리를 써서 차이는 1.8배뿐이고, prefill(연산 위주)에서는 GPU가 압도한다.

## 이번 주에 한 환경 세팅 (참고)

- 계정 `skkaiaccel` 생성 (sudo, video 그룹)
- 인터넷이 없어서 CUDA 컴파일러(nvcc 12.6)와 cuBLAS 개발 패키지를 노트북에서 받아 `dpkg -i`로 설치
- llama.cpp b11946 소스를 옮겨 CUDA 빌드: `~/llama.cpp-b11946/build/bin/`
- 네트워크: Jetson 유선(10.110.1.3, 모빌리티팀 라이다 설정 그대로) + GS308 스위치 + ipTIME 공유기, Jetson에 192.168.0.250 임시 주소 추가
