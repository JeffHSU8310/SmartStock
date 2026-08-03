@echo off
chcp 65001 > NUL
title SmartStock 高效能 AI 智慧股票期貨量化交易平台
echo 正在啟動 SmartStock 量化平台...
python "%~dp0main.py"
pause
