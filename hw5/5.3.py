def my_map(func, data):
    if data == []:
        return []
    return [func(data[0])] + my_map(func, data[1:])


def my_filter(predicate, data):
    if data == []:
        return []

    if predicate(data[0]):
        return [data[0]] + my_filter(predicate, data[1:])

    return my_filter(predicate, data[1:])


def my_reduce(func, data, initial=None):
    if data == []:
        return initial

    if initial is None:
        if len(data) == 1:
            return data[0]
        return my_reduce(func, data[1:], data[0])

    return my_reduce(func, data[1:], func(initial, data[0]))


def bubble_pass(data):
    """使用自製 reduce 做一次 Bubble Sort 掃描。"""
    if len(data) <= 1:
        return data

    def step(state, item):
        result, last = state

        if last is None:
            return (result, item)

        if last > item:
            return (result + [item], last)

        return (result + [last], item)

    result, last = my_reduce(step, data, ([], None))
    return result + [last]


def bubble_sort(data):
    """完全不使用迴圈。"""
    data = my_map(lambda x: x, data)

    def sort_recursive(values, times):
        if times <= 1:
            return values

        return sort_recursive(
            bubble_pass(values),
            times - 1
        )

    return sort_recursive(data, len(data))


if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]

    print("原始資料：", data)
    print("my_map(x*2)：", my_map(lambda x: x * 2, data))
    print("my_filter(偶數)：", my_filter(lambda x: x % 2 == 0, data))
    print("my_reduce(加總)：", my_reduce(lambda a, b: a + b, data, 0))
    print("Bubble Sort：", bubble_sort(data))
