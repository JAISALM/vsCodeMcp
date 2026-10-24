@echo off
rem Daily RAG pipeline (Windows task VsCodeMcp-RagDaily, 08:00 Asia/Calcutta)
rem Task-context fix (2026-10-25): scheduler session cannot write C:\Users\user\AppData\Local\Temp
rem -> pin TEMP/TMP to a workspace dir (sentence_transformers/hf-hub use tempfile).
set TEMP=D:\models\vsCodeMcp\rag\temp
set TMP=D:\models\vsCodeMcp\rag\temp
if not exist "%TEMP%" mkdir "%TEMP%"
set HF_HUB_CACHE=D:\models\vsCodeMcp\rag\hf_cache
set HF_HOME=D:\models\vsCodeMcp\rag\hf_home
"D:\models\vsCodeMcp\rag\.venv\Scripts\python.exe" "D:\models\vsCodeMcp\rag\daily.py" >> "D:\models\vsCodeMcp\rag\news\logs\scheduled.log" 2>&1
