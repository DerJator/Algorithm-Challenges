def hopcroft_karp(graph, n, m):
    assert (n == len(graph))
    match1 = [-1] * n
    match2 = [-1] * m

    for node in range(n):
        for neigh in graph[node]:
            if match2[neigh] == -1:
                match1[node] = neigh
                match2[neigh] = node
                break
    while True:
        bfs = [node for node in range(n) if match1[node] == -1]
        depth = [-1] * n
        for node in bfs:
            depth[node] = 0

        for node in bfs:
            for neigh in graph[node]:
                next_node = match2[neigh]
                if next_node == -1:
                    break
                if depth[next_node] == -1:
                    depth[next_node] = depth[node] + 1
                    bfs.append(next_node)
            else:
                continue
            break
        else:
            break

        pointer = [len(c) for c in graph]
        dfs = [node for node in range(n) if depth[node] == 0]
        while dfs:
            node = dfs[-1]
            while pointer[node]:
                pointer[node] -= 1
                neigh = graph[node][pointer[node]]
                next_node = match2[neigh]
                if next_node == -1:
                    # Augmenting path found
                    while neigh != -1:
                        node = dfs.pop()
                        match2[neigh], match1[node], neigh = node, neigh, match1[node]
                    break
                elif depth[node] + 1 == depth[next_node]:
                    dfs.append(next_node)
                    break
            else:
                dfs.pop()
    return match1, match2


def get_index(item, list):
    for i in range(len(list)):
        if list[i] == item:
            return i
    return -1


def get_neighbours(i, j, height, width, schweden):
    ret = []
    # i -1 , j
    if i > 0 and schweden[i-1][j] == 1:
        ret.append((i-1, j))
    # i , j +1
    if j < width - 1 and schweden[i][j+1] == 1:
        ret.append((i, j+1))
    # i +1 ,j
    if i < height - 1 and schweden[i+1][j] == 1:
        ret.append((i+1, j))
    # i , j - 1
    if j > 0 and schweden[i][j-1] == 1:
        ret.append((i, j-1))
    return ret


if __name__ == '__main__':

    scenarios = int(input())

    for _ in range(scenarios):
        temp = input().split(' ')
        height, width = int(temp[0]), int(temp[1])

        schweden = []
        u = []
        v = []
        len_u = 0
        len_v = 0
        amount = 0

        for i in range(height):
            line = input()

            schweden.append([1 if j == '*' else 0 for j in line])

        for i in range(height):
            if i % 2 == 0:
                begin = 0
            else:
                begin = 1
                if schweden[i][0]:
                    amount += 1
                    temp_two = i * width
                    if not v.__contains__(temp_two):
                        neighbours = get_neighbours(i, 0, height, width, schweden)
                        if len(neighbours) == 0:
                            v.append(temp_two)
                            len_v += 1
            for j in range(begin, width, 2):
                if schweden[i][j] == 1:
                    amount += 1
                    index = i * width + j
                    u.append([])

                    neighbours = get_neighbours(i, j, height, width, schweden)
                    for row, col in neighbours:
                        neighbour_index = row * width + col
                        if v.__contains__(neighbour_index):
                            edge = get_index(neighbour_index, v)
                            u[-1].append(edge)
                        else:
                            v.append(neighbour_index)
                            len_v += 1
                            u[-1].append(len_v-1)


                if j+1 < width:
                    if schweden[i][j + 1]:
                        amount += 1
                        temp_three = i * width + j + 1
                        if not v.__contains__(temp_three):
                            neighbours = get_neighbours(i, j+1, height, width, schweden)
                            if len(neighbours) == 0:
                                v.append(temp_three)
                                len_v += 1

        match1, match2 = hopcroft_karp(u, len(u), len(v))
        lonley_1 = match1.count(-1)
        lonley2 = match2.count(-1)
        sum = lonley_1 + lonley2

        print(sum + (amount-sum) // 2)
