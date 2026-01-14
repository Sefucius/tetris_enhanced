@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   俄罗斯方块 - Nuitka 构建脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.6 或更高版本
    pause
    exit /b 1
)

REM 检查 Nuitka 是否安装
python -m Nuitka --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Nuitka 未安装，正在安装...
    pip install nuitka
    if errorlevel 1 (
        echo ❌ Nuitka 安装失败
        pause
        exit /b 1
    )
)

REM 检查 GCC 编译器
gcc --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告: 未找到 GCC 编译器
    echo 构建可能会失败，请安装 MinGW64 或 Visual Studio
    echo.
)

echo ✅ 环境检查完成
echo.
echo 开始构建...
echo.

REM 执行构建脚本
python build_nuitka.py

if errorlevel 1 (
    echo.
    echo ❌ 构建失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 构建成功！
echo ========================================
echo.
echo 可执行文件位于: dist\
echo.
echo 按任意键关闭此窗口...
pause >nul
