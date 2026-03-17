import math
import random

class Action:
    def __init__(self, name, cost, keep=3, inc_boost=0, cash_boost=0, vp_boost=0):
        self.name = name
        self.cost = cost
        self.keep = keep
        self.inc_boost = inc_boost
        self.cash_boost = cash_boost
        self.vp_boost = vp_boost

# --- デッキ定義 ---
deck = [
    Action("発電所建設", cost=40, inc_boost=9),
    Action("小惑星採掘", cost=40, cash_boost=50),
    Action("植林プロジェクト", cost=40, vp_boost=3),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4),
    Action("研究施設", cost=20, inc_boost=4),
    Action("風力発電所", cost=25, inc_boost=5),
    Action("巨大氷山運搬", cost=50, cash_boost=30, vp_boost=2)
]

def evaluate_best_move(turn, current_income, my_hand, market, current_money):
    best_move = None
    max_v = -float('inf')
    
    # 9, 10ターン目はVP至上主義
    current_vp_rate = 1000000 if turn >= 9 else (5 * (1.25 ** (turn - 1)))

    def calc_score(action, is_keep=False, virtual_turn=None):
        t = virtual_turn if virtual_turn else (turn + 1 if is_keep else turn)
        remaining_turns = 11 - t
        if remaining_turns < 0: remaining_turns = 0
        
        v_inc = action.inc_boost * remaining_turns if turn < 9 else 0
        v_csh = action.cash_boost
        v_vp = action.vp_boost * current_vp_rate
        
        score = v_inc + v_csh + v_vp - action.cost
        if is_keep: score -= action.keep
        return score

    # 1. PLAYの評価
    for action in my_hand:
        if action.cost <= current_money:
            val = calc_score(action)
            if val > max_v:
                max_v = val
                best_move = (action, "PLAY")

    # 2. KEEPの評価（9・10ターンの特殊ロジック込）
    for action in market:
        if action.keep <= current_money:
            if turn == 9:
                next_money = current_money - action.keep + current_income
                if action.cost <= next_money:
                    val = calc_score(action, is_keep=True, virtual_turn=10)
                else: val = -999999
            elif turn == 10:
                val = -999999
            else:
                next_money = current_money - action.keep + current_income
                val = calc_score(action, is_keep=True)
                if action.cost > next_money: val -= 20
            
            if val > max_v:
                max_v = val
                best_move = (action, "KEEP")

    # 何もしない(WAIT)を基準値0として評価
    if max_v < 0: return None
    return best_move

# --- シミュレーション実行部分 ---
def run_simulation():
    current_money = 50
    current_income = 10
    total_vp = 0
    my_hand = []

    for turn in range(1, 11):
        market = random.sample(deck, 2)
        move = evaluate_best_move(turn, current_income, my_hand, market, current_money)

        if move:
            action, move_type = move
            if move_type == "PLAY":
                current_money -= action.cost
                my_hand.remove(action)
                current_income += action.inc_boost
                total_vp += action.vp_boost
                current_money += action.cash_boost
            elif move_type == "KEEP":
                current_money -= action.keep
                my_hand.append(action)
        current_money += current_income
    return total_vp

# --- 100回テスト実行 ---
num_trials = 100
scores = [run_simulation() for _ in range(num_trials)]

# 結果の集計
avg_score = sum(scores) / num_trials
max_score = max(scores)
min_score = min(scores)

print(f"=== {num_trials}回シミュレーション結果 ===")
print(f"平均スコア : {avg_score:.2f} VP")
print(f"最高スコア : {max_score} VP")
print(f"最低スコア : {min_score} VP")
print("="*30)

# 簡易的な分布表示
print("\n[スコア分布]")
for s in sorted(set(scores)):
    count = scores.count(s)
    print(f"{s:2}VP: {'*' * count} ({count}回)")