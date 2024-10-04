import heapq


def dijkstra(adj_list, start):
    dist = {node: float('inf') for node in adj_list}
    dist[start] = 0
    shortest_path_tree = {}

    queue = [(0, start)]

    while queue:
        # Pop smallest distance
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > dist[current_node]:
            continue

        # Explore neighbors and update distances if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return dist


def dijkstra_with_path(adj_list, start):
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0
    predecessors = {node: None for node in adj_list}

    # Priority queue to track num_nodes and current shortest distance
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if a shorter distance to current_node is already found
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors and update distances if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors


def shortest_path(predecessors, start, target):
    path = []
    while target is not None:
        path.append(target)
        target = predecessors[target]
    path.reverse()
    return path


def edge_list_to_adjacency_list(edge_list):
    adj_list = {}
    for (src, dest, weight) in edge_list:
        if src not in adj_list:
            adj_list[src] = {}
        if dest not in adj_list:
            adj_list[dest] = {}

        adj_list[src][dest] = weight
        adj_list[dest][src] = weight

    return adj_list


if __name__ == '__main__':
    num_tc = int(input())

    for _ in range(num_tc):
        input()
        num_places, num_streets = map(int, input().split(" "))
        edge_list = []
        for _ in range(num_streets):
            src, dest, weight = input().split(" ")
            edge_list.append((src, dest, int(weight)))

        home, party = input().split(" ")
        adj_list = edge_list_to_adjacency_list(edge_list)

        # shortest path from home to all other places
        home_shortest_distances, home_predecessors = dijkstra_with_path(adj_list, home)
        # print(home_shortest_distances)
        length_shortest_path = home_shortest_distances[party]
        # print(length_shortest_path)

        # get all num_nodes in the shortest path
        shortest_path_edges = shortest_path(home_predecessors, home, party)
        # print(shortest_path_edges)

        # try leaving each one of the edges of the shortest path out and do a new dijkstra
        min_length_start = 1000 * 1000 * 10
        min_length = min_length_start
        for i in range(len(shortest_path_edges) - 1):
            src = shortest_path_edges[i]
            dest = shortest_path_edges[i + 1]
            weight = adj_list[src][dest]
            adj_list[src].pop(dest)
            adj_list[dest].pop(src)
            new_shortest_distances = dijkstra(adj_list, home)
            min_length = min(min_length, new_shortest_distances[party])
            adj_list[src][dest] = weight
            adj_list[dest][src] = weight

        if min_length < min_length_start:
            # print("second shortest path:")
            print(length_shortest_path, min_length)
        else:
            print(length_shortest_path)
