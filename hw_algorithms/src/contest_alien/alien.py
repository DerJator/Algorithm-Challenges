from collections import defaultdict

class UnionFind:
    def __init__(self, N):
        self.rank = [0] * N
        self.p = [i for i in range(N)]

    def find_set(self, i):
        if self.p[i] == i:
            return i
        else:
            self.p[i] = self.find_set(self.p[i])
            return self.p[i]

    def is_same_set(self, i, j):
        return self.find_set(i) == self.find_set(j)

    def union_set(self, i, j):
        if not self.is_same_set(i, j):
            x = self.find_set(i)
            y = self.find_set(j)
            if self.rank[x] > self.rank[y]:
                self.p[y] = x
            else:
                self.p[x] = y
                if self.rank[x] == self.rank[y]:
                    self.rank[y] += 1



if __name__ == '__main__':
    n, n_fs = map(int, input().split(' '))
    uf = UnionFind(n)

    for fs_edge in range(n_fs):
        x_i, x_j = map(int, input().split(' '))
        uf.union_set(x_i - 1, x_j - 1)

    p_list = uf.p
    # print(p_list)

    hist = dict()

    for x in p_list:
        final_p = uf.find_set(x)
        if final_p in hist:
            hist[final_p] += 1
        else:
            hist[final_p] = 1

    # print(uf.p)
    # print(hist)
    print(max(hist.values()))
    # final_p = [uf.find_set(x) for x in p_list]

    #final_p.count()
