import random


def quickselect_median(l, pivot_fn=random.choice):
    if len(l) % 2 == 1:
        return quickselect(l, len(l) // 2, pivot_fn)
    else:
        return 0.5 * (quickselect(l, len(l) / 2 - 1, pivot_fn) +
                      quickselect(l, len(l) / 2, pivot_fn))


def quickselect(l, k, pivot_fn):
    """
    Select the kth element in l (0 based)
    :param l: List of numerics
    :param k: Index
    :param pivot_fn: Function to choose a pivot
    :return: The kth element of l
    """
    # print(l)
    # print(f"{k=}")

    if len(l) == 1:
        assert k == 0
        return l[0]

    pivot = pivot_fn(l)

    lows = [el for el in l if el < pivot]
    highs = [el for el in l if el > pivot]
    # pivots = [el for el in l if el == pivot]

    # print(f"{pivot=}")
    # print(f"{lows=}")
    # print(f"{highs=}")
    # print(f"{k=}, {len(lows)+1=}")
    if len(lows) > k:
        return quickselect(lows, k, pivot_fn)
    elif len(lows) + 1 > k:
        # We got lucky and guessed the median
        return pivot
    else:
        return quickselect(highs, k - len(lows) - 1, pivot_fn)


def ansi_rand(a_0, n):
    rand_num = [a_0] * n
    rand_num[0] = (a_0 * 1103515245 + 12345) % 2147483648
    for i in range(1, n):
        rand_num[i] = (rand_num[i-1] * 1103515245 + 12345) % 2147483648

    return rand_num


if __name__ == '__main__':
    n_cases = int(input())
    for c in range(n_cases):
        a, n_iter = input().split(" ")
        median = quickselect_median(ansi_rand(int(a), int(n_iter)))
        print(median)
