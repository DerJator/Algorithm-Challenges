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
        print(smith_waterman(s2, s1, match, mismatch, gap))
