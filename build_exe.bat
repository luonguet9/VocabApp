@echo off
chcp 65001 > nul
echo Building Vocab Practice Server Executable...

set PYINSTALLER_CMD=
if exist "C:\Users\luong\AppData\Local\Python\pythoncore-3.14-64\Scripts\pyinstaller.exe" (
    set PYINSTALLER_CMD="C:\Users\luong\AppData\Local\Python\pythoncore-3.14-64\Scripts\pyinstaller.exe"
) else (
    py -m PyInstaller --version > nul 2>&1
    if %errorlevel% == 0 ( set PYINSTALLER_CMD=py -m PyInstaller ) else ( set PYINSTALLER_CMD=python -m PyInstaller )
)

%PYINSTALLER_CMD% --noconfirm --onefile --add-data "app/templates;templates/" --hidden-import waitress --hidden-import flask "app/main.py" --name "VocabServer"

echo.
echo ========================================================
echo Build Complete! File exe nam trong thu muc dist/VocabServer.exe
echo ========================================================
pause
