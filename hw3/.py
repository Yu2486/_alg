from itertools import product
import re

# 示範公式：
# (A OR B) AND (!A OR C) AND (!B OR !C)
DEFAULT_CLAUSES = [
    ["A", "B"],
    ["!A", "C"],
    ["!B", "!C"],
]


def parse_literal(literal):
    """解析變數，例如 A 或 !A。"""
    literal = literal.strip()

    negated = literal.startswith("!") or literal.startswith("~")
    variable = literal[1:] if negated else literal

    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", variable):
        raise ValueError(f"不合法的變數：{literal}")

    return variable, negated


def get_variables(clauses):
    """找出所有變數並排序。"""
    variables = set()

    for clause in clauses:
        for literal in clause:
            variable, _ = parse_literal(literal)
            variables.add(variable)

    return sorted(variables)


def evaluate_literal(literal, assignment):
    """計算一個變數或否定變數的真假。"""
    variable, negated = parse_literal(literal)
    value = assignment[variable]

    return not value if negated else value


def evaluate_clause(clause, assignment):
    """子句內使用 OR。"""
    return any(
        evaluate_literal(literal, assignment)
        for literal in clause
    )


def evaluate_cnf(clauses, assignment):
    """所有子句之間使用 AND。"""
    return all(
        evaluate_clause(clause, assignment)
        for clause in clauses
    )


def read_clauses():
    """讀取公式；直接按 Enter 使用範例。"""
    print("每行輸入一個子句，變數以空白分隔。")
    print("例如 A B 代表 A OR B，!A C 代表 NOT A OR C。")
    print("不同子句之間代表 AND，空白行結束輸入。")
    print("直接按 Enter 使用內建範例。\n")

    clauses = []

    while True:
        line = input(f"子句 {len(clauses) + 1}：").strip()

        if line == "":
            break

        literals = line.split()

        try:
            for literal in literals:
                parse_literal(literal)
        except ValueError as error:
            print("格式錯誤：", error)
            continue

        clauses.append(literals)

    if not clauses:
        print("使用內建範例。")
        clauses = [clause[:] for clause in DEFAULT_CLAUSES]

    return clauses


def solve_sat(clauses):
    """列舉所有可能的指派並建立真值表。"""
    variables = get_variables(clauses)
    total = 2 ** len(variables)
    sat_count = 0
    first_solution = None

    print("\n公式：")
    for i, clause in enumerate(clauses, start=1):
        print(f"C{i}: " + " OR ".join(clause))

    headers = (
        variables
        + [f"C{i}" for i in range(1, len(clauses) + 1)]
        + ["公式結果"]
    )

    print("\n真值表（T=True，F=False）：")
    print(" | ".join(headers))
    print("-" * max(24, 6 * len(headers)))

    # 每個變數都有 False 和 True 兩種選擇。
    # n 個變數總共有 2^n 種組合。
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values))

        clause_results = [
            evaluate_clause(clause, assignment)
            for clause in clauses
        ]

        formula_result = all(clause_results)

        row = [
            "T" if assignment[var] else "F"
            for var in variables
        ]

        row += [
            "T" if result else "F"
            for result in clause_results
        ]

        row.append("SAT" if formula_result else "不滿足")
        print(" | ".join(row))

        if formula_result:
            sat_count += 1

            if first_solution is None:
                first_solution = assignment.copy()

    print(f"\n變數數量：{len(variables)}")
    print(f"列舉的指派總數：{total}")
    print(f"滿足公式的指派數：{sat_count}")

    if sat_count > 0:
        print("結果：SAT（公式可滿足）")
        print("其中一組解：")

        for variable, value in first_solution.items():
            print(f"{variable} = {'True' if value else 'False'}")

    else:
        print("結果：UNSAT（公式不可滿足）")

    print("\n複雜度分析：")
    print("時間複雜度：O(2^n * L)")
    print("空間複雜度：O(n + L)，不計輸出")


def main():
    clauses = read_clauses()
    solve_sat(clauses)


if __name__ == "__main__":
    main()
