import numpy as np
import sys

def fast_exp(A, n: int, thresh: int):
    """ Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh. """
    a_dim = A.shape[0]
    if n == 0:
        return np.identity(a_dim, dtype=int)
    res = fast_exp(A, int(n/2), thresh) % (10 ** thresh)
    R = np.dot(res, res)
    if n % 2 == 1:
        return np.dot(R, A)
    return R

def parse_txt(input: str):
    lines = input.split('\n')
    no_samples = eval(lines.pop(0))
    params = np.zeros((no_samples, 5), dtype=int)
    numbers = []

    for i in range(no_samples):
        params[i] = [eval(s) for s in lines.pop(0).split(" ")]
        n_vals = [eval(s) for s in lines.pop(0).split(" ")]
        print(lines.pop(0))

        numbers.append(n_vals)


    return no_samples, params, numbers


if __name__ == '__main__':
    #input_string = sys.argv[1]
    with open("1.in", "r") as f:
        no_samples, params, vals = parse_txt(f.read())

    for j in range(no_samples):
        N, S, L, R, X = params[j]
        N_in = vals[j]
        # print(f"{N=}, {S=}, {L=}, {R=}, {X=}")
        # print(f"{N_in=}")

        """ Build matrix """
        a_mat = np.zeros((N, N), dtype=int)

        # First row
        a_mat[0, N-1] = L
        a_mat[0, 0] = 1
        a_mat[0, 1] = R

        # in-between rows
        for i in range(1, N - 1):
            a_mat[i, (i-1):(i+2)] = [L, 1, R]

        # Last row
        a_mat[N-1, N-2] = L
        a_mat[N-1, N-1] = 1
        a_mat[N-1, 0] = R

        """ The calculation """

        run_N = np.array(N_in, dtype=int)
        run_N = fast_exp(a_mat, S, X) @ run_N

        with open("1.ans", "a") as file:
            file.write(' '.join(map(str, run_N % (10 ** X))))
            if not j == no_samples - 1:
                file.write("\n")