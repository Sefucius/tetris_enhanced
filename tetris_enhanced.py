"""
俄罗斯方块游戏 - 增强版
使用 Pygame 库实现的可交互式俄罗斯方块

新增功能：
✨ 音效系统（程序生成音效）
🎵 背景音乐
💥 连击和特效动画
🌟 霓虹发光模式
🏆 排行榜系统

控制方式：
- ← → : 左右移动
- ↑ : 旋转方块
- ↓ : 加速下落
- 空格键 : 直接落地
- P : 暂停/继续
- R : 重新开始
- Q : 退出游戏
- N : 切换霓虹模式
- M : 静音/取消静音
"""

import pygame
import random
import sys
import json
import os
import math
import array
import threading
import queue
from datetime import datetime

# 初始化 Pygame 和音频
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# 颜色定义（RGB）- 现代配色方案
DARK_BG = (18, 18, 24)
GRID_BG = (24, 24, 32)
GRID_BORDER = (40, 40, 50)
WHITE = (240, 240, 245)
TEXT_GRAY = (150, 150, 160)

# 方块颜色 - 霓虹增强版
COLOR_I = (0, 229, 255)
COLOR_O = (255, 215, 0)
COLOR_T = (170, 0, 255)
COLOR_L = (255, 140, 0)
COLOR_J = (30, 144, 255)
COLOR_Z = (255, 80, 80)
COLOR_S = (100, 255, 100)
COLOR_EMPTY = (30, 30, 40)

COLORS = [COLOR_EMPTY, COLOR_I, COLOR_O, COLOR_T, COLOR_L, COLOR_J, COLOR_Z, COLOR_S]

HIGHLIGHT_COLORS = [
    (40, 40, 50), (100, 255, 255), (255, 235, 100), (200, 100, 255),
    (255, 180, 80), (100, 180, 255), (255, 140, 140), (150, 255, 150)
]

SHADOW_COLORS = [
    (20, 20, 30), (0, 180, 200), (200, 170, 0), (130, 0, 200),
    (200, 100, 0), (20, 100, 200), (200, 50, 50), (70, 200, 70)
]

# ==================== 主题系统 ====================

class GameTheme:
    """游戏主题类 - 定义配色、音乐风格和视觉效果"""

    def __init__(self, name, display_name, description,
                 # 背景配色
                 bg_color, bg_color2, grid_bg, grid_border,
                 # UI配色
                 text_color, text_highlight, panel_bg,
                 # 方块配色 (I, O, T, L, J, Z, S)
                 piece_colors, highlight_colors, shadow_colors,
                 # 粒子效果颜色
                 particle_colors,
                 # 音乐配置 (调式: major/minor, 速度: 0.5-2.0, 风格)
                 music_scale, music_speed, music_style,
                 # 特殊效果
                 bg_effect_type):  # 'gradient', 'particles', 'waves', 'stars', 'aurora'
        self.name = name
        self.display_name = display_name
        self.description = description

        # 背景配色
        self.bg_color = bg_color
        self.bg_color2 = bg_color2  # 用于渐变
        self.grid_bg = grid_bg
        self.grid_border = grid_border

        # UI配色
        self.text_color = text_color
        self.text_highlight = text_highlight
        self.panel_bg = panel_bg

        # 方块配色
        self.piece_colors = piece_colors
        self.highlight_colors = highlight_colors
        self.shadow_colors = shadow_colors

        # 粒子效果颜色
        self.particle_colors = particle_colors

        # 音乐配置
        self.music_scale = music_scale  # 'major' 或 'minor'
        self.music_speed = music_speed  # 速度倍率
        self.music_style = music_style  # 'electronic', 'retro', 'peaceful', 'energetic'

        # 背景特效类型
        self.bg_effect_type = bg_effect_type


# 定义6个独特的主题
THEMES = [
    # 1. 霓虹城市 - 默认主题，赛博朋克风格
    GameTheme(
        name="neon_city",
        display_name="霓虹城市",
        description="赛博朋克风格的霓虹都市，充满未来感",
        bg_color=(18, 18, 24),
        bg_color2=(30, 20, 40),
        grid_bg=(24, 24, 32),
        grid_border=(40, 40, 50),
        text_color=(240, 240, 245),
        text_highlight=(0, 229, 255),
        panel_bg=(20, 20, 28),
        piece_colors=[(30, 30, 40), (0, 229, 255), (255, 215, 0), (170, 0, 255),
                     (255, 140, 0), (30, 144, 255), (255, 80, 80), (100, 255, 100)],
        highlight_colors=[(40, 40, 50), (100, 255, 255), (255, 235, 100), (200, 100, 255),
                        (255, 180, 80), (100, 180, 255), (255, 140, 140), (150, 255, 150)],
        shadow_colors=[(20, 20, 30), (0, 180, 200), (200, 170, 0), (130, 0, 200),
                      (200, 100, 0), (20, 100, 200), (200, 50, 50), (70, 200, 70)],
        particle_colors=[(0, 229, 255), (255, 215, 0), (170, 0, 255), (255, 80, 80)],
        music_scale="major",
        music_speed=1.0,
        music_style="electronic",
        bg_effect_type="gradient"
    ),

    # 2. 太空科幻 - 深邃宇宙风格
    GameTheme(
        name="space_scifi",
        display_name="太空科幻",
        description="深邃的宇宙空间，星辰点点",
        bg_color=(5, 5, 15),
        bg_color2=(10, 10, 30),
        grid_bg=(8, 8, 20),
        grid_border=(30, 30, 60),
        text_color=(200, 220, 255),
        text_highlight=(100, 150, 255),
        panel_bg=(10, 10, 25),
        piece_colors=[(15, 15, 25), (100, 180, 255), (255, 255, 200), (180, 130, 255),
                     (200, 150, 255), (130, 180, 255), (255, 130, 150), (150, 255, 200)],
        highlight_colors=[(25, 25, 35), (150, 220, 255), (255, 255, 230), (210, 170, 255),
                        (230, 190, 255), (170, 220, 255), (255, 170, 190), (190, 255, 230)],
        shadow_colors=[(10, 10, 20), (70, 140, 200), (200, 200, 150), (140, 100, 200),
                      (150, 110, 200), (100, 140, 200), (200, 100, 120), (110, 200, 150)],
        particle_colors=[(100, 180, 255), (200, 200, 255), (150, 150, 255), (255, 255, 255)],
        music_scale="major",
        music_speed=0.8,
        music_style="peaceful",
        bg_effect_type="stars"
    ),

    # 3. 复古像素 - 8-bit游戏风格
    GameTheme(
        name="retro_pixel",
        display_name="复古像素",
        description="经典8-bit游戏风格，怀旧感十足",
        bg_color=(40, 30, 50),
        bg_color2=(60, 40, 70),
        grid_bg=(50, 40, 60),
        grid_border=(80, 60, 90),
        text_color=(255, 240, 200),
        text_highlight=(255, 200, 100),
        panel_bg=(45, 35, 55),
        piece_colors=[(30, 30, 40), (255, 100, 100), (100, 255, 100), (100, 100, 255),
                     (255, 200, 100), (100, 200, 255), (255, 100, 200), (200, 255, 100)],
        highlight_colors=[(50, 50, 60), (255, 140, 140), (150, 255, 150), (150, 150, 255),
                        (255, 220, 140), (140, 220, 255), (255, 140, 220), (220, 255, 140)],
        shadow_colors=[(25, 25, 35), (200, 70, 70), (70, 200, 70), (70, 70, 200),
                      (200, 150, 70), (70, 150, 200), (200, 70, 150), (150, 200, 70)],
        particle_colors=[(255, 200, 100), (255, 100, 100), (100, 255, 100), (255, 255, 100)],
        music_scale="major",
        music_speed=1.2,
        music_style="retro",
        bg_effect_type="particles"
    ),

    # 4. 海洋世界 - 深海探险风格
    GameTheme(
        name="ocean_world",
        display_name="海洋世界",
        description="深邃的海底世界，宁静而神秘",
        bg_color=(5, 30, 50),
        bg_color2=(10, 50, 70),
        grid_bg=(10, 35, 55),
        grid_border=(30, 70, 100),
        text_color=(200, 240, 255),
        text_highlight=(100, 200, 255),
        panel_bg=(8, 32, 52),
        piece_colors=[(15, 35, 50), (100, 200, 255), (255, 255, 150), (180, 150, 255),
                     (255, 180, 100), (100, 180, 220), (255, 120, 150), (120, 220, 180)],
        highlight_colors=[(25, 45, 60), (140, 220, 255), (255, 255, 190), (200, 170, 255),
                        (255, 200, 140), (140, 200, 240), (255, 150, 180), (150, 240, 200)],
        shadow_colors=[(10, 30, 45), (70, 170, 220), (220, 220, 120), (150, 120, 220),
                      (220, 150, 80), (70, 150, 190), (220, 90, 120), (90, 190, 150)],
        particle_colors=[(100, 200, 255), (150, 220, 255), (200, 240, 255), (255, 255, 255)],
        music_scale="major",
        music_speed=0.7,
        music_style="peaceful",
        bg_effect_type="waves"
    ),

    # 5. 日落黄昏 - 温暖渐变风格
    GameTheme(
        name="sunset_dusk",
        display_name="日落黄昏",
        description="温暖的黄昏时光，金色渐变",
        bg_color=(40, 25, 30),
        bg_color2=(60, 35, 40),
        grid_bg=(45, 30, 35),
        grid_border=(80, 50, 60),
        text_color=(255, 240, 230),
        text_highlight=(255, 180, 100),
        panel_bg=(42, 28, 32),
        piece_colors=[(30, 30, 35), (255, 150, 80), (255, 220, 100), (255, 120, 180),
                     (255, 180, 60), (255, 130, 200), (255, 160, 140), (200, 220, 120)],
        highlight_colors=[(45, 45, 50), (255, 180, 110), (255, 240, 140), (255, 150, 210),
                        (255, 200, 100), (255, 160, 220), (255, 190, 170), (220, 240, 150)],
        shadow_colors=[(25, 25, 30), (220, 120, 60), (220, 180, 70), (220, 90, 140),
                      (220, 150, 40), (220, 100, 160), (220, 130, 110), (170, 190, 90)],
        particle_colors=[(255, 180, 80), (255, 200, 100), (255, 150, 150), (255, 220, 150)],
        music_scale="minor",
        music_speed=0.9,
        music_style="peaceful",
        bg_effect_type="gradient"
    ),

    # 6. 森林秘境 - 自然清新风格
    GameTheme(
        name="forest_mystic",
        display_name="森林秘境",
        description="神秘的森林深处，自然清新",
        bg_color=(15, 35, 20),
        bg_color2=(25, 50, 30),
        grid_bg=(20, 40, 25),
        grid_border=(40, 80, 50),
        text_color=(220, 255, 230),
        text_highlight=(150, 255, 150),
        panel_bg=(18, 38, 23),
        piece_colors=[(20, 35, 25), (150, 255, 150), (255, 255, 150), (200, 180, 255),
                     (255, 200, 120), (150, 200, 255), (255, 150, 180), (200, 255, 180)],
        highlight_colors=[(30, 45, 35), (180, 255, 180), (255, 255, 190), (220, 200, 255),
                        (255, 220, 150), (180, 220, 255), (255, 180, 200), (220, 255, 200)],
        shadow_colors=[(15, 30, 20), (120, 220, 120), (220, 220, 120), (170, 150, 220),
                      (220, 170, 100), (120, 170, 220), (220, 120, 150), (170, 220, 150)],
        particle_colors=[(150, 255, 150), (200, 255, 150), (150, 220, 255), (255, 255, 200)],
        music_scale="major",
        music_speed=0.85,
        music_style="peaceful",
        bg_effect_type="aurora"
    ),
]

# 游戏配置
GRID_WIDTH = 10
GRID_HEIGHT = 21  # 调整为21以匹配右边卡片高度
BLOCK_SIZE = 25
GRID_X_OFFSET = 40
GRID_Y_OFFSET = 40  # 保持原来的值

WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + GRID_X_OFFSET * 2 + 200
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + GRID_Y_OFFSET * 2 + 120

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]]   # S
]


