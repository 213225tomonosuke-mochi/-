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

# --- 1. デッキ（多めに用意） ---
deck = [
    Action("発電所建設", cost=40, inc_boost=2),
    Action("小惑星採掘", cost=40, cash_boost=45),
    Action("植林プロジェクト", cost=40, vp_boost=3),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4),
    Action("研究施設", cost=20, inc_boost=1),
    Action("風力発電所", cost=25, inc_boost=1),
    Action("巨大氷山運搬", cost=50, cash_boost=30, vp_boost=2)
]

def evaluate_best_move(turn, current_income, my_hand, market, current_money):
    best_move = None
    max_v = 0
    current_vp_rate = 5 * (1.25 ** (turn - 1))

    def calc_score(action, is_keep=False):
        # 実行ターンを想定（KEEPなら来ターン以降の前提）
        target_turn = turn + 1 if is_keep else turn
        p = math.ceil((action.cost - current_income) / 15) if (action.cost - current_income) > 0 else 1
        
        v_inc = (action.inc_boost * (58 - 2 * target_turn)) / p
        v_csh = action.cash_boost + (v_inc / p if action.cash_boost > 0 else 0)
        v_vp = action.vp_boost * current_vp_rate
        
        score = v_inc + v_csh + v_vp - action.cost
        if is_keep:
            score -= action.keep # 購入コストを差し引く
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
            # 【進化ポイント】来ターンの予算（所持金 - keep + 収入）でプレイ可能かチェック
            next_turn_money = current_money - action.keep + current_income
            if action.cost <= next_turn_money:
                # 来ターン打てるなら高評価
                val = calc_score(action, is_keep=True)
            else:
                # 来ターンも打てないなら、少し評価を下げる（塩漬けリスク）
                val = calc_score(action, is_keep=True) - 10
            
            if val > max_v:
                max_v = val
                best_move = (action, "KEEP")

    return best_move

# --- メインシミュレーション ---
current_money = 50
current_income = 10
my_hand = []

for turn in range(1, 11): # 10ターンに延長
    # 市場を新しく2枚引き直す（毎ターンの入れ替え）
    market = random.sample(deck, 2)
    
    print(f"\n--- ターン {turn} (金: {current_money}, 収入: {current_income}) ---")
    print(f"手札: {[a.name for a in my_hand]}")
    print(f"市場: {[a.name for a in market]}")

    move = evaluate_best_move(turn, current_income, my_hand, market, current_money)

    if move:
        action, move_type = move
        if move_type == "PLAY":
            current_money -= action.cost
            my_hand.remove(action)
            current_income += action.inc_boost
            print(f"👉 【PLAY】{action.name} を実行！")
        elif move_type == "KEEP":
            current_money -= action.keep
            # 市場からは消えるが、実行は来ターン以降
            my_hand.append(action)
            print(f"👉 【KEEP】{action.name} を購入（来ターン以降の準備）")
    else:
        print("👉 【WAIT】資金温存...")

    # 収入
    current_money += current_income