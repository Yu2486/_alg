def simplify(expr):
    """簡單化微分結果。"""
    if isinstance(expr, (int, float)) or expr == "x":
        return expr

    op = expr[0]
    a = simplify(expr[1])
    b = simplify(expr[2])

    if op == "add":
        if a == 0:
            return b
        if b == 0:
            return a
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + b
        return ("add", a, b)

    if op == "sub":
        if b == 0:
            return a
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a - b
        return ("sub", a, b)

    if op == "mul":
        if a == 0 or b == 0:
            return 0
        if a == 1:
            return b
        if b == 1:
            return a
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a * b
        return ("mul", a, b)

    if op == "div":
        if a == 0:
            return 0
        if b == 1:
            return a
        return ("div", a, b)

    if op == "pow":
        if b == 0:
            return 1
        if b == 1:
            return a
        return ("pow", a, b)

    raise ValueError(f"未知運算：{op}")


def sym_diff(expr):
    """對以 x 為變數的符號式做遞迴微分。"""
    # 常數
    if isinstance(expr, (int, float)):
        return 0

    # x
    if expr == "x":
        return 1

    if not isinstance(expr, tuple):
        raise TypeError(f"不認識的 expression：{expr}")

    op = expr[0]
    a = expr[1]
    b = expr[2]

    if op == "add":
        return simplify(("add", sym_diff(a), sym_diff(b)))

    if op == "sub":
        return simplify(("sub", sym_diff(a), sym_diff(b)))

    if op == "mul":
        # (fg)' = f'g + fg'
        return simplify((
            "add",
            ("mul", sym_diff(a), b),
            ("mul", a, sym_diff(b))
        ))

    if op == "div":
        # (f/g)' = (f'g - fg') / g^2
        numerator = (
            "sub",
            ("mul", sym_diff(a), b),
            ("mul", a, sym_diff(b))
        )
        denominator = ("pow", b, 2)
        return simplify(("div", numerator, denominator))

    if op == "pow":
        # (f^n)' = n*f^(n-1)*f'
        if not isinstance(b, (int, float)):
            raise ValueError("目前次方只支援常數，例如 x^2、(x+1)^3")

        if b == 0:
            return 0

        return simplify((
            "mul",
            ("mul", b, ("pow", a, b - 1)),
            sym_diff(a)
        ))

    raise ValueError(f"不支援的運算：{op}")


def expr_to_string(expr):
    """把 Expression Tree 轉成容易閱讀的數學式。"""
    if isinstance(expr, (int, float)):
        return str(expr)

    if expr == "x":
        return "x"

    op, a, b = expr

    if op == "add":
        return f"({expr_to_string(a)} + {expr_to_string(b)})"
    if op == "sub":
        return f"({expr_to_string(a)} - {expr_to_string(b)})"
    if op == "mul":
        return f"({expr_to_string(a)} * {expr_to_string(b)})"
    if op == "div":
        return f"({expr_to_string(a)} / {expr_to_string(b)})"
    if op == "pow":
        return f"({expr_to_string(a)} ^ {expr_to_string(b)})"

    raise ValueError(f"未知運算：{op}")


if __name__ == "__main__":
    # 3*x^2 + 5*x - 2
    expr1 = (
        "add",
        (
            "add",
            ("mul", 3, ("pow", "x", 2)),
            ("mul", 5, "x")
        ),
        -2
    )

    result1 = sym_diff(expr1)
    print("原式：", expr_to_string(expr1))
    print("微分：", expr_to_string(result1))

    # (x + 1)^3
    expr2 = ("pow", ("add", "x", 1), 3)
    result2 = sym_diff(expr2)
    print("原式：", expr_to_string(expr2))
    print("微分：", expr_to_string(result2))
