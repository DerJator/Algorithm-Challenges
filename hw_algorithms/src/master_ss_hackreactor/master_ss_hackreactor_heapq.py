import heapq
from heapq import *

class MedianTracker:

    def __init__(self):
        self.mins = []
        self.maxs = []
        self.in_stream = []
        self.min_len = 0
        self.max_len = 0

    def add_number(self, v: int,):
        """ To mins add negative value, so that maximum is easier to access """
        heappush(self.in_stream, v)

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
        print(self.mins, self.maxs)
        if len(self.mins) > len(self.maxs):
            return -self.mins[0]
        elif len(self.maxs) > len(self.mins):
            return self.maxs[0]
        else:
            return -self.mins[0], self.maxs[0]

    def integrate_stream(self):
        """ The lower half of the stream is put into mins, the bigger half is put into maxs """
        if len(self.mins) < len(self.maxs):
            n_lower = len(self.in_stream) // 2 + 1  # put 1 element more in the mins to compensate
        else:
            n_lower = len(self.in_stream) // 2

        for i in range(n_lower):
            v = heappop(self.in_stream)  # get the next smallest element to put it in mins
            heappush(self.mins, -v)

        for i in range(len(self.in_stream)):
            v = heappop(self.in_stream)  # get the next smallest elements of the higher half
            heappush(self.maxs, v)



if __name__ == '__main__':
    n_cmds = int(input())
    tracker = MedianTracker()

    for n in range(n_cmds):
        line = input().strip().split(' ')
        # print(f"{line=}")
        if len(line) == 2: # R num
            tracker.add_number(int(line[1]))
        elif len(line) == 1: # W
            tracker.integrate_stream()
            median = tracker.get_median()
            if type(median) == int:
                print(median)
            else:
                print(*median)
        else:
            print("This shouldn't happen!")

        print(tracker.in_stream)
        print("mins", tracker.mins)
        print("maxs", tracker.maxs)

