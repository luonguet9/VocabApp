@echo off
chcp 65001 >nul
set /p USER_ID="Nhap ID nguoi dung (vd: luong, khanh) [mac dinh: luong]: "
if "%USER_ID%"=="" set USER_ID=luong
echo [BUILD] Dang dong goi ban Mobile PWA cho %USER_ID%...
python create_mobile_app.py --user %USER_ID%
echo.
echo [DONE] Hoan tat! Nay ban co the vuot lam moi (Refresh) tren iPhone nhe!
pause
