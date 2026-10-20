# 第 1 題：T(n) = T(n-1) + 8，T(1) = 1
def t1_recursive(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    if n == 1:
        return 1
    return t1_recursive(n - 1) + 8


def t1_formula(n):
    return 8 * n - 7


# 第 2 題：T(n) = 2T(n-1) + 9，T(1) = 1
def t2_recursive(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    if n == 1:
        return 1
    return 2 * t2_recursive(n - 1) + 9


def t2_formula(n):
    return 5 * (2 ** n) - 9


# 判斷 n 是否為 2 的次方
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


# 第 3 題：T(n) = 2T(n/2) + 1，T(1) = 1
def t3_recursive(n):
    if not is_power_of_two(n):
        raise ValueError("n 必須是正的 2 次方")
    if n == 1:
        return 1
    return 2 * t3_recursive(n // 2) + 1


def t3_formula(n):
    return 2 * n - 1


# 第 4 題：T(n) = T(n/2) + 1，T(1) = 1
def t4_recursive(n):
    if not is_power_of_two(n):
        raise ValueError("n 必須是正的 2 次方")
    if n == 1:
        return 1
    return t4_recursive(n // 2) + 1


def t4_formula(n):
    # n 是 2 的次方時，bit_length() = 1 + log2(n)
    return n.bit_length()


def main():
    n = 10
    m = 16

    print("第 1、2 題測試 n =", n)
    print("第 1 題：", t1_recursive(n), t1_formula(n))
    print("第 2 題：", t2_recursive(n), t2_formula(n))

    print("\n第 3、4 題測試 n =", m)
    print("第 3 題：", t3_recursive(m), t3_formula(m))
    print("第 4 題：", t4_recursive(m), t4_formula(m))

    print("\n複雜度整理：")
    print("1. T(n) = 8n - 7       -> O(n)")
    print("2. T(n) = 5 * 2^n - 9  -> O(2^n)")
    print("3. T(n) = 2n - 1       -> O(n)")
    print("4. T(n) = 1 + log2(n)  -> O(log n)")

    assert t1_recursive(n) == t1_formula(n)
    assert t2_recursive(n) == t2_formula(n)
    assert t3_recursive(m) == t3_formula(m)
    assert t4_recursive(m) == t4_formula(m)

    print("\n驗證成功：四題的遞迴結果都與公式一致。")


if __name__ == "__main__":
    main()
