import math


def min_bus_cost(bus_costs):
    n_cities = len(bus_costs)
    shortest_paths = [[math.inf] * n_cities for _ in range(n_cities)]

    for dest in range(1, n_cities):  # we don't need to get to 0
        path_options = [bus_costs[0][dest]]  # Find the shortest path
        # print(f"1->{dest+1}")
        for m in range(1, dest):
            # print(f"1->{m+1} + {m+1}->{dest+1}")
            path_options.append(bus_costs[0][m] + bus_costs[m][dest])

        shortest_paths[0][dest] = min(path_options)

    result = shortest_paths[0][n_cities - 1]
    if result == math.inf:
        print("IMPOSSIBLE")
    else:
        print(result)
        # print(f"Add 1->{dest+1}: {shortest_paths[0][dest]}")

if __name__ == '__main__':
    n_cases = int(input())

    for c in range(n_cases):
        n_cities = int(input())
        # print(f"{n_cities=}")
        bus_costs = [[math.inf for _ in range(n_cities)] for _ in range(n_cities)]
        for i in range(n_cities - 1):
            bus_lines_from_i = list(map(int, input().split()))
            min_cost = math.inf
            # print(f"{bus_lines_from_i=}")
            for j in range(len(bus_lines_from_i)-1, -1, -1):
                if bus_lines_from_i[j] > 0:
                    min_cost = min(min_cost, bus_lines_from_i[j])
                    bus_costs[i][j + i + 1] = min_cost
                else:
                    bus_costs[i][j + i + 1] = min_cost

                # print(f"{min_cost=} (min('', {bus_lines_from_i[j]}))")
        # print(f"{bus_costs=}")
        res = min_bus_cost(bus_costs)

