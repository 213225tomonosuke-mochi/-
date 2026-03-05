import math 
import random

class Action:
    def __init__(self, name, cost, inc_boost=0, cash_boost=0, vp_boost=0):
        self.name = name
        self.cost = cost
        self.inc_boost = inc_boost    # 産出量アップ
        self.cash_boost = cash_boost  # 即時資金ゲット
        self.vp_boost = vp_boost      # 勝利点ゲット

# --- 1. アクションのリスト定義 ---
actions = [
    Action("発電所建設", cost=40, inc_boost=2),           # 投資型
    Action("小惑星採掘", cost=40, cash_boost=45),         # 即金型
    Action("植林プロジェクト", cost=40, vp_boost=3),      # 勝利点型
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4)  # 複合型
]

# --- 山札からランダムに3枚引く ---
# random.sample(対象, 枚数) を使うのが最も効率的です
hand = random.sample(actions, 3)

print("--- 今月の手札（ランダム） ---")
for h in hand:
    print(f"- {h.name} (コスト: {h.cost})")
print("-" * 30)

# --- 2. 評価関数の実行 ---
def evaluate_best_action(turn, current_income, available_actions):
    best_action = None
    max_v = -float('inf')
    
    current_vp_rate = 5 * (1.25 ** (turn - 1))

    # 全アクションではなく、渡された「手札」の中だけで比較する
    for action in available_actions:
        p = math.ceil((action.cost - current_income) / 15) if (action.cost - current_income) > 0 else 1
        v_inc = (action.inc_boost * (58 - 2 * turn)) / p
        v_csh = action.cash_boost + (v_inc / p if action.cash_boost > 0 else 0)
        v_vp = action.vp_boost * current_vp_rate
        
        total_v = v_inc + v_csh + v_vp - action.cost
        
        if total_v > max_v:
            max_v = total_v
            best_action = action
            
    return best_action

# --- 3. テスト実行 ---
print(f"--- ターン 2 の意思決定 ---")
best_2 = evaluate_best_action(turn=2, current_income=10, available_actions=hand)
print(f"👉 推奨アクション: {best_2.name}\n")

print(f"--- ターン 12 の意思決定 ---")
best_12 = evaluate_best_action(turn=12, current_income=30, available_actions=hand)
print(f"👉 推奨アクション: {best_12.name}")