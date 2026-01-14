@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   推送代码到 GitHub
echo ========================================
echo.

cd /d "E:\Claude Code\Demo\tetris_enhanced"

echo 检查状态...
git status
echo.

echo 推送到 GitHub...
GIT_SSH_COMMAND="ssh -i C:\Users\86131\.ssh\id_ed25519_tetris" git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   推送成功！
    echo ========================================
) else (
    echo.
    echo ========================================
    echo   推送失败！
    echo ========================================
)

echo.
echo 按任意键关闭...
pause >nul
