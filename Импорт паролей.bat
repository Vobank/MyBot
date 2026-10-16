@echo off
chcp 65001 >nul
title МойБот - импорт паролей из файла
cd /d "%~dp0"
python "Импорт паролей.py"
