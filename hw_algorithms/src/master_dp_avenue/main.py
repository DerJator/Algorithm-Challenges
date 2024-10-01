# import math
import random
#
#
#
# def solve(n,trees,pd,index):
#     if index == n-1:
#         pd[index] = set()
#         return pd[index]
#     current_tree = trees[index]
#     #nicht faellen
#     fallen = set()
#     for i in range(n-1,index,-1):
#     #for i in range(index +1 ,n):
#         if pd[i] == None:
#             pd[i] = solve(n, trees, pd, i)
#
#         if trees[i] > current_tree:
#             fallen.update(k for k in pd[i] if trees[k - 1] >= current_tree)
#         else:
#             fallen.add(i + 1)
#     #faellen
#     if pd[index+1] == None:
#         pd[index+1] = solve(n,trees,pd,index+1)
#
#     #temp = {index+1}.union(pd[index+1])
#     temp = {index + 1} | pd[index + 1]
#     if len(temp) < len(fallen):
#         pd[index] = temp
#     else:
#         pd[index] = fallen
#     return pd[index]
#

def find_indices_to_remove(nums):
    n = len(nums)
    if n == 0:
        return []

    # lengths[i] speichert die Länge der längsten aufsteigenden Teilfolge bis Index i
    lengths = [1] * n

    # predecessors[i] speichert den Index des Vorgängers von nums[i] in der längsten Teilfolge
    predecessors = [-1] * n

    # Durchlaufe die Liste, um die Längen der längsten aufsteigenden Teilfolgen zu finden
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j] and lengths[i] < lengths[j] + 1:
                lengths[i] = lengths[j] + 1
                predecessors[i] = j

    # Finde die Länge der längsten Teilfolge und den Endindex
    max_length = max(lengths)
    max_index = lengths.index(max_length)

    # Rekonstruiere die längste aufsteigende Teilfolge
    longest_subsequence = []
    while max_index != -1:
        longest_subsequence.append(max_index)
        max_index = predecessors[max_index]

    longest_subsequence.reverse()

    # Bestimme die Indizes der Zahlen, die entfernt werden müssen
    indices_to_remove = [i+1 for i in range(n) if i not in longest_subsequence]
    return indices_to_remove


if __name__ == '__main__':
    testcases = int(input())
    for i in range(testcases):
        line = input()
        components = line.split(" ")
        temp = [int(x) for x in components]
        solution = find_indices_to_remove(temp[1:])
        s_len = len(solution)
        if s_len == 0:
            print("none")
        else:
            for i in range(s_len -1):
                print(str(solution[i]) + " " , end = "")
            print(solution[s_len-1])

    # print(list(solve(10,[10,10,9,8,7,6,5,4,3,2,1][1:],[None for i in range(10)],0)))
    # print(solve(10,[10,1,2,3,4,5,6,7,8,9,10][1:],[None for i in range(10)],1))
    # print(solve(7,[7,1,2,3,3,4,5,6][1:],[None for i in range(7)],0))
    # print(solve(7, [7,1,2,3,4,3,5,6][1:], [None for i in range(7)], 0))
    # print(solve(7, [7,6,5,3,4,3,2,1][1:], [None for i in range(7)], 0))
    # print(solve(5, [5,4711,4711,4711,4711,4711][1:], [None for i in range(5)], 0))


    # test = [1000]
    # for i in range(1000):
    #     test.append(random.randint(0,100000))
    # #print(test)
    # maha = solve(test[0],test[1:],[None for i in range(len(test))], 0)
    # print(maha)
    #
    # haha = [13,37,15,49,33,83,7,53,49,39,37,24,13,93]
    # maha = solve(len(haha),haha,[None for i in range(len(haha))], 0)
    # #maha.sort()
    # print(maha)







