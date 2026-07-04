@echo off
chcp 65001 >nul
echo [BUILD] Đang đóng gói bản Mobile PWA mới nhất...
python create_mobile_app.py
echo.
echo [DONE] Hoàn tất! Nay bạn có thể vuốt làm mới (Refresh) trên iPhone nhé!
pause
