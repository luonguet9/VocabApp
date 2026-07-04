@echo off
chcp 65001 > nul
echo  Dang them Vocab Practice Server vao Windows Startup...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\VocabPracticeServer.lnk'); $Shortcut.TargetPath = 'D:\Script\ENG\run.bat'; $Shortcut.WorkingDirectory = 'D:\Script\ENG'; $Shortcut.Description = 'Vocab Practice Server'; $Shortcut.Save()"

if %errorlevel% == 0 (
    echo.
    echo =========================================================================
    echo  Da them thanh cong!
    echo  Tu nay moi lan mo may, file run.bat (Vocab Server) se tu dong chay.
    echo =========================================================================
) else (
    echo.
    echo  Co loi xay ra khi them vao Startup!
)
pause
