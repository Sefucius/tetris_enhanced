# 🏗️ 构建说明文档

本文档说明如何将俄罗斯方块游戏打包成独立的可执行文件。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [快速开始](#快速开始)
3. [详细步骤](#详细步骤)
4. [常见问题](#常见问题)

---

## 💻 系统要求

### 开发环境（您的电脑）

- **Python**: 3.6 或更高版本
- **Nuitka**: `pip install nuitka`
- **C编译器**: MinGW64 或 Visual Studio
  - 您的系统已经安装了 MinGW64 (GCC 8.1.0)
- **操作系统**: Windows 10/11

### 运行环境（用户的电脑）

- **操作系统**: Windows 10/11
- **不需要**: Python 或任何其他依赖

---

## 🚀 快速开始

### 方法一：一键构建（推荐）

双击运行 `build.bat` 文件，脚本会自动完成所有步骤。

```bash
# 或者在命令行中运行
build.bat
```

### 方法二：使用 Python 脚本

```bash
# 1. 安装 Nuitka（首次运行）
pip install nuitka

# 2. 构建可执行文件
python build_nuitka.py

# 3. 创建发布包
python build_release.py
```

---

## 📝 详细步骤

### 步骤 1: 安装 Nuitka

Nuitka 是一个 Python 编译器，可以将 Python 代码编译成 C 代码再编译成机器码。

```bash
pip install nuitka
```

**验证安装：**
```bash
python -m nuitka --version
```

### 步骤 2: 构建可执行文件

运行构建脚本：

```bash
python build_nuitka.py
```

**脚本会执行以下操作：**
1. ✅ 检查 Nuitka 是否安装
2. ✅ 检查主脚本是否存在
3. ✅ 检查 C 编译器
4. 🧹 清理旧的构建目录（可选）
5. 🔨 使用 Nuitka 编译代码
6. 📦 将可执行文件复制到 `dist/` 目录

**构建时间：** 约 5-15 分钟（取决于 CPU 性能）

**输出文件：**
```
dist/
  └── Tetris_Enhanced_v1.0.0.exe  (30-50 MB)
```

### 步骤 3: 测试可执行文件

双击运行 `dist/Tetris_Enhanced_v1.0.0.exe`，确保游戏正常运行。

### 步骤 4: 创建发布包

运行发布包生成脚本：

```bash
python build_release.py
```

**脚本会执行以下操作：**
1. 📁 创建 `release/` 目录
2. 📋 复制可执行文件
3. 📄 生成说明文档
4. 🗜️ 打包成 ZIP 文件

**输出文件：**
```
release/
  ├── Tetris_Enhanced_v1.0.0.zip       ← 分发给用户的压缩包
  └── Tetris_Enhanced_v1.0.0/
      ├── Tetris_Enhanced.exe
      ├── README_RELEASE.txt
      └── 使用指南.txt
```

### 步骤 5: 分发游戏

将 `release/Tetris_Enhanced_v1.0.0.zip` 文件分享给用户。

**用户只需：**
1. 下载 ZIP 文件
2. 解压到任意文件夹
3. 双击 `Tetris_Enhanced.exe` 开始游戏

---

## 🔧 构建选项说明

### Nuitka 主要选项

在 `build_nuitka.py` 中配置的选项：

| 选项 | 说明 |
|------|------|
| `--standalone` | 创建独立可执行文件 |
| `--onefile` | 打包成单个 exe 文件 |
| `--windows-disable-console` | 不显示控制台窗口 |
| `--enable-plugin=pygame` | 启用 Pygame 支持 |
| `--follow-imports` | 包含所有导入的模块 |
| `--output-dir=build` | 输出到 build 目录 |

### 性能优化

Nuitka 相比 PyInstaller 的优势：

- ✅ **性能提升 30%-300%**：代码被编译成机器码
- ✅ **体积更小**：优化后的可执行文件更小
- ✅ **启动更快**：不需要解释 Python 代码
- ✅ **更安全**：编译后的代码更难反编译

---

## ❓ 常见问题

### Q1: 构建失败，提示找不到编译器

**解决方案：**
```bash
# 检查 GCC 是否安装
gcc --version

# 如果未安装，下载 MinGW64
# https://github.com/niXman/mingw-builds-binaries/releases
```

### Q2: 构建时间太长

**正常情况：**
- 首次构建：10-20 分钟（Nuitka 需要编译）
- 后续构建：5-10 分钟（有缓存）

**加速方法：**
- 使用 SSD 硬盘
- 关闭杀毒软件（构建时）
- 使用多核 CPU

### Q3: 可执行文件体积太大

**体积参考：**
- PyInstaller: 50-80 MB
- Nuitka: 30-50 MB
- 正常范围：包含 Python 运行时 + Pygame 库

**优化方法：**
```bash
# 在 build_nuitka.py 中添加
--include-package-only=pygame  # 只包含需要的包
```

### Q4: 杀毒软件报毒

**原因：**
- PyInstaller/Nuitka 打包的程序有时会被误报

**解决方案：**
1. 在杀毒软件中添加白名单
2. 使用 Nuitka（误报率更低）
3. 对文件进行数字签名（需要证书）

### Q5: 游戏运行时缺少 DLL

**原因：**
- `--onefile` 选项会自动包含所有依赖
- 如果仍有问题，使用 `--standalone` 代替

**解决方案：**
编辑 `build_nuitka.py`，移除 `--onefile` 选项：
```python
NUITKA_OPTIONS = [
    "--standalone",
    # "--onefile",  # 注释掉这一行
    ...
]
```

这会生成一个文件夹，包含所有 DLL 文件。

---

## 📊 性能对比

### 不同打包方式对比

| 方案 | 构建时间 | 文件大小 | 运行性能 | 启动速度 |
|------|---------|---------|---------|---------|
| Python 原版 | - | 小文件 | 慢 | 快 |
| PyInstaller | 2-5 分钟 | 50-80 MB | 慢 | 慢 |
| Nuitka | 10-20 分钟 | 30-50 MB | 快 | 中 |

### 实际游戏性能

- **帧率**: 稳定 60 FPS
- **内存占用**: 约 80-120 MB
- **CPU 占用**: 约 5-15%

---

## 🎯 发布检查清单

在发布游戏前，请确认：

- [ ] 可执行文件可以正常运行
- [ ] 所有游戏功能正常
- [ ] 音效和音乐正常播放
- [ ] 设置保存功能正常
- [ ] 在不同 Windows 版本测试（Win10/Win11）
- [ ] README 文档完整
- [ ] 检查文件大小是否合理
- [ ] 测试解压后的 ZIP 文件

---

## 📞 获取帮助

如有问题，请访问：
- **GitHub**: https://github.com/Sefucius/tetris_enhanced
- **Nuitka 文档**: https://nuitka.net/

---

**祝您构建顺利！🎉**
