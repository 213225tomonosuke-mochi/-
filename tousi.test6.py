import math
import random

class Action:
    def __init__(self, name, cost, inc_boost=0, cash_boost=0, vp_boost=0, keep=0):
        self.name = name
        self.cost = cost
        self.inc_boost = inc_boost
        self.cash_boost = cash_boost
        self.vp_boost = vp_boost
        self.keep = keep

# --- 1. アクションのリスト定義 ---
actions = [
    Action("発電所建設", cost=40, inc_boost=2, keep=5),
    Action("小惑星採掘", cost=40, cash_boost=55, keep=5),
    Action("植林プロジェクト", cost=40, vp_boost=3, keep=5),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4, keep=5)
]

# --- 2. 評価関数の実行（引数に available_actions と current_money を追加） ---
def evaluate_best_action(turn, current_income, available_actions, current_money, market_action):
    best_action = None
    max_v = -float('inf')
    
    current_vp_rate = 5 * (1.25 ** (turn - 1))

    for action in available_actions:
        # 所持金チェック：買えないカードは無視
        if action.cost > current_money:
            continue

        p = math.ceil((action.cost - current_income) / 15) if (action.cost - current_income) > 0 else 1
        v_inc = (action.inc_boost * (58 - 2 * turn)) / p
        v_csh = action.cash_boost + (v_inc / p if action.cash_boost > 0 else 0)
        v_vp = action.vp_boost * current_vp_rate
        
        total_v = v_inc + v_csh + v_vp - action.cost   # keepのペナルティは考慮しない（keepは次ターン以降の価値に影響するため）
        
        if total_v > max_v:
            max_v = total_v
            best_action = action

    for action in market_action:
        # 所持金チェック：買えないカードは無視
        if action.cost > current_money:
            continue

        p = math.ceil((action.cost - current_income) / 15) if (action.cost - current_income) > 0 else 1
        v_inc = (action.inc_boost * (58 - 2 * turn)) / p
        v_csh = action.cash_boost + (v_inc / p if action.cash_boost > 0 else 0)
        v_vp = action.vp_boost * current_vp_rate
        
        total_v = v_inc + v_csh + v_vp - action.cost - action.keep   # keepのペナルティを追加
        
        if total_v > max_v:
            max_v = total_v
            best_action = action
            
            

    return best_action

# --- 3. 実行部分（手札と所持金を指定） ---
current_money = 50  # 今の所持金
market_action = random.sample(actions, 2)  # 山札から2枚引く
hand = []

print(f"--- ターン 2 (所持金: {current_money}) ---")
print("手札:", [a.name for a in hand])

# 全ての引数を正しく渡して呼び出す
best = evaluate_best_action(turn=2, current_income=10, available_actions=hand, current_money=current_money, market_action=market_action)

if best:
    print(f"👉 推奨アクション: {best.name}")
else:
    print("👉 推奨アクション: 何もしない（お金が足りません）")