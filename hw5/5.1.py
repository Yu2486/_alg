def hanoi_recursive(n, source="A", target="C", auxiliary="B"):
    """用遞迴解河內塔，回傳移動步驟。"""
    if n <= 0:
        return []

    if n == 1:
        return [(1, source, target)]

    return (
        hanoi_recursive(n - 1, source, auxiliary, target)
        + [(n, source, target)]
        + hanoi_recursive(n - 1, auxiliary, target, source)
    )


def hanoi_non_recursive(n, source="A", target="C", auxiliary="B"):
    """禁止使用遞迴，改用 stack 模擬遞迴呼叫。"""
    if n <= 0:
        return []

    # frame = (n, source, target, auxiliary, state)
    stack = [(n, source, target, auxiliary, 0)]
    moves = []

    while stack:
        disks, src, dst, aux, state = stack.pop()

        if disks == 0:
            continue

        if disks == 1:
            moves.append((1, src, dst))
            continue

        if state == 0:
            # 模擬：
            # hanoi(n-1, src, aux, dst)
            # move n
            # hanoi(n-1, aux, dst, src)
            stack.append((disks, src, dst, aux, 1))
            stack.append((disks - 1, src, aux, dst, 0))

        elif state == 1:
            moves.append((disks, src, dst))
            stack.append((disks - 1, aux, dst, src, 0))

    return moves


def print_moves(title, moves):
    print(title)
    for disk, src, dst in moves:
        print(f"Disk {disk}: {src} -> {dst}")
    print(f"總步數 = {len(moves)}")
    print()


if __name__ == "__main__":
    n = 3

    recursive_moves = hanoi_recursive(n)
    non_recursive_moves = hanoi_non_recursive(n)

    print_moves("=== 遞迴版本 ===", recursive_moves)
    print_moves("=== 非遞迴版本 ===", non_recursive_moves)

    print("兩種方法結果是否相同：", recursive_moves == non_recursive_moves)
    print("理論最少步數：", 2 ** n - 1)
