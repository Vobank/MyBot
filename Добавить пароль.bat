@echo off
chcp 65001 >nul
title МойБот - добавить пароль (безопасно)
cd /d "%~dp0"
python "Добавить пароль.py"
