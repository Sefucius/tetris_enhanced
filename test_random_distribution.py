"""
测试7-bag随机系统的方块分布
验证每7个方块中是否包含所有类型
"""

import random

# 方块形状定义（与游戏相同）
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]]   # S
]

PIECE_NAMES = ['I', 'O', 'T', 'L', 'J', 'Z', 'S']

def test_old_random(count=1000):
    """测试旧的完全随机算法"""
    print("=" * 60)
    print("旧的完全随机算法 (测试1000个方块)")
    print("=" * 60)

    pieces = []
    for _ in range(count):
        piece_idx = random.randint(0, len(SHAPES) - 1)
        pieces.append(piece_idx)

    # 统计每种方块的数量
    distribution = [pieces.count(i) for i in range(len(SHAPES))]

    print("\n方块分布:")
    for i, name in enumerate(PIECE_NAMES):
        percentage = (distribution[i] / count) * 100
        print(f"  {name}: {distribution[i]:3d} 个 ({percentage:5.2f}%)")

    # 检查连续出现情况
    consecutive_issues = []
    for i in range(len(pieces) - 3):
        if pieces[i] == pieces[i+1] == pieces[i+2]:
            consecutive_issues.append((i, PIECE_NAMES[pieces[i]]))

    print(f"\n连续3次或以上相同方块: {len(consecutive_issues)} 次")
    if consecutive_issues[:10]:
        print("  前10个例子:", consecutive_issues[:10])

    return distribution


def test_7bag_random(count=1000):
    """测试新的7-bag随机算法"""
    print("\n" + "=" * 60)
    print("新的7-bag随机算法 (测试1000个方块)")
    print("=" * 60)

    piece_bag = []
    pieces = []

    for _ in range(count):
        # 如果袋子空了，重新装满
        if not piece_bag:
            piece_bag = list(range(len(SHAPES)))
            random.shuffle(piece_bag)

        # 从袋子中取出一个方块
        piece_idx = piece_bag.pop()
        pieces.append(piece_idx)

    # 统计每种方块的数量
    distribution = [pieces.count(i) for i in range(len(SHAPES))]

    print("\n方块分布:")
    for i, name in enumerate(PIECE_NAMES):
        percentage = (distribution[i] / count) * 100
        print(f"  {name}: {distribution[i]:3d} 个 ({percentage:5.2f}%)")

    # 检查连续出现情况
    consecutive_issues = []
    for i in range(len(pieces) - 3):
        if pieces[i] == pieces[i+1] == pieces[i+2]:
            consecutive_issues.append((i, PIECE_NAMES[pieces[i]]))

    print(f"\n连续3次或以上相同方块: {len(consecutive_issues)} 次")

    # 验证每7个方块是否包含所有类型
    perfect_bags = 0
    for i in range(0, len(pieces) - 6, 7):
        bag = pieces[i:i+7]
        if len(set(bag)) == 7:  # 包含所有7种方块
            perfect_bags += 1

    total_bags = len(pieces) // 7
    print(f"\n完美的7-bag序列: {perfect_bags}/{total_bags} ({perfect_bags/total_bags*100:.1f}%)")

    return distribution


def simulate_actual_gameplay():
    """模拟实际游戏，展示连续14个方块的序列"""
    print("\n" + "=" * 60)
    print("示例：连续14个方块序列")
    print("=" * 60)

    piece_bag = []
    pieces = []

    for _ in range(14):
        if not piece_bag:
            piece_bag = list(range(len(SHAPES)))
            random.shuffle(piece_bag)
        piece_idx = piece_bag.pop()
        pieces.append(piece_idx)

    print("\n方块序列:")
    for i, piece_idx in enumerate(pieces):
        if i == 7:
            print("--- 新袋子 ---")
        print(f"{i+1:2d}. {PIECE_NAMES[piece_idx]}")

    # 验证分布
    first_7 = pieces[:7]
    second_7 = pieces[7:14]
    print(f"\n前7个方块: 包含所有7种 = {len(set(first_7)) == 7}")
    print(f"后7个方块: 包含所有7种 = {len(set(second_7)) == 7}")


if __name__ == "__main__":
    # 测试旧算法
    old_dist = test_old_random(1000)

    # 测试新算法
    new_dist = test_7bag_random(1000)

    # 对比
    print("\n" + "=" * 60)
    print("对比分析")
    print("=" * 60)
    print("\n7-bag算法的优势:")
    print("  [√] 每7个方块必定包含所有类型")
    print("  [√] 不会连续出现太多相同的方块")
    print("  [√] 玩家可以更好地规划策略")
    print("  [√] 更容易打出连击和Tetris")
    print("  [√] 符合现代Tetris官方标准")

    # 模拟实际游戏
    simulate_actual_gameplay()

    print("\n" + "=" * 60)
