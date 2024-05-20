alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']


def schnipsel(doc):
    schnipsels = set()
    for i in range(len(doc) - m + 1):
        schnipsels.add(doc[i:i + m])

    schnipsels = sorted(schnipsels)

    return schnipsels


def int_to_schnipsel(n, k, m):
    result = []

    while n > 0:
        remainder = n % k
        result.append(alphabet[remainder])
        n = n // k

    missing = m - len(result)
    result.append(('a' * missing))

    return ''.join(result[::-1])


if __name__ == '__main__':

    n_cases = int(input().strip())

    for case in range(n_cases):
        # n: doc length, m: max query length, k: letters 1..k
        n, m, k = map(int, input().strip().split(' '))
        doc_string = input().strip()

        doc_schnipsel = schnipsel(doc_string)

        for i in range(k**m):
            perm = int_to_schnipsel(i, k, m)
            if i >= len(doc_schnipsel):
                print(perm)
                break
            if doc_schnipsel[i] != perm:
                print(perm)
                break
