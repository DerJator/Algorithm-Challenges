import heapq
from heapq import *

class MedianTracker:

    def __init__(self):
        self.mins = []
        self.maxs = []
        heapify(self.mins)
        heapify(self.maxs)

    def binary_insert(self, val: int, division: list):
        left, right = 0, len(division) - 1

        while left <= right:
            mid = (left + right) // 2
            if division[mid] == val:
                division.insert(mid, val)
                return
            elif division[mid] < val:
                left = mid + 1
            elif division[mid] > val:
                right = mid - 1

        division.insert(left, val)

    def add_number(self, v: int,):
        """ To mins add negative value, so that maximum is easier to access """
        if len(self.mins) == 0 and len(self.maxs) == 0:
            heappush(self.mins, -v)
        elif len(self.mins) == 0 and len(self.maxs) > 0:
            if v >= self.maxs[0]:
                heappush(self.maxs, v)
            else:
                heappush(self.mins, -v)
        else:
            if v <= -self.mins[0]:
                heappush(self.mins, -v)
            else:
                heappush(self.maxs, v)

        # Balance the lists
        if len(self.maxs) > len(self.mins):
            x = heappop(self.maxs)
            heappush(self.mins, -x)
        elif len(self.mins) > len(self.maxs):
            x = -heappop(self.mins)
            heappush(self.maxs, x)

        # print(f"{self.mins=}, {self.maxs=}")

    def get_median(self):
        if len(self.mins) > len(self.maxs):
            return -self.mins[0]
        elif len(self.maxs) > len(self.mins):
            return self.maxs[0]
        else:
            return -self.mins[0], self.maxs[0]

if __name__ == '__main__':
    n_cmds = int(input())
    tracker = MedianTracker()

    for n in range(n_cmds):
        line = input().strip().split(' ')
        # print(f'{line=}')
        if len(line) == 2:
            tracker.add_number(int(line[1]))
        elif len(line) == 1:
            median = tracker.get_median()
            if type(median) == int:
                print(median)
            else:
                print(*median)
        else:
            print("This shouldn't happen!")

