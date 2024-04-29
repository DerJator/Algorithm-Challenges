import numpy as np
import math

if __name__ == '__main__':
    # Test values, need parsing
    N, S, L, R, X = 3, 1, 1, 1, 3
    N_in = [23, 42, 0]

    N, S, L, R, X = [4, 10, 2, 1, 9]
    N_in = [1, 2, 3, 4]

    N, S, L, R, X = 5, 999999999, 3, 8, 7
    N_in = [8, 7, 8, 7, 12]

    M = math.log(np.power(10, X), np.max(N_in))
    M = np.round(M)

    print(f"{M=}")

    a_mat = np.zeros((N, N))
    # First row
    a_mat[0, N-1] = L
    a_mat[0, 0] = 1
    a_mat[0, 1] = R

    # in-between rows
    for i in range(1, N - 1):
        print(f"{i=}")
        a_mat[i, (i-1):(i+2)] = [L, 1, R]

    # Last row
    a_mat[N-1, N-2] = L
    a_mat[N-1, N-1] = 1
    a_mat[N-1, 0] = R

    print(a_mat)

    """ Eigendecomposition """

    eigvals, eigvecs = np.linalg.eig(a_mat)
    print(eigvals)
    print(eigvecs)