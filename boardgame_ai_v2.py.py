import math
import random

# --- クラス・デッキ定義は前回と同じ ---
class Action:
    def __init__(self, name, cost, keep=3, inc_boost=0, cash_boost=0, vp_boost=0):
        self.name = name
        self.cost = cost
        self.keep = keep
        self.inc_boost = inc_boost
        self.cash_boost = cash_boost
        self.vp_boost = vp_boost

deck = [
    Action("発電所建設", cost=40, inc_boost=9),
    Action("小惑星採掘", cost=40, cash_boost=50),
    Action("植林プロジェクト", cost=40, vp_boost=3),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4),
    Action("研究施設", cost=20, inc_boost=4),
    Action("風力発電所", cost=25, inc_boost=5),
    Action("巨大氷山運搬", cost=50, cash_boost=30, vp_boost=2)
]

def run_simulation():
    current_money = 50
    current_income = 10
    total_vp = 0
    my_hand = []

    for turn in range(1, 11):
        market = random.sample(deck, 2)
        
        # --- [1] 購入フェーズ (フリーアクション) ---
        # お金がある限り、市場のカードを評価して「得」なら買う
        for action in market[:]: # リストをコピーしてループ
            # 評価基準: calc_scoreがプラス、かつお金が足りるなら買う
            # 簡易的に、終盤以外で価値が一定以上のものを買うロジック
            current_vp_rate = 1000000 if turn >= 9 else (5 * (1.25 ** (turn - 1)))
            
            # 簡易評価（KEEPするかどうか）
            remaining_turns = 11 - (turn + 1)
            v_inc = action.inc_boost * (remaining_turns if turn < 9 else 0)
            v_vp = action.vp_boost * current_vp_rate
            score = v_inc + v_vp + action.cash_boost - action.cost - action.keep
            
            if current_money >= action.keep and score > 0:
                current_money -= action.keep
                my_hand.append(action)
                market.remove(action)

        # --- [2] 実行フェーズ (1ターンに1回) ---
        best_play = None
        max_v = -float('inf')
        current_vp_rate = 1000000 if turn >= 9 else (5 * (1.25 ** (turn - 1)))

        for action in my_hand:
            if action.cost <= current_money:
                # 評価計算
                remaining_turns = 11 - turn
                v_inc = action.inc_boost * (remaining_turns if turn < 9 else 0)
                v_vp = action.vp_boost * current_vp_rate
                val = v_inc + v_vp + action.cash_boost - action.cost
                
                if val > max_v:
                    max_v = val
                    best_play = action
        
        # 実行（最も価値が高いものを1つだけ）
        if best_play and max_v > 0:
            current_money -= best_play.cost
            current_income += best_play.inc_boost
            total_vp += best_play.vp_boost
            current_money += best_play.cash_boost
            my_hand.remove(best_play)

        # 収入フェーズ
        current_money += current_income
        
    return total_vp

# --- 100回テスト実行 ---
num_trials = 100
scores = [run_simulation() for _ in range(num_trials)]

print(f"=== {num_trials}回シミュレーション (ルール変更後) ===")
print(f"平均スコア : {sum(scores) / num_trials:.2f} VP")
print(f"最高スコア : {max(scores)} VP")
print(f"最低スコア : {min(scores)} VP")