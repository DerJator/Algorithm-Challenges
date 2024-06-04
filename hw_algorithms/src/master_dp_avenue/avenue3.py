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


def find_lis(seq):
    min_ends = []  # Stores the smallest end for a subsequence of a length at that index
    indices = []  # Stores the corresponding index
    indices_cache = None

    for i in range(len(seq)):
        # if next element is larger than smallest ending of longest subsequence: append
        if len(min_ends) == 0 or seq[i] > min_ends[-1]:
            min_ends.append(seq[i])
            indices.append(i)
            # Cache new longest subsequence, because indices can get blended
            indices_cache = indices.copy()
        elif seq[i] < min_ends[-1]:
            # Insert a smaller than the last number into the sorted list
            # of last elements, where it could replace a higher value for
            # that subsequence length (greedy, might be beneficial in future)
            k = find_first_greater(min_ends, seq[i])
            if k is None:
                continue

            min_ends[k] = seq[i]
            indices[k] = i

    return indices_cache

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
