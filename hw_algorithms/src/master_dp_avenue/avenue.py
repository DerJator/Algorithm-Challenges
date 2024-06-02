from bisect import bisect_right

def lis(a):
    n = len(a)
    inf = 1e9
    d = [inf] * (n + 1)
    d[0] = -inf
    ix = [-1] * (n + 1)

    for i in range(n):
        l = bisect_right(d, a[i])
        if d[l-1] < a[i] < d[l]:
            d[l] = a[i]
            ix[l] = i

    ans = 0
    for l in range(n + 1):
        if d[l] < inf:
            ans = l
    return ans, [i for i in ix if i >= 0]

# Example usage:

if __name__ == '__main__':
    n_cases = int(input())

    for case in range(n_cases):
        heights = list(map(int, input().split()))[1:]
        print(*lis(heights))
