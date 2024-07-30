def extract_triplets(sequence):
    return [sequence[i:i+3] for i in range(0, len(sequence), 3)]


def neighb_options(alignment, i, j, aa1, aa2, w_match, w_mism, w_gap):

    if aa1 == aa2:
        opt_mis_match = alignment[i-1][j-1] + w_match
    else:
        opt_mis_match = alignment[i-1][j-1] + w_mism

    opt_gap_1 = alignment[i-1][j] + w_gap
    opt_gap_2 = alignment[i][j-1] + w_gap

    # print(f"Check {aa1}({i}) vs. {aa2}({j})")
    # print(fr"\{opt_mis_match}, <{opt_gap_1}, ^{opt_gap_2}")

    return opt_mis_match, opt_gap_1, opt_gap_2


def smith_waterman(seq1: str, seq2: str, w_match, w_mism, w_gap):
    alignment = [[0 for _ in range(len(seq2))] for _ in range(len(seq1))]

    for i1, aa1 in enumerate(seq1):
        for i2, aa2 in enumerate(seq2):
            if i1 == 0 and i2 == 0:
                alignment[i1][i2] = w_match if aa1 == aa2 else w_mism
            elif i1 == 0:
                alignment[i1][i2] += alignment[i1][i2-1] + w_gap
            elif i2 == 0:
                alignment[i1][i2] += alignment[i1-1][i2] + w_gap
            else:
                alignment[i1][i2] = max(neighb_options(alignment, i1, i2, aa1, aa2, w_match, w_mism, w_gap))

    return alignment[i1][i2]


def edit_distance_ukkonen(s1, s2, w_match, w_mismatch, w_gap):
    len1, len2 = len(s1), len(s2)
    if len1 < len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    # Initialize
    max_dist = len1 + len2
    current_row = [j * w_gap for j in range(len2 + 1)]

    # Iterate over increasing distances
    # iteration ranges anpassen. wenn i o. j == 0:
    # opt_left ausrechnen mit opt_left = i * gap (j==0)
    # opt_up ausrechnen mit opt_up = j * gap (i==0)
    # Iteration range dann für i range(len1), für j range(max(0, i - k), min(len2, i + k) + 1)
    for k in range(1, max_dist + 1):
        prev_row, current_row = current_row, [max_dist * w_gap] * (len2 + 1)
        print(f"{k=}, {current_row=}, {prev_row=}")
        for i in range(1, len1 + 1): # First row already initialized
            print(f"{current_row=}, {prev_row=}")
            for j in range(max(0, i - k), min(len2, i + k) + 1):
                #if i == 0:
                    # current_row[j] = j * gap
                if j == 0:
                    current_row[j] = i * w_gap
                else:
                    mm_cost = w_match if s1[i - 1] == s2[j - 1] else w_mismatch
                    current_row[j] = max(
                        up := prev_row[j] + w_gap,    # Deletion
                        left := current_row[j - 1] + w_gap,  # Insertion
                        diag := prev_row[j - 1] + mm_cost  # Substitution or Match
                    )
                    print(f"({j}): {up=}, {left=}, {diag=}")
            print(f"({i}, :), {current_row=}")
            prev_row, current_row = current_row, prev_row
        # Terminate if threshold is small enough
        if current_row[len2] <= k * max(w_gap, mismatch):
            return current_row[len2]
    return max_dist * w_gap


if __name__ == '__main__':
    while True:
        try:
            match, mismatch, gap = map(int, input().split(' '))
            protein1 = input()
            protein2 = input()
        except EOFError:
            break

        s1 = extract_triplets(protein1)
        s2 = extract_triplets(protein2)
        # print(smith_waterman(s2, s1, match, mismatch, gap))
        print(edit_distance_ukkonen(s1, s2, match, mismatch, gap))
