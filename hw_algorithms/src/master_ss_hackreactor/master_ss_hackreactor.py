from collections import deque

class MedianTracker:

    def __init__(self):
        self.mins = []
        self.maxs = []
        self.min_len = 0
        self.max_len = 0

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
        if len(self.mins) == 0 and len(self.maxs) == 0:
            self.mins.append(v)
        elif len(self.maxs) > 0:
            if v > self.maxs[0]:
                self.binary_insert(v, self.maxs)
            else:
                self.binary_insert(v, self.mins)
        elif len(self.mins) > 0:
            if v <= self.mins[len(self.mins) - 1]:
                self.binary_insert(v, self.mins)
            else:
                self.binary_insert(v, self.maxs)

        # Balance the lists
        if len(self.maxs) > len(self.mins):
            x = self.maxs.pop(0)
            self.mins.append(x)
        elif len(self.mins) > len(self.maxs):
            x = self.mins.pop()
            self.maxs.insert(0, x)

        # print(f"{self.mins=}, {self.maxs=}")

    def get_median(self):
        if len(self.mins) > len(self.maxs):
            return self.mins[len(self.mins) - 1]
        elif len(self.maxs) > len(self.mins):
            return self.maxs[0]
        else:
            return self.mins[len(self.mins) - 1], self.maxs[0]

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

