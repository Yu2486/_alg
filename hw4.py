"""
作業一：用迭代法求解方程式
題目：求解 x = cos(x)

方法：固定點迭代法（Fixed-Point Iteration）
迭代公式：x_(n+1) = cos(x_n)
初始值：x_0 = 0.5
停止條件：|x_(n+1) - x_n| < 1e-10
最大迭代次數：100 次
"""

import math


def fixed_point_iteration(x0: float, tolerance: float = 1e-10, max_iter: int = 100):
    """使用固定點迭代法求解 x = cos(x)。"""
    x = x0

    print("迭代次數\t x_n\t\t\t x_(n+1)\t\t\t 誤差")
    print("-" * 72)

    for n in range(1, max_iter + 1):
        x_next = math.cos(x)
        error = abs(x_next - x)

        print(f"{n:>4}\t\t{x:.12f}\t{x_next:.12f}\t{error:.3e}")

        if error < tolerance:
            return x_next, n, error

        x = x_next

    raise RuntimeError("迭代次數已達上限，尚未收斂。")


if __name__ == "__main__":
    root, iterations, error = fixed_point_iteration(0.5)

    print("\n計算結果")
    print(f"根的近似值 = {root:.12f}")
    print(f"迭代次數   = {iterations}")
    print(f"最後誤差   = {error:.3e}")
    print(f"驗證 cos(x) = {math.cos(root):.12f}")
