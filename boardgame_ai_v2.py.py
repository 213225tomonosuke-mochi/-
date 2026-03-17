import math
import random

# --- 1. アクションの定義（keepコストを追加） ---
class Action:
    def __init__(self, name, cost, keep=3, inc_boost=0, cash_boost=0, vp_boost=0):
        self.name = name
        self.cost = cost      # プレイ（実行）コスト
        self.keep = keep      # キープ（購入）コスト
        self.inc_boost = inc_boost
        self.cash_boost = cash_boost
        self.vp_boost = vp_boost

# --- 2. 山札（データ元） ---
deck = [
    Action("発電所建設", cost=40, inc_boost=2),
    Action("小惑星採掘", cost=40, cash_boost=45),
    Action("植林プロジェクト", cost=40, vp_boost=3),
    Action("都市開発", cost=60, inc_boost=1, vp_boost=4),
    Action("研究施設", cost=20, inc_boost=1)
]

# --- 3. 評価関数（PLAY, KEEP, WAIT の3択） ---
def evaluate_best_move(turn, current_income, my_hand, market, current_money):
    best_move = None
    max_v = 0  # 0以下なら「何もしない(Wait)」になる
    
    current_vp_rate = 5 * (1.25 ** (turn - 1))

    # 評価スコア計算用
    def calc_score(action):
        p = math.ceil((action.cost - current_income) / 15) if (action.cost - current_income) > 0 else 1
        v_inc = (action.inc_boost * (58 - 2 * turn)) / p
        v_csh = action.cash_boost + (v_inc / p if action.cash_boost > 0 else 0)
        v_vp = action.vp_boost * current_vp_rate
        return v_inc + v_csh + v_vp - action.cost

    # パターン1: 手札から PLAY
    for action in my_hand:
        if action.cost <= current_money:
            val = calc_score(action)
            if val > max_v:
                max_v = val
                best_move = (action, "PLAY")

    # パターン2: 市場から KEEP
    for action in market:
        if action.keep <= current_money:
            # KEEPは将来への投資なので、評価を少し補正（-10は仮の調整値）
            val = calc_score(action) - action.keep - 10 
            if val > max_v:
                max_v = val
                best_move = (action, "KEEP")

    return best_move

# --- 4. メインループ（5ターン） ---
current_money = 50
current_income = 10
my_hand = []
market = random.sample(deck, 3)

for turn in range(1, 6):
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
            print(f"👉 【実行】{action.name}")
        elif move_type == "KEEP":
            current_money -= action.keep
            market.remove(action)
            my_hand.append(action)
            print(f"👉 【購入】{action.name} を手札へ")
    else:
        print("👉 【待機】パスしました")

    current_money += current_income
    if len(market) < 3:
        market.append(random.choice(deck))