import heapq
from heapq import *

class MedianTracker:

    def __init__(self):
        self.mins = []
        self.maxs = []
        self.min_len = 0
        self.max_len = 0
        heapify(self.mins)
        heapify(self.maxs)


    # def binary_insert(self, val: int, division: list):
    #     left, right = 0, len(division) - 1
    #
    #     while left <= right:
    #         mid = (left + right) // 2
    #         if division[mid] == val:
    #             division.insert(mid, val)
    #             return
    #         elif division[mid] < val:
    #             left = mid + 1
    #         elif division[mid] > val:
    #             right = mid - 1
    #
    #     division.insert(left, val)

    def add_number(self, v: int,):
        """ To mins add negative value, so that maximum is easier to access """
        if self.min_len == 0 or v < -self.mins[0]:
            heappush(self.mins, -v)
            self.min_len += 1
        else:
            heappush(self.maxs, v)
            self.max_len += 1

        self.balance()

    def balance(self):
        # Balance the lists
        if self.max_len > self.min_len:
            x = heappop(self.maxs)
            self.max_len -= 1
            heappush(self.mins, -x)
            self.min_len += 1
        elif self.min_len > self.max_len:
            x = -heappop(self.mins)
            self.min_len -= 1
            heappush(self.maxs, x)
            self.max_len += 1

        # print(f"{self.mins=}, {self.maxs=}")

    def get_median(self):
        if self.min_len > self.max_len:
            return -self.mins[0]
        elif self.max_len > self.min_len:
            return self.maxs[0]
        else:
            return -self.mins[0], self.maxs[0]

if __name__ == '__main__':
    n_cmds = int(input())
    tracker = MedianTracker()

    for n in range(n_cmds):
        line = input().strip().split(' ')
        # print(f"{line=}")
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

