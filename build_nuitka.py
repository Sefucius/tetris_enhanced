"""
Nuitka 构建脚本 - 将俄罗斯方块打包成高性能可执行文件
使用 Nuitka 编译器，性能提升30%-300%

使用方法：
    python build_nuitka.py

要求：
    - Python 3.6+
    - Nuitka: pip install nuitka
    - C编译器: MinGW64 或 Visual Studio (已检测到您的系统已安装 MinGW64)
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

# 项目信息
PROJECT_NAME = "Tetris Enhanced"
MAIN_SCRIPT = "tetris_enhanced.py"
VERSION = "1.0.0"

# Nuitka 构建选项
NUITKA_OPTIONS = [
    "--standalone",                    # 独立可执行文件
    "--onefile",                       # 打包成单个exe文件
    "--windows-disable-console",       # 禁用控制台窗口
    # "--enable-plugin=pygame",        # 移除：Nuitka 2.x 不再需要单独的 pygame 插件
    "--include-package=dataclasses",   # 包含dataclasses模块
    "--include-package=pygame",        # 包含pygame包（新版用 --include-package）

    # 性能优化选项
    "--follow-imports",                # 跟随所有导入

    # 输出选项
    "--output-dir=build",              # 输出到build目录
    "--remove-output",                 # 构建完成后删除临时文件

    # 其他选项
    "--assume-yes-for-downloads",      # 自动确认下载依赖
]

# ==================== 函数 ====================

def print_banner():
    """打印横幅"""
    print("=" * 70)
    print(f"  {PROJECT_NAME} - Nuitka 构建脚本")
    print(f"  版本: {VERSION}")
    print("=" * 70)
    print()

def check_nuitka():
    """检查是否安装了Nuitka"""
    print("🔍 检查 Nuitka...")
    try:
        import nuitka
        # 尝试获取版本
        try:
            from nuitka.Version import getNuitkaVersion
            version = getNuitkaVersion()
            print(f"✅ Nuitka 已安装: {version}")
        except:
            print(f"✅ Nuitka 已安装")
        return True
    except ImportError:
        pass

    print("❌ Nuitka 未安装")
    print("\n请运行以下命令安装 Nuitka:")
    print("  pip install nuitka")
    return False

def check_main_script():
    """检查主脚本是否存在"""
    print(f"\n🔍 检查主脚本: {MAIN_SCRIPT}")
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ 找不到主脚本: {MAIN_SCRIPT}")
        print(f"   请确保在项目根目录运行此脚本")
        return False
    print(f"✅ 找到主脚本: {MAIN_SCRIPT}")
    return True

def check_compiler():
    """检查C编译器"""
    print(f"\n🔍 检查 C 编译器...")
    try:
        result = subprocess.run(
            ["gcc", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ C 编译器已安装: {version}")
            return True
    except Exception:
        pass

    print("❌ 未找到 C 编译器 (GCC)")
    print("   请安装 MinGW64 或 Visual Studio")
    return False

def clean_build_dirs():
    """清理旧的构建目录"""
    print(f"\n🧹 清理旧的构建目录...")

    dirs_to_clean = [
        "build",
        f"{MAIN_SCRIPT}.dist",
        f"{MAIN_SCRIPT}.build",
        f"{MAIN_SCRIPT}.onefile-build",
    ]

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✓ 删除: {dir_name}")
            except Exception as e:
                print(f"  ✗ 删除失败 {dir_name}: {e}")

def build_executable():
    """使用Nuitka构建可执行文件"""
    print(f"\n🚀 开始构建可执行文件...")
    print("=" * 70)

    # 构建命令 - 直接使用 Python 调用 nuitka
    nuitka_args = NUITKA_OPTIONS + [MAIN_SCRIPT]
    cmd = [sys.executable, "-m", "nuitka"] + nuitka_args

    print("执行命令:")
    print(" ".join(cmd))
    print()

    # 执行构建
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 70)
        print("✅ 构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 构建失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消构建")
        return False

def find_executable():
    """查找生成的可执行文件"""
    print(f"\n🔍 查找生成的可执行文件...")

    # 可能的路径
    possible_paths = [
        Path(f"build/{MAIN_SCRIPT.replace('.py', '.exe')}"),
        Path(f"build/{MAIN_SCRIPT.replace('.py', '.dist')}/{MAIN_SCRIPT.replace('.py', '.exe')}"),
        Path(f"{MAIN_SCRIPT}.dist/{MAIN_SCRIPT.replace('.py', '.exe')}"),
    ]

    for path in possible_paths:
        if path.exists():
            print(f"✅ 找到可执行文件: {path}")
            return path

    print("❌ 未找到生成的可执行文件")
    return None

def copy_to_dist(executable_path):
    """复制可执行文件到dist目录"""
    print(f"\n📦 准备发布包...")

    # 创建dist目录
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    # 复制可执行文件
    target_name = f"Tetris_Enhanced_v{VERSION}.exe"
    target_path = dist_dir / target_name

    try:
        shutil.copy2(executable_path, target_path)
        print(f"✅ 复制到: {target_path}")
        return target_path
    except Exception as e:
        print(f"❌ 复制失败: {e}")
        return None

def show_result(executable_path):
    """显示构建结果"""
    print("\n" + "=" * 70)
    print("🎉 构建完成！")
    print("=" * 70)
    print(f"\n可执行文件位置:")
    print(f"  {os.path.abspath(executable_path)}")
    print(f"\n文件大小: {get_file_size(executable_path)}")
    print(f"\n📁 发布文件位于: dist/")
    print("\n下一步:")
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
    if not check_nuitka():
        return 1
    if not check_main_script():
        return 1
    if not check_compiler():
        print("\n⚠️  警告: 未找到C编译器，但将继续尝试构建...")

    # 询问是否清理
    print(f"\n是否清理旧的构建目录? (y/N): ", end='')
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

    # 复制到dist目录
    final_path = copy_to_dist(exe_path)
    if not final_path:
        return 1

    # 显示结果
    show_result(final_path)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
