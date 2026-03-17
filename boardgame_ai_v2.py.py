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

# --- 1. 強化されたデッキの定義 ---
deck = [
    Action("発電所建設", cost=40, inc_boost=9),       # 大幅強化
    Action("小惑星採掘", cost=40, cash_boost=50),     # 50にアップ
    Action("植林プロジェクト", cost=40, vp_boost=3),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4),
    Action("研究施設", cost=20, inc_boost=4),        # 4に強化
    Action("風力発電所", cost=25, inc_boost=5),      # 5に強化
    Action("巨大氷山運搬", cost=50, cash_boost=30, vp_boost=2)
]

def evaluate_best_move(turn, current_income, my_hand, market, current_money):
    best_move = None
    max_v = 0
    current_vp_rate = 5 * (1.25 ** (turn - 1))

    def calc_score(action, is_keep=False):
        # 評価基準：残りターン数(11-turn)を考慮
        remaining_turns = 11 - (turn + 1 if is_keep else turn)
        if remaining_turns < 0: remaining_turns = 0
        
        # 産出の価値 = 増加量 × 残りターン
        v_inc = action.inc_boost * remaining_turns
        # 現金の価値（即効性）
        v_csh = action.cash_boost
        # 勝利点の価値
        v_vp = action.vp_boost * current_vp_rate
        
        score = v_inc + v_csh + v_vp - action.cost
        if is_keep:
            score -= action.keep
        return score

    # 手札から PLAY
    for action in my_hand:
        if action.cost <= current_money:
            val = calc_score(action, is_keep=False)
            if val > max_v:
                max_v = val
                best_move = (action, "PLAY")

    # 市場から KEEP
    for action in market:
        if action.keep <= current_money:
            # 翌ターンの見込み資金
            next_turn_money = current_money - action.keep + current_income
            val = calc_score(action, is_keep=True)
            
            # 来ターン打てそうなら加点、無理そうなら大幅減点
            if action.cost > next_turn_money:
                val -= 20 
            
            if val > max_v:
                max_v = val
                best_move = (action, "KEEP")

    return best_move

# --- 2. 実行 ---
current_money = 50
current_income = 10
total_vp = 0
my_hand = []

for turn in range(1, 11):
    market = random.sample(deck, 2)
    print(f"\n[Turn {turn}] 金: {current_money}, 収: {current_income}, VP: {total_vp}")
    
    move = evaluate_best_move(turn, current_income, my_hand, market, current_money)

    if move:
        action, move_type = move
        if move_type == "PLAY":
            current_money -= action.cost
            my_hand.remove(action)
            current_income += action.inc_boost
            total_vp += action.vp_boost
            current_money += action.cash_boost
            print(f"👉 【PLAY】{action.name}")
        elif move_type == "KEEP":
            current_money -= action.keep
            my_hand.append(action)
            print(f"👉 【KEEP】{action.name}")
    else:
        print("👉 【WAIT】")

    current_money += current_income

print(f"\n最終結果: VP {total_vp} / 収入 {current_income} / 残金 {current_money}")