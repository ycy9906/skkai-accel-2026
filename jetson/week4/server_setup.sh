#!/usr/bin/env bash
# 4090 서버 1회 세팅 (Week 4~6 공용). 서버에서: bash server_setup.sh
set -e
WORK=${WORK:-$HOME/skkai-jetson}
mkdir -p "$WORK" && cd "$WORK"

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install torch transformers datasets safetensors accelerate peft trl bitsandbytes "huggingface_hub[cli]" matplotlib

# llama.cpp: GGUF 변환 스크립트 + 서버용 CUDA 빌드 (7B 양자화·perplexity용)
[ -d llama.cpp ] || git clone --depth 1 https://github.com/ggml-org/llama.cpp
pip install -r llama.cpp/requirements.txt
cmake -S llama.cpp -B llama.cpp/build -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j

# 원본 모델 (HF 형식). 7B는 약 15 GB
huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct --local-dir models/Qwen2.5-1.5B-Instruct
huggingface-cli download Qwen/Qwen2.5-7B-Instruct --local-dir models/Qwen2.5-7B-Instruct

echo "done: $WORK  (다음부터: cd $WORK && source .venv/bin/activate)"
