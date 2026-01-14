# 🎮 俄罗斯方块 - 增强版
<!-- <p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python" />
  <img src="https://img.shields.io/badge/Pygame-2.0+-green.svg" alt="Pygame" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
  <img src="https://img.shields.io/badge/Version-1.0.0-brightgreen.svg" alt="Version" />
</p> -->

<div align="center">

# 🎮 俄罗斯方块 - 增强版

**一个功能丰富、视觉精美的经典俄罗斯方块游戏**

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)](https://github.com/Sefucius/tetris_enhanced)

**✨ 特性** | **🎨 主题** | **🎵 音乐** | **🏆 成就**
---|---|---|---
连击系统 | 6个独特主题 | 程序生成音乐 | 解锁成就
幽灵方块 | 随机加载 | 多种调式风格 | 排行榜
霓虹模式 | 实时切换 | 动态音效 | 统计追踪

</div>

---

## 📸 游戏截图

<!-- 如果有截图，可以在这里添加 -->
<!-- <p align="center">
  <img src="screenshot1.png" width="800" alt="游戏截图1">
</p> -->

---

## ✨ 核心特性

### 🎨 6大主题系统

每个主题都有独特的**配色方案**、**背景音乐**和**视觉特效**：

| 主题 | 风格 | 音乐 | 特效 |
|------|------|------|------|
| 🌆 **霓虹城市** | 赛博朋克 | 电子乐-大调 | 垂直渐变 |
| 🚀 **太空科幻** | 深邃星空 | 宁静-大调 | 星空闪烁 |
| 🎮 **复古像素** | 8-bit怀旧 | 复古-大调 | 浮动方块 |
| 🌊 **海洋世界** | 深海探险 | 宁静-大调 | 波浪动画 |
| 🌅 **日落黄昏** | 温暖黄昏 | 宁静-小调 | 垂直渐变 |
| 🌲 **森林秘境** | 自然清新 | 宁静-大调 | 极光效果 |

*每次启动游戏随机加载一个主题，按 `R` 键可切换主题！*

### 🎵 动态音乐系统

- ✅ **程序生成音乐** - 无需外部音频文件
- ✅ **多种调式** - 大调（明亮）和小调（忧郁）
- ✅ **不同风格** - 电子乐、复古、宁静
- ✅ **实时合成** - 使用数学函数合成音频
- ✅ **8秒循环** - 流畅的背景音乐体验

### 🎯 完整游戏系统

- 🔥 **连击系统** - 连续消除获得额外分数奖励
- 👻 **幽灵方块** - 显示方块落地预览位置
- ✨ **霓虹模式** - 炫酷的发光特效
- 📊 **统计数据** - 详细的游戏数据分析
- 🏆 **排行榜** - 记录您的最佳成绩
- 🎖️ **成就系统** - 解锁各种成就徽章

### 🎨 视觉效果

- 💥 **粒子效果** - 方块落地、行消除的华丽特效
- 📳 **屏幕震动** - 多行消除时的视觉冲击
- 💫 **冲击波** - 强力消除的震撼效果
- 🎈 **浮动文字** - 分数、连击的动态显示
- 🌈 **背景特效** - 渐变、星空、波浪、极光

---

## 🚀 快速开始

### 📥 下载可执行文件（推荐玩家）

> **无需安装 Python**，直接运行！

```bash
# 1. 下载发布包
git clone https://github.com/Sefucius/tetris_enhanced.git
cd tetris_enhanced/Tetris_Enhanced_v1.0.0

# 2. 双击运行
Tetris Enhanced.exe

# 3. 按空格键开始游戏！
```

### 💻 从源代码运行（开发者）

**系统要求：**
- Windows 10/11
- Python 3.6+
- Pygame 2.0+

**安装步骤：**

```bash
# 1. 安装依赖
pip install pygame

# 2. 运行游戏
python tetris_enhanced.py

# 3. 开始游戏！
按空格键或回车键
```

---

## 🕹️ 游戏控制

| 按键 | 功能 | 说明 |
|------|------|------|
| **← →** | 左右移动 | 移动方块位置 |
| **↑** | 旋转方块 | 顺时针旋转 |
| **↓** | 加速下落 | 软降 |
| **空格** | 直接落地 | 硬降 |
| **ESC** | 设置菜单 | 调整设置 |
| **P** | 暂停 | 暂停/继续 |
| **R** | 重新开始 | 切换主题 |
| **N** | 霓虹模式 | 切换特效 |
| **M** | 静音 | 切换音效 |
| **TAB** | 统计面板 | 查看统计 |
| **H** | 成就面板 | 查看成就 |
| **Q** | 退出 | 关闭游戏 |

---

## 🎬 游戏机制

### 📊 评分系统

```
┌─────────────┬──────────┬────────┐
│ 消除行数    │   分数   │  加成   │
├─────────────┼──────────┼────────┤
│ 1 行        │ 100 × 等级 │  -     │
│ 2 行        │ 300 × 等级 │  -     │
│ 3 行        │ 500 × 等级 │  -     │
│ 4 行        │ 800 × 等级 │  -     │
│ 连击        │  额外加分 │ 50%-150%│
└─────────────┴──────────┴────────┘
```

### 📈 等级系统

```
每消除 10 行 → 升一级
等级越高 → 下落速度越快
速度公式: 500 - (level - 1) × 50 毫秒
```

### 🔥 连击奖励

```
2连击 → 额外 50% 分数
3连击 → 额外 100% 分数
4连击及以上 → 额外 150% 分数
```

---

## 🎯 游戏技巧

### 💡 基础技巧

1. **规划落点** - 使用幽灵方块预览最佳位置
2. **保持平整** - 避免形成空洞
3. **优先消除** - 及时消除行，避免堆积过高
4. **学会旋转** - 熟练掌握7种方块的旋转特性

### 🎓 高级技巧

1. **连击策略** - 累积多行后一次性消除
2. **T-Spin** - 使用T方块旋转消除（高难度）
3. **保持冷静** - 速度加快后不要慌张
4. **使用硬降** - 空格键瞬间落地，节省时间

### 🎨 主题利用

| 主题 | 适用场景 | 特点 |
|------|---------|------|
| 🌆 霓虹/🎮 复古 | 冲分模式 | 节奏明快 |
| 🚀 太空/🌊 海洋 | 长时间游玩 | 音乐舒缓 |
| 🌅 日落/🌲 森林 | 放松休闲 | 视觉舒适 |

---

## 🏗️ 开发者指南

### 📦 构建可执行文件

```bash
# 一键构建（推荐）
build.bat

# 或使用 Python 脚本
python build_pyinstaller.py
python build_release.py
```

**构建结果：**
- `Tetris Enhanced.exe` (26-27 MB)
- 完全独立，无需 Python 环境

### 🔧 技术栈

```
语言: Python 3.11.9
框架: Pygame 2.6.1
特色: 程序生成音频
```

**核心模块：**
- 主题系统 - 面向对象管理
- 动画管理器 - 统一动画控制
- 音效管理器 - 程序化音频生成
- 统计系统 - 异步数据持久化

---

## 📊 项目结构

```
tetris_enhanced/
├── tetris_enhanced.py       # 主游戏程序 (189 KB)
├── README.md                # 项目说明
├── build.bat               # 一键构建脚本
├── git_push.bat            # Git 推送脚本
├── build_pyinstaller.py    # PyInstaller 构建脚本
├── build_nuitka.py         # Nuitka 构建脚本
├── build_release.py        # 发布包生成脚本
├── .gitignore               # Git 忽略配置
└── Tetris_Enhanced_v1.0.0/ # 游戏资源
```

---

## 📝 更新日志

### v1.0.0 (2025-01-14)

- ✅ 完整的 6 主题系统
- ✅ 下拉框主题选择器
- ✅ 优化的设置面板布局
- ✅ 连击和特效动画
- ✅ 统计数据和排行榜
- ✅ 成就系统
- ✅ 霓虹模式和幽灵方块
- ✅ 构建打包脚本
- ✅ 程序生成音乐系统
- ✅ SSH 配置优化

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**贡献方式：**
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- Pygame 开发团队
- 经典俄罗斯方块游戏
- 所有贡献者和支持者

---

<div align="center">

**享受游戏！🎉**

Made with ❤️ by [Sefucius](https://github.com/Sefucius)

**⭐ 如果这个项目对您有帮助，请给一个 Star！**

[⬆️ 回到顶部](#-俄罗斯方块---增强版)

</div>
