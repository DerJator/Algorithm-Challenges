def trees_to_cut(nums):
    n = len(nums)
    if n == 0:
        return []

    lengths = [1] * n
    predecessors = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j] and lengths[i] < lengths[j] + 1:
                lengths[i] = lengths[j] + 1
                predecessors[i] = j

    max_length = max(lengths)
    max_ix = lengths.index(max_length)

    longest_subseq = []
    while max_ix != -1:
        longest_subseq.append(max_ix)
        max_ix = predecessors[max_ix]

    longest_subseq.reverse()

    indices_to_remove = [i+1 for i in range(n) if i not in longest_subseq]
    return indices_to_remove


if __name__ == '__main__':
    n_cases = int(input())

    for i in range(n_cases):
        line = input()
        in_seq = line.split(" ")
        vals = [int(x) for x in in_seq]

        # Do this
        solution = trees_to_cut(vals[1:])
        s_len = len(solution)

        if s_len == 0:
            print("none")
        else:
            for i in range(s_len -1):
                print(str(solution[i]) + " " , end = "")
            print(solution[s_len-1])
