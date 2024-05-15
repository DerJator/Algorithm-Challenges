if __name__ == '__main__':
    opts = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    n, a, b, c, d = map(int, input().split(' '))

    if n > 2:
        n_cubes = n ** 3 - (n-2) ** 3
    else:
        n_cubes = n ** 3

    for i, val in enumerate([a, b, c, d]):
        if val == n_cubes:
            print(opts[i])
            break
