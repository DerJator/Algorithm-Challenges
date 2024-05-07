import sys


class Identity:
    def __init__(self):
        self.value = True


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


def triband_multiply(dim, coeffs, M):
    new_M = [[0 for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            for k in range(0, 2+1):
                new_M[i][j] += coeffs[k] * M[i - 1 + k, j]

    return new_M


def identity_matrix(size):
    """ Generate identity matrix of given size. """
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def fast_exp(A, n: int, thresh: int, strip: bool = False):
    """ Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh. """
    # print(f"{n=}, {strip=}")
    if n == 0:
        return Identity()

    res = fast_exp(A, n // 2, thresh, not strip)

    if type(res) is not Identity:
        # print("No Identity")
        R = matrix_multiply(res, res)
    else:
        # print("Identity returned")
        R = A

    if n % 2 == 1 and n != 1:
       R = matrix_multiply(R, A)

    if strip:  # Only take thresh last digits to avoid huge numbers
        R = [[elem % 10 ** thresh for elem in row] for row in R]

    return R


def parse_txt():
    no_samples = int(input())
    params = []
    numbers = []

    for i in range(no_samples):
        param_values = [int(s) for s in input().split(" ")]
        params.append(param_values)
        n_vals = [int(s) for s in input().split(" ")]
        if i < no_samples - 1:
            _ = input()  # Pop the empty line

        numbers.append(n_vals)

    return no_samples, params, numbers


if __name__ == '__main__':
    # input_string = sys.argv[0]
    # with open("./1.in", "r") as f:
        # no_samples, params, vals = parse_txt(f.read())
    no_samples, params, vals = parse_txt()

    for j in range(no_samples):
        N, S, L, R, X = params[j]
        N_in = vals[j]
        # print(f"{N=}, {S=}, {L=}, {R=}, {X=}")
        # print(f"{N_in=}")

        """ Build matrix """
        a_mat = [[0] * N for _ in range(N)]  # Unnecessary, only redundancy
        matrix_coeffs = [L, 1, R]

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
        A_n = fast_exp(a_mat, S, thresh=X, strip=True)
        if type(A_n) is not Identity:
            run_N = matrix_multiply(A_n, run_N)

        [print(f"{elem % (10 ** X)} ", end="") for elem in run_N]
        print()