class SettingsManager:
    """游戏设置管理器"""

    def __init__(self, filename='tetris_settings.json'):
        self.filename = filename
        self.settings = {
            'sound_enabled': True,
            'music_enabled': True,
            'music_volume': 0.5,
            'sfx_volume': 0.5,
            'show_ghost': True,
            'neon_mode': True,  # 默认开启霓虹模式
            'theme': 'default'
        }
        self.load_settings()

    def load_settings(self):
        """加载设置"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except:
                pass

    def save_settings(self):
        """保存设置"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except (PermissionError, IOError):
            pass

    def get(self, key, default=None):
        """获取设置值"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """设置值并保存"""
        self.settings[key] = value
        self.save_settings()


class KeyBindManager:
    """键位绑定管理器"""

    # 默认键位映射
    DEFAULT_BINDINGS = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'rotate': pygame.K_UP,
        'soft_drop': pygame.K_DOWN,
        'hard_drop': pygame.K_SPACE,
        'pause': pygame.K_p,
        'neon': pygame.K_n,
        'mute': pygame.K_m,
        'restart': pygame.K_r,
        'quit': pygame.K_q,
        'stats': pygame.K_TAB,
        'achievements': pygame.K_h,
        'settings': pygame.K_ESCAPE
    }

    # 键位名称映射（用于显示）
    KEY_NAMES = {
        pygame.K_LEFT: "←",
        pygame.K_RIGHT: "→",
        pygame.K_UP: "↑",
        pygame.K_DOWN: "↓",
        pygame.K_SPACE: "Space",
        pygame.K_RETURN: "Enter",
        pygame.K_ESCAPE: "Esc",
        pygame.K_TAB: "Tab",
        pygame.K_p: "P",
        pygame.K_n: "N",
        pygame.K_m: "M",
        pygame.K_r: "R",
        pygame.K_q: "Q",
        pygame.K_h: "H"
    }

    # 动作名称映射
    ACTION_NAMES = {
        'left': "左移",
        'right': "右移",
        'rotate': "旋转",
        'soft_drop': "软降",
        'hard_drop': "硬降",
        'pause': "暂停",
        'neon': "霓虹模式",
        'mute': "静音",
        'restart': "重新开始",
        'quit': "退出游戏",
        'stats': "统计面板",
        'achievements': "成就面板",
        'settings': "设置菜单"
    }

    def __init__(self, filename='tetris_keybinds.json'):
        self.filename = filename
        self.bindings = self.DEFAULT_BINDINGS.copy()
        self.load_bindings()

    def load_bindings(self):
        """加载键位绑定"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 将字符串键码转换为pygame键码
                    for action, key_code in data.items():
                        self.bindings[action] = key_code
            except:
                pass

    def save_bindings(self):
        """保存键位绑定"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.bindings, f, indent=2, ensure_ascii=False)
        except (PermissionError, IOError):
            pass

    def get_key(self, action):
        """获取动作对应的键码"""
        return self.bindings.get(action, self.DEFAULT_BINDINGS.get(action))

    def set_key(self, action, key_code):
        """设置动作的键码"""
        self.bindings[action] = key_code
        self.save_bindings()

    def get_key_name(self, action):
        """获取动作的按键名称"""
        key_code = self.get_key(action)

        # 先查找预定义的名称
        if key_code in self.KEY_NAMES:
            return self.KEY_NAMES[key_code]

        # 使用pygame的默认名称并格式化
        name = pygame.key.name(key_code)

        # 格式化常见按键
        if name.startswith('['):
            return name.upper()  # 如 [1] -> [1]
        elif len(name) == 1:
            return name.upper()  # 单个字母转大写
        elif name in ('space',):
            return 'Space'
        elif name in ('return',):
            return 'Enter'
        elif name in ('escape',):
            return 'Esc'
        elif name in ('tab',):
            return 'Tab'
        elif name.startswith('kp'):
            # 小键盘按键: kp1 -> Num1
            return 'Num' + name[2:].upper()
        elif name.startswith('f') and len(name) > 1:
            # 功能键: f1 -> F1
            return name.upper()
        else:
            # 首字母大写
            return name[0].upper() + name[1:] if len(name) > 1 else name.upper()

    def is_key_bound(self, key_code):
        """检查按键是否已被绑定"""
        return key_code in self.bindings.values()

    def reset_to_defaults(self):
        """恢复所有键位到默认设置"""
        self.bindings = self.DEFAULT_BINDINGS.copy()
        self.save_bindings()


class SoundManager:
    """音效管理器 - 程序生成音效和背景音乐"""

    def __init__(self):
        self.enabled = True
        self.music_enabled = True
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.sounds = {}
        self.background_music = None
        self.music_channel = None
        self.generate_sounds()
        self.generate_background_music()

    def generate_tone(self, frequency, duration, volume=0.3):
        """生成音调"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)

        # 生成立体声波形
        samples = []
        for t in range(n_samples):
            value = int(volume * 32767 * math.sin(2 * math.pi * frequency * t / sample_rate))
            samples.append([value, value])  # 左声道和右声道

        sound_array = array.array('h', [item for sublist in samples for item in sublist])
        return pygame.mixer.Sound(buffer=sound_array)

    def generate_background_music(self, theme=None):
        """生成背景音乐（循环旋律）- 根据主题生成不同风格的音乐"""
        if theme is None:
            # 默认使用霓虹城市主题
            theme = THEMES[0]

        sample_rate = 44100
        duration = 8.0  # 8秒循环
        n_samples = int(sample_rate * duration)

        # 根据主题的调式选择旋律
        # 大调音阶: C(261.63), D(293.66), E(329.63), F(349.23), G(392.00), A(440.00), B(493.88)
        # 小调音阶: C(261.63), D(293.66), Eb(311.13), F(349.23), G(392.00), Ab(415.30), Bb(466.16)

        if theme.music_scale == "minor":
            # 小调旋律（更忧郁、神秘）
            base_melody = [
                (261.63, 0.5), (293.66, 0.5), (311.13, 0.5), (349.23, 0.5),  # C D Eb F
                (392.00, 1.0), (349.23, 0.5), (311.13, 0.5), (293.66, 0.5),  # G F Eb D
                (261.63, 1.0), (293.66, 0.5), (261.63, 0.5), (392.00, 1.0),  # C D C G
                (349.23, 0.5), (311.13, 0.5), (293.66, 0.5), (261.63, 2.0),  # F Eb D C
                (349.23, 0.5), (415.30, 0.5), (466.16, 0.5), (415.30, 0.5), (349.23, 1.0),  # F Ab Bb Ab F
                (311.13, 0.5), (293.66, 0.5), (261.63, 1.0), (293.66, 0.5), (261.63, 2.0),  # Eb D C D C
            ]
        else:
            # 大调旋律（明亮、欢快）
            base_melody = [
                (261.63, 0.5), (293.66, 0.5), (329.63, 0.5), (349.23, 0.5),  # C D E F
                (392.00, 1.0), (349.23, 0.5), (329.63, 0.5), (293.66, 0.5),  # G F E D
                (261.63, 1.0), (293.66, 0.5), (261.63, 0.5), (392.00, 1.0),  # C D C G
                (349.23, 0.5), (329.63, 0.5), (293.66, 0.5), (261.63, 2.0),  # F E D C
                (349.23, 0.5), (392.00, 0.5), (440.00, 0.5), (392.00, 0.5), (349.23, 1.0),  # F G A G F
                (329.63, 0.5), (293.66, 0.5), (261.63, 1.0), (293.66, 0.5), (261.63, 2.0),  # E D C D C
            ]

        # 根据主题的风格调整旋律
        melody = []
        for freq, dur in base_melody:
            # 应用速度调整
            adjusted_dur = dur / theme.music_speed
            melody.append((freq, adjusted_dur))

        samples = []
        current_time = 0

        # 根据音乐风格调整参数
        if theme.music_style == "electronic":
            main_volume = 0.4
            third_volume = 0.2
            fifth_volume = 0.15
            bass_volume = 0.3
            overall_volume = 0.3
        elif theme.music_style == "retro":
            main_volume = 0.5
            third_volume = 0.1
            fifth_volume = 0.1
            bass_volume = 0.2
            overall_volume = 0.35
        elif theme.music_style == "peaceful":
            main_volume = 0.35
            third_volume = 0.25
            fifth_volume = 0.2
            bass_volume = 0.25
            overall_volume = 0.25
        else:  # energetic
            main_volume = 0.45
            third_volume = 0.15
            fifth_volume = 0.2
            bass_volume = 0.35
            overall_volume = 0.35

        for freq, dur in melody:
            note_samples = int(sample_rate * dur)
            for t in range(note_samples):
                # 使用和弦和包络
                t_total = current_time + t
                value = 0

                # 主音
                value += main_volume * math.sin(2 * math.pi * freq * t_total / sample_rate)
                # 三度和弦
                value += third_volume * math.sin(2 * math.pi * (freq * 1.2599) * t_total / sample_rate)
                # 五度和弦
                value += fifth_volume * math.sin(2 * math.pi * (freq * 1.5) * t_total / sample_rate)

                # 包络（淡入淡出）
                env_pos = t / note_samples
                envelope = 1.0
                if env_pos < 0.1:  # Attack
                    envelope = env_pos / 0.1
                elif env_pos > 0.8:  # Release
                    envelope = (1.0 - env_pos) / 0.2

                # 低音（bass）
                bass_freq = freq / 2
                value += bass_volume * math.sin(2 * math.pi * bass_freq * t_total / sample_rate)

                sample_value = int(overall_volume * 32767 * value * envelope)
                samples.append([sample_value, sample_value])

            current_time += note_samples

        # 填充到完整长度
        while len(samples) < n_samples:
            samples.append([0, 0])

        sound_array = array.array('h', [item for sublist in samples for item in sublist])
        self.background_music = pygame.mixer.Sound(buffer=sound_array)

    def play_music(self, loops=-1):
        """播放背景音乐（loops=-1表示无限循环）"""
        if self.music_enabled and self.background_music:
            # 开局时音乐音量增加20%
            boosted_volume = min(1.0, self.music_volume * 1.2)
            self.background_music.set_volume(boosted_volume)
            self.background_music.play(loops=loops)

    def stop_music(self):
        """停止背景音乐"""
        if self.background_music:
            self.background_music.stop()

    def set_music_volume(self, volume):
        """设置音乐音量（0.0-1.0）"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.background_music:
            self.background_music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """设置音效音量（0.0-1.0）"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def toggle_music(self):
        """切换背景音乐"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()
        return self.music_enabled

    def generate_sounds(self):
        """生成游戏音效"""
        import array

        # 移动音效
        self.sounds['move'] = self.generate_tone(440, 0.05, 0.1)

        # 旋转音效
        self.sounds['rotate'] = self.generate_tone(520, 0.08, 0.15)

        # 落地音效（普通）
        self.sounds['land'] = self.generate_tone(330, 0.08, 0.15)

        # 硬降音效（更响、更短）
        self.sounds['hard_drop'] = self.generate_tone(220, 0.12, 0.25)

        # 消除音效（不同等级）
        self.sounds['clear1'] = self.generate_tone(523, 0.15, 0.25)  # 单行
        self.sounds['clear2'] = self.generate_tone(659, 0.2, 0.3)   # 双行
        self.sounds['clear3'] = self.generate_tone(784, 0.25, 0.35)  # 三行
        self.sounds['clear4'] = self.generate_tone(880, 0.3, 0.4)   # 四行

        # 连击音效
        self.sounds['combo'] = self.generate_tone(1047, 0.2, 0.35)

        # 游戏结束音效
        self.sounds['gameover'] = self.generate_tone(200, 0.5, 0.3)

    def play(self, sound_name):
        """播放音效"""
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def toggle(self):
        """切换静音"""
        self.enabled = not self.enabled
        return self.enabled


class Particle:
    """粒子效果类"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.uniform(3, 6)

    def update(self):
        """更新粒子状态"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # 重力
        self.life -= self.decay

    def draw(self, surface):
        """绘制粒子"""
        if self.life > 0:
            alpha = int(self.life * 255)
            color = (*self.color[:3], alpha)
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class SuckInParticle:
    """吸入式粒子 - 从边缘向中心移动，创造真空效果"""

    def __init__(self, x, y, target_x, target_y, color, speed=3.0):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.color = color

        # 计算方向向量
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        # 标准化并应用速度
        if distance > 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = 0
            self.vy = 0

        self.life = 1.0
        self.decay = random.uniform(0.015, 0.03)
        self.size = random.uniform(2, 5)
        self.trail = []  # 尾迹效果

    def update(self):
        """更新粒子状态 - 向目标移动"""
        # 保存位置用于尾迹
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)

        self.x += self.vx
        self.y += self.vy

        # 加速效果（越接近目标越快）
        self.vx *= 1.05
        self.vy *= 1.05

        self.life -= self.decay

    def draw(self, surface):
        """绘制粒子带尾迹"""
        if self.life > 0:
            alpha = int(self.life * 255)

            # 绘制尾迹
            for i, (tx, ty) in enumerate(self.trail):
                trail_alpha = int(alpha * (i / len(self.trail)) * 0.5)
                trail_size = self.size * (i / len(self.trail))
                color = (*self.color[:3], trail_alpha)
                s = pygame.Surface((int(trail_size * 2), int(trail_size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (int(trail_size), int(trail_size)), int(trail_size))
                surface.blit(s, (int(tx - trail_size), int(ty - trail_size)))

            # 绘制主粒子
            color = (*self.color[:3], alpha)
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class LightBeamAnimation:
    """光带动画类 - 霓虹风格"""

    def __init__(self, start_y, end_y, grid_rect, beam_type, color):
        """
        创建光带动画
        beam_type: 'horizontal_left_right' | 'horizontal_center_out' | 'vertical_top_down' | 'rainbow'
        """
        self.start_y = start_y  # 消除行的Y坐标
        self.end_y = end_y  # 结束Y坐标
        self.grid_rect = grid_rect  # 网格区域矩形
        self.beam_type = beam_type
        self.color = color
        self.progress = 0.0  # 动画进度 0-1
        self.speed = 0.05  # 动画速度
        self.alpha = 255  # 透明度

        # 彩虹色序列
        self.rainbow_colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130),
            (148, 0, 211)
        ]

    def update(self):
        """更新动画状态"""
        self.progress += self.speed
        if self.beam_type == 'rainbow':
            # 彩虹模式：慢慢淡出
            if self.progress > 0.5:
                self.alpha = max(0, 255 - int((self.progress - 0.5) * 2 * 255))
        else:
            # 其他模式：逐渐淡出
            self.alpha = max(0, 255 - int(self.progress * 255))
        return self.progress < 1.0  # 返回False表示动画结束

    def draw(self, surface, scale):
        """绘制光带动画"""
        if self.alpha <= 0:
            return

        grid_x, grid_y, grid_width, grid_height = self.grid_rect
        block_size = int(25 * scale)

        # 计算消除行的实际Y坐标
        line_y = grid_y + self.start_y * block_size
        line_height = (self.end_y - self.start_y + 1) * block_size

        if self.beam_type == 'horizontal_left_right':
            # 青色光带从左到右扫过
            beam_width = int(grid_width * self.progress)
            s = pygame.Surface((beam_width, line_height), pygame.SRCALPHA)
            s.fill((*self.color, self.alpha))
            surface.blit(s, (grid_x, line_y))

            # 添加发光边缘
            if beam_width > 0:
                edge_x = grid_x + beam_width
                pygame.draw.line(surface, (*self.color, min(255, self.alpha + 50)),
                               (edge_x, line_y), (edge_x, line_y + line_height), 3)

        elif self.beam_type == 'horizontal_center_out':
            # 绿色光带从中间向两边扩散
            center_x = grid_x + grid_width // 2
            max_width = int(grid_width // 2 * self.progress)

            # 左侧光带
            s = pygame.Surface((max_width, line_height), pygame.SRCALPHA)
            s.fill((*self.color, self.alpha))
            surface.blit(s, (center_x - max_width, line_y))

            # 右侧光带
            surface.blit(s, (center_x, line_y))

            # 发光边缘
            if max_width > 0:
                pygame.draw.line(surface, (*self.color, min(255, self.alpha + 50)),
                               (center_x - max_width, line_y),
                               (center_x - max_width, line_y + line_height), 3)
                pygame.draw.line(surface, (*self.color, min(255, self.alpha + 50)),
                               (center_x + max_width, line_y),
                               (center_x + max_width, line_y + line_height), 3)

        elif self.beam_type == 'vertical_top_down':
            # 紫色光带从上到下流动
            beam_height = int(line_height * self.progress)
            if beam_height > 0:
                s = pygame.Surface((grid_width, beam_height), pygame.SRCALPHA)
                s.fill((*self.color, self.alpha))
                surface.blit(s, (grid_x, line_y))

                # 发光边缘
                edge_y = line_y + beam_height
                pygame.draw.line(surface, (*self.color, min(255, self.alpha + 50)),
                               (grid_x, edge_y), (grid_x + grid_width, edge_y), 3)

        elif self.beam_type == 'rainbow':
            # 彩虹光效 - 多色循环
            if self.progress < 1.0:
                color_index = int(self.progress * len(self.rainbow_colors))
                color_index = min(color_index, len(self.rainbow_colors) - 1)
                color = self.rainbow_colors[color_index]

                # 绘制彩虹渐变
                for i in range(len(self.rainbow_colors)):
                    offset = int((i / len(self.rainbow_colors)) * grid_width)
                    width = int(grid_width / len(self.rainbow_colors)) + 1
                    alpha = int(self.alpha * (1 - abs(i - color_index) / len(self.rainbow_colors)))
                    alpha = max(0, min(255, alpha))

                    s = pygame.Surface((width, line_height), pygame.SRCALPHA)
                    s.fill((*self.rainbow_colors[i], alpha))
                    surface.blit(s, (grid_x + offset, line_y))

                # 添加强烈发光效果
                glow_alpha = int(self.alpha * 0.3)
                glow_surface = pygame.Surface((grid_width, line_height), pygame.SRCALPHA)
                glow_surface.fill((255, 255, 255, glow_alpha))
                surface.blit(glow_surface, (grid_x, line_y))


class ScreenShake:
    """屏幕震动效果"""

    def __init__(self, intensity, duration):
        """
        intensity: 震动强度（像素偏移量）
        duration: 震动持续时间（毫秒）
        """
        self.intensity = intensity
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def get_offset(self):
        """获取当前震动偏移量"""
        if not self.active:
            return (0, 0)

        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.active = False
            return (0, 0)

        # 使用正弦波创建震动效果，随时间衰减
        decay = 1 - (elapsed / self.duration)
        offset_x = int(math.sin(elapsed * 0.05) * self.intensity * decay)
        offset_y = int(math.cos(elapsed * 0.07) * self.intensity * decay)
        return (offset_x, offset_y)


class PieceAnimation:
    """方块平滑动画类"""

    def __init__(self):
        self.animating = False
        self.animation_type = None  # 'move', 'rotate', 'drop'
        self.start_time = 0
        self.duration = 100  # 动画持续时间（毫秒）
        self.start_x = 0
        self.start_y = 0
        self.target_x = 0
        self.target_y = 0
        self.start_piece = None
        self.target_piece = None

    def start_move_animation(self, start_x, start_y, target_x, target_y):
        """开始移动动画"""
        self.animating = True
        self.animation_type = 'move'
        self.start_time = pygame.time.get_ticks()
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y

    def start_rotate_animation(self, start_piece, target_piece):
        """开始旋转动画"""
        self.animating = True
        self.animation_type = 'rotate'
        self.start_time = pygame.time.get_ticks()
        self.start_piece = start_piece
        self.target_piece = target_piece

    def start_drop_animation(self, start_y, target_y):
        """开始下落动画"""
        self.animating = True
        self.animation_type = 'drop'
        self.start_time = pygame.time.get_ticks()
        self.duration = 80  # 下落动画更快
        self.start_y = start_y
        self.target_y = target_y

    def update(self):
        """更新动画状态"""
        if not self.animating:
            return True  # 动画未激活或已完成

        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.animating = False
            return True  # 动画完成
        return False  # 动画进行中

    def get_current_position(self, current_x, current_y):
        """获取当前动画位置（平滑插值）"""
        if not self.animating or self.animation_type != 'move':
            return current_x, current_y

        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)

        # 使用缓动函数（ease-out）
        ease_progress = 1 - (1 - progress) ** 2

        anim_x = self.start_x + (self.target_x - self.start_x) * ease_progress
        anim_y = self.start_y + (self.target_y - self.start_y) * ease_progress

        return anim_x, anim_y

    def get_current_drop_y(self, current_y):
        """获取当前下落动画Y坐标"""
        if not self.animating or self.animation_type != 'drop':
            return current_y

        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)

        # 使用缓动函数（ease-in）
        ease_progress = progress ** 2

        anim_y = self.start_y + (self.target_y - self.start_y) * ease_progress
        return anim_y


class LandingFlash:
    """落地闪光效果 - 方块落地时的白色闪光过渡"""

    def __init__(self, center_x, center_y, piece_width, piece_height, duration):
        self.center_x = center_x
        self.center_y = center_y
        self.width = piece_width * 25  # BLOCK_SIZE = 25
        self.height = piece_height * 25
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def update(self):
        """更新闪光状态"""
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.active = False
            return False
        return True

    def draw(self, surface):
        """绘制闪光效果"""
        if not self.active:
            return

        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)

        # 快速淡出（开始很亮，快速消失）
        alpha = int(255 * (1 - progress ** 0.5))

        # 计算闪光矩形（从方块大小开始稍微扩大）
        expand = progress * 10  # 扩大10像素
        rect = pygame.Rect(
            self.center_x - self.width // 2 - expand,
            self.center_y - self.height // 2 - expand,
            self.width + expand * 2,
            self.height + expand * 2
        )

        # 绘制半透明白色闪光
        s = pygame.Surface((int(rect.width), int(rect.height)), pygame.SRCALPHA)
        s.fill((255, 255, 255, alpha))
        surface.blit(s, rect)


class ShockwaveEffect:
    """冲击波效果 - 用于多行消除"""

    def __init__(self, center_x, center_y, max_radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.max_radius = max_radius
        self.color = color
        self.current_radius = 0
        self.alpha = 255
        self.speed = max_radius / 20  # 20帧扩展到最大半径
        self.active = True

    def update(self):
        """更新冲击波状态"""
        self.current_radius += self.speed
        # 透明度随半径增大而减小
        progress = self.current_radius / self.max_radius
        self.alpha = int(255 * (1 - progress))

        if self.current_radius >= self.max_radius:
            self.active = False
            return False
        return True

    def draw(self, surface):
        """绘制冲击波"""
        if not self.active or self.alpha <= 0:
            return

        # 绘制多个同心圆形成冲击波效果
        for i in range(3):
            radius = int(self.current_radius - i * 15)
            if radius > 0:
                alpha = max(0, self.alpha - i * 50)
                s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, alpha), (radius, radius), radius, 3)
                surface.blit(s, (self.center_x - radius, self.center_y - radius))


class FloatingText:
    """浮动文字效果"""

    def __init__(self, text, x, y, color, font_size=36):
        self.text = text
        self.x = x
        self.y = y
        self.start_y = y
        self.color = color
        self.font_size = font_size
        self.alpha = 255
        self.scale = 1.0
        self.life = 1.0  # 生命值 1.0 -> 0
        self.velocity_y = -2  # 向上浮动

    def update(self):
        """更新文字状态"""
        self.y += self.velocity_y
        self.life -= 0.02
        self.alpha = int(255 * self.life)
        self.scale = 1.0 + (1.0 - self.life) * 0.5  # 逐渐放大

        return self.life > 0

    def draw(self, surface, font):
        """绘制浮动文字"""
        if self.life <= 0:
            return

        # 创建缩放后的文字
        scaled_size = int(self.font_size * self.scale)
        if scaled_size > 0:
            try:
                scaled_font = pygame.font.Font(font, scaled_size)
            except:
                scaled_font = pygame.font.Font(None, scaled_size)

            text_surf = scaled_font.render(self.text, True, self.color)
            text_surf.set_alpha(self.alpha)

            # 居中绘制
            rect = text_surf.get_rect(center=(self.x, int(self.y)))
            surface.blit(text_surf, rect)


class AnimationManager:
    """动画管理器"""

    def __init__(self, theme=None):
        self.particles = []
        self.suck_in_particles = []  # 吸入式粒子列表
        self.line_clear_animations = []  # 行消除动画
        self.light_beams = []  # 光带动画列表
        self.screen_shake = None  # 屏幕震动效果
        self.shockwaves = []  # 冲击波效果列表
        self.floating_texts = []  # 浮动文字列表
        self.landing_flashes = []  # 落地闪光效果列表
        self.theme = theme  # 当前主题（用于粒子颜色）

    def add_line_clear(self, line_y, combo_count):
        """添加行消除动画（保留旧方法兼容）"""
        self.line_clear_animations.append({
            'y': line_y,
            'alpha': 255,
            'combo': combo_count,
            'scale': 1.0
        })

    def add_light_beam(self, start_y, end_y, grid_rect, lines_cleared, neon_mode):
        """添加霓虹光带动画 - 增强版（带吸入粒子效果）"""
        grid_x, grid_y, grid_width, grid_height = grid_rect
        block_size = 25  # 基础方块大小

        # 计算消除行的中心位置（用于冲击波和浮动文字）
        center_y = grid_y + (start_y + end_y) / 2 * block_size + block_size // 2
        center_x = grid_x + grid_width // 2

        if lines_cleared == 1:
            # 单行：青色光带从左到右
            beam = LightBeamAnimation(start_y, end_y, grid_rect,
                                    'horizontal_left_right', (0, 255, 255))
            self.light_beams.append(beam)

            # 单行也有轻微震动
            self.add_screen_shake(3, 200)

            # 单行文字提示
            self.floating_texts.append(FloatingText("SINGLE!", center_x, center_y, (0, 255, 255), 28))

            # 添加吸入式粒子（从左右两侧向中心）
            for _ in range(20):
                # 左侧粒子
                start_x = grid_x - random.randint(50, 150)
                start_y = center_y + random.randint(-30, 30)
                self.suck_in_particles.append(
                    SuckInParticle(start_x, start_y, center_x, center_y, (0, 255, 255), speed=4.0)
                )
                # 右侧粒子
                start_x = grid_x + grid_width + random.randint(50, 150)
                self.suck_in_particles.append(
                    SuckInParticle(start_x, start_y, center_x, center_y, (0, 255, 255), speed=4.0)
                )

        elif lines_cleared == 2:
            # 双行：绿色光带从中间向两边
            beam = LightBeamAnimation(start_y, end_y, grid_rect,
                                    'horizontal_center_out', (0, 255, 100))
            self.light_beams.append(beam)

            # 双行震动增强
            self.add_screen_shake(5, 250)

            # 双行文字提示
            self.floating_texts.append(FloatingText("DOUBLE!", center_x, center_y, (0, 255, 100), 32))

            # 添加冲击波效果
            max_radius = grid_width * 0.6
            self.shockwaves.append(ShockwaveEffect(center_x, center_y, max_radius, (0, 255, 100)))

            # 增强吸入式粒子（四角向中心）
            for _ in range(30):
                # 从四个角落
                corners = [
                    (grid_x - random.randint(100, 200), grid_y - random.randint(100, 200)),
                    (grid_x + grid_width + random.randint(100, 200), grid_y - random.randint(100, 200)),
                    (grid_x - random.randint(100, 200), grid_y + grid_height + random.randint(100, 200)),
                    (grid_x + grid_width + random.randint(100, 200), grid_y + grid_height + random.randint(100, 200))
                ]
                start_x, start_y = random.choice(corners)
                self.suck_in_particles.append(
                    SuckInParticle(start_x, start_y, center_x, center_y, (0, 255, 100), speed=5.0)
                )

        elif lines_cleared == 3:
            # 三行：紫色光带从上到下
            beam = LightBeamAnimation(start_y, end_y, grid_rect,
                                    'vertical_top_down', (200, 0, 255))
            self.light_beams.append(beam)

            # 三行剧烈震动
            self.add_screen_shake(8, 350)

            # 三行文字提示
            self.floating_texts.append(FloatingText("TRIPLE!", center_x, center_y, (200, 0, 255), 36))

            # 添加冲击波效果（更大）
            max_radius = grid_width * 0.8
            self.shockwaves.append(ShockwaveEffect(center_x, center_y, max_radius, (200, 0, 255)))

            # 增加粒子数量（普通粒子）
            for _ in range(50):  # 三行消除更多粒子
                x = center_x + random.randint(-grid_width//2, grid_width//2)
                y = center_y + random.randint(-50, 50)
                color = (random.randint(150, 255), 0, random.randint(200, 255))
                self.particles.append(Particle(x, y, color))

            # 大量吸入式粒子（全屏幕向中心）
            for _ in range(50):
                # 从屏幕边缘随机位置
                side = random.choice(['top', 'bottom', 'left', 'right'])
                if side == 'top':
                    start_x = random.randint(0, WINDOW_WIDTH)
                    start_y = -random.randint(50, 150)
                elif side == 'bottom':
                    start_x = random.randint(0, WINDOW_WIDTH)
                    start_y = WINDOW_HEIGHT + random.randint(50, 150)
                elif side == 'left':
                    start_x = -random.randint(50, 150)
                    start_y = random.randint(0, WINDOW_HEIGHT)
                else:  # right
                    start_x = WINDOW_WIDTH + random.randint(50, 150)
                    start_y = random.randint(0, WINDOW_HEIGHT)

                self.suck_in_particles.append(
                    SuckInParticle(start_x, start_y, center_x, center_y,
                                 (random.randint(150, 255), 0, random.randint(200, 255)), speed=6.0)
                )

        else:  # 4行或更多 - Tetris!
            # 四行：彩虹光效
            beam = LightBeamAnimation(start_y, end_y, grid_rect,
                                    'rainbow', (255, 255, 255))
            self.light_beams.append(beam)

            # Tetris超剧烈震动
            self.add_screen_shake(12, 500)

            # Tetris文字提示（超大）
            self.floating_texts.append(FloatingText("TETRIS!!!", center_x, center_y, (255, 215, 0), 48))
            self.floating_texts.append(FloatingText("PERFECT!", center_x, center_y - 50, (255, 100, 100), 36))

            # 多个冲击波（产生层次感）
            for i in range(3):
                max_radius = grid_width * (0.5 + i * 0.3)
                color = [(255, 255, 0), (255, 100, 100), (100, 255, 255)][i]
                # 延迟启动不同的冲击波
                shockwave = ShockwaveEffect(center_x, center_y, max_radius, color)
                shockwave.current_radius = -i * 30  # 延迟启动
                self.shockwaves.append(shockwave)

            # 大量粒子爆炸
            for _ in range(100):  # Tetris消除超多粒子
                x = center_x + random.randint(-grid_width//2, grid_width//2)
                y = center_y + random.randint(-100, 100)
                color = random.choice([
                    (255, 255, 0), (255, 100, 100), (100, 255, 255),
                    (255, 0, 255), (255, 255, 255), (255, 215, 0)
                ])
                self.particles.append(Particle(x, y, color))

            # 超多彩虹吸入式粒子（全屏所有方向）
            rainbow_colors = [
                (255, 0, 0), (255, 127, 0), (255, 255, 0),
                (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
            ]
            for _ in range(100):
                # 从屏幕外围大范围随机位置
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(400, 600)
                start_x = center_x + math.cos(angle) * distance
                start_y = center_y + math.sin(angle) * distance
                color = random.choice(rainbow_colors)

                self.suck_in_particles.append(
                    SuckInParticle(start_x, start_y, center_x, center_y, color, speed=8.0)
                )

    def add_screen_shake(self, intensity, duration):
        """添加屏幕震动效果"""
        self.screen_shake = ScreenShake(intensity, duration)

    def add_combo_effects(self, combo_count, center_x, center_y):
        """添加连击特效 - 根据连击数提供不同级别的视觉反馈"""
        if combo_count < 2:
            return  # 无连击，无特效

        grid_x, grid_y = GRID_X_OFFSET, GRID_Y_OFFSET
        grid_width = GRID_WIDTH * BLOCK_SIZE

        # 连击级别判定
        if combo_count >= 10:
            # 传奇连击（10+）：史诗级特效
            combo_level = "LEGENDARY!"
            colors = [(255, 0, 0), (255, 215, 0), (0, 255, 255), (255, 0, 255)]
            font_size = 60
            shake_intensity = 10
            particle_count = 80
            speed_mult = 1.5

        elif combo_count >= 6:
            # 超级连击（6-9）：炫彩特效
            combo_level = "SUPER!"
            colors = [(255, 165, 0), (255, 255, 0), (0, 255, 255)]
            font_size = 52
            shake_intensity = 7
            particle_count = 60
            speed_mult = 1.3

        elif combo_count >= 4:
            # 高级连击（4-5）：增强特效
            combo_level = "AMAZING!"
            colors = [(255, 215, 0), (255, 100, 100)]
            font_size = 44
            shake_intensity = 5
            particle_count = 40
            speed_mult = 1.2

        elif combo_count == 3:
            # 中级连击（3）：标准增强
            combo_level = "GREAT!"
            colors = [(255, 255, 0), (255, 165, 0)]
            font_size = 38
            shake_intensity = 4
            particle_count = 30
            speed_mult = 1.1

        else:  # combo_count == 2
            # 低级连击（2）：基础特效
            combo_level = "GOOD!"
            colors = [(200, 200, 255)]
            font_size = 32
            shake_intensity = 2
            particle_count = 20
            speed_mult = 1.0

        # 添加连击等级文字
        color = colors[0]
        self.floating_texts.append(FloatingText(combo_level, center_x, center_y - 80, color, font_size))

        # 添加连击计数文字（例如 "5x COMBO!"）
        combo_color = colors[-1] if len(colors) > 1 else colors[0]
        self.floating_texts.append(FloatingText(f"{combo_count}x COMBO!", center_x, center_y - 40, combo_color, int(font_size * 0.7)))

        # 添加震动效果
        self.add_screen_shake(shake_intensity, 300)

        # 添加旋转粒子效果（围绕中心）
        for i in range(particle_count):
            angle = (i / particle_count) * 2 * math.pi
            distance = random.randint(50, 150)
            start_x = center_x + math.cos(angle) * distance
            start_y = center_y + math.sin(angle) * distance

            # 粒子向中心旋转吸入
            particle_color = random.choice(colors)
            self.suck_in_particles.append(
                SuckInParticle(start_x, start_y, center_x, center_y, particle_color, speed=3.0 * speed_mult)
            )

        # 添加冲击波效果（高等级连击）
        if combo_count >= 4:
            max_radius = grid_width * (0.4 + (combo_count - 4) * 0.1)
            shockwave_color = colors[0]
            self.shockwaves.append(ShockwaveEffect(center_x, center_y, max_radius, shockwave_color))

        # 多重冲击波（传奇连击）
        if combo_count >= 10:
            for i in range(1, 3):
                max_radius = grid_width * (0.3 + i * 0.2)
                color = colors[i % len(colors)]
                shockwave = ShockwaveEffect(center_x, center_y, max_radius, color)
                shockwave.current_radius = -i * 40  # 延迟启动
                self.shockwaves.append(shockwave)

    def add_explosion(self, x, y, color):
        """添加爆炸效果"""
        for _ in range(30):
            self.particles.append(Particle(x, y, color))

    def add_landing_effect(self, piece_x, piece_y, piece_width, piece_height, drop_distance=1):
        """添加方块落地特效 - 丝滑过渡动画"""
        # 计算落地位置
        center_x = GRID_X_OFFSET + piece_x * BLOCK_SIZE + piece_width * BLOCK_SIZE // 2
        center_y = GRID_Y_OFFSET + piece_y * BLOCK_SIZE + piece_height * BLOCK_SIZE // 2

        # 根据下落距离确定效果强度
        if drop_distance >= 10:  # 硬降或长距离下落
            particle_count = 25
            shake_intensity = 3
            shockwave_radius = 60
            flash_duration = 150
        elif drop_distance >= 5:
            particle_count = 15
            shake_intensity = 2
            shockwave_radius = 40
            flash_duration = 100
        else:  # 短距离下落
            particle_count = 8
            shake_intensity = 1
            shockwave_radius = 25
            flash_duration = 50

        # 1. 添加落地闪光效果（丝滑过渡）
        self.landing_flashes.append(LandingFlash(center_x, center_y, piece_width, piece_height, flash_duration))

        # 2. 添加冲击波效果（延迟一点点启动，让闪光先出现）
        shockwave = ShockwaveEffect(center_x, center_y, shockwave_radius, (200, 200, 200))
        shockwave.current_radius = -5  # 延迟5帧开始，让闪光先出现
        self.shockwaves.append(shockwave)

        # 3. 添加轻微震动
        self.add_screen_shake(shake_intensity, 150)

        # 4. 添加落地粒子（从方块形状内向外爆发）
        for _ in range(particle_count):
            # 在方块范围内随机位置（更自然）
            offset_x = random.uniform(-piece_width * BLOCK_SIZE / 2.5, piece_width * BLOCK_SIZE / 2.5)
            offset_y = random.uniform(-piece_height * BLOCK_SIZE / 2.5, piece_height * BLOCK_SIZE / 2.5)
            start_x = center_x + offset_x
            start_y = center_y + offset_y

            # 粒子向外快速扩散 - 使用主题粒子颜色
            if self.theme and self.theme.particle_colors:
                color = random.choice(self.theme.particle_colors)
            else:
                # 默认白色粒子
                color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            particle = Particle(start_x, start_y, color)

            # 根据位置计算向外方向
            angle = math.atan2(offset_y, offset_x)
            speed = random.uniform(2, 5)
            particle.vx = math.cos(angle) * speed
            particle.vy = math.sin(angle) * speed - 0.5  # 稍微向上
            self.particles.append(particle)

    def update(self):
        """更新所有动画"""
        # 更新粒子
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

        # 更新吸入式粒子
        self.suck_in_particles = [p for p in self.suck_in_particles if p.life > 0]
        for particle in self.suck_in_particles:
            particle.update()

        # 更新落地闪光
        self.landing_flashes = [lf for lf in self.landing_flashes if lf.update()]

        # 更新行消除动画
        for anim in self.line_clear_animations:
            anim['alpha'] -= 10
            anim['scale'] += 0.05
        self.line_clear_animations = [a for a in self.line_clear_animations if a['alpha'] > 0]

        # 更新光带动画
        self.light_beams = [beam for beam in self.light_beams if beam.update()]

        # 更新冲击波
        self.shockwaves = [sw for sw in self.shockwaves if sw.update()]

        # 更新浮动文字
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

    def get_shake_offset(self):
        """获取震动偏移量"""
        if self.screen_shake:
            return self.screen_shake.get_offset()
        return (0, 0)

    def draw(self, surface, scale=1.0):
        """绘制所有动画"""
        # 绘制光带动画
        for beam in self.light_beams:
            beam.draw(surface, scale)

        # 绘制落地闪光效果（最上层）
        for flash in self.landing_flashes:
            flash.draw(surface)

        # 绘制冲击波
        for shockwave in self.shockwaves:
            shockwave.draw(surface)

        # 绘制粒子
        for particle in self.particles:
            particle.draw(surface)

        # 绘制吸入式粒子
        for particle in self.suck_in_particles:
            particle.draw(surface)

        # 绘制浮动文字
        for ft in self.floating_texts:
            # 尝试使用游戏字体路径
            font_paths = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]
            font = None
            for font_path in font_paths:
                try:
                    font = font_path
                    break
                except:
                    continue
            ft.draw(surface, font)

        # 绘制行消除特效
        for anim in self.line_clear_animations:
            if anim['alpha'] > 0:
                # 绘制闪光效果
                s = pygame.Surface((WINDOW_WIDTH, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((255, 255, 255, anim['alpha']))
                surface.blit(s, (0, GRID_Y_OFFSET + anim['y'] * BLOCK_SIZE))

                # 绘制连击文字
                if anim['combo'] > 1:
                    font = pygame.font.Font(None, int(36 * anim['scale']))
                    text = font.render(f"{anim['combo']}x COMBO!", True, (255, 255, 100))
                    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, GRID_Y_OFFSET + anim['y'] * BLOCK_SIZE))
                    surface.blit(text, text_rect)


class Statistics:
    """统计数据系统 - 支持异步持久化存储"""

    def __init__(self, filename='tetris_statistics.json'):
        self.filename = filename
        self.load_statistics()
        # 设置新的游戏开始时间（不覆盖累计数据）
        self.game_start_time = pygame.time.get_ticks()
        self.current_session_time = 0  # 当前会话的游戏时间
        self.last_piece_type = None
        self.consecutive_same_pieces = 0
        self.five_line_clears_time = 0

        # 异步保存支持
        self._save_queue = queue.Queue()
        self._save_thread = None
        self._stop_thread = False
        self._start_save_thread()

    def _start_save_thread(self):
        """启动后台保存线程"""
        if self._save_thread is None or not self._save_thread.is_alive():
            self._stop_thread = False
            self._save_thread = threading.Thread(target=self._save_worker, daemon=True)
            self._save_thread.start()

    def _save_worker(self):
        """后台保存工作线程"""
        while not self._stop_thread:
            try:
                # 等待保存任务，超时0.1秒检查是否需要停止
                data = self._save_queue.get(timeout=0.1)
                if data is not None:
                    self._save_to_file(data)
                self._save_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                # 静默处理保存错误
                pass

    def _save_to_file(self, data):
        """实际写入文件的方法"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (PermissionError, IOError):
            pass  # 无法保存文件时静默失败

    def __del__(self):
        """析构函数，确保线程正确停止"""
        self._stop_thread = True
        if self._save_thread and self._save_thread.is_alive():
            self._save_thread.join(timeout=1.0)

    def load_statistics(self):
        """加载统计数据"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 加载累计数据
                    self.total_game_time = data.get('total_game_time', 0)
                    self.total_moves = data.get('total_moves', 0)
                    self.total_rotations = data.get('total_rotations', 0)
                    self.highest_combo = data.get('highest_combo', 0)
                    self.single_line_clears = data.get('single_line_clears', 0)
                    self.double_line_clears = data.get('double_line_clears', 0)
                    self.triple_line_clears = data.get('triple_line_clears', 0)
                    self.tetris_clears = data.get('tetris_clears', 0)
                    self.max_consecutive_same = data.get('max_consecutive_same', 0)
                    self.games_played = data.get('games_played', 0)
                    self.total_score = data.get('total_score', 0)
                    self.highest_score = data.get('highest_score', 0)
                    return
            except:
                pass

        # 如果加载失败或文件不存在，初始化为默认值
        self.total_game_time = 0
        self.total_moves = 0
        self.total_rotations = 0
        self.highest_combo = 0
        self.single_line_clears = 0
        self.double_line_clears = 0
        self.triple_line_clears = 0
        self.tetris_clears = 0
        self.max_consecutive_same = 0
        self.games_played = 0
        self.total_score = 0
        self.highest_score = 0

    def save_statistics(self):
        """异步保存统计数据 - 不阻塞游戏"""
        try:
            # 更新累计游戏时间
            self.update_total_game_time()

            data = {
                'total_game_time': self.total_game_time,
                'total_moves': self.total_moves,
                'total_rotations': self.total_rotations,
                'highest_combo': self.highest_combo,
                'single_line_clears': self.single_line_clears,
                'double_line_clears': self.double_line_clears,
                'triple_line_clears': self.triple_line_clears,
                'tetris_clears': self.tetris_clears,
                'max_consecutive_same': self.max_consecutive_same,
                'games_played': self.games_played,
                'total_score': self.total_score,
                'highest_score': self.highest_score,
            }
            # 将保存任务放入队列，由后台线程处理
            self._save_queue.put(data)
        except Exception:
            # 无法保存时静默失败
            pass

    def reset_current_session(self):
        """重置当前会话数据（游戏重新开始时调用）"""
        self.game_start_time = pygame.time.get_ticks()
        self.current_session_time = 0
        self.last_piece_type = None
        self.consecutive_same_pieces = 0
        self.five_line_clears_time = 0
        self.games_played += 1  # 游戏次数+1
        self.save_statistics()  # 保存

    def update_total_game_time(self):
        """更新累计游戏时间"""
        current_time = pygame.time.get_ticks()
        self.current_session_time = current_time - self.game_start_time
        # total_game_time 是历史累计时间，不包含当前会话
        # 只有在保存时才会合并

    def get_total_game_time_with_session(self):
        """获取包含当前会话的总游戏时间"""
        current_time = pygame.time.get_ticks()
        session_time = current_time - self.game_start_time
        return self.total_game_time + session_time

    def update_game_time(self):
        """更新游戏时间（用于显示）"""
        # 这个方法现在返回包含当前会话的总时间
        self.current_session_time = pygame.time.get_ticks() - self.game_start_time

    def get_formatted_time(self, milliseconds):
        """格式化时间为 HH:MM:SS"""
        seconds = milliseconds // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def record_line_clear(self, lines_count):
        """记录消除统计"""
        if lines_count == 1:
            self.single_line_clears += 1
        elif lines_count == 2:
            self.double_line_clears += 1
        elif lines_count == 3:
            self.triple_line_clears += 1
        elif lines_count == 4:
            self.tetris_clears += 1

    def record_combo(self, combo_count):
        """记录连击"""
        if combo_count > self.highest_combo:
            self.highest_combo = combo_count

    def record_score(self, score):
        """记录分数"""
        self.total_score += score
        if score > self.highest_score:
            self.highest_score = score


class Achievement:
    """成就系统"""

    ACHIEVEMENTS_LIST = [
        # 基础成就
        {"id": "first_piece", "name": "初出茅庐", "desc": "放置第一个方块", "type": "basic"},
        {"id": "first_clear", "name": "初次消除", "desc": "消除第一行", "type": "basic"},
        {"id": "score_500", "name": "五百小胜", "desc": "达到500分", "type": "basic"},
        {"id": "level_3", "name": "渐入佳境", "desc": "达到3级", "type": "basic"},
        {"id": "combo_3", "name": "连击新手", "desc": "达成3连击", "type": "basic"},
        {"id": "tetris_1", "name": "Tetris入门", "desc": "达成1次四行消除", "type": "basic"},
        {"id": "survive_5min", "name": "坚持不懈", "desc": "游戏时间超过5分钟", "type": "basic"},
        {"id": "moves_100", "name": "勤能补拙", "desc": "操作次数达到100", "type": "basic"},
        {"id": "neon_master", "name": "霓虹爱好者", "desc": "开启霓虹模式", "type": "basic"},
        {"id": "score_1000", "name": "千分王者", "desc": "达到1000分", "type": "advanced"},
        {"id": "score_10000", "name": "万分传说", "desc": "达到10000分", "type": "advanced"},
        {"id": "combo_10", "name": "极速连击", "desc": "达成10连击", "type": "advanced"},
        {"id": "clear_500", "name": "消除500", "desc": "累计消除500行", "type": "advanced"},
        {"id": "clear_1000", "name": "消除1000", "desc": "累计消除1000行", "type": "advanced"},
        {"id": "moves_1000", "name": "幽灵操作", "desc": "操作次数超过1000", "type": "advanced"},
        {"id": "tetris_10", "name": "Tetris大师", "desc": "达成10次四行消除", "type": "advanced"},
        {"id": "lightning", "name": "闪电手", "desc": "10秒内消除5行", "type": "advanced"},
        {"id": "lucky", "name": "幸运儿", "desc": "连续得到相同方块5次", "type": "advanced"},
        {"id": "legend", "name": "不朽传奇", "desc": "游戏时间超过1小时", "type": "advanced"},
    ]

    def __init__(self, filename='tetris_achievements.json'):
        self.filename = filename
        self.unlocked = self.load_achievements()
        self.notification_queue = []  # 待显示的通知
        self.notification_timer = 0
        self.notification_duration = 3000  # 显示3秒
        self.current_notification = None

    def load_achievements(self):
        """加载已解锁成就"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('unlocked', [])
            except:
                return []
        return []

    def save_achievements(self):
        """保存成就"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({'unlocked': self.unlocked}, f, indent=2, ensure_ascii=False)
        except (PermissionError, IOError):
            # 无法保存文件时静默失败
            pass

    def unlock(self, achievement_id):
        """解锁成就"""
        if achievement_id not in self.unlocked and achievement_id in [a['id'] for a in self.ACHIEVEMENTS_LIST]:
            self.unlocked.append(achievement_id)
            self.save_achievements()
            # 添加通知
            achievement = next(a for a in self.ACHIEVEMENTS_LIST if a['id'] == achievement_id)
            self.notification_queue.append(achievement)
            return True
        return False

    def update(self, current_time):
        """更新通知显示"""
        if self.current_notification:
            if current_time - self.notification_timer > self.notification_duration:
                self.current_notification = None
        elif self.notification_queue:
            self.current_notification = self.notification_queue.pop(0)
            self.notification_timer = current_time

    def draw_notification(self, screen, window_width, scale_factor=1.0):
        """绘制成就解锁通知"""
        if not self.current_notification:
            return

        # 通知框参数
        notification_width = int(300 * scale_factor)
        notification_height = int(60 * scale_factor)
        x = (window_width - notification_width) // 2
        y = 20  # 顶部显示

        # 背景
        bg_rect = pygame.Rect(x, y, notification_width, notification_height)
        s = pygame.Surface((notification_width, notification_height), pygame.SRCALPHA)
        s.fill((40, 40, 50, 230))  # 半透明背景
        screen.blit(s, (x, y))

        # 金色边框
        pygame.draw.rect(screen, (255, 215, 0), bg_rect, 2, border_radius=int(8 * scale_factor))

        # 动态字体
        title_size = max(14, int(20 * scale_factor))
        desc_size = max(10, int(14 * scale_factor))

        # 尝试加载中文字体
        font_paths = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]
        title_font = None
        desc_font = None
        for font_path in font_paths:
            try:
                title_font = pygame.font.Font(font_path, title_size)
                desc_font = pygame.font.Font(font_path, desc_size)
                break
            except:
                continue
        if not title_font:
            title_font = pygame.font.Font(None, title_size)
        if not desc_font:
            desc_font = pygame.font.Font(None, desc_size)

        # 绘制文字
        title_text = title_font.render(f"🏆 成就解锁: {self.current_notification['name']}", True, (255, 215, 0))
        desc_text = desc_font.render(self.current_notification['desc'], True, (200, 200, 220))

        screen.blit(title_text, (x + int(10 * scale_factor), y + int(10 * scale_factor)))
        screen.blit(desc_text, (x + int(10 * scale_factor), y + int(35 * scale_factor)))


class Leaderboard:
    """排行榜系统"""

    def __init__(self, filename='tetris_leaderboard.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """加载排行榜"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_scores(self):
        """保存排行榜"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
        except (PermissionError, IOError):
            # 无法保存文件时静默失败
            pass

    def add_score(self, score, level, lines):
        """添加分数"""
        entry = {
            'score': score,
            'level': level,
            'lines': lines,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]  # 只保留前10名
        self.save_scores()

    def get_top_scores(self, limit=5):
        """获取前N名"""
        return self.scores[:limit]

    def is_high_score(self, score):
        """检查是否是高分"""
        if len(self.scores) < 10:
            return True
        return score > self.scores[-1]['score']


class Tetris:
    """俄罗斯方块游戏主类 - 增强版"""

    def __init__(self):
        """初始化游戏"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("俄罗斯方块 - 增强版")
        self.clock = pygame.time.Clock()

        # 字体路径管理（必须在加载字体之前初始化）
        self.font_path = None

        # 尝试加载中文字体
        self.font = self.load_chinese_font(24)
        self.large_font = self.load_chinese_font(48)

        # 窗口大小管理
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.scale_factor = 1.0  # 缩放因子

        # 游戏状态
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.waiting_to_start = True  # 等待开始状态
        self.countdown = 3  # 倒计时秒数
        self.countdown_timer = 0  # 倒计时计时器
        self.countdown_active = False  # 倒计时是否激活

        # 方块
        self.piece_bag = []  # 7-bag随机系统的袋子
        self.current_piece = self.create_piece()
        self.next_piece = self.create_piece()
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0

        # 下落计时器
        self.fall_time = 0
        self.fall_speed = 500

        # 新增功能
        self.settings_manager = SettingsManager()
        self.keybind_manager = KeyBindManager()
        self.sound_manager = SoundManager()

        # 🎨 主题系统 - 随机选择主题（必须在AnimationManager之前）
        self.current_theme = random.choice(THEMES)

        # 从设置加载初始状态（如果配置文件存在则使用配置的值，否则使用默认值）
        self.sound_manager.enabled = self.settings_manager.get('sound_enabled', True)
        self.sound_manager.music_enabled = self.settings_manager.get('music_enabled', True)
        self.show_ghost = self.settings_manager.get('show_ghost', True)
        self.neon_mode = self.settings_manager.get('neon_mode', True)  # 默认开启霓虹模式

        # 现在可以创建AnimationManager并传递主题
        self.animation_manager = AnimationManager(theme=self.current_theme)  # 传递主题
        self.piece_animation = PieceAnimation()  # 方块动画管理器
        self.leaderboard = Leaderboard()
        self.statistics = Statistics()
        self.achievement = Achievement()
        self.combo_count = 0
        self.last_clear_time = 0
        self.show_statistics = False  # 是否显示统计面板
        self.show_achievements = False  # 是否显示成就面板
        self.show_settings = False  # 是否显示设置菜单
        self.key_binding_mode = None  # 当前正在绑定的键位
        self.dragging_slider = None  # 当前正在拖动的滑块 ('music' 或 'sfx')
        self.first_piece_placed = False  # 成就跟踪
        self.last_save_time = pygame.time.get_ticks()  # 统计数据上次保存时间

        # 按钮点击反馈
        self.reset_button_clicked = 0  # 点击动画计时器
        self.reset_keybind_button_clicked = 0  # 键位重置按钮点击动画计时器

        # 主题下拉框状态
        self.theme_dropdown_opened = False  # 下拉框是否展开

        # 面板自动暂停
        self.was_paused_before_panel = False  # 记录打开面板前的暂停状态

        # 生成背景音乐（使用当前主题）
        self.sound_manager.generate_background_music(self.current_theme)

    def draw_theme_background(self):
        """根据主题绘制背景效果"""
        theme = self.current_theme
        width, height = self.window_width, self.window_height

        # 根据主题效果类型绘制不同的背景
        if theme.bg_effect_type == "gradient":
            # 垂直渐变背景
            for y in range(height):
                ratio = y / height
                r = int(theme.bg_color[0] * (1 - ratio) + theme.bg_color2[0] * ratio)
                g = int(theme.bg_color[1] * (1 - ratio) + theme.bg_color2[1] * ratio)
                b = int(theme.bg_color[2] * (1 - ratio) + theme.bg_color2[2] * ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))

        elif theme.bg_effect_type == "stars":
            # 星空背景 - 先填充深色
            self.screen.fill(theme.bg_color)
            # 绘制星星（使用随机位置但固定种子，避免每帧闪烁）
            import hashlib
            seed = int(hashlib.md5(str(pygame.time.get_ticks() // 1000).encode()).hexdigest(), 16) % 1000
            random.seed(seed)
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                color = (
                    min(255, theme.bg_color2[0] + brightness),
                    min(255, theme.bg_color2[1] + brightness),
                    min(255, theme.bg_color2[2] + brightness)
                )
                pygame.draw.circle(self.screen, color, (x, y), size)

        elif theme.bg_effect_type == "particles":
            # 粒子背景 - 浮动的小方块
            self.screen.fill(theme.bg_color)
            import hashlib
            seed = int(hashlib.md5(str(pygame.time.get_ticks() // 500).encode()).hexdigest(), 16) % 1000
            random.seed(seed)
            for _ in range(30):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(3, 8)
                color = random.choice(theme.particle_colors)
                # 添加透明度
                s = pygame.Surface((size, size), pygame.SRCALPHA)
                alpha = random.randint(30, 80)
                s.fill((color[0], color[1], color[2], alpha))
                self.screen.blit(s, (x, y))

        elif theme.bg_effect_type == "waves":
            # 波浪效果背景
            self.screen.fill(theme.bg_color)
            import hashlib
            seed = int(hashlib.md5(str(pygame.time.get_ticks() // 200).encode()).hexdigest(), 16) % 1000
            random.seed(seed)
            for i in range(5):
                wave_y = int(height * (0.2 + 0.15 * i))
                amplitude = 10 + i * 5
                for x in range(0, width, 5):
                    wave_offset = math.sin(x * 0.02 + pygame.time.get_ticks() * 0.001 + i) * amplitude
                    y = wave_y + int(wave_offset)
                    alpha = 30 - i * 5
                    color = (
                        min(255, theme.bg_color2[0] + 50),
                        min(255, theme.bg_color2[1] + 50),
                        min(255, theme.bg_color2[2] + 50)
                    )
                    s = pygame.Surface((5, 2), pygame.SRCALPHA)
                    s.fill((color[0], color[1], color[2], alpha))
                    self.screen.blit(s, (x, y))

        elif theme.bg_effect_type == "aurora":
            # 极光效果 - 使用多个渐变叠加
            self.screen.fill(theme.bg_color)
            # 绘制极光带
            import hashlib
            seed = int(hashlib.md5(str(pygame.time.get_ticks() // 300).encode()).hexdigest(), 16) % 1000
            random.seed(seed)
            for i in range(3):
                aurora_y = int(height * (0.3 + 0.2 * i))
                color = theme.particle_colors[i % len(theme.particle_colors)]
                for x in range(0, width, 10):
                    wave_offset = math.sin(x * 0.01 + pygame.time.get_ticks() * 0.002 + i * 2) * 30
                    y = aurora_y + int(wave_offset)
                    s = pygame.Surface((15, 20 + i * 10), pygame.SRCALPHA)
                    alpha = 20 - i * 5
                    s.fill((color[0], color[1], color[2], alpha))
                    self.screen.blit(s, (x, y))

        else:
            # 默认纯色背景
            self.screen.fill(theme.bg_color)

    def load_chinese_font(self, size):
        """加载支持中文的字体"""
        # Windows 系统字体列表（按优先级）
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",    # 黑体
            "C:/Windows/Fonts/simsun.ttc",    # 宋体
            "C:/Windows/Fonts/simkai.ttf",    # 楷体
        ]

        for font_path in font_paths:
            try:
                self.font_path = font_path  # 保存字体路径
                return pygame.font.Font(font_path, size)
            except:
                continue

        # 如果都失败，使用默认字体（但不支持中文）
        self.font_path = None
        return pygame.font.Font(None, size)

    def get_scaled_offset(self, base_x, base_y):
        """根据窗口缩放计算偏移量"""
        scaled_x = int(base_x * self.scale_factor)
        scaled_y = int(base_y * self.scale_factor)
        return scaled_x, scaled_y

    def get_scaled_size(self, base_size):
        """根据窗口缩放计算大小"""
        return int(base_size * self.scale_factor)

    def create_piece(self):
        """使用7-bag随机系统创建新方块"""
        # 如果袋子空了，重新装满（7种方块各一个）
        if not self.piece_bag:
            # 所有7种方块的索引
            self.piece_bag = list(range(len(SHAPES)))
            random.shuffle(self.piece_bag)

        # 从袋子中取出一个方块
        piece_index = self.piece_bag.pop()

        # 根据索引获取形状和颜色
        shape = SHAPES[piece_index]
        color = piece_index + 1  # 颜色索引 = 方块索引 + 1

        return [[color if cell == 1 else 0 for cell in row] for row in shape]

    def get_next_pieces_preview(self, count=5):
        """获取接下来N个方块的预览（用于UI显示）"""
        preview = []
        temp_bag = self.piece_bag.copy()
        temp_piece_index = piece_index = 0

        # 模拟从袋子中取方块
        for _ in range(count):
            if not temp_bag:
                temp_bag = list(range(len(SHAPES)))
                random.shuffle(temp_bag)

            piece_idx = temp_bag.pop()
            shape = SHAPES[piece_idx]
            color = piece_idx + 1
            piece = [[color if cell == 1 else 0 for cell in row] for row in shape]
            preview.append(piece)

        return preview

    def rotate_piece(self, piece):
        """旋转方块"""
        return [list(row) for row in zip(*piece[::-1])]

    def valid_move(self, piece, offset_x, offset_y):
        """检查移动是否有效"""
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell != 0:
                    new_x = x + offset_x
                    new_y = y + offset_y

                    if (new_x < 0 or new_x >= GRID_WIDTH or
                        new_y >= GRID_HEIGHT):
                        return False

                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return False
        return True

    def merge_piece(self):
        """合并方块到网格"""
        # 计算下落距离（用于落地特效）
        piece_height = len(self.current_piece)
        piece_width = len(self.current_piece[0])

        # 查找幽灵方块位置来计算下落距离
        ghost_y = self.current_y
        while self.valid_move(self.current_piece, self.current_x, ghost_y + 1):
            ghost_y += 1
        drop_distance = max(1, ghost_y - self.current_y)

        # 合并方块到网格
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell != 0:
                    grid_y = y + self.current_y
                    grid_x = x + self.current_x
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = cell

        # 添加落地特效
        self.animation_manager.add_landing_effect(
            self.current_x, self.current_y, piece_width, piece_height, drop_distance
        )

        # 播放落地音效（根据下落距离调整音量）
        if drop_distance >= 10:
            self.sound_manager.play('hard_drop')
        else:
            self.sound_manager.play('land')

        # 成就跟踪
        if not self.first_piece_placed:
            self.first_piece_placed = True
            self.achievement.unlock('first_piece')

    def clear_lines(self):
        """清除完整的行 - 增强版带连击和霓虹光效"""
        current_time = pygame.time.get_ticks()

        # 检查连击（2秒内连续消除）
        if current_time - self.last_clear_time < 2000:
            self.combo_count += 1
        else:
            self.combo_count = 1

        self.last_clear_time = current_time

        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        if lines_to_clear:
            lines_count = len(lines_to_clear)

            # 统计跟踪
            self.statistics.record_line_clear(lines_count)
            self.statistics.record_combo(self.combo_count)

            # 闪电手成就 - 10秒内消除5行
            if self.statistics.five_line_clears_time == 0:
                self.statistics.five_line_clears_time = current_time
            lines_so_far = (self.statistics.single_line_clears +
                          self.statistics.double_line_clears * 2 +
                          self.statistics.triple_line_clears * 3 +
                          self.statistics.tetris_clears * 4)
            if current_time - self.statistics.five_line_clears_time <= 10000 and lines_so_far >= 5:
                self.achievement.unlock('lightning')

            # 成就解锁
            self.achievement.unlock('first_clear')

            if lines_count == 4:
                self.achievement.unlock('tetris_1')
                total_tetris = self.statistics.tetris_clears
                if total_tetris >= 10:
                    self.achievement.unlock('tetris_10')

            if self.combo_count >= 3:
                self.achievement.unlock('combo_3')
            if self.combo_count >= 10:
                self.achievement.unlock('combo_10')

            total_cleared = (self.statistics.single_line_clears +
                           self.statistics.double_line_clears * 2 +
                           self.statistics.triple_line_clears * 3 +
                           self.statistics.tetris_clears * 4)
            if total_cleared >= 500:
                self.achievement.unlock('clear_500')
            if total_cleared >= 1000:
                self.achievement.unlock('clear_1000')

            # 播放消除音效
            if lines_count == 1:
                self.sound_manager.play('clear1')
            elif lines_count == 2:
                self.sound_manager.play('clear2')
            elif lines_count == 3:
                self.sound_manager.play('clear3')
            else:
                self.sound_manager.play('clear4')

            # 连击音效
            if self.combo_count > 1:
                self.sound_manager.play('combo')

            # 添加霓虹光带动画（炫酷消除效果）
            if lines_to_clear:
                grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
                block_size = self.get_scaled_size(BLOCK_SIZE)
                grid_rect = (grid_x, grid_y, GRID_WIDTH * block_size, GRID_HEIGHT * block_size)

                start_y = min(lines_to_clear)
                end_y = max(lines_to_clear)

                # 计算消除行中心位置（用于连击特效）
                center_y = grid_y + (start_y + end_y) / 2 * block_size + block_size // 2
                center_x = grid_x + GRID_WIDTH * block_size // 2

                # 添加光带动画（会自动触发震动）
                self.animation_manager.add_light_beam(start_y, end_y, grid_rect, lines_count, self.neon_mode)

                # 添加增强连击特效
                self.animation_manager.add_combo_effects(self.combo_count, center_x, center_y)

            # 保留旧的粒子效果（兼容）
            for line_y in lines_to_clear:
                self.animation_manager.add_line_clear(line_y, self.combo_count)

                # 在每行添加爆炸效果
                for x in range(GRID_WIDTH):
                    color = COLORS[self.grid[line_y][x]]
                    center_x = GRID_X_OFFSET + x * BLOCK_SIZE + BLOCK_SIZE // 2
                    center_y = GRID_Y_OFFSET + line_y * BLOCK_SIZE + BLOCK_SIZE // 2
                    self.animation_manager.add_explosion(center_x, center_y, color)

            # 移除行并添加新行
            for y in sorted(lines_to_clear, reverse=True):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

            # 计算分数（带连击加成）
            base_score = lines_count * 100 * self.level
            combo_bonus = (self.combo_count - 1) * 50 * lines_count
            self.score += base_score + combo_bonus

            self.lines_cleared += lines_count
            old_level = self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 50)

            # 成就解锁 - 分数和等级
            if self.score >= 500:
                self.achievement.unlock('score_500')
            if self.score >= 1000:
                self.achievement.unlock('score_1000')
            if self.score >= 10000:
                self.achievement.unlock('score_10000')
            if self.level >= 3:
                self.achievement.unlock('level_3')

    def new_piece(self):
        """生成新方块"""
        self.current_piece = self.next_piece
        self.next_piece = self.create_piece()
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0

        # 跟踪方块类型（用于幸运儿成就）
        current_piece_type = self.get_piece_type(self.current_piece)
        if self.statistics.last_piece_type == current_piece_type:
            self.statistics.consecutive_same_pieces += 1
        else:
            self.statistics.consecutive_same_pieces = 1
            self.statistics.last_piece_type = current_piece_type

        if self.statistics.consecutive_same_pieces > self.statistics.max_consecutive_same:
            self.statistics.max_consecutive_same = self.statistics.consecutive_same_pieces

        if self.statistics.consecutive_same_pieces >= 5:
            self.achievement.unlock('lucky')

        if not self.valid_move(self.current_piece, self.current_x, self.current_y):
            self.game_over = True
            self.sound_manager.play('gameover')

            # 保存统计数据
            self.statistics.record_score(self.score)
            self.statistics.save_statistics()

            # 检查是否是高分
            if self.leaderboard.is_high_score(self.score):
                self.leaderboard.add_score(self.score, self.level, self.lines_cleared)

    def get_piece_type(self, piece):
        """获取方块类型（用于成就跟踪）"""
        # 将方块转换为元组字符串作为唯一标识
        return tuple(tuple(row) for row in piece)

    def draw_3d_block(self, rect, color_index):
        """绘制3D方块 - 使用主题配色"""
        # 使用主题配色方案
        main_color = self.current_theme.piece_colors[color_index]
        highlight = self.current_theme.highlight_colors[color_index]
        shadow = self.current_theme.shadow_colors[color_index]

        # 霓虹发光效果
        if self.neon_mode:
            glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*main_color, 50),
                           (10, 10, rect.width, rect.height))
            self.screen.blit(glow_surface, (rect.x - 10, rect.y - 10))

        # 主方块
        main_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
        pygame.draw.rect(self.screen, main_color, main_rect)

        # 高光和阴影
        pygame.draw.line(self.screen, highlight,
                        (rect.x + 2, rect.y + 2), (rect.right - 2, rect.y + 2), 3)
        pygame.draw.line(self.screen, highlight,
                        (rect.x + 2, rect.y + 2), (rect.x + 2, rect.bottom - 2), 3)
        pygame.draw.line(self.screen, shadow,
                        (rect.x + 2, rect.bottom - 2), (rect.right - 2, rect.bottom - 2), 3)
        pygame.draw.line(self.screen, shadow,
                        (rect.right - 2, rect.y + 2), (rect.right - 2, rect.bottom - 2), 3)

    def draw_grid(self):
        """绘制游戏网格 - 使用主题配色"""
        # 计算缩放后的位置和大小
        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        grid_rect = pygame.Rect(
            grid_x - 2, grid_y - 2,
            GRID_WIDTH * block_size + 4, GRID_HEIGHT * block_size + 4
        )
        pygame.draw.rect(self.screen, self.current_theme.grid_bg, grid_rect)

        # 霓虹边框增强 - 使用主题高亮色
        if self.neon_mode:
            # 外层发光边框（主题高亮色）
            pygame.draw.rect(self.screen, self.current_theme.text_highlight, grid_rect, 3)
            # 内层亮边框（主题文字色）
            inner_rect = pygame.Rect(
                grid_x - 1, grid_y - 1,
                GRID_WIDTH * block_size + 2, GRID_HEIGHT * block_size + 2
            )
            pygame.draw.rect(self.screen, self.current_theme.text_color, inner_rect, 1)
        else:
            # 普通双层边框 - 使用主题网格边框色
            pygame.draw.rect(self.screen, self.current_theme.grid_border, grid_rect, 3)
            inner_rect = pygame.Rect(
                grid_x - 1, grid_y - 1,
                GRID_WIDTH * block_size + 2, GRID_HEIGHT * block_size + 2
            )
            # 稍微提亮的边框
            bright_border = tuple(min(255, c + 40) for c in self.current_theme.grid_border)
            pygame.draw.rect(self.screen, bright_border, inner_rect, 1)

        # 棋盘格效果：从主题网格背景色派生的两种颜色
        checker_color_1 = self.current_theme.grid_bg
        checker_color_2 = tuple(min(255, c + 10) for c in self.current_theme.grid_bg)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    grid_x + x * block_size,
                    grid_y + y * block_size,
                    block_size, block_size
                )

                if self.grid[y][x] != 0:
                    self.draw_3d_block(rect, self.grid[y][x])
                else:
                    # 使用棋盘格效果绘制空格子
                    cell_color = checker_color_1 if (x + y) % 2 == 0 else checker_color_2
                    pygame.draw.rect(self.screen, cell_color, rect)
                    # 绘制细线网格
                    pygame.draw.rect(self.screen, (40, 40, 50), rect, 1)

    def draw_piece(self, piece, offset_x, offset_y, animated=False):
        """绘制方块 - 支持缩放和动画"""
        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        # 如果启用了动画，获取动画插值位置
        if animated and self.piece_animation.animating:
            if self.piece_animation.animation_type == 'move':
                anim_x, anim_y = self.piece_animation.get_current_position(offset_x, offset_y)
                offset_x, offset_y = anim_x, anim_y

        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell != 0:
                    rect = pygame.Rect(
                        grid_x + (x + offset_x) * block_size,
                        grid_y + (y + offset_y) * block_size,
                        block_size, block_size
                    )
                    self.draw_3d_block(rect, cell)

    def get_ghost_piece_y(self, piece, start_y):
        """计算幽灵方块的Y坐标（最低有效位置）"""
        ghost_y = start_y
        while self.valid_move(piece, self.current_x, ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def draw_ghost_piece(self):
        """绘制幽灵方块 - 方案C: 多层幽灵方块"""
        if self.game_over or self.waiting_to_start or self.countdown_active or not self.show_ghost:
            return

        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        # 计算幽灵方块位置
        ghost_y = self.get_ghost_piece_y(self.current_piece, self.current_y)

        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell != 0:
                    rect = pygame.Rect(
                        grid_x + (x + self.current_x) * block_size,
                        grid_y + (y + ghost_y) * block_size,
                        block_size, block_size
                    )

                    # 获取方块颜色
                    main_color = COLORS[cell]

                    # 第一层（底层）：灰色半透明 (30% alpha)
                    s1 = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
                    s1.fill((100, 100, 100, 76))  # 30% alpha
                    self.screen.blit(s1, rect.topleft)

                    # 第二层（中层）：当前方块颜色半透明 (20% alpha)
                    s2 = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
                    s2.fill((*main_color, 51))  # 20% alpha
                    self.screen.blit(s2, rect.topleft)

                    # 第三层（顶层）：白色边框 (50% alpha)
                    pygame.draw.rect(self.screen, (255, 255, 255, 128), rect, 2)

                    # 霓虹模式下发光
                    if self.neon_mode:
                        glow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surface, (*main_color, 30),
                                       (5, 5, rect.width, rect.height))
                        self.screen.blit(glow_surface, (rect.x - 5, rect.y - 5))

    def draw_statistics_panel(self):
        """绘制统计面板 - 方案A: 弹窗式"""
        scale = self.scale_factor

        # 半透明背景遮罩
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 面板尺寸
        panel_width = int(420 * scale)
        panel_height = int(520 * scale)
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        # 面板背景
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (28, 28, 36), panel_rect, border_radius=int(12 * scale))
        pygame.draw.rect(self.screen, (0, 200, 255), panel_rect, 2, border_radius=int(12 * scale))

        # 动态字体
        title_size = max(20, int(32 * scale))
        text_size = max(11, int(16 * scale))
        small_size = max(10, int(14 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            text_font = pygame.font.Font(self.font_path, text_size)
            small_font = pygame.font.Font(self.font_path, small_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            text_font = pygame.font.Font(None, text_size)
            small_font = pygame.font.Font(None, small_size)

        # 标题
        title_text = title_font.render("📊 详细统计", True, (0, 200, 255))
        title_rect = title_text.get_rect(center=(self.window_width // 2, panel_y + int(30 * scale)))
        self.screen.blit(title_text, title_rect)

        # 分隔线
        line_y = panel_y + int(55 * scale)
        pygame.draw.line(self.screen, (0, 200, 255),
                        (panel_x + int(20 * scale), line_y),
                        (panel_x + panel_width - int(20 * scale), line_y), 2)

        # 更新并格式化数据
        total_time = self.statistics.get_total_game_time_with_session()
        total_lines = (self.statistics.single_line_clears +
                      self.statistics.double_line_clears * 2 +
                      self.statistics.triple_line_clears * 3 +
                      self.statistics.tetris_clears * 4)
        total_ops = self.statistics.total_moves + self.statistics.total_rotations

        stats_data = [
            ("累计游戏时间", self.statistics.get_formatted_time(total_time), (100, 200, 255)),
            ("总消除行数", str(total_lines), (150, 255, 150)),
            ("最高连击", f"{self.statistics.highest_combo}x", (255, 200, 100)),
            ("操作次数", str(total_ops), (200, 150, 255)),
            ("历史最高分", f"{self.statistics.highest_score:,}", (255, 215, 0)),
            ("累计得分", f"{self.statistics.total_score:,}", (255, 180, 50)),
            ("游戏场次", str(self.statistics.games_played), (180, 180, 200)),
            ("", "", (0, 0, 0)),  # 分隔
            ("单行消除", str(self.statistics.single_line_clears), (200, 200, 200)),
            ("双行消除", str(self.statistics.double_line_clears), (200, 200, 200)),
            ("三行消除", str(self.statistics.triple_line_clears), (200, 200, 200)),
            ("四行消除", str(self.statistics.tetris_clears), (255, 100, 100)),
        ]

        # 绘制统计项
        start_y = panel_y + int(70 * scale)
        line_height = int(32 * scale)

        for i, (label, value, color) in enumerate(stats_data):
            if label == "":  # 分隔线
                sep_y = start_y + i * line_height - int(5 * scale)
                pygame.draw.line(self.screen, (60, 60, 80),
                                (panel_x + int(20 * scale), sep_y),
                                (panel_x + panel_width - int(20 * scale), sep_y), 1)
                continue

            y = start_y + i * line_height

            # 标签
            label_text = text_font.render(label + ":", True, (200, 200, 220))
            self.screen.blit(label_text, (panel_x + int(30 * scale), y))

            # 数值
            value_text = text_font.render(value, True, color)
            value_rect = value_text.get_rect(right=panel_x + panel_width - int(30 * scale), centery=y + int(6 * scale))
            self.screen.blit(value_text, value_rect)

        # 底部提示
        hint_text = small_font.render("按 Tab 关闭", True, (150, 150, 170))
        hint_rect = hint_text.get_rect(center=(self.window_width // 2, panel_y + panel_height - int(25 * scale)))
        self.screen.blit(hint_text, hint_rect)

    def draw_achievements_panel(self):
        """绘制成就面板"""
        scale = self.scale_factor

        # 半透明背景遮罩
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 面板尺寸（更大以显示更多成就）
        panel_width = int(500 * scale)
        panel_height = int(580 * scale)
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        # 面板背景
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (28, 28, 36), panel_rect, border_radius=int(12 * scale))
        pygame.draw.rect(self.screen, (255, 215, 0), panel_rect, 2, border_radius=int(12 * scale))

        # 动态字体
        title_size = max(20, int(32 * scale))
        text_size = max(11, int(15 * scale))
        small_size = max(10, int(13 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            text_font = pygame.font.Font(self.font_path, text_size)
            small_font = pygame.font.Font(self.font_path, small_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            text_font = pygame.font.Font(None, text_size)
            small_font = pygame.font.Font(None, small_size)

        # 标题
        title_text = title_font.render("成就系统", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.window_width // 2, panel_y + int(30 * scale)))
        self.screen.blit(title_text, title_rect)

        # 分隔线
        line_y = panel_y + int(55 * scale)
        pygame.draw.line(self.screen, (255, 215, 0),
                        (panel_x + int(20 * scale), line_y),
                        (panel_x + panel_width - int(20 * scale), line_y), 2)

        # 计算已解锁成就数量
        unlocked_count = len(self.achievement.unlocked)
        total_count = len(Achievement.ACHIEVEMENTS_LIST)

        # 统计信息
        stats_text = text_font.render(f"已解锁: {unlocked_count}/{total_count} ({unlocked_count*100//total_count}%)", True, (150, 200, 255))
        self.screen.blit(stats_text, (panel_x + int(20 * scale), panel_y + int(65 * scale)))

        # 成就列表（分两列显示）
        start_y = panel_y + int(95 * scale)
        item_height = int(42 * scale)
        col_width = (panel_width - int(60 * scale)) // 2
        col1_x = panel_x + int(20 * scale)
        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)

        for i, achievement in enumerate(Achievement.ACHIEVEMENTS_LIST):
            col = i % 2
            row = i // 2

            x = col1_x if col == 0 else col2_x
            y = start_y + row * item_height

            # 检查是否已解锁
            is_unlocked = achievement['id'] in self.achievement.unlocked

            # 成就图标
            icon = "★" if is_unlocked else "☆"
            icon_color = (255, 215, 0) if is_unlocked else (100, 100, 100)
            icon_text = text_font.render(icon, True, icon_color)
            self.screen.blit(icon_text, (x, y))

            # 成就名称
            name_color = (255, 255, 255) if is_unlocked else (120, 120, 120)
            name_text = text_font.render(achievement['name'], True, name_color)
            self.screen.blit(name_text, (x + int(25 * scale), y))

            # 成就描述
            desc_color = (180, 180, 200) if is_unlocked else (80, 80, 80)
            desc_text = small_font.render(achievement['desc'], True, desc_color)
            self.screen.blit(desc_text, (x + int(25 * scale), y + int(18 * scale)))

        # 底部提示
        hint_text = small_font.render("按 H 关闭", True, (150, 150, 170))
        hint_rect = hint_text.get_rect(center=(self.window_width // 2, panel_y + panel_height - int(25 * scale)))
        self.screen.blit(hint_text, hint_rect)

    def draw_settings_panel(self):
        """绘制图形化设置菜单 - 竖版布局"""
        scale = self.scale_factor

        # 半透明背景遮罩
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 面板尺寸（竖版，更紧凑）
        panel_width = int(500 * scale)
        panel_height = int(650 * scale)
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        # 面板背景
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (28, 28, 36), panel_rect, border_radius=int(12 * scale))
        pygame.draw.rect(self.screen, (100, 100, 150), panel_rect, 3, border_radius=int(12 * scale))

        # 动态字体
        title_size = max(20, int(32 * scale))
        text_size = max(11, int(16 * scale))
        small_size = max(10, int(14 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            text_font = pygame.font.Font(self.font_path, text_size)
            small_font = pygame.font.Font(self.font_path, small_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            text_font = pygame.font.Font(None, text_size)
            small_font = pygame.font.Font(None, small_size)

        # 标题
        title_text = title_font.render("设置", True, (150, 150, 255))
        title_rect = title_text.get_rect(center=(self.window_width // 2, panel_y + int(35 * scale)))
        self.screen.blit(title_text, title_rect)

        # 分隔线
        line_y = panel_y + int(60 * scale)
        pygame.draw.line(self.screen, (100, 100, 150),
                        (panel_x + int(20 * scale), line_y),
                        (panel_x + panel_width - int(20 * scale), line_y), 2)

        # 竖版布局：两列
        col_width = (panel_width - int(60 * scale)) // 2
        col1_x = panel_x + int(20 * scale)
        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)
        start_y = panel_y + int(80 * scale)
        item_height = int(70 * scale)

        # 左列：开关设置
        # 音效开关
        self._draw_setting_item_vertical(col1_x, start_y, col_width, int(60 * scale),
                                       "音效", "开启/关闭游戏音效",
                                       self.sound_manager.enabled, text_font, small_font, scale)

        # 背景音乐开关
        music_y = start_y + item_height
        self._draw_setting_item_vertical(col1_x, music_y, col_width, int(60 * scale),
                                       "背景音乐", "开启/关闭背景音乐",
                                       self.sound_manager.music_enabled, text_font, small_font, scale)

        # 幽灵方块开关
        ghost_y = music_y + item_height
        self._draw_setting_item_vertical(col1_x, ghost_y, col_width, int(60 * scale),
                                       "幽灵方块", "显示方块落地预览",
                                       self.show_ghost, text_font, small_font, scale)

        # 霓虹模式开关
        neon_y = ghost_y + item_height
        self._draw_setting_item_vertical(col1_x, neon_y, col_width, int(60 * scale),
                                       "霓虹模式", "炫酷霓虹发光效果",
                                       self.neon_mode, text_font, small_font, scale)

        # 右列：音量控制和主题选择
        col2_start_y = start_y
        item_spacing = int(10 * scale)  # 统一间距

        # 音乐音量滑块
        music_vol_y = col2_start_y
        music_vol_height = int(80 * scale)
        self._draw_volume_slider_vertical(col2_x, music_vol_y, col_width, music_vol_height,
                                         "音乐音量", "music", self.sound_manager.music_volume,
                                         text_font, small_font, scale)

        # 音效音量滑块
        sfx_vol_y = music_vol_y + music_vol_height + item_spacing
        sfx_vol_height = int(80 * scale)
        self._draw_volume_slider_vertical(col2_x, sfx_vol_y, col_width, sfx_vol_height,
                                         "音效音量", "sfx", self.sound_manager.sfx_volume,
                                         text_font, small_font, scale)

        # 🎨 主题下拉框（与音量滑块对齐）
        theme_dropdown_y = sfx_vol_y + sfx_vol_height + item_spacing
        theme_dropdown_height = int(60 * scale)
        self._draw_theme_dropdown(col2_x, theme_dropdown_y, col_width, theme_dropdown_height,
                                   text_font, small_font, scale)

        # 恢复所有数据按钮（在底部提示文字上方1cm处）
        # 1cm ≈ 37-38像素，使用int(38 * scale)
        hint_y = panel_y + panel_height - int(35 * scale)
        reset_button_y = hint_y - int(45 * scale) - int(38 * scale)  # 按钮高度45 + 间距38
        reset_button_width = panel_width - int(40 * scale)
        reset_button_height = int(45 * scale)
        reset_button_x = panel_x + int(20 * scale)

        reset_button_rect = pygame.Rect(reset_button_x, reset_button_y, reset_button_width, reset_button_height)

        # 点击反馈效果
        current_time = pygame.time.get_ticks()
        is_clicked = current_time - self.reset_button_clicked < 200  # 200ms动画
        if is_clicked:
            # 点击时的颜色（更亮）
            pygame.draw.rect(self.screen, (255, 150, 150), reset_button_rect, border_radius=int(8 * scale))
            pygame.draw.rect(self.screen, (255, 200, 200), reset_button_rect, 3, border_radius=int(8 * scale))
        else:
            pygame.draw.rect(self.screen, (200, 50, 50), reset_button_rect, border_radius=int(8 * scale))
            pygame.draw.rect(self.screen, (255, 100, 100), reset_button_rect, 2, border_radius=int(8 * scale))

        # 按钮文字
        reset_button_text = text_font.render("恢复所有数据到出厂设置", True, (255, 255, 255))
        reset_button_text_rect = reset_button_text.get_rect(center=(reset_button_x + reset_button_width // 2, reset_button_y + reset_button_height // 2))
        self.screen.blit(reset_button_text, reset_button_text_rect)

        # 底部提示
        hint_y = panel_y + panel_height - int(35 * scale)

        if self.key_binding_mode:
            hint_text = small_font.render("按下要绑定的按键... (按 Esc 取消)", True, (255, 255, 100))
        elif self.dragging_slider:
            hint_text = small_font.render("拖动滑块调整音量 | 释放鼠标完成", True, (150, 200, 255))
        else:
            hint_text = small_font.render("点击设置切换 | 拖动滑块 | 点击主题切换 | 按 K 键位 | Esc 关闭", True, (150, 150, 170))

        hint_rect = hint_text.get_rect(center=(self.window_width // 2, hint_y))
        self.screen.blit(hint_text, hint_rect)

    def _draw_setting_item_vertical(self, x, y, width, height, title, desc, enabled, font, small_font, scale):
        """绘制单个设置项（竖版开关类型）- 文字左对齐，开关右对齐"""
        # 背景卡片
        item_rect = pygame.Rect(x, y, width, height)
        bg_color = (40, 40, 50) if not enabled else (50, 60, 80)
        pygame.draw.rect(self.screen, bg_color, item_rect, border_radius=int(8 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), item_rect, 2, border_radius=int(8 * scale))

        # 标题（左对齐）
        title_color = (255, 255, 255) if enabled else (150, 150, 150)
        title_surf = font.render(title, True, title_color)
        self.screen.blit(title_surf, (x + int(12 * scale), y + int(12 * scale)))

        # 描述（左对齐）
        desc_color = (180, 180, 200) if enabled else (100, 100, 100)
        desc_surf = small_font.render(desc, True, desc_color)
        self.screen.blit(desc_surf, (x + int(12 * scale), y + int(35 * scale)))

        # 开关指示器（右侧，竖向居中）
        switch_width = int(44 * scale)
        switch_height = int(22 * scale)
        switch_x = x + width - switch_width - int(12 * scale)
        switch_y = y + (height - switch_height) // 2

        switch_rect = pygame.Rect(switch_x, switch_y, switch_width, switch_height)
        switch_color = (0, 200, 100) if enabled else (100, 100, 100)
        pygame.draw.rect(self.screen, switch_color, switch_rect, border_radius=int(switch_height // 2))

        # 开关圆点
        circle_x = switch_x + int(switch_width * 0.72) if enabled else switch_x + int(switch_width * 0.28)
        circle_y = switch_y + switch_height // 2
        pygame.draw.circle(self.screen, (255, 255, 255), (circle_x, circle_y), int(switch_height * 0.35))

    def _draw_volume_slider_vertical(self, x, y, width, height, title, slider_type, volume, font, small_font, scale):
        """绘制音量滑块（竖版，可拖动）"""
        # 背景卡片
        item_rect = pygame.Rect(x, y, width, height)
        bg_color = (40, 40, 50)
        pygame.draw.rect(self.screen, bg_color, item_rect, border_radius=int(8 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), item_rect, 2, border_radius=int(8 * scale))

        # 标题（左对齐）
        title_surf = font.render(f"{title}", True, (200, 200, 220))
        self.screen.blit(title_surf, (x + int(12 * scale), y + int(12 * scale)))

        # 百分比显示（右对齐，在右上角与标题同一水平线）
        percent_text = small_font.render(f"{int(volume * 100)}%", True, (150, 200, 255))
        percent_rect = percent_text.get_rect(right=(x + width - int(12 * scale)), top=(y + int(14 * scale)))
        self.screen.blit(percent_text, percent_rect)

        # 滑块轨道（竖版，在底部）
        slider_width = width - int(30 * scale)
        slider_x = x + int(15 * scale)
        slider_y_start = y + int(48 * scale)
        slider_height = int(12 * scale)

        track_rect = pygame.Rect(slider_x, slider_y_start, slider_width, slider_height)
        pygame.draw.rect(self.screen, (60, 60, 70), track_rect, border_radius=int(slider_height // 2))

        # 已填充部分
        fill_width = int(slider_width * volume)
        fill_rect = pygame.Rect(slider_x, slider_y_start, fill_width, slider_height)
        fill_color = (100, 150, 255) if slider_type == 'music' else (0, 200, 100)
        pygame.draw.rect(self.screen, fill_color, fill_rect, border_radius=int(slider_height // 2))

        # 滑块按钮（可拖动的圆 - 缩小）
        button_x = slider_x + fill_width
        button_y = slider_y_start + slider_height // 2
        button_color = (255, 255, 255) if self.dragging_slider == slider_type else (200, 200, 220)
        button_radius = int(slider_height * 1.2)  # 缩小白点
        pygame.draw.circle(self.screen, button_color, (button_x, button_y), button_radius)

        # 如果正在拖动，添加高亮效果
        if self.dragging_slider == slider_type:
            pygame.draw.circle(self.screen, (150, 200, 255), (button_x, button_y), button_radius + 3, 2)

    def _draw_setting_item(self, x, y, width, height, title, desc, enabled, font, small_font, scale):
        """绘制单个设置项（开关类型）"""
        # 背景卡片
        item_rect = pygame.Rect(x, y, width, height)
        bg_color = (40, 40, 50) if not enabled else (50, 60, 80)
        pygame.draw.rect(self.screen, bg_color, item_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), item_rect, 1, border_radius=int(6 * scale))

        # 标题
        title_color = (255, 255, 255) if enabled else (150, 150, 150)
        title_surf = font.render(title, True, title_color)
        self.screen.blit(title_surf, (x + int(10 * scale), y + int(8 * scale)))

        # 描述
        desc_color = (180, 180, 200) if enabled else (100, 100, 100)
        desc_surf = small_font.render(desc, True, desc_color)
        self.screen.blit(desc_surf, (x + int(10 * scale), y + int(28 * scale)))

        # 开关指示器
        switch_size = int(20 * scale)
        switch_x = x + width - switch_size - int(10 * scale)
        switch_y = y + (height - switch_size) // 2

        switch_rect = pygame.Rect(switch_x, switch_y, switch_size * 2, switch_size)
        switch_color = (0, 200, 100) if enabled else (100, 100, 100)
        pygame.draw.rect(self.screen, switch_color, switch_rect, border_radius=int(switch_size // 2))

        # 开关圆点
        circle_x = switch_x + int(switch_size * 1.5) if enabled else switch_x + int(switch_size * 0.5)
        circle_y = switch_y + switch_size // 2
        pygame.draw.circle(self.screen, (255, 255, 255), (circle_x, circle_y), int(switch_size * 0.35))

    def _draw_theme_dropdown(self, x, y, width, height, font, small_font, scale):
        """绘制主题下拉框"""
        # 下拉框按钮背景
        dropdown_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (40, 40, 50), dropdown_rect, border_radius=int(8 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), dropdown_rect, 2, border_radius=int(8 * scale))

        # 标题
        title_surf = small_font.render("🎨 主题", True, (200, 200, 220))
        self.screen.blit(title_surf, (x + int(12 * scale), y + int(8 * scale)))

        # 当前主题名称
        theme_name_surf = font.render(self.current_theme.display_name, True, self.current_theme.text_highlight)
        self.screen.blit(theme_name_surf, (x + int(12 * scale), y + int(28 * scale)))

        # 下拉箭头（右侧）
        arrow_size = int(10 * scale)
        arrow_x = x + width - int(20 * scale)
        arrow_y = y + height // 2

        # 根据展开状态绘制箭头方向
        if self.theme_dropdown_opened:
            # 向上箭头
            pygame.draw.polygon(self.screen, (180, 180, 200), [
                (arrow_x, arrow_y - arrow_size // 2),
                (arrow_x - arrow_size, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size, arrow_y + arrow_size // 2)
            ])
        else:
            # 向下箭头
            pygame.draw.polygon(self.screen, (180, 180, 200), [
                (arrow_x, arrow_y + arrow_size // 2),
                (arrow_x - arrow_size, arrow_y - arrow_size // 2),
                (arrow_x + arrow_size, arrow_y - arrow_size // 2)
            ])

        # 如果下拉框展开，绘制下拉列表
        if self.theme_dropdown_opened:
            dropdown_list_height = int(180 * scale)
            dropdown_list_y = y + height

            # 下拉列表背景
            list_rect = pygame.Rect(x, dropdown_list_y, width, dropdown_list_height)
            # 半透明背景
            s = pygame.Surface((width, dropdown_list_height), pygame.SRCALPHA)
            s.fill((30, 30, 40, 245))  # 带alpha的背景
            self.screen.blit(s, (x, dropdown_list_y))
            pygame.draw.rect(self.screen, (100, 100, 150), list_rect, 2, border_radius=int(8 * scale))

            # 绘制主题列表
            item_height = int(28 * scale)
            for i, theme in enumerate(THEMES):
                item_y = dropdown_list_y + int(5 * scale) + i * item_height

                # 检查是否是当前主题
                is_current = (theme == self.current_theme)

                # 主题项背景
                if is_current:
                    item_rect = pygame.Rect(x + int(5 * scale), item_y, width - int(10 * scale), item_height - int(4 * scale))
                    pygame.draw.rect(self.screen, theme.bg_color, item_rect, border_radius=int(4 * scale))
                    pygame.draw.rect(self.screen, theme.text_highlight, item_rect, 1, border_radius=int(4 * scale))

                # 主题名称
                name_color = theme.text_highlight if is_current else (200, 200, 220)
                theme_name = theme.display_name
                theme_name_surf = small_font.render(theme_name, True, name_color)
                self.screen.blit(theme_name_surf, (x + int(15 * scale), item_y + int(6 * scale)))

                # 如果是当前主题，添加"✓"
                if is_current:
                    check_surf = small_font.render("✓", True, theme.text_highlight)
                    check_x = x + width - int(30 * scale)
                    self.screen.blit(check_surf, (check_x, item_y + int(6 * scale)))


    def _draw_volume_slider(self, x, y, width, height, title, volume, font, small_font, scale):
        """绘制音量滑块"""
        # 背景
        item_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (40, 40, 50), item_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), item_rect, 1, border_radius=int(6 * scale))

        # 标题
        title_surf = font.render(f"{title}: {int(volume * 100)}%", True, (200, 200, 220))
        self.screen.blit(title_surf, (x + int(10 * scale), y + int(8 * scale)))

        # 滑块轨道
        slider_width = width - int(60 * scale)
        slider_x = x + int(10 * scale)
        slider_y = y + int(30 * scale)
        slider_height = int(6 * scale)

        track_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        pygame.draw.rect(self.screen, (60, 60, 70), track_rect, border_radius=int(slider_height // 2))

        # 已填充部分
        fill_width = int(slider_width * volume)
        fill_rect = pygame.Rect(slider_x, slider_y, fill_width, slider_height)
        pygame.draw.rect(self.screen, (100, 150, 255), fill_rect, border_radius=int(slider_height // 2))

        # 滑块按钮
        button_x = slider_x + fill_width
        button_y = slider_y + slider_height // 2
        pygame.draw.circle(self.screen, (255, 255, 255), (button_x, button_y), int(slider_height * 1.5))

    def draw_keybind_panel(self):
        """绘制键位绑定面板"""
        scale = self.scale_factor

        # 半透明背景遮罩
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # 面板尺寸（增加高度以容纳按钮）
        panel_width = int(550 * scale)
        panel_height = int(650 * scale)  # 从580增加到650
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        # 面板背景
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (28, 28, 36), panel_rect, border_radius=int(12 * scale))
        pygame.draw.rect(self.screen, (255, 215, 0), panel_rect, 2, border_radius=int(12 * scale))

        # 动态字体
        title_size = max(20, int(32 * scale))
        text_size = max(11, int(15 * scale))
        small_size = max(10, int(13 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            text_font = pygame.font.Font(self.font_path, text_size)
            small_font = pygame.font.Font(self.font_path, small_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            text_font = pygame.font.Font(None, text_size)
            small_font = pygame.font.Font(None, small_size)

        # 标题
        title_text = title_font.render("键位绑定", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.window_width // 2, panel_y + int(35 * scale)))
        self.screen.blit(title_text, title_rect)

        # 分隔线
        line_y = panel_y + int(60 * scale)
        pygame.draw.line(self.screen, (255, 215, 0),
                        (panel_x + int(20 * scale), line_y),
                        (panel_x + panel_width - int(20 * scale), line_y), 2)

        # 键位列表（分两列）
        start_y = panel_y + int(80 * scale)
        item_height = int(42 * scale)
        col_width = (panel_width - int(60 * scale)) // 2
        col1_x = panel_x + int(20 * scale)
        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)

        actions = ['left', 'right', 'rotate', 'soft_drop', 'hard_drop',
                  'pause', 'neon', 'mute', 'restart', 'stats', 'achievements']

        for i, action in enumerate(actions):
            col = i % 2
            row = i // 2

            x = col1_x if col == 0 else col2_x
            y = start_y + row * item_height

            # 获取动作名称和当前键位
            action_name = self.keybind_manager.ACTION_NAMES.get(action, action)
            key_name = self.keybind_manager.get_key_name(action)

            # 高亮正在绑定的项
            is_binding = self.key_binding_mode == action
            bg_color = (60, 80, 100) if is_binding else (40, 40, 50)
            border_color = (255, 215, 0) if is_binding else (80, 80, 100)

            # 背景卡片
            item_rect = pygame.Rect(x, y, col_width, int(38 * scale))
            pygame.draw.rect(self.screen, bg_color, item_rect, border_radius=int(6 * scale))
            pygame.draw.rect(self.screen, border_color, item_rect, 2 if is_binding else 1, border_radius=int(6 * scale))

            # 动作名称
            name_color = (255, 255, 200) if is_binding else (200, 200, 220)
            name_text = text_font.render(action_name, True, name_color)
            self.screen.blit(name_text, (x + int(8 * scale), y + int(8 * scale)))

            # 当前键位
            key_color = (255, 255, 100) if is_binding else (150, 200, 255)
            key_text = small_font.render(f"[{key_name}]", True, key_color)
            key_rect = key_text.get_rect(right=x + col_width - int(8 * scale), centery=y + int(19 * scale))
            self.screen.blit(key_text, key_rect)

        # 恢复默认键位按钮（往下移动防止重叠）
        button_y = start_y + len(actions) // 2 * item_height + int(80 * scale)  # 从20增加到80
        button_width = panel_width - int(40 * scale)
        button_height = int(45 * scale)
        button_x = panel_x + int(20 * scale)

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # 点击反馈效果
        current_time = pygame.time.get_ticks()
        is_clicked = current_time - self.reset_keybind_button_clicked < 200  # 200ms动画
        if is_clicked:
            # 点击时的颜色（更亮）
            pygame.draw.rect(self.screen, (255, 150, 150), button_rect, border_radius=int(8 * scale))
            pygame.draw.rect(self.screen, (255, 200, 200), button_rect, 3, border_radius=int(8 * scale))
        else:
            pygame.draw.rect(self.screen, (200, 50, 50), button_rect, border_radius=int(8 * scale))
            pygame.draw.rect(self.screen, (255, 100, 100), button_rect, 2, border_radius=int(8 * scale))

        # 按钮文字
        button_text = text_font.render("恢复默认键位", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.screen.blit(button_text, button_text_rect)

        # 底部提示
        hint_y = panel_y + panel_height - int(30 * scale)

        if self.key_binding_mode:
            hint_text = small_font.render("按下要绑定的按键... (按 Esc 取消)", True, (255, 255, 100))
        else:
            hint_text = small_font.render("点击键位进行修改 | 点击按钮恢复默认 | 按 Esc 返回设置", True, (150, 150, 170))

        hint_rect = hint_text.get_rect(center=(self.window_width // 2, hint_y))
        self.screen.blit(hint_text, hint_rect)

    def handle_settings_click(self, pos):
        """处理设置菜单的点击事件（竖版布局）"""
        scale = self.scale_factor
        panel_width = int(500 * scale)
        panel_height = int(650 * scale)
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        # 竖版布局：两列
        col_width = (panel_width - int(60 * scale)) // 2
        col1_x = panel_x + int(20 * scale)
        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)
        start_y = panel_y + int(80 * scale)
        item_height = int(70 * scale)

        # 左列：开关设置
        # 音效开关
        if self._is_in_rect(pos, col1_x, start_y, col_width, int(60 * scale)):
            self.sound_manager.enabled = not self.sound_manager.enabled
            self.settings_manager.set('sound_enabled', self.sound_manager.enabled)
            return

        # 背景音乐开关
        music_y = start_y + item_height
        if self._is_in_rect(pos, col1_x, music_y, col_width, int(60 * scale)):
            if self.sound_manager.toggle_music():
                self.settings_manager.set('music_enabled', True)
            else:
                self.settings_manager.set('music_enabled', False)
            return

        # 幽灵方块开关
        ghost_y = music_y + item_height
        if self._is_in_rect(pos, col1_x, ghost_y, col_width, int(60 * scale)):
            self.show_ghost = not self.show_ghost
            self.settings_manager.set('show_ghost', self.show_ghost)
            return

        # 霓虹模式开关
        neon_y = ghost_y + item_height
        if self._is_in_rect(pos, col1_x, neon_y, col_width, int(60 * scale)):
            self.neon_mode = not self.neon_mode
            self.settings_manager.set('neon_mode', self.neon_mode)
            return

        # 右列：音量控制和主题选择
        col2_start_y = start_y
        item_spacing = int(10 * scale)  # 统一间距

        # 音乐音量滑块
        music_vol_y = col2_start_y
        music_vol_height = int(80 * scale)
        music_slider_x = col2_x + int(15 * scale)
        music_slider_track_x = music_slider_x
        music_slider_track_width = col_width - int(30 * scale)
        music_slider_track_y = music_vol_y + int(48 * scale)
        music_slider_track_height = int(12 * scale)

        # 检测是否点击音乐音量滑块区域（扩大点击范围）
        if self._is_in_rect(pos, col2_x, music_vol_y, col_width, music_vol_height):
            self.dragging_slider = 'music'
            # 更新音量到点击位置
            self._update_slider_volume(pos, music_slider_track_x, music_slider_track_y,
                                      music_slider_track_width, 'music')
            return

        # 音效音量滑块
        sfx_vol_y = music_vol_y + music_vol_height + item_spacing
        sfx_vol_height = int(80 * scale)
        sfx_slider_track_x = col2_x + int(15 * scale)
        sfx_slider_track_width = col_width - int(30 * scale)
        sfx_slider_track_y = sfx_vol_y + int(48 * scale)

        # 检测是否点击音效音量滑块区域
        if self._is_in_rect(pos, col2_x, sfx_vol_y, col_width, sfx_vol_height):
            self.dragging_slider = 'sfx'
            # 更新音量到点击位置
            self._update_slider_volume(pos, sfx_slider_track_x, sfx_slider_track_y,
                                      sfx_slider_track_width, 'sfx')
            return

        # 🎨 主题下拉框点击检测
        theme_dropdown_y = sfx_vol_y + sfx_vol_height + item_spacing
        theme_dropdown_height = int(60 * scale)

        # 检查是否点击了下拉框按钮或展开的列表
        dropdown_list_height = int(180 * scale) if self.theme_dropdown_opened else 0

        # 检查是否点击了下拉框区域
        if self._is_in_rect(pos, col2_x, theme_dropdown_y, col_width, theme_dropdown_height + dropdown_list_height):
            # 如果下拉列表是展开的
            if self.theme_dropdown_opened:
                # 计算点击了哪个主题
                item_height = int(28 * scale)
                list_start_y = theme_dropdown_y + theme_dropdown_height + int(5 * scale)

                relative_y = pos[1] - list_start_y

                for i, theme in enumerate(THEMES):
                    theme_y = i * item_height
                    if theme_y <= relative_y < theme_y + item_height:
                        # 点击了这个主题，切换到它
                        if theme != self.current_theme:  # 只切换到不同的主题
                            self.current_theme = theme
                            # 重新生成背景音乐
                            self.sound_manager.generate_background_music(self.current_theme)
                            # 更新AnimationManager的主题
                            self.animation_manager.theme = self.current_theme
                            # 播放确认音效
                            self.sound_manager.play('rotate')

                        # 选择后关闭下拉框
                        self.theme_dropdown_opened = False
                        return

                # 如果点击了下拉列表但没有点到任何主题，关闭下拉框
                self.theme_dropdown_opened = False
            else:
                # 下拉框未展开，点击展开
                self.theme_dropdown_opened = True
            return

        # 点击设置面板的其他地方时，关闭下拉框
        if self.theme_dropdown_opened:
            self.theme_dropdown_opened = False

        # 检测是否点击恢复所有数据按钮
        # 恢复按钮在底部提示文字上方1cm处
        hint_y = panel_y + panel_height - int(35 * scale)
        reset_button_y = hint_y - int(45 * scale) - int(38 * scale)
        reset_button_width = panel_width - int(40 * scale)
        reset_button_height = int(45 * scale)
        reset_button_x = panel_x + int(20 * scale)

        if self._is_in_rect(pos, reset_button_x, reset_button_y, reset_button_width, reset_button_height):
            self.reset_all_data()
            self.reset_button_clicked = pygame.time.get_ticks()  # 触发点击动画
            self.sound_manager.play('drop')  # 播放音效
            return

    def _update_slider_volume(self, mouse_pos, slider_x, slider_y, slider_width, slider_type):
        """根据鼠标位置更新音量"""
        # 计算鼠标在滑块上的相对位置
        relative_x = mouse_pos[0] - slider_x
        # 限制在滑块范围内
        relative_x = max(0, min(relative_x, slider_width))
        # 计算新音量 (0.0 - 1.0)
        new_volume = relative_x / slider_width

        if slider_type == 'music':
            self.sound_manager.set_music_volume(new_volume)
            self.settings_manager.set('music_volume', new_volume)
        elif slider_type == 'sfx':
            self.sound_manager.set_sfx_volume(new_volume)
            self.settings_manager.set('sfx_volume', new_volume)

    def handle_keybind_click(self, pos):
        """处理键位绑定面板的点击事件"""
        scale = self.scale_factor
        panel_width = int(550 * scale)
        panel_height = int(650 * scale)
        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2

        start_y = panel_y + int(80 * scale)
        item_height = int(42 * scale)
        col_width = (panel_width - int(60 * scale)) // 2
        col1_x = panel_x + int(20 * scale)
        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)

        actions = ['left', 'right', 'rotate', 'soft_drop', 'hard_drop',
                  'pause', 'neon', 'mute', 'restart', 'stats', 'achievements']

        for i, action in enumerate(actions):
            col = i % 2
            row = i // 2

            x = col1_x if col == 0 else col2_x
            y = start_y + row * item_height

            if self._is_in_rect(pos, x, y, col_width, int(38 * scale)):
                self.key_binding_mode = action
                return

        # 检测是否点击恢复默认按钮
        button_y = start_y + len(actions) // 2 * item_height + int(80 * scale)  # 与绘制位置一致
        button_width = panel_width - int(40 * scale)
        button_height = int(45 * scale)
        button_x = panel_x + int(20 * scale)

        if self._is_in_rect(pos, button_x, button_y, button_width, button_height):
            self.keybind_manager.reset_to_defaults()
            self.reset_keybind_button_clicked = pygame.time.get_ticks()  # 触发点击动画
            self.sound_manager.play('drop')  # 播放音效
            return

    def _is_in_rect(self, pos, x, y, width, height):
        """检查位置是否在矩形内"""
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def reset_all_data(self):
        """恢复所有游戏数据到出厂设置"""
        import os
        import json

        # 需要删除的持久化文件
        files_to_delete = [
            'tetris_settings.json',
            'tetris_keybinds.json',
            'tetris_statistics.json',
            'tetris_achievements.json',
            'tetris_leaderboard.json'
        ]

        # 删除文件
        for filename in files_to_delete:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except:
                    pass

        # 重新初始化管理器（使用默认值）
        self.settings_manager = SettingsManager()
        self.keybind_manager = KeyBindManager()
        self.statistics = Statistics()
        self.achievement = Achievement()
        self.leaderboard = Leaderboard()  # 重新初始化排行榜

        # 应用默认设置
        self.sound_manager.enabled = self.settings_manager.get('sound_enabled', True)
        self.sound_manager.music_enabled = self.settings_manager.get('music_enabled', True)
        self.show_ghost = self.settings_manager.get('show_ghost', True)
        self.neon_mode = True  # 恢复出厂设置时开启霓虹模式

        # 重置当前游戏状态
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.waiting_to_start = True
        self.countdown = 3
        self.countdown_timer = 0
        self.countdown_active = False
        self.piece_bag = []
        self.current_piece = self.create_piece()
        self.next_piece = self.create_piece()
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.combo_count = 0
        self.last_clear_time = 0
        self.show_statistics = False
        self.show_achievements = False
        # 保持设置面板打开状态，不设置 show_settings = False
        self.first_piece_placed = False

    def draw_next_piece(self):
        """绘制下一个方块预览 - 支持缩放"""
        scale = self.scale_factor

        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        preview_x = int(grid_x + GRID_WIDTH * block_size + 25 * scale)
        preview_y = int(grid_y + 35 * scale)  # 调整为35，使卡片顶端与网格对齐

        # 动态调整字体大小
        font_size = max(12, int(20 * scale))
        if self.font_path:
            dynamic_font = pygame.font.Font(self.font_path, font_size)
        else:
            dynamic_font = pygame.font.Font(None, font_size)

        # 预览方块（增大）
        preview_block_size = int(block_size * 0.9)

        # 绘制预览方框（包含"下一个:"文字）
        box_size = preview_block_size * 4
        # 与下面的卡片对齐：使用相同的x位置和宽度
        info_x = int(grid_x + GRID_WIDTH * block_size + 20 * scale)
        card_width = int(190 * scale)
        card_x = info_x - 6
        card_y = preview_y - int(35 * scale)
        card_height = box_size + int(25 * scale)  # 缩小高度到25

        # 计算下一个卡片底部位置，用于对齐
        next_card_bottom = card_y + card_height

        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        pygame.draw.rect(self.screen, (28, 28, 36), card_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), card_rect, 2, border_radius=int(6 * scale))

        # 标题文字（靠左对齐）
        text = dynamic_font.render("下一个:", True, (200, 200, 220))
        text_x = card_x + int(6 * scale)
        text_y = card_y + int(6 * scale)
        self.screen.blit(text, (text_x, text_y))

        # 分隔线
        line_y = text_y + int(26 * scale)
        pygame.draw.line(self.screen, (80, 80, 100),
                        (card_x + int(6 * scale), line_y),
                        (card_x + card_width - int(6 * scale), line_y), 1)

        # 调整图案起始位置，增加与分隔线的距离
        adjusted_preview_y = line_y + int(10 * scale)

        for y, row in enumerate(self.next_piece):
            for x, cell in enumerate(row):
                if cell != 0:
                    # 靠左显示方块
                    block_x = card_x + int(6 * scale)
                    rect = pygame.Rect(
                        block_x + x * preview_block_size,
                        adjusted_preview_y + y * preview_block_size,
                        preview_block_size, preview_block_size
                    )
                    self.draw_3d_block(rect, cell)

    def draw_info(self):
        """绘制游戏信息 - 支持缩放"""
        scale = self.scale_factor

        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        info_x = int(grid_x + GRID_WIDTH * block_size + 20 * scale)
        info_y = int(grid_y + 121 * scale)  # 向上移动7像素，从128改为121

        # 缩放卡片大小
        card_width = int(190 * scale)
        card_height = int(140 * scale)

        card_rect = pygame.Rect(info_x - 6, info_y - 6, card_width, card_height)
        pygame.draw.rect(self.screen, (28, 28, 36), card_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (60, 60, 80), card_rect, 2, border_radius=int(6 * scale))

        # 动态字体大小
        base_font_size = max(11, int(18 * scale))
        large_font_size = max(14, int(24 * scale))

        if self.font_path:
            font = pygame.font.Font(self.font_path, base_font_size)
        else:
            font = pygame.font.Font(None, base_font_size)
        large_font = pygame.font.Font(None, large_font_size)

        # 标题
        title_text = font.render("游戏状态", True, (200, 200, 220))
        self.screen.blit(title_text, (info_x, info_y))

        # 分隔线
        line_y = info_y + int(26 * scale)
        pygame.draw.line(self.screen, (60, 60, 80),
                        (info_x, line_y),
                        (info_x + card_width - 12, line_y), 1)

        # 第一行：分数
        score_y = info_y + int(32 * scale)
        score_label = font.render("分数:", True, (200, 200, 220))
        score_text = large_font.render(f"{self.score:,}", True, (0, 255, 200))

        # 对齐：根据字体高度调整位置
        label_height = score_label.get_height()
        text_height = score_text.get_height()
        label_y = score_y + (text_height - label_height)
        text_y = score_y

        self.screen.blit(score_label, (info_x, label_y))
        self.screen.blit(score_text, (info_x + int(52 * scale), text_y))

        # 第二行：等级和消除（并排）
        stats_y = info_y + int(62 * scale)
        level_text = font.render(f"Lv{self.level}", True, (255, 200, 100))
        lines_text = font.render(f"消除{self.lines_cleared}", True, (100, 200, 255))
        self.screen.blit(level_text, (info_x, stats_y))
        self.screen.blit(lines_text, (info_x + int(70 * scale), stats_y))

        # 第三行：连击（如果有）
        status_y = info_y + int(87 * scale)
        if self.combo_count > 1:
            combo_text = font.render(f"{self.combo_count}x连击!", True, (255, 255, 100))
            self.screen.blit(combo_text, (info_x, status_y))
            status_y += int(18 * scale)

        # 第四行：模式状态
        neon_color = (0, 255, 255) if self.neon_mode else TEXT_GRAY
        neon_text = font.render(f"霓虹{'ON' if self.neon_mode else 'OFF'}", True, neon_color)
        self.screen.blit(neon_text, (info_x, status_y))

        # 第五行：音效状态
        sound_status = "ON" if self.sound_manager.enabled else "OFF"
        sound_color = (100, 255, 100) if self.sound_manager.enabled else TEXT_GRAY
        sound_text = font.render(f"音效{sound_status}", True, sound_color)
        self.screen.blit(sound_text, (info_x + int(90 * scale), status_y))

    def draw_leaderboard(self):
        """绘制排行榜 - 支持缩放"""
        scale = self.scale_factor

        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        leaderboard_x = int(grid_x + GRID_WIDTH * block_size + 20 * scale)
        leaderboard_y = int(grid_y + 269 * scale)  # 向上移动7像素，从276改为269

        # 缩放卡片大小
        card_width = int(190 * scale)
        card_height = int(130 * scale)

        card_rect = pygame.Rect(leaderboard_x - 6, leaderboard_y - 6, card_width, card_height)
        pygame.draw.rect(self.screen, (28, 28, 36), card_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (255, 215, 0), card_rect, 2, border_radius=int(6 * scale))

        # 动态字体
        font_size = max(11, int(16 * scale))
        if self.font_path:
            font = pygame.font.Font(self.font_path, font_size)
        else:
            font = pygame.font.Font(None, font_size)

        # 标题（金色）
        title_text = font.render("排行榜 TOP5", True, (255, 215, 0))
        self.screen.blit(title_text, (leaderboard_x, leaderboard_y))

        # 分隔线
        line_y = leaderboard_y + int(22 * scale)
        pygame.draw.line(self.screen, (255, 215, 0),
                        (leaderboard_x, line_y),
                        (leaderboard_x + card_width - 12, line_y), 1)

        # 排行榜条目
        top_scores = self.leaderboard.get_top_scores(5)

        # 排名颜色：第1名金色，第2名白色，第3名棕色，第4-5名银色
        rank_colors = [(255, 215, 0), WHITE, (160, 82, 45),  # 金、白、棕色
                      (192, 192, 192), (192, 192, 192)]  # 银色

        for i, entry in enumerate(top_scores):
            y_pos = leaderboard_y + int(24 * scale) + i * int(19 * scale)

            # 使用当前排名的颜色
            color = rank_colors[i]

            # 排名
            rank_text = font.render(f"#{i + 1}", True, color)
            self.screen.blit(rank_text, (leaderboard_x, y_pos))

            # 等级（中间）
            level_text = font.render(f"Lv{entry['level']}", True, color)
            level_rect = level_text.get_rect()
            self.screen.blit(level_text, (leaderboard_x + int(35 * scale), y_pos))

            # 分数（右对齐，留出足够的边距）
            score_text = font.render(f"{entry['score']}", True, color)
            score_width = score_text.get_width()
            # 右对齐，距离卡片右边缘增加8像素（约2mm）
            score_x = leaderboard_x + card_width - score_width - int(23 * scale)
            self.screen.blit(score_text, (score_x, y_pos))

        # 如果没有记录
        if not top_scores:
            no_record = font.render("暂无记录", True, TEXT_GRAY)
            self.screen.blit(no_record, (leaderboard_x + int(70 * scale), leaderboard_y + int(55 * scale)))

    def draw_game_over(self):
        """绘制游戏结束画面"""
        scale = self.scale_factor

        # 创建半透明遮罩
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 动态字体
        title_size = max(30, int(50 * scale))
        text_size = max(14, int(22 * scale))
        hint_size = max(12, int(18 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            text_font = pygame.font.Font(self.font_path, text_size)
            hint_font = pygame.font.Font(self.font_path, hint_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            text_font = pygame.font.Font(None, text_size)
            hint_font = pygame.font.Font(None, hint_size)

        game_over_text = title_font.render("游戏结束!", True, WHITE)
        score_text = text_font.render(f"最终分数: {self.score}", True, WHITE)

        # 居中显示
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 60))
        score_rect = score_text.get_rect(center=(self.window_width // 2, self.window_height // 2))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        # 检查是否是新纪录
        is_high_score = self.leaderboard.is_high_score(self.score)
        if is_high_score and self.score > 0:
            record_text = text_font.render("新纪录!", True, (255, 215, 0))
            record_rect = record_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 100))
            self.screen.blit(record_text, record_rect)

        restart_text = hint_font.render("按 R 重新开始，按 Q 退出", True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def draw_waiting_to_start(self):
        """绘制等待开始画面"""
        # 如果有任何面板打开，不显示等待开始画面
        if self.show_settings or self.show_statistics or self.show_achievements:
            return

        # 创建半透明遮罩
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        scale = self.scale_factor

        # 动态字体
        title_size = max(40, int(60 * scale))
        hint_size = max(16, int(24 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            hint_font = pygame.font.Font(self.font_path, hint_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            hint_font = pygame.font.Font(None, hint_size)

        # 标题
        title_text = title_font.render("俄罗斯方块", True, (0, 255, 255))
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 60))
        self.screen.blit(title_text, title_rect)

        # 提示文字（带闪烁效果）
        import math
        alpha = int(155 + 100 * math.sin(pygame.time.get_ticks() / 300))
        hint_text = hint_font.render("按 空格 或 回车 开始", True, (255, 255, 255))
        hint_text.set_alpha(alpha)
        hint_rect = hint_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 30))
        self.screen.blit(hint_text, hint_rect)

    def draw_countdown(self):
        """绘制倒计时画面"""
        # 创建半透明遮罩
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        scale = self.scale_factor

        # 动态字体（倒计时数字）
        number_size = max(80, int(150 * scale))

        if self.font_path:
            number_font = pygame.font.Font(self.font_path, number_size)
        else:
            number_font = pygame.font.Font(None, number_size)

        # 根据倒计时数字显示不同颜色
        if self.countdown == 3:
            color = (255, 100, 100)  # 红色
        elif self.countdown == 2:
            color = (255, 200, 100)  # 橙色
        elif self.countdown == 1:
            color = (100, 255, 100)  # 绿色
        else:
            color = (100, 200, 255)  # 蓝色

        # 绘制倒计时数字
        if self.countdown > 0:
            countdown_text = number_font.render(str(self.countdown), True, color)
            text_rect = countdown_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(countdown_text, text_rect)
        else:
            # "GO!" 文字
            go_text = number_font.render("GO!", True, (0, 255, 255))
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(go_text, go_rect)

    def draw_pause(self):
        """绘制暂停画面"""
        # 如果有任何面板打开，不显示暂停浮窗
        if self.show_settings or self.show_statistics or self.show_achievements:
            return

        scale = self.scale_factor

        # 创建半透明遮罩
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 动态字体
        title_size = max(30, int(50 * scale))
        hint_size = max(14, int(22 * scale))

        if self.font_path:
            title_font = pygame.font.Font(self.font_path, title_size)
            hint_font = pygame.font.Font(self.font_path, hint_size)
        else:
            title_font = pygame.font.Font(None, title_size)
            hint_font = pygame.font.Font(None, hint_size)

        pause_text = title_font.render("暂停", True, WHITE)
        continue_text = hint_font.render("按 P 继续", True, WHITE)

        pause_rect = pause_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
        continue_rect = continue_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 30))

        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)

    def draw_controls(self):
        """绘制控制说明 - 支持缩放"""
        scale = self.scale_factor

        grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
        block_size = self.get_scaled_size(BLOCK_SIZE)

        controls_x = int(grid_x + GRID_WIDTH * block_size + 20 * scale)
        controls_y = int(grid_y + 407 * scale)  # 向上移动7像素，从414改为407

        # 缩放卡片大小
        card_width = int(190 * scale)
        card_height = int(130 * scale)  # 增加高度到130以容纳11个按键

        card_rect = pygame.Rect(controls_x - 6, controls_y - 6, card_width, card_height)
        pygame.draw.rect(self.screen, (28, 28, 36), card_rect, border_radius=int(6 * scale))
        pygame.draw.rect(self.screen, (80, 80, 100), card_rect, 2, border_radius=int(6 * scale))

        # 动态字体
        font_size = max(9, int(12 * scale))
        if self.font_path:
            font = pygame.font.Font(self.font_path, font_size)
        else:
            font = pygame.font.Font(None, font_size)

        # 标题
        title_text = font.render("操作", True, (200, 200, 220))
        self.screen.blit(title_text, (controls_x, controls_y))

        # 分隔线
        line_y = controls_y + int(22 * scale)
        pygame.draw.line(self.screen, (80, 80, 100),
                        (controls_x, line_y),
                        (controls_x + card_width - 12, line_y), 1)

        # 控制键（两列布局）- 从键位绑定管理器获取
        controls = [
            (self.keybind_manager.get_key_name('rotate'), "旋转", (100, 200, 255)),
            (self.keybind_manager.get_key_name('pause'), "暂停", (150, 150, 170)),
            (self.keybind_manager.get_key_name('left'), "左", (100, 200, 255)),
            (self.keybind_manager.get_key_name('neon'), "霓虹", (150, 150, 170)),
            (self.keybind_manager.get_key_name('right'), "右", (100, 200, 255)),
            (self.keybind_manager.get_key_name('mute'), "静音", (150, 150, 170)),
            (self.keybind_manager.get_key_name('soft_drop'), "加速", (100, 200, 255)),
            (self.keybind_manager.get_key_name('restart'), "重来", (150, 150, 170)),
            (self.keybind_manager.get_key_name('hard_drop'), "下落", (255, 200, 100)),
            (self.keybind_manager.get_key_name('achievements'), "成就", (255, 215, 0)),
            (self.keybind_manager.get_key_name('stats'), "统计", (0, 200, 255)),
            (self.keybind_manager.get_key_name('settings'), "设置", (150, 150, 170)),
        ]

        col_width = card_width // 2
        start_y = controls_y + int(26 * scale)
        row_height = int(14 * scale)

        for i in range(len(controls)):
            item = controls[i]
            if len(item) == 0 or item[0] == "":
                continue

            row = i // 2
            col = i % 2

            x = controls_x + col * col_width + int(4 * scale)
            y = start_y + row * row_height

            if len(item) >= 3:
                key, label, color = item
            else:
                continue

            # 按键
            key_text = font.render(key, True, color)
            self.screen.blit(key_text, (x, y))

            # 功能说明
            label_text = font.render(label, True, TEXT_GRAY)
            key_width = key_text.get_width()
            offset = key_width + int(5 * scale)
            self.screen.blit(label_text, (x + offset, y))

    def run(self):
        """运行游戏主循环"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 处理窗口大小调整
                if event.type == pygame.VIDEORESIZE:
                    self.window_width = event.w
                    self.window_height = event.h

                    # 计算缩放因子（使用宽度和高度的较小值，更保守）
                    width_scale = self.window_width / WINDOW_WIDTH
                    height_scale = self.window_height / WINDOW_HEIGHT
                    self.scale_factor = min(width_scale, height_scale)

                    # 限制缩放范围，避免过度缩放
                    self.scale_factor = max(0.6, min(1.5, self.scale_factor))

                    # 重新创建屏幕表面
                    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

                # 处理鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        mouse_pos = pygame.mouse.get_pos()

                        # 设置菜单点击处理
                        if self.show_settings and self.key_binding_mode != 'panel':
                            self.handle_settings_click(mouse_pos)

                        # 键位绑定面板点击处理
                        elif self.show_settings and self.key_binding_mode == 'panel':
                            if not self.key_binding_mode or self.key_binding_mode == 'panel':
                                self.handle_keybind_click(mouse_pos)

                # 处理鼠标移动事件（滑块拖动）
                if event.type == pygame.MOUSEMOTION:
                    if self.dragging_slider and self.show_settings:
                        scale = self.scale_factor
                        panel_width = int(500 * scale)
                        panel_height = int(650 * scale)
                        panel_x = (self.window_width - panel_width) // 2
                        panel_y = (self.window_height - panel_height) // 2

                        col_width = (panel_width - int(60 * scale)) // 2
                        col2_x = panel_x + int(20 * scale) + col_width + int(20 * scale)
                        start_y = panel_y + int(80 * scale)
                        item_height = int(70 * scale)

                        vol_start_y = start_y
                        slider_x = col2_x + int(15 * scale)
                        slider_width = col_width - int(30 * scale)

                        if self.dragging_slider == 'music':
                            slider_track_y = vol_start_y + int(48 * scale)
                            self._update_slider_volume(event.pos, slider_x, slider_track_y,
                                                     slider_width, 'music')
                        elif self.dragging_slider == 'sfx':
                            sfx_vol_y = vol_start_y + item_height
                            slider_track_y = sfx_vol_y + int(48 * scale)
                            self._update_slider_volume(event.pos, slider_x, slider_track_y,
                                                     slider_width, 'sfx')

                # 处理鼠标释放事件（停止拖动滑块）
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # 左键释放
                        if self.dragging_slider:
                            self.dragging_slider = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                    # Tab键切换统计面板（任何时候都有效）
                    if event.key == pygame.K_TAB and not self.waiting_to_start:
                        if not self.show_statistics:
                            # 打开统计面板 - 记录并暂停
                            if not (self.show_achievements or self.show_settings):
                                # 如果没有其他面板打开，记录当前暂停状态
                                self.was_paused_before_panel = self.paused
                            self.paused = True
                        else:
                            # 关闭统计面板 - 如果没有其他面板，恢复之前的暂停状态
                            if not (self.show_achievements or self.show_settings):
                                self.paused = self.was_paused_before_panel

                        self.show_statistics = not self.show_statistics
                        # 关闭成就面板和设置
                        self.show_achievements = False
                        self.show_settings = False
                        self.theme_dropdown_opened = False  # 关闭下拉框
                        continue

                    # H键切换成就面板（任何时候都有效）
                    if event.key == pygame.K_h and not self.waiting_to_start:
                        if not self.show_achievements:
                            # 打开成就面板 - 记录并暂停
                            if not (self.show_statistics or self.show_settings):
                                # 如果没有其他面板打开，记录当前暂停状态
                                self.was_paused_before_panel = self.paused
                            self.paused = True
                        else:
                            # 关闭成就面板 - 如果没有其他面板，恢复之前的暂停状态
                            if not (self.show_statistics or self.show_settings):
                                self.paused = self.was_paused_before_panel

                        self.show_achievements = not self.show_achievements
                        # 关闭统计面板和设置菜单
                        self.show_statistics = False
                        self.show_settings = False
                        self.theme_dropdown_opened = False  # 关闭下拉框
                        continue

                    # ESC键切换设置菜单（任何时候都有效）
                    if event.key == pygame.K_ESCAPE:
                        if self.show_settings:
                            # 如果在键位绑定模式，先退出键位绑定
                            if self.key_binding_mode:
                                self.key_binding_mode = None
                            else:
                                # 关闭设置菜单 - 恢复之前的暂停状态
                                self.paused = self.was_paused_before_panel
                                self.show_settings = False
                                self.theme_dropdown_opened = False  # 关闭下拉框
                        else:
                            # 打开设置菜单 - 记录并暂停
                            if not (self.show_statistics or self.show_achievements):
                                # 如果没有其他面板打开，记录当前暂停状态
                                self.was_paused_before_panel = self.paused
                            self.paused = True
                            self.show_settings = True
                            self.show_statistics = False
                            self.show_achievements = False
                        continue

                    # K键打开键位绑定（仅在设置菜单打开时）
                    if event.key == pygame.K_k and self.show_settings and not self.key_binding_mode:
                        # 切换到键位绑定面板
                        self.key_binding_mode = 'panel'  # 特殊标记表示进入键位面板
                        continue

                    # 键位绑定模式：按任意键绑定
                    if self.key_binding_mode and self.key_binding_mode != 'panel':
                        # 退出绑定
                        if event.key == pygame.K_ESCAPE:
                            self.key_binding_mode = None
                        else:
                            # 绑定新按键
                            self.keybind_manager.set_key(self.key_binding_mode, event.key)
                            self.key_binding_mode = None
                        continue

                    # R键重新开始（任何状态下都有效，除了等待开始）
                    if event.key == pygame.K_r and not self.waiting_to_start:
                        # 保存当前统计数据
                        self.statistics.record_score(self.score)
                        self.statistics.save_statistics()

                        # 停止旧的保存线程
                        self.statistics._stop_thread = True
                        if self.statistics._save_thread and self.statistics._save_thread.is_alive():
                            self.statistics._save_thread.join(timeout=0.5)

                        # 🎨 切换到新主题（排除当前主题）
                        available_themes = [t for t in THEMES if t != self.current_theme]
                        self.current_theme = random.choice(available_themes)

                        # 重新生成背景音乐（使用新主题）
                        self.sound_manager.generate_background_music(self.current_theme)

                        # 更新AnimationManager的主题
                        self.animation_manager.theme = self.current_theme

                        # 保存一些设置
                        neon = self.neon_mode
                        sound_enabled = self.sound_manager.enabled

                        # 重置游戏状态（不重新初始化Statistics对象）
                        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                        self.score = 0
                        self.level = 1
                        self.lines_cleared = 0
                        self.game_over = False
                        self.paused = False
                        self.waiting_to_start = True
                        self.countdown = 3
                        self.countdown_timer = 0
                        self.countdown_active = False
                        self.piece_bag = []  # 重置方块袋子
                        self.current_piece = self.create_piece()
                        self.next_piece = self.create_piece()
                        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                        self.current_y = 0
                        self.fall_time = 0
                        self.fall_speed = 500
                        self.combo_count = 0
                        self.last_clear_time = 0
                        self.show_statistics = False
                        self.show_achievements = False
                        self.first_piece_placed = False

                        # 重新创建动画管理器（使用新主题）
                        self.animation_manager = AnimationManager(theme=self.current_theme)
                        self.piece_animation = PieceAnimation()

                        # 恢复设置
                        self.neon_mode = neon
                        self.sound_manager.enabled = sound_enabled

                        # 重置统计数据的当前会话
                        self.statistics.reset_current_session()

                        # 重新启动保存线程
                        self.statistics._stop_thread = False
                        self.statistics._start_save_thread()
                        continue

                    # 等待开始状态，按空格或回车开始
                    if self.waiting_to_start:
                        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            self.waiting_to_start = False
                            self.countdown_active = True
                            self.countdown = 3
                            self.countdown_timer = pygame.time.get_ticks()
                            self.sound_manager.play('rotate')  # 播放音效提示
                        continue

                    # 游戏结束状态下的其他按键
                    if self.game_over:
                        continue

                    if event.key == pygame.K_p:
                        self.paused = not self.paused

                    if event.key == pygame.K_n:
                        self.neon_mode = not self.neon_mode
                        self.achievement.unlock('neon_master')  # 解锁霓虹成就

                    if event.key == pygame.K_m:
                        self.sound_manager.toggle()

                    if not self.paused and not self.countdown_active and not self.show_statistics:
                        # 使用键位绑定管理器获取键位
                        if event.key == self.keybind_manager.get_key('left'):
                            if self.valid_move(self.current_piece, self.current_x - 1, self.current_y):
                                # 启动移动动画
                                self.piece_animation.start_move_animation(
                                    self.current_x, self.current_y,
                                    self.current_x - 1, self.current_y
                                )
                                self.current_x -= 1
                                self.sound_manager.play('move')
                                self.statistics.total_moves += 1

                        elif event.key == self.keybind_manager.get_key('right'):
                            if self.valid_move(self.current_piece, self.current_x + 1, self.current_y):
                                # 启动移动动画
                                self.piece_animation.start_move_animation(
                                    self.current_x, self.current_y,
                                    self.current_x + 1, self.current_y
                                )
                                self.current_x += 1
                                self.sound_manager.play('move')
                                self.statistics.total_moves += 1

                        elif event.key == self.keybind_manager.get_key('rotate'):
                            rotated = self.rotate_piece(self.current_piece)
                            if self.valid_move(rotated, self.current_x, self.current_y):
                                self.current_piece = rotated
                                # 可以在这里添加旋转动画（未来实现）
                                self.sound_manager.play('rotate')
                                self.statistics.total_rotations += 1

                        elif event.key == self.keybind_manager.get_key('soft_drop'):
                            if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                                self.current_y += 1

                        elif event.key == self.keybind_manager.get_key('hard_drop'):
                            # 记录开始位置用于动画
                            start_y = self.current_y
                            while self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                                self.current_y += 1
                            # 启动下落动画
                            self.piece_animation.start_drop_animation(start_y, self.current_y)
                            self.sound_manager.play('drop')

            # 游戏逻辑更新（只有游戏开始后才更新）
            if not self.game_over and not self.paused and not self.waiting_to_start and not self.countdown_active:
                current_time = pygame.time.get_ticks()
                if current_time - self.fall_time > self.fall_speed:
                    if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                        self.current_y += 1
                    else:
                        self.merge_piece()
                        self.clear_lines()
                        self.new_piece()
                    self.fall_time = current_time

            # 倒计时逻辑
            if self.countdown_active:
                current_time = pygame.time.get_ticks()
                if current_time - self.countdown_timer > 1000:  # 每秒更新
                    self.countdown -= 1
                    self.countdown_timer = current_time
                    if self.countdown > 0:
                        self.sound_manager.play('move')  # 倒计时音效
                    if self.countdown <= 0:
                        self.countdown_active = False
                        # 确保第一个方块从顶部开始
                        self.current_y = 0
                        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                        self.fall_time = current_time  # 重置下落计时器
                        self.sound_manager.play('drop')  # 开始游戏音效
                        self.sound_manager.play_music(loops=-1)  # 开始播放背景音乐
                        # 重置当前会话统计数据
                        self.statistics.reset_current_session()

            # 更新动画
            self.animation_manager.update()
            self.piece_animation.update()  # 更新方块动画

            # 更新成就通知
            current_time = pygame.time.get_ticks()
            self.achievement.update(current_time)

            # 定期检查时间相关成就
            self.statistics.update_game_time()
            if self.statistics.total_game_time >= 5 * 60 * 1000:  # 5分钟
                self.achievement.unlock('survive_5min')
            if self.statistics.total_game_time >= 60 * 60 * 1000:  # 1小时
                self.achievement.unlock('legend')

            # 操作次数成就
            total_ops = self.statistics.total_moves + self.statistics.total_rotations
            if total_ops >= 100:
                self.achievement.unlock('moves_100')
            if total_ops >= 1000:
                self.achievement.unlock('moves_1000')

            # 定期保存统计数据（每1秒）
            if current_time - self.last_save_time > 1000:  # 1秒
                self.statistics.save_statistics()
                self.last_save_time = current_time

            # 获取震动偏移
            shake_x, shake_y = self.animation_manager.get_shake_offset()

            # 绘制
            # 🎨 使用主题背景系统
            self.draw_theme_background()

            # 如果没有面板打开，正常绘制游戏（带震动效果）
            if not self.show_settings and not self.show_statistics and not self.show_achievements:
                # 如果有震动，对网格应用偏移
                if shake_x != 0 or shake_y != 0:
                    # 先绘制UI（不震动）
                    self.draw_next_piece()
                    self.draw_info()
                    self.draw_leaderboard()
                    self.draw_controls()

                    # 手动绘制网格和方块（带偏移）
                    grid_x, grid_y = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
                    block_size = self.get_scaled_size(BLOCK_SIZE)

                    # 应用震动偏移
                    grid_x += shake_x
                    grid_y += shake_y

                    # 绘制网格背景
                    grid_rect = pygame.Rect(
                        grid_x - 2, grid_y - 2,
                        GRID_WIDTH * block_size + 4, GRID_HEIGHT * block_size + 4
                    )

                    # 霓虹边框增强（与主网格一致）
                    if self.neon_mode:
                        # 外层发光边框（青色）
                        pygame.draw.rect(self.screen, (0, 200, 255), grid_rect, 3)
                        # 内层亮边框（白色）
                        inner_rect = pygame.Rect(
                            grid_x - 1, grid_y - 1,
                            GRID_WIDTH * block_size + 2, GRID_HEIGHT * block_size + 2
                        )
                        pygame.draw.rect(self.screen, (200, 255, 255), inner_rect, 1)
                    else:
                        # 普通双层边框
                        pygame.draw.rect(self.screen, (60, 60, 80), grid_rect, 3)
                        # 内层边框（较亮）
                        inner_rect = pygame.Rect(
                            grid_x - 1, grid_y - 1,
                            GRID_WIDTH * block_size + 2, GRID_HEIGHT * block_size + 2
                        )
                        pygame.draw.rect(self.screen, (100, 100, 120), inner_rect, 1)

                    # 棋盘格效果
                    checker_color_1 = (24, 24, 32)
                    checker_color_2 = (30, 30, 40)

                    # 绘制网格内容
                    for y in range(GRID_HEIGHT):
                        for x in range(GRID_WIDTH):
                            rect = pygame.Rect(
                                grid_x + x * block_size,
                                grid_y + y * block_size,
                                block_size, block_size
                            )
                            if self.grid[y][x] != 0:
                                self.draw_3d_block(rect, self.grid[y][x])
                            else:
                                # 使用棋盘格效果
                                cell_color = checker_color_1 if (x + y) % 2 == 0 else checker_color_2
                                pygame.draw.rect(self.screen, cell_color, rect)
                                pygame.draw.rect(self.screen, (40, 40, 50), rect, 1)

                    # 绘制幽灵方块（不震动）
                    if not self.game_over and not self.waiting_to_start and not self.countdown_active:
                        # 恢复无震动偏移的坐标
                        grid_x_unshook, grid_y_unshook = self.get_scaled_offset(GRID_X_OFFSET, GRID_Y_OFFSET)
                        self.draw_ghost_piece()

                    # 绘制当前方块
                    if not self.game_over and not self.waiting_to_start and not self.countdown_active:
                        for y, row in enumerate(self.current_piece):
                            for x, cell in enumerate(row):
                                if cell != 0:
                                    rect = pygame.Rect(
                                        grid_x + (x + self.current_x) * block_size,
                                        grid_y + (y + self.current_y) * block_size,
                                        block_size, block_size
                                    )
                                    self.draw_3d_block(rect, cell)
                else:
                    # 正常绘制
                    self.draw_grid()

                    # 绘制幽灵方块
                    if not self.game_over and not self.waiting_to_start and not self.countdown_active:
                        self.draw_ghost_piece()

                    if not self.game_over and not self.waiting_to_start and not self.countdown_active:
                        # 启用动画绘制
                        self.draw_piece(self.current_piece, self.current_x, self.current_y, animated=True)
                    self.draw_next_piece()
                    self.draw_info()
                    self.draw_leaderboard()
                    self.draw_controls()
            else:
                # 有面板打开时，绘制游戏界面作为背景
                self.draw_grid()
                self.draw_next_piece()
                self.draw_info()
                self.draw_leaderboard()
                self.draw_controls()

            # 在游戏界面之上绘制面板（覆盖层）
            # 如果显示设置菜单（优先级最高）
            if self.show_settings:
                if self.key_binding_mode == 'panel':
                    # 显示键位绑定面板
                    self.draw_keybind_panel()
                else:
                    # 显示设置菜单
                    self.draw_settings_panel()
            # 如果显示统计面板
            elif self.show_statistics:
                self.draw_statistics_panel()
            # 如果显示成就面板
            elif self.show_achievements:
                self.draw_achievements_panel()

            # 绘制动画（传入scale参数）
            self.animation_manager.draw(self.screen, self.scale_factor)

            # 绘制成就通知（在最上层）
            self.achievement.draw_notification(self.screen, self.window_width, self.scale_factor)

            if self.waiting_to_start:
                self.draw_waiting_to_start()
            elif self.countdown_active:
                self.draw_countdown()
            elif self.game_over:
                self.draw_game_over()
            elif self.paused:
                self.draw_pause()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    try:
        import array
        game = Tetris()
        game.run()
    except ImportError:
        print("错误: 未安装 Pygame 库")
        print("请运行: pip install pygame")
        sys.exit(1)
