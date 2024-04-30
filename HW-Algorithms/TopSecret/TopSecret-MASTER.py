import sys
import numpy as np


def mat_vec_mult(A, v):
    result = [0 for _ in range(len(A))]

    for i in range(len(A)):
        result[i] = sum([A[i][j] * v[j] for j in range(len(A[0]))])

    return result

def matrix_multiply(A, B):
    """ Multiply two matrices. """
    rows_A = len(A)
    cols_A = len(A[0])
    if not type(B[0]) == int:
        cols_B = len(B[0])
    else:
        return mat_vec_mult(A, B)

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


def identity_matrix(size):
    """ Generate identity matrix of given size. """
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def fast_exp(A, n: int, thresh: int):
    """ Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh. """
    if n == 0:
        return identity_matrix(len(A))

    res = fast_exp(A, n // 2, thresh)
    res = [[elem % (10 ** thresh) for elem in row] for row in res]  # Only take thresh last digits to avoid huge numbers
    R = matrix_multiply(res, res)

    if n % 2 == 1:
        R = matrix_multiply(R, A)

    return R

def parse_txt(input: str):
    lines = input.split('\n')
    no_samples = eval(lines.pop(0))
    params = []
    numbers = []

    for _ in range(no_samples):
        param_values = [int(s) for s in lines.pop(0).split(" ")]
        params.append(param_values)
        n_vals = [int(s) for s in lines.pop(0).split(" ")]
        _ = lines.pop(0)  # Pop the empty line

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
        a_mat = [[0] * N for _ in range(N)]

        # First row
        a_mat[0][N - 1] = L
        a_mat[0][0] = 1
        a_mat[0][1] = R

        # In-between rows
        for i in range(1, N - 1):
            a_mat[i][i - 1] = L
            a_mat[i][i] = 1
            a_mat[i][i + 1] = R

        # Last row
        a_mat[N - 1][N - 2] = L
        a_mat[N - 1][N - 1] = 1
        a_mat[N - 1][0] = R

        run_N = N_in[:]
        run_N = matrix_multiply(fast_exp(a_mat, S, X), run_N)

        with open("1.ans", "a") as file:
            file.write(' '.join(map(str, [elem % (10 ** X) for elem in run_N])))
            if not j == no_samples - 1:
                file.write("\n")