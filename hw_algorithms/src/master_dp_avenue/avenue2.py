import random


def trees_not_in_las(avenue):
    n = len(avenue)
    if n == 0:
        return []

    # length of LAS until ix
    las_lengths = [1] * n
    # save predecessor of ix
    predecessors = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if avenue[i] > avenue[j] and las_lengths[i] < las_lengths[j] + 1:
                las_lengths[i] = las_lengths[j] + 1
                predecessors[i] = j

    max_len = max(las_lengths)
    max_ix = las_lengths.index(max_len)

    # Get LAS from predecessors
    las = []
    pre_ix = max_ix
    while pre_ix != -1:
        las.append(pre_ix)
        pre_ix = predecessors[pre_ix]

    las.reverse()

    trees_to_remove = [i + 1 for i in range(n) if i not in las]

    return trees_to_remove


if __name__ == '__main__':
    n_cases = int(input())
    for i in range(n_cases):
        avenue = list(map(int, input().split(' ')))
        cut_list = trees_not_in_las(avenue[1:])

        if len(cut_list) == 0:
            print("none")
        else:
            for tree_no in cut_list:
                print(f"{tree_no} ", end="")
            print("")
