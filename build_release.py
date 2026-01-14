"""
发布包生成脚本 - 创建完整的游戏发布包

使用方法：
    python build_release.py

功能：
    1. 复制可执行文件到发布目录
    2. 生成说明文档
    3. 打包成 ZIP 文件
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 设置控制台编码为 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ==================== 配置 ====================

PROJECT_NAME = "Tetris Enhanced"
VERSION = "1.0.0"
AUTHOR = "Sefucius"
GITHUB_URL = "https://github.com/Sefucius/tetris_enhanced"

# 文件配置
EXECUTABLE_NAME = f"Tetris Enhanced.exe"
README_FILE = "README_RELEASE.txt"
USER_GUIDE_FILE = "使用指南.txt"

# ==================== 函数 ====================

def print_banner():
    """打印横幅"""
    print("=" * 70)
    print(f"  {PROJECT_NAME} - 发布包生成脚本")
    print(f"  版本: {VERSION}")
    print("=" * 70)
    print()

def get_executable_path():
    """查找可执行文件"""
    print("🔍 查找可执行文件...")

    # 可能的路径
    possible_paths = [
        Path("dist") / EXECUTABLE_NAME,
        Path(f"build/Tetris_Enhanced_v{VERSION}.exe"),
        Path(f"build/tetris_enhanced.exe"),
        Path(f"tetris_enhanced.dist/tetris_enhanced.exe"),
    ]

    for path in possible_paths:
        if path.exists():
            print(f"✅ 找到: {path}")
            return path

    print("❌ 未找到可执行文件")
    print("   请先运行 python build_nuitka.py 或 build.bat")
    return None

def create_release_dir():
    """创建发布目录"""
    release_dir = Path(f"release/Tetris_Enhanced_v{VERSION}")

    # 清理旧的发布目录
    if release_dir.exists():
        shutil.rmtree(release_dir)
        print(f"🧹 清理旧的发布目录")

    # 创建新的发布目录
    release_dir.mkdir(parents=True)
    print(f"📁 创建发布目录: {release_dir}")

    return release_dir

def create_readme():
    """创建发布说明文档"""
    content = f"""
{'=' * 70}
  {PROJECT_NAME} v{VERSION}
{'=' * 70}

感谢您下载 {PROJECT_NAME}！

📮 官方仓库: {GITHUB_URL}
👤 开发者: {AUTHOR}
📅 发布日期: {datetime.now().strftime('%Y-%m-%d')}

{'=' * 70}
🚀 快速开始
{'=' * 70}

1. 双击运行 {EXECUTABLE_NAME}
2. 按空格键或回车键开始游戏
3. 使用方向键控制方块
4. 尽情享受游戏！

{'=' * 70}
🕹️ 游戏控制
{'=' * 70}

基础操作:
  ← →     左右移动
  ↑       旋转方块
  ↓       加速下落
  空格    直接落地

系统功能:
  ESC     设置菜单
  P       暂停/继续
  R       重新开始（切换主题）
  N       切换霓虹模式
  M       静音/取消静音
  TAB     查看统计面板
  H       查看成就面板
  Q       退出游戏

{'=' * 70}
✨ 游戏特色
{'=' * 70}

🎨 6个独特的主题
   - 霓虹城市（赛博朋克）
   - 太空科幻（深邃星空）
   - 复古像素（8-bit怀旧）
   - 海洋世界（动态波浪）
   - 日落黄昏（温暖小调）
   - 森林秘境（极光效果）

🎵 动态音乐系统
   - 程序生成背景音乐
   - 每个主题独特旋律
   - 多种调式和风格

🏆 完整的游戏系统
   - 连击系统和特效
   - 统计数据和排行榜
   - 成就系统
   - 幽灵方块预览
   - 霓虹发光模式

{'=' * 70}
⚙️ 设置
{'=' * 70}

游戏中按 ESC 打开设置菜单，可以调整：
  - 音效开关
  - 背景音乐
  - 音乐音量
  - 音效音量
  - 幽灵方块
  - 霓虹模式
  - 主题选择

{'=' * 70}
📊 评分系统
{'=' * 70}

  单行消除: 100 × 等级
  双行消除: 300 × 等级
  三行消除: 500 × 等级
  四行消除: 800 × 等级
  连击奖励: 额外加分

