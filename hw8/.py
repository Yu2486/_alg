"""
第七週習題：旅行推銷員問題（TSP）五種方法比較。

方法：
1. 改良法：貪婪初始解 + 2-opt 最佳改良
2. 爬山演算法：隨機初始路徑 + 隨機交換，只接受更短的路徑
3. 模擬退火法：2-opt 鄰居，允許按機率接受較差解
4. 梯度下降法：連續鬆弛 + softmax + 城市唯一性懲罰 + 離散解碼
5. 貪婪演算法：最近鄰居法

只使用 Python 標準函式庫，不需要額外安裝套件。
執行：python tsp_five_methods.py
"""

import math
import random
import time


# 使用固定亂數種子，保證每次執行使用同一組城市座標。
N_CITIES = 20
_CITY_RNG = random.Random(42)

CITIES = [
    (_CITY_RNG.uniform(0, 100), _CITY_RNG.uniform(0, 100))
    for _ in range(N_CITIES)
]

DIST = [
    [math.dist(city_a, city_b) for city_b in CITIES]
    for city_a in CITIES
]


def tour_length(tour):
    """計算封閉巡迴路徑總長度，最後一個城市會回到起點。"""
    if not tour:
        return 0.0

    return sum(
        DIST[tour[i]][tour[(i + 1) % len(tour)]]
        for i in range(len(tour))
    )


def valid_tour(tour):
    """確認路徑是否恰好造訪每個城市一次。"""
    return (
        len(tour) == N_CITIES
        and sorted(tour) == list(range(N_CITIES))
    )


# ------------------------------------------------------------
# 1. 改良法：貪婪初始解 + 2-opt
# ------------------------------------------------------------

def improved_2opt(initial_tour=None):
    """
    以貪婪解為起點，使用 2-opt 不斷改善路徑。
    每輪檢查所有合法的 2-opt 改動，採用改善最多的一個。
    """
    tour = (
        list(initial_tour)
        if initial_tour is not None
        else greedy()
    )

    n = len(tour)

    while True:
        best_delta = -1e-12
        best_pair = None

        for i in range(n - 1):
            for j in range(i + 2, n):

                # 首尾兩條邊在環上相鄰，反轉沒有意義。
                if i == 0 and j == n - 1:
                    continue

                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]

                # 2-opt 只會改變兩條邊。
                delta = (
                    DIST[a][c] + DIST[b][d]
                    - DIST[a][b] - DIST[c][d]
                )

                if delta < best_delta:
                    best_delta = delta
                    best_pair = (i, j)

        # 找不到更短的路徑，就停止。
        if best_pair is None:
            break

        i, j = best_pair

        # 反轉中間一段城市的順序。
        tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])

    return tour


# ------------------------------------------------------------
# 2. 爬山演算法：只接受更短的路徑
# ------------------------------------------------------------

def hill_climbing(iterations=12000, seed=1):
    """
    隨機產生初始路徑。
    每次交換兩個城市的位置。
    新路徑較短才接受，否則還原。
    """
    rng = random.Random(seed)

    tour = list(range(N_CITIES))
    rng.shuffle(tour)

    current_length = tour_length(tour)

    for _ in range(iterations):
        i, j = rng.sample(range(N_CITIES), 2)

        # 交換兩個城市。
        tour[i], tour[j] = tour[j], tour[i]

        candidate_length = tour_length(tour)

        if candidate_length < current_length:
            current_length = candidate_length
        else:
            # 新路徑沒有改善，還原交換。
            tour[i], tour[j] = tour[j], tour[i]

    return tour


# ------------------------------------------------------------
# 3. 模擬退火法：允許以機率接受較差解
# ------------------------------------------------------------

def simulated_annealing(
    initial_temperature=100.0,
    final_temperature=0.05,
    cooling_rate=0.97,
    iterations_per_temperature=80,
    seed=2,
):
    """
    使用 2-opt 產生候選路徑。

    路徑變好時直接接受。
    路徑變差時，依 exp(-delta / temperature) 的機率接受。

    溫度逐漸降低，使搜尋從廣泛探索逐步轉向穩定改善。
    """
    rng = random.Random(seed)

    current_tour = list(range(N_CITIES))
    rng.shuffle(current_tour)

    current_length = tour_length(current_tour)

    best_tour = current_tour[:]
    best_length = current_length

    temperature = initial_temperature

    while temperature > final_temperature:
        for _ in range(iterations_per_temperature):
            i, j = sorted(rng.sample(range(N_CITIES), 2))

            # 反轉一段城市順序，產生 2-opt 候選路徑。
            candidate = (
                current_tour[:i]
                + current_tour[i:j + 1][::-1]
                + current_tour[j + 1:]
            )

            candidate_length = tour_length(candidate)
            delta = candidate_length - current_length

            # 變好一定接受；變差則按機率接受。
            if (
                delta < 0
                or rng.random() < math.exp(-delta / temperature)
            ):
                current_tour = candidate
                current_length = candidate_length

                # 記錄整個搜尋過程中的最佳路徑。
                if current_length < best_length:
                    best_tour = current_tour[:]
                    best_length = current_length

        # 降低溫度。
        temperature *= cooling_rate

    return best_tour


# ------------------------------------------------------------
# 4. 梯度下降法：連續鬆弛 + softmax + 解碼
# ------------------------------------------------------------

def softmax_rows(weights):
    """對矩陣每一列執行數值穩定的 softmax。"""
    probabilities = []

    for row in weights:
        max_value = max(row)

        exps = [
            math.exp(value - max_value)
            for value in row
        ]

        total = sum(exps)

        probabilities.append([
            value / total for value in exps
        ])

    return probabilities


