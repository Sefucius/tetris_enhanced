"""
PyInstaller 构建脚本 - 将俄罗斯方块打包成可执行文件
作为 Nuitka 的备选方案，PyInstaller 对编译器要求更低

使用方法：
    python build_pyinstaller.py

要求：
    - Python 3.6+
    - PyInstaller: pip install pyinstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 设置控制台编码为 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ==================== 配置 ====================

PROJECT_NAME = "Tetris Enhanced"
MAIN_SCRIPT = "tetris_enhanced.py"
VERSION = "1.0.0"

# PyInstaller 选项
PYINSTALLER_OPTIONS = [
    "--onefile",                       # 打包成单个exe文件
    "--windowed",                      # 无控制台窗口
    "--name=Tetris Enhanced",          # 可执行文件名称
    "--icon=NONE",                     # 图标（暂时无）
    "--clean",                         # 清理临时文件
    "--noconfirm",                     # 不询问确认
    "--distpath=dist",                 # 输出目录
    "--workpath=build/pyinstaller",    # 工作目录
]

# ==================== 函数 ====================

def print_banner():
    """打印横幅"""
    print("=" * 70)
    print(f"  {PROJECT_NAME} - PyInstaller 构建脚本")
    print(f"  版本: {VERSION}")
    print("=" * 70)
    print()

def check_pyinstaller():
    """检查是否安装了PyInstaller"""
    print("检查 PyInstaller...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"PyInstaller 已安装: {result.stdout.strip()}")
            return True
    except Exception:
        pass

    print("PyInstaller 未安装")
    print("\n请运行以下命令安装 PyInstaller:")
    print("  pip install pyinstaller")
    return False

def check_main_script():
    """检查主脚本是否存在"""
    print(f"\n检查主脚本: {MAIN_SCRIPT}")
    if not os.path.exists(MAIN_SCRIPT):
        print(f"找不到主脚本: {MAIN_SCRIPT}")
        print(f"   请确保在项目根目录运行此脚本")
        return False
    print(f"找到主脚本: {MAIN_SCRIPT}")
    return True

def clean_build_dirs():
    """清理旧的构建目录"""
    print(f"\n清理旧的构建目录...")

    dirs_to_clean = [
        "build",
        "dist",
    ]

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  删除: {dir_name}")
            except Exception as e:
                print(f"  删除失败 {dir_name}: {e}")

def build_executable():
    """使用PyInstaller构建可执行文件"""
    print(f"\n开始构建可执行文件...")
    print("=" * 70)

    # 构建命令
    cmd = [sys.executable, "-m", "PyInstaller"] + PYINSTALLER_OPTIONS + [MAIN_SCRIPT]

    print("执行命令:")
    print(" ".join(cmd))
    print()

    # 执行构建
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 70)
        print("构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n构建失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n用户取消构建")
        return False

def find_executable():
    """查找生成的可执行文件"""
    print(f"\n查找生成的可执行文件...")

    # 可能的路径
    possible_paths = [
        Path("dist/Tetris Enhanced.exe"),
        Path("dist/Tetris_Enhanced.exe"),
        Path("dist/tetris_enhanced.exe"),
    ]

    for path in possible_paths:
        if path.exists():
            print(f"找到可执行文件: {path}")
            return path

    print("未找到生成的可执行文件")
    return None

def show_result(executable_path):
    """显示构建结果"""
    print("\n" + "=" * 70)
    print("构建完成！")
    print("=" * 70)
    print(f"\n可执行文件位置:")
    print(f"  {os.path.abspath(executable_path)}")
    print(f"\n文件大小: {get_file_size(executable_path)}")
    print(f"\n下一步:")
    print("  1. 测试运行可执行文件")
    print("  2. 运行 python build_release.py 创建完整发布包")
    print("  3. 将 dist/ 目录压缩成 .zip 文件发布")
    print("=" * 70)

def get_file_size(file_path):
    """获取文件大小的友好显示"""
    size = os.path.getsize(file_path)

    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

    return f"{size:.2f} TB"

# ==================== 主函数 ====================

def main():
    """主函数"""
    print_banner()

    # 检查环境
    if not check_pyinstaller():
        return 1
    if not check_main_script():
        return 1

    # 询问是否清理
    print(f"\n是否清理旧的构建目录? (y/N): ")
    try:
        choice = input().strip().lower()
        if choice == 'y':
            clean_build_dirs()
    except:
        clean_build_dirs()

    # 构建可执行文件
    if not build_executable():
        return 1

    # 查找可执行文件
    exe_path = find_executable()
    if not exe_path:
        return 1

    # 显示结果
    show_result(exe_path)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