每消除 10 行升一级，速度会逐渐加快！

{'=' * 70}
💾 数据存储
{'=' * 70}

游戏数据会自动保存在游戏目录下：
  - tetris_settings.json      (游戏设置)
  - tetris_keybinds.json      (键位绑定)
  - tetris_statistics.json    (统计数据)
  - tetris_achievements.json  (成就记录)
  - tetris_leaderboard.json   (排行榜)

{'=' * 70}
❓ 常见问题
{'=' * 70}

Q: 背景音乐不播放？
A: 在设置中开启"背景音乐"开关，检查音量设置

Q: 游戏运行缓慢？
A: 关闭霓虹模式（按N键），降低窗口大小

Q: 如何切换主题？
A: 按R重新开始会自动切换，或在设置菜单中选择

Q: 如何重置所有数据？
A: 在设置菜单点击"恢复所有数据到出厂设置"

{'=' * 70}
📞 获取帮助
{'=' * 70}

如有问题或建议，请访问:
  {GITHUB_URL}

{'=' * 70}
📄 许可证
{'=' * 70}

MIT License

{'=' * 70}
祝您游戏愉快！🎉
{'=' * 70}
"""

    return content.strip() + "\n"

def copy_user_guide():
    """复制使用指南"""
    source = Path("使用指南.md")
    if source.exists():
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def create_release_package(release_dir, executable_path):
    """创建发布包"""
    print(f"\n📦 创建发布包...")

    # 1. 复制可执行文件
    target_exe = release_dir / EXECUTABLE_NAME
    shutil.copy2(executable_path, target_exe)
    print(f"  ✓ 复制可执行文件: {EXECUTABLE_NAME}")

    # 2. 创建README
    readme_path = release_dir / README_FILE
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(create_readme())
    print(f"  ✓ 创建: {README_FILE}")

    # 3. 复制使用指南（如果存在）
    user_guide = copy_user_guide()
    if user_guide:
        guide_path = release_dir / USER_GUIDE_FILE
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(user_guide)
        print(f"  ✓ 创建: {USER_GUIDE_FILE}")

    # 4. 计算总大小
    total_size = sum(f.stat().st_size for f in release_dir.rglob('*') if f.is_file())
    print(f"\n📊 发布包大小: {format_size(total_size)}")

    return release_dir

def create_zip_archive(release_dir):
    """创建ZIP压缩包"""
    print(f"\n🗜️  创建ZIP压缩包...")

    zip_name = f"Tetris_Enhanced_v{VERSION}.zip"
    zip_path = Path("release") / zip_name

    # 删除旧的zip文件
    if zip_path.exists():
        zip_path.unlink()

    # 创建新的zip文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in release_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(release_dir.parent)
                zipf.write(file, arcname)
                print(f"  ✓ 添加: {file.name}")

    zip_size = zip_path.stat().st_size
    print(f"\n✅ 压缩包创建成功: {zip_name}")
    print(f"   文件大小: {format_size(zip_size)}")
    print(f"   位置: {zip_path.absolute()}")

    return zip_path

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def show_result(zip_path):
    """显示结果"""
    print("\n" + "=" * 70)
    print("🎉 发布包创建成功！")
    print("=" * 70)
    print(f"\n📦 发布文件: {zip_path.name}")
    print(f"📍 位置: {zip_path.absolute()}")
    print(f"\n📂 发布目录内容:")
    print(f"   - {EXECUTABLE_NAME}")
    print(f"   - {README_FILE}")
    print(f"   - {USER_GUIDE_FILE}")
    print(f"\n🚀 下一步:")
    print(f"   1. 测试运行 release/ 目录中的可执行文件")
    print(f"   2. 将 {zip_path.name} 上传到网盘或GitHub Releases")
    print(f"   3. 分享给朋友们下载游玩！")
    print("=" * 70)

# ==================== 主函数 ====================

def main():
    """主函数"""
    print_banner()

    # 查找可执行文件
    exe_path = get_executable_path()
    if not exe_path:
        return 1

    # 创建发布目录
    release_dir = create_release_dir()

    # 创建发布包
    create_release_package(release_dir, exe_path)

    # 创建ZIP压缩包
    zip_path = create_zip_archive(release_dir)

    # 显示结果
    show_result(zip_path)

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
