import math
from functools import reduce


def gcd_of_list(numbers):
    if not numbers:
        return None  # or raise an exception if you prefer
    return reduce(math.gcd, numbers)


if __name__ == '__main__':
    n_cases = int(input())

    for t in range(n_cases):
        serial = int(input())
        cache = []
        tens = []

        for c in range(serial):
            a = list(map(int, input().split(' ')))
            summ = 0
            for i in range(9):
                summ += a[i]
            summ -= a[9]
            summ = abs(summ)
            cache.append(summ)
            tens.append(a[9])

        N = gcd_of_list(cache)

        passed = True
        for a10 in tens:
            if a10 >= N:
                print("impossible")
                passed = False
                break

        if passed:
            print(N)

