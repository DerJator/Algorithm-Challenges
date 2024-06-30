import re

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


def extract_coordinates(point_str):
    # Extract all integer numbers from the string
    coordinates = re.findall(r'\d+', point_str)
    # Convert them to integers
    return int(coordinates[0]), int(coordinates[1])


if __name__ == '__main__':
    m, n = map(int, input().split(' '))
    uf = UnionFind(m*n)

    while True:
        try:
            cmd, p1, p2 = input().split(' ')
            # transform into 1-dim index
            p1_x, p1_y = extract_coordinates(p1)
            p1_k = (p1_x - 1) * m + (p1_y - 1)
            p2_x, p2_y = extract_coordinates(p2)
            p2_k = (p2_x - 1) * m + (p2_y - 1)

            if cmd == "WIRE":
                uf.union_set(p1_k, p2_k)
            elif cmd == "CHECK":
                set1 = uf.find_set(p1_k)
                set2 = uf.find_set(p2_k)
                if set1 == set2:
                    print("FLOW")
                else:
                    print("NO FLOW")
        except EOFError:
            break