def decode_probabilities(probabilities):
    """
    將位置－城市機率矩陣解碼成合法排列。
    每個位置與每個城市只能使用一次。
    """
    n = len(probabilities)

    pairs = sorted(
        (
            (probabilities[position][city], position, city)
            for position in range(n)
            for city in range(n)
        ),
        reverse=True,
    )

    tour = [-1] * n
    used_positions = set()
    used_cities = set()

    for _, position, city in pairs:
        if (
            position not in used_positions
            and city not in used_cities
        ):
            tour[position] = city
            used_positions.add(position)
            used_cities.add(city)

            if len(used_positions) == n:
                break

    return tour


def gradient_descent(
    steps=900,
    learning_rate=0.05,
    penalty=15.0,
    seed=3,
):
    """
    以連續鬆弛近似 TSP，再解碼成合法路徑。

    P[position][city] 代表某個位置選擇該城市的機率。

    損失函數包含：
    1. 期望路徑距離。
    2. 每個城市應該恰好造訪一次的懲罰項。

    注意：這是教學用途的簡化版本，不保證全域最佳解。
    """
    n = N_CITIES
    rng = random.Random(seed)

    # 將距離正規化，讓梯度數值較穩定。
    average_distance = (
        sum(sum(row) for row in DIST) / (n * n)
    )

    dist = [
        [value / average_distance for value in row]
        for row in DIST
    ]

    # 初始化可訓練權重矩陣。
    weights = [
        [rng.uniform(-0.1, 0.1) for _ in range(n)]
        for _ in range(n)
    ]

    for step in range(steps):
        probabilities = softmax_rows(weights)

        # 計算每個城市被所有位置選中的總機率。
        column_sums = [
            sum(
                probabilities[position][city]
                for position in range(n)
            )
            for city in range(n)
        ]

        # 對機率 P 的梯度。
        grad_p = [[0.0] * n for _ in range(n)]

        for position in range(n):
            next_position = (position + 1) % n
            previous_position = (position - 1) % n

            for city in range(n):
                distance_gradient = 0.0

                for other_city in range(n):
                    distance_gradient += dist[city][other_city] * (
                        probabilities[next_position][other_city]
                        + probabilities[previous_position][other_city]
                    )

                # 懲罰城市被重複選取或未被選取。
                unique_city_penalty = (
                    2.0 * penalty * (column_sums[city] - 1.0)
                )

                grad_p[position][city] = (
                    distance_gradient + unique_city_penalty
                )

        # 使用 row-wise softmax 的梯度公式。
        grad_w = [[0.0] * n for _ in range(n)]

        for position in range(n):
            row_dot = sum(
                grad_p[position][city]
                * probabilities[position][city]
                for city in range(n)
            )

            for city in range(n):
                p = probabilities[position][city]

                grad_w[position][city] = p * (
                    grad_p[position][city] - row_dot
                )

        # 隨迭代進行逐步降低學習率。
        rate = (
            learning_rate
            * (1.0 - 0.9 * step / steps)
            * 10.0
        )

        for position in range(n):
            for city in range(n):
                weights[position][city] -= (
                    rate * grad_w[position][city]
                )

    # 將最後的機率矩陣轉換成城市排列。
    final_probabilities = softmax_rows(weights)

    return decode_probabilities(final_probabilities)


# ------------------------------------------------------------
# 5. 貪婪演算法：最近鄰居法
# ------------------------------------------------------------

def greedy(start=0):
    """
    從指定城市出發，每次前往最近的未造訪城市。
    最後會回到起點，形成封閉巡迴路徑。
    """
    unvisited = set(range(N_CITIES))
    unvisited.remove(start)

    tour = [start]

    while unvisited:
        current = tour[-1]

        next_city = min(
            unvisited,
            key=lambda city: DIST[current][city]
        )

        tour.append(next_city)
        unvisited.remove(next_city)

    return tour


# ------------------------------------------------------------
# 執行與比較五種方法
# ------------------------------------------------------------

def main():
    methods = [
        ("1. 改良法（Greedy + 2-opt）", improved_2opt),
        ("2. 爬山演算法", hill_climbing),
        ("3. 模擬退火法", simulated_annealing),
        ("4. 梯度下降法（連續鬆弛）", gradient_descent),
        ("5. 貪婪演算法（最近鄰居）", greedy),
    ]

    print(
        f"旅行推銷員問題（TSP）："
        f"城市數量 = {N_CITIES}"
    )

    print(
        "城市座標使用固定亂數種子 42；"
        "每種方法使用相同距離矩陣。"
    )

    print("路徑最後會回到起點。\n")

    results = []

    for name, method in methods:
        start_time = time.perf_counter()

        tour = method()

        elapsed = time.perf_counter() - start_time

        # 確認每個城市恰好出現一次。
        if not valid_tour(tour):
            raise RuntimeError(
                f"{name} 產生不合法路徑：{tour}"
            )

        length = tour_length(tour)

        results.append((
            name,
            tour,
            length,
            elapsed,
        ))

        print(name)

        print(
            "  路徑："
            + " -> ".join(map(str, tour + [tour[0]]))
        )

        print(f"  總距離：{length:.2f}")
        print(f"  執行時間：{elapsed:.6f} 秒")
        print()

    best_result = min(
        results,
        key=lambda result: result[2]
    )

    print("=" * 68)

    print(
        "本次結果中距離最短的方法："
        f"{best_result[0]}"
    )

    print(f"最短總距離：{best_result[2]:.2f}")

    print(
        "注意：啟發式演算法不保證找到全域最佳解，"
        "隨機方法的結果可能變動。"
    )


if __name__ == "__main__":
    main()
