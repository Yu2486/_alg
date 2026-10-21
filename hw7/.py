def lcs_dynamic_programming(a, b):
    """動態規劃版本：回傳一個 LCS 字串及 DP 計算的格子數。"""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 從右下角回溯，還原一個最長共同子序列。
    i, j = m, n
    result = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return "".join(result), m * n


def is_subsequence(candidate, text):
    """檢查 candidate 是否為 text 的子序列。"""
    pos = 0
    for char in text:
        if pos < len(candidate) and candidate[pos] == char:
            pos += 1
    return pos == len(candidate)


def main():
    print("第七週習題：LCS 最長共同子序列")
    print("比較非動態規劃（直接遞迴）與動態規劃。")
    print("直接按 Enter 使用預設範例。")

    a = input("第一段文字 A：")
    if a == "":
        a = "ABCBDAB"
    b = input("第二段文字 B：")
    if b == "":
        b = "BDCABA"

    print("\n文字 A =", repr(a))
    print("文字 B =", repr(b))
    print("-" * 56)

    recursive_result = None
    if len(a) + len(b) <= MAX_RECURSIVE_TOTAL_LENGTH:
        stats = {"calls": 0}
        start = perf_counter()
        try:
            recursive_result = lcs_recursive(a, b, stats)
            elapsed = perf_counter() - start
            print("【非動態規劃：直接遞迴】")
            print("LCS =", repr(recursive_result))
            print("LCS 長度 =", len(recursive_result))
            print("遞迴呼叫次數 =", stats["calls"])
            print(f"執行時間 = {elapsed:.9f} 秒")
        except RecursiveLimitExceeded as error:
            elapsed = perf_counter() - start
            print("【非動態規劃：直接遞迴】")
            print("測試已安全停止：", error)
            print(f"停止前經過 = {elapsed:.6f} 秒")
    else:
        print("【非動態規劃：直接遞迴】")
        print(
            f"兩段文字合計長度超過 {MAX_RECURSIVE_TOTAL_LENGTH}，"
            "為避免指數級遞迴耗時，本次略過純遞迴測試。"
        )

    start = perf_counter()
    dp_result, cells = lcs_dynamic_programming(a, b)
    dp_elapsed = perf_counter() - start

    print("\n【動態規劃：DP 表格】")
    print("LCS =", repr(dp_result))
    print("LCS 長度 =", len(dp_result))
    print("填表狀態數 =", cells)
    print(f"執行時間 = {dp_elapsed:.9f} 秒")

    print("\n【結果驗證】")
    print("DP 結果是 A 的子序列：", is_subsequence(dp_result, a))
    print("DP 結果是 B 的子序列：", is_subsequence(dp_result, b))
    if recursive_result is not None:
        print("兩種方法的 LCS 長度相同：", len(recursive_result) == len(dp_result))
        print("若有多個同長度的 LCS，兩種方法可能回傳不同字串。")

    print("\n【複雜度比較】")
    print("非動態規劃：時間為指數級，常用上界 O(2^(m+n))；")
    print("             空間約 O(m+n) 遞迴堆疊，另有字串操作成本。")
    print("動態規劃：  時間 O(m*n)，空間 O(m*n)。")
    print("其中 m、n 分別是兩段文字的長度。")


if __name__ == "__main__":
    main()
