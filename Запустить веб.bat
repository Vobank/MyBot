@echo off
chcp 65001 >nul
title MoyBot Web
cd /d "%~dp0"
set "PY=C:\Users\VovaPC\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" web\server.py 2>"web\error.log"
echo.
echo Server stopped. Tell the bot if it did not work.
pause >nul
