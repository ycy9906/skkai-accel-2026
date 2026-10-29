@echo off
REM Week 2 files: 1.5B F16, 1.5B Q4_K_M, 7B Q4_K_M (baseline), wikitext-2
REM Run from this folder (double-click or: download.bat). Saves to ..\models
REM Re-running resumes partial downloads.
setlocal
set HF=https://huggingface.co
set M=%~dp0..\models
if not exist "%M%" mkdir "%M%"
cd /d "%M%"

echo [1/4] wikitext-2 (small)
curl -fL -C - -o wikitext-2-raw-v1.zip %HF%/datasets/ggml-org/ci/resolve/main/wikitext-2-raw-v1.zip || goto :fail
tar -xf wikitext-2-raw-v1.zip || goto :fail

echo [2/4] Qwen2.5-1.5B Q4_K_M (1.1 GB)
curl -fL -C - -o qwen2.5-1.5b-instruct-q4_k_m.gguf %HF%/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf || goto :fail

echo [3/4] Qwen2.5-1.5B F16 (3.6 GB)
curl -fL -C - -o qwen2.5-1.5b-instruct-fp16.gguf %HF%/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-fp16.gguf || goto :fail

echo [4/4] Qwen2.5-7B Q4_K_M (4.7 GB, may be split in 2 files)
set R7=%HF%/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main
curl -fL -C - -o qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf %R7%/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf && curl -fL -C - -o qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf %R7%/qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf && goto :done
echo split files not found, trying single file...
del /q qwen2.5-7b-instruct-q4_k_m-0000*.gguf 2>nul
curl -fL -C - -o qwen2.5-7b-instruct-q4_k_m.gguf %R7%/qwen2.5-7b-instruct-q4_k_m.gguf || goto :fail

:done
echo.
echo DONE. Files in %M%
dir /b "%M%"
pause
exit /b 0

:fail
echo.
echo FAILED. Check the file name on huggingface.co and edit this script.
pause
exit /b 1
