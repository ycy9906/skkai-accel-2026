@echo off
REM Copy Week 2 files from ..\models to Jetson ~/models (wired: 10.110.1.3)
REM One password prompt per scp line.
setlocal
set J=skkaiaccel@10.110.1.3
cd /d "%~dp0..\models"
ssh %J% "mkdir -p ~/models"
scp wikitext-2-raw\wiki.test.raw wikitext-2-raw\wiki.train.raw %J%:~/models/
scp qwen2.5-1.5b-instruct-fp16.gguf %J%:~/models/
scp qwen2.5-7b-instruct-q4_k_m*.gguf %J%:~/models/
echo DONE
pause
