#!/usr/bin/env bash
# HF 모델 폴더 -> F16 GGUF -> 양자화 GGUF (서버에서)
# 사용: bash to_gguf.sh models/Qwen2.5-1.5B-Instruct-drop4 Q4_K_M [imatrix.dat]
set -e
mkdir -p gguf
SRC=${1%/}; Q=${2:-Q4_K_M}; IM=$3
NAME=$(basename "$SRC" | tr 'A-Z' 'a-z')
python llama.cpp/convert_hf_to_gguf.py "$SRC" --outfile "gguf/$NAME-f16.gguf" --outtype f16
if [ -n "$IM" ]; then
  llama.cpp/build/bin/llama-quantize --imatrix "$IM" "gguf/$NAME-f16.gguf" "gguf/$NAME-${Q,,}.gguf" "$Q"
else
  llama.cpp/build/bin/llama-quantize "gguf/$NAME-f16.gguf" "gguf/$NAME-${Q,,}.gguf" "$Q"
fi
ls -lh "gguf/$NAME-${Q,,}.gguf"
