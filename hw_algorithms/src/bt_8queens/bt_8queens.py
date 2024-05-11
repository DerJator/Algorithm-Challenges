def read_input():
    i_q, j_q = input().strip().split(' ')
    try:
        input()
    except EOFError:
        pass
    i_q, j_q = [int(i_q), int(j_q)]

    return i_q, j_q


def solve(i_q, j_q, n_q=8):
    correct_ix = i_q - 1
    correct_jx = j_q - 1

    # With 1 existing pos
    columns = [-1 if i != correct_ix else correct_jx for i in range(n_q)]
    pos_diag = {correct_ix + correct_jx}
    neg_diag = {correct_ix - correct_jx}

    # Without 1 existing pos
    # columns = set()
    # pos_diag = set()
    # neg_diag = set()

    res = []

    def backtrack(row):
        # print(columns, pos_diag, neg_diag)
        # print(f"NEW BACKTRACK: {row=}, {columns=}, {pos_diag=}, {neg_diag=}")
        if row == correct_ix:
            res.append([c + 1 for c in columns])
            print(' '.join([str(c + 1) for c in columns]))
            return

        for col in range(n_q):
            # print(f"##{col=}")
            if col in columns:
                # print(f"\tCol {col} in {columns=}")
                continue
            elif (row + col) in pos_diag:
                # print(f"\t{row+col}(+) in {pos_diag}")
                continue
            elif (row - col) in neg_diag:
                # print(f"\t{row-col}(-) in {neg_diag}")
                continue

            columns[row] = col
            pos_diag.add(row + col)
            neg_diag.add(row - col)

            # print(f"\tr+c: {row+col}, r-c: {row-col}")

            # print(columns)
            backtrack((row + 1) % n_q)

            columns[row] = -1
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)

            # print(f"BACKTRACK'S BACK ({row+1}->{row}): {columns=}, {pos_diag=}, {neg_diag=}")

    backtrack((correct_ix + 1) % n_q)
    print()
    # print(res)

if __name__ == '__main__':
    n_samples = int(input())
    input()
    for n in range(n_samples):
        queen_pos = read_input()
        if queen_pos is not None:
            i_queen, j_queen = queen_pos
            solve(i_queen, j_queen, 8)

