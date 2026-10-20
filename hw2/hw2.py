from pathlib import Path
import zipfile, subprocess, sys, ast

base = Path("/mnt/data/recurrence_homework")
base.mkdir(parents=True, exist_ok=True)

program = r'''"""
習題 2：求解遞迴方程式，並比較演算法複雜度。

遞迴式：
1. T(n) = T(n-1) + 8, T(1) = 1
2. T(n) = 2T(n-1) + 9, T(1) = 1
3. T(n) = 2T(n/2) + 1, T(1) = 1
4. T(n) = T(n/2) + 1, T(1) = 1

第 3、4 題假設 n 是 2 的次方。
"""


def is_power_of_two(n):
    """判斷 n 是否為正的 2 次方。"""
    return n > 0 and (n & (n - 1)) == 0


# 第 1 題：T(n) = T(n-1) + 8，T(1) = 1
def t1_recursive(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    if n == 1:
        return 1
    return t1_recursive(n - 1) + 8


def t1_formula(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    return 8 * n - 7


# 第 2 題：T(n) = 2T(n-1) + 9，T(1) = 1
def t2_recursive(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    if n == 1:
        return 1
    return 2 * t2_recursive(n - 1) + 9


def t2_formula(n):
    if n < 1:
        raise ValueError("n 必須大於或等於 1")
    return 5 * (2 ** n) - 9


# 第 3 題：T(n) = 2T(n/2) + 1，T(1) = 1
# n 必須是 2 的次方。
def t3_recursive(n):
    if not is_power_of_two(n):
        raise ValueError("第 3 題的 n 必須是正的 2 次方，例如 1、2、4、8、16")
    if n == 1:
        return 1
    return 2 * t3_recursive(n // 2) + 1


def t3_formula(n):
    if not is_power_of_two(n):
        raise ValueError("第 3 題的 n 必須是正的 2 次方")
    return 2 * n - 1


# 第 4 題：T(n) = T(n/2) + 1，T(1) = 1
# n 必須是 2 的次方。
def t4_recursive(n):
    if not is_power_of_two(n):
        raise ValueError("第 4 題的 n 必須是正的 2 次方，例如 1、2、4、8、16")
    if n == 1:
        return 1
    return t4_recursive(n // 2) + 1


def t4_formula(n):
    if not is_power_of_two(n):
        raise ValueError("第 4 題的 n 必須是正的 2 次方")
    # 對 2 的次方，bit_length() - 1 就是 log2(n) 的整數值。
    return 1 + (n.bit_length() - 1)


def main():
    # 第 1、2 題可以使用任意正整數 n。
    n = 10

    print("習題 2：遞迴方程式與演算法複雜度")
    print("=" * 58)
    print(f"第 1、2 題測試 n = {n}")
    print(f"第 1 題：遞迴計算 = {t1_recursive(n)}, 精確公式 = {t1_formula(n)}")
    print(f"第 2 題：遞迴計算 = {t2_recursive(n)}, 精確公式 = {t2_formula(n)}")

    # 第 3、4 題以 2 的次方為測試值。
    m = 16
    print()
    print(f"第 3、4 題測試 n = {m}（2 的次方）")
    print(f"第 3 題：遞迴計算 = {t3_recursive(m)}, 精確公式 = {t3_formula(m)}")
    print(f"第 4 題：遞迴計算 = {t4_recursive(m)}, 精確公式 = {t4_formula(m)}")

    print()
    print("複雜度整理：")
    print("1. T(n) = 8n - 7       -> Θ(n), O(n)")
    print("2. T(n) = 5 * 2^n - 9  -> Θ(2^n), O(2^n)")
    print("3. T(n) = 2n - 1       -> Θ(n), O(n)")
    print("4. T(n) = 1 + log2(n)  -> Θ(log n), O(log n)")

    # 確認遞迴結果與精確公式一致。
    assert t1_recursive(n) == t1_formula(n)
    assert t2_recursive(n) == t2_formula(n)
    assert t3_recursive(m) == t3_formula(m)
    assert t4_recursive(m) == t4_formula(m)
    print()
    print("驗證成功：四題的遞迴計算結果都與精確公式一致。")


if __name__ == "__main__":
    main()
'''

