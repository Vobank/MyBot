@echo off
chcp 65001 >nul
title МойБот - личный ИИ-агент
cd /d "%~dp0"
python bot.py
echo.
pause
