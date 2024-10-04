# Python program to find strongly connected components in a given
# directed graph using Tarjan's algorithm (single DFS)
# Complexity : O(V+E)

from collections import defaultdict


# This class represents an directed graph
# using adjacency list representation


class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

        self.Time = 0

        self.sccs = [0] * vertices
        self.curr_scc_id = 0

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    def SCCUtil(self, u, low, disc, stackMember, st):

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)

        # Go through all vertices adjacent to this
        for v in self.graph[u]:

            # If v is not visited yet, then recur for it
            if disc[v] == -1:

                self.SCCUtil(v, low, disc, stackMember, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)
                low[u] = min(low[u], low[v])

            elif stackMember[v] == True:
                low[u] = min(low[u], disc[v])

        # head node found, pop the stack and print an SCC
        w = -1  # To store stack extracted vertices

        if low[u] == disc[u]:
            self.curr_scc_id += 1
            curr_scc_id = self.curr_scc_id
            while w != u:
                w = st.pop()
                # print(w, end=" ")
                self.sccs[w] = curr_scc_id
                stackMember[w] = False


    def SCC(self):
        disc = [-1] * (self.V)
        low = [-1] * (self.V)
        stackMember = [False] * (self.V)
        st = []

        for i in range(self.V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)


def str_to_int(s):
    res = 0
    for c in s:
        res = res * 26 + ord(c) - ord("A")
    return res


def main():
    num_tc = int(input())
    for _ in range(num_tc):
        junctions, roads = map(int, input().split())
        g = Graph(junctions)
        for _ in range(roads):
            u, v = map(str_to_int, input().split("=>"))
            # print("adding edge from ", u, " to ", v)
            g.addEdge(u, v)
        g.SCC()
        # print(g.sccs)

        while True:
            try:
                u, v = map(str_to_int, input().split("<=>"))
            except ValueError:
                break
            except EOFError:
                break

            if g.sccs[u] == g.sccs[v]:
                print("Car is OK")
            else:
                print("Footwalking")


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(5000)
    main()

