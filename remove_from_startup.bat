@echo off
chcp 65001 > nul
echo  Dang xoa Vocab Practice Server khoi Windows Startup...

if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\VocabPracticeServer.lnk" (
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\VocabPracticeServer.lnk"
    echo.
    echo =========================================================================
    echo  Da xoa thanh cong khoi Windows Startup!
    echo =========================================================================
) else (
    echo.
    echo  Khong tim thay shortcut trong Startup (co the chua them hoac da xoa roi).
)
pause
