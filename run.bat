@echo off
chcp 65001 > nul
title Vocab Practice Server

set PORT=5100
set PYTHONIOENCODING=utf-8

:: --- Kill server cu tren port ---
for /f "tokens=5" %%p in (
    'netstat -ano ^| findstr ":%PORT% " ^| findstr "LISTENING" 2^>nul'
) do (
    taskkill /PID %%p /F /T > nul 2>&1
)

:: --- Kiem tra Python ---
set PYTHON_CMD=
py -m pip --version > nul 2>&1
if %errorlevel% == 0 ( set PYTHON_CMD=py & goto :python_ok )
python -m pip --version > nul 2>&1
if %errorlevel% == 0 ( set PYTHON_CMD=python & goto :python_ok )
echo  Khong tim thay Python!
pause & exit /b

:python_ok

:: --- Kiem tra Flask + Waitress ---
%PYTHON_CMD% -c "import flask, waitress" > nul 2>&1
if %errorlevel% neq 0 (
    echo  Dang cai Flask, Waitress...
    %PYTHON_CMD% -m pip install flask waitress -q
)

:: --- Mo trinh duyet sau 2 giay (tach khoi Python de khong bi kill theo) ---
start /b cmd /c "ping 127.0.0.1 -n 3 > nul & start """" http://localhost:%PORT%"

:: --- Chay server ---
%PYTHON_CMD% -m app.main

