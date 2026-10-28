    for _, position, city in pairs:
        if position not in used_positions and city not in used_cities:
            tour[position] = city
            used_positions.add(position)
            used_cities.add(city)
            if len(used_positions) == n:
                break

    return tour


def gradient_descent(steps=900, learning_rate=0.05, penalty=15.0, seed=3):
    """以 softmax 連續鬆弛近似 TSP，再把結果解碼成合法路徑。

    P[k][i] 表示第 k 個位置選擇城市 i 的機率。
    損失包含期望路徑長度和「每個城市只造訪一次」的懲罰項。

    注意：這是用於教學比較的簡化梯度下降版本，不能保證全域最佳解。
    """
    n = N_CITIES
    rng = random.Random(seed)

    # 將距離正規化，讓梯度數值比較穩定。
    average_distance = sum(map(sum, DIST)) / (n * n)
    dist = [[value / average_distance for value in row] for row in DIST]

    weights = [[rng.uniform(-0.1, 0.1) for _ in range(n)] for _ in range(n)]

    for step in range(steps):
        probabilities = softmax_rows(weights)

        # 每個城市被所有位置選中的總機率；理想上應該為 1。
        column_sums = [
            sum(probabilities[position][city] for position in range(n))
            for city in range(n)
        ]

        # 對 P 的梯度：前後位置的期望距離 + 城市重複造訪懲罰。
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
                unique_city_penalty = 2.0 * penalty * (column_sums[city] - 1.0)
                grad_p[position][city] = distance_gradient + unique_city_penalty

        # 經過 row-wise softmax 的梯度公式，求對 weights 的梯度。
        grad_w = [[0.0] * n for _ in range(n)]
        for position in range(n):
            row_dot = sum(
                grad_p[position][city] * probabilities[position][city]
                for city in range(n)
            )
            for city in range(n):
                p = probabilities[position][city]
                grad_w[position][city] = p * (grad_p[position][city] - row_dot)

        # 學習率逐步降低，讓後期更新更穩定。
        rate = learning_rate * (1.0 - 0.9 * step / steps) * 10.0
        for position in range(n):
            for city in range(n):
                weights[position][city] -= rate * grad_w[position][city]

    final_probabilities = softmax_rows(weights)
    return decode_probabilities(final_probabilities)


# ------------------------------------------------------------
# 同一組城市測試五種方法
# ------------------------------------------------------------
def main():
    methods = [
        ("1. 改良法（Greedy + 2-opt）", improved_2opt),
        ("2. 爬山演算法", hill_climbing),
        ("3. 模擬退火法", simulated_annealing),
        ("4. 梯度下降法（連續鬆弛）", gradient_descent),
        ("5. 貪婪演算法（最近鄰居）", greedy),
    ]

    print(f"旅行推銷員問題（TSP）：城市數量 = {N_CITIES}")
    print("城市座標使用固定亂數種子 42；每種方法使用相同距離矩陣。")
    print("路徑最後會回到起點。\n")

    results = []
    for name, method in methods:
        start_time = time.perf_counter()
        tour = method()
        elapsed = time.perf_counter() - start_time

        if not valid_tour(tour):
            raise RuntimeError(f"{name} 產生不合法路徑：{tour}")

        length = tour_length(tour)
        results.append((name, tour, length, elapsed))
        print(name)
        print(f"  路徑：{' -> '.join(map(str, tour + [tour[0]]))}")
        print(f"  總距離：{length:.2f}")
        print(f"  執行時間：{elapsed:.6f} 秒")
        print()

    best_result = min(results, key=lambda result: result[2])
    print("=" * 68)
    print(f"本次結果中距離最短的方法：{best_result[0]}")
    print(f"最短總距離：{best_result[2]:.2f}")
    print("注意：啟發式演算法不保證找到全域最佳解，隨機方法的結果可能變動。")


if __name__ == "__main__":
    main()
