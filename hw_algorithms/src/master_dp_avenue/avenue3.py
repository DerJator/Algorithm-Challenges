def find_first_greater(numbers, N):
    """
    Find the position of the first element in the ordered list `numbers`
    that is larger than the given number `N`.
    """
    if len(numbers) == 1:
        return 0

    left, right = 0, len(numbers) - 1

    if numbers[left] < numbers[right]:
        while left < right:
            mid = left + (right - left) // 2
            if numbers[mid] > N:
                right = max(0, mid - 1)
            elif numbers[mid] == N:
                return None
            else:
                left = min(len(numbers) - 1, mid + 1)

        return left


def enter_predecessor(tree_dicts: [dict], lvl: int, new: int, new_ix: int):
    """
    From the cached structure, get the predecessor of the new element at level 'lvl'
    """
    tree_dicts[lvl][new] = None  # Placeholder for predecessor
    if lvl > 0:
        # Of all possible predecessors, take oldest that is smaller than new entry
        for pre_opt in tree_dicts[lvl-1].keys():
            if pre_opt < new:
                tree_dicts[lvl][new] = (new_ix, pre_opt)
                break
    else:
        tree_dicts[lvl][new] = (new_ix, None)


def get_path_from_tree(tree_dicts: [dict]):
    # seq = [-1] * len(tree_dicts)
    ix_seq = [-1] * len(tree_dicts)
    pre_key = list(tree_dicts[-1].keys())[0]  # Last element in seq: First entry with max_len sequence

    for i, entries in enumerate(reversed(tree_dicts)):
        # print(f"{pre_key=}")
        lvl = len(tree_dicts) - i - 1
        # print(lvl, entries)
        # seq[lvl] = pre_key
        entry_ix = entries[pre_key][0]

        ix_seq[lvl] = entry_ix

        pre_key = entries[pre_key][1]  # Key for lower layer is the entry of current layer key

    return ix_seq


def find_lis(seq):
    min_ends = []  # Stores the smallest end for a subsequence of a length at that index
    indices = []  # Stores the corresponding index
    tree_dicts = []  # Stores the predecessor and index of a newly added element

    for i, num in enumerate(seq):
        # if next element is larger than smallest ending of longest subsequence: append
        # New longest subsequence
        if len(min_ends) == 0 or num > min_ends[-1]:
            min_ends.append(num)
            indices.append(i)
            tree_dicts.append({})

            k = len(min_ends) - 1
            enter_predecessor(tree_dicts, lvl=k, new=num, new_ix=i)

        elif num < min_ends[-1]:
            # Insert a smaller than the last number into the sorted list
            # of last elements, where it could replace a higher value for
            # that subsequence length (greedy, might be beneficial in future)
            k = find_first_greater(min_ends, num)
            if k is None:
                continue

            min_ends[k] = num
            indices[k] = i
            enter_predecessor(tree_dicts, k, num, new_ix=i)

    return get_path_from_tree(tree_dicts)


if __name__ == '__main__':
    n_cases = int(input())
    for av in range(n_cases):
        avenue = list(map(int, input().split(' ')))
        n_trees = avenue[0]
        lis_ics = find_lis(avenue[1:])

        # Avenue is perfect, cut none
        if len(lis_ics) == n_trees:
            print("none")
            continue

        # Print list of trees to cut
        for tree_ix in range(n_trees):
            if tree_ix not in lis_ics:
                print(f"{tree_ix + 1} ", end='')
        print()
