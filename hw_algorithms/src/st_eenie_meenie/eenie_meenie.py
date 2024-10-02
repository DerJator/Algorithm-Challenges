if __name__ == '__main__':
    magic_number = int(input())
    for _ in range(magic_number):
        n, m, k = map(int, input().split())
        n_out = 0
        n_left = n
        current = 0
        k -= 1  # correct index

        while n_left > 0:
            next_out = (current + (m - 1)) % n_left
            current = next_out
            n_out += 1
            n_left -= 1
            if next_out < k:
                k -= 1
            elif next_out == k:
                print(n_out)
                break