readme = r'''# 習題 2：求解遞迴方程式與演算法複雜度

## 作業目的

本作業分析四個遞迴方程式，求出精確公式，並判斷各自的時間複雜度。

---

## 第 1 題

題目：

```text
T(n) = T(n-1) + 8
T(1) = 1
```

逐步展開：

```text
T(n) = T(n-1) + 8
     = T(n-2) + 8 + 8
     = T(n-3) + 8 + 8 + 8
     = ...
     = T(1) + 8(n-1)
```

因為 `T(1) = 1`：

```text
T(n) = 1 + 8(n-1)
     = 1 + 8n - 8
     = 8n - 7
```

**精確解：**

```text
T(n) = 8n - 7
```

**時間複雜度：**

```text
Θ(n)，所以也是 O(n)
```

每次只比前一項多 8，總共增加約 n 次，因此是線性成長。

---

## 第 2 題

題目：

```text
T(n) = 2T(n-1) + 9
T(1) = 1
```

逐步展開：

```text
T(n) = 2T(n-1) + 9
     = 2[2T(n-2) + 9] + 9
     = 4T(n-2) + 18 + 9
     = 8T(n-3) + 36 + 18 + 9
     = ...
```

展開到 `T(1)`：

```text
T(n) = 2^(n-1)T(1) + 9(1 + 2 + 4 + ... + 2^(n-2))
```

利用等比級數：

```text
1 + 2 + 4 + ... + 2^(n-2) = 2^(n-1) - 1
```

又因為 `T(1) = 1`：

```text
T(n) = 2^(n-1) + 9(2^(n-1) - 1)
     = 10 * 2^(n-1) - 9
     = 5 * 2^n - 9
```

**精確解：**

```text
T(n) = 5 * 2^n - 9
```

**時間複雜度：**

```text
Θ(2^n)，所以也是 O(2^n)
```

因為每一層會將前一項乘以 2，所以數值呈指數成長。

---

## 第 3 題

題目：

```text
T(n) = 2T(n/2) + 1
T(1) = 1
```

這一題假設 `n` 是 2 的次方，例如 `1、2、4、8、16`。

使用遞迴樹分析：

| 層數 | 節點數 | 每個節點的額外成本 | 該層總成本 |
|---|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 1 | 2 | 1 | 2 |
| 2 | 4 | 1 | 4 |
| ... | ... | ... | ... |
| 最後一層 | n | 1 | n |

最後一層有 `n` 個基本問題，每個基本問題的成本為 `T(1) = 1`，所以葉節點成本總和是 `n`。

所有內部節點的成本總和為：

```text
1 + 2 + 4 + ... + n/2 = n - 1
```

所以：

```text
T(n) = n + (n - 1)
     = 2n - 1
```

**精確解（n 為 2 的次方）：**

```text
T(n) = 2n - 1
```

**時間複雜度：**

```text
Θ(n)，所以也是 O(n)
```

也可以使用主定理：`a = 2`、`b = 2`、`f(n) = 1`，因此 `n^(log_b(a)) = n`，可得 `Θ(n)`。

---

## 第 4 題

題目：

```text
T(n) = T(n/2) + 1
T(1) = 1
```

同樣假設 `n` 是 2 的次方。

逐步展開：

```text
T(n) = T(n/2) + 1
     = T(n/4) + 2
     = T(n/8) + 3
     = ...
```

當除以 2 共 `k` 次後，會到達 1：

```text
n / 2^k = 1
```

所以：

```text
2^k = n
k = log2(n)
```

因此：

```text
T(n) = T(1) + log2(n)
     = 1 + log2(n)
```

**精確解（n 為 2 的次方）：**

```text
T(n) = 1 + log2(n)
```

**時間複雜度：**

```text
Θ(log n)，所以也是 O(log n)
```

每次把問題規模減半，因此只需要對數層的遞迴。

---

## 四題答案整理

| 題目 | 精確解 | 時間複雜度 |
|---|---|---|
| 1 | `T(n) = 8n - 7` | `Θ(n)`，也就是 `O(n)` |
| 2 | `T(n) = 5 * 2^n - 9` | `Θ(2^n)`，也就是 `O(2^n)` |
| 3 | `T(n) = 2n - 1`（n 為 2 的次方） | `Θ(n)`，也就是 `O(n)` |
| 4 | `T(n) = 1 + log2(n)`（n 為 2 的次方） | `Θ(log n)`，也就是 `O(log n)` |

---

## Python 程式說明

檔案：`recurrence_homework.py`

程式包含四題的遞迴版本與精確公式版本，並用 `assert` 確認遞迴計算結果和公式相同。

執行方式：

```bash
python recurrence_homework.py
```

第 1、2 題測試 `n = 10`；第 3、4 題測試 `n = 16`，因為第 3、4 題的推導假設 `n` 是 2 的次方。

預期測試結果：

```text
第 1 題：遞迴計算 = 73, 精確公式 = 73
第 2 題：遞迴計算 = 5111, 精確公式 = 5111
第 3 題：遞迴計算 = 31, 精確公式 = 31
第 4 題：遞迴計算 = 5, 精確公式 = 5
```

最後會印出驗證成功訊息，表示遞迴結果和精確公式一致。

---

## 結論

第 1 題每次只增加固定的 8，因此是線性複雜度 `Θ(n)`。

第 2 題每次將前一項乘以 2，因此是指數複雜度 `Θ(2^n)`。

第 3 題每層的總成本會加倍，直到葉節點層；所有節點加總後得到 `2n - 1`，因此是線性複雜度 `Θ(n)`。

第 4 題每次把問題大小除以 2，所以只需要 `log2(n)` 層，複雜度是 `Θ(log n)`。

這份作業讓我了解，可以透過展開遞迴式、等比級數、遞迴樹和主定理，求出遞迴方程式的精確解或漸進複雜度。
'''

py_path = base / "recurrence_homework.py"
readme_path = base / "README.md"
py_path.write_text(program, encoding="utf-8")
readme_path.write_text(readme, encoding="utf-8")

# Syntax-check and execute the Python assignment.
ast.parse(program)
proc = subprocess.run(
    [sys.executable, str(py_path)],
    capture_output=True,
    text=True,
    timeout=10,
)
print(proc.stdout)
if proc.stderr:
    print("STDERR:", proc.stderr[:1500])
if proc.returncode != 0:
    raise RuntimeError("The recurrence homework program did not run successfully.")

zip_path = Path("/mnt/data/recurrence_homework.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(py_path, arcname="recurrence_homework.py")
    zf.write(readme_path, arcname="README.md")

print("Created:", py_path)
print("Created:", readme_path)
print("Created:", zip_path)
