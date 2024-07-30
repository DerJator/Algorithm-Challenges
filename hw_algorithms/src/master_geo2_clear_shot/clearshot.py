from collections import defaultdict
import heapq
import math

class ClearShot:
    def __init__(self, line_start, line_end, line_y, ):
        self.line_start = line_start
        self.line_end = line_end
        self.line_y = line_y
        self.min_angle =
        self.max_angle =

        self.active_obstacles = 0
        self.viewpoints = [-1, -1]
        self.clear_shots = []
        heapq.heapify(self.clear_shots)

    def obst_start(self, angle):
        if self.active_obstacles == 0 and self.viewpoints[1] >= 0:
            self.viewpoints[1] = angle
            self.calc_view()
        self.active_obstacles += 1

    def obst_end(self, angle):
        self.active_obstacles -= 1
        if self.active_obstacles == 0:
            self.viewpoints[0] = angle
    def clear_start(self):
        pass

    def calc_view(self):
        if self.viewpoints[0] < math.pi / 2 and self.viewpoints[1] < math.pi / 2:

            p1 = self.line_y * math.atan(math.pi / 2 - self.viewpoints[0])
            p2 = self.line_y * math.atan(math.pi / 2 - self.viewpoints[1])
            self.clear_shots.append(p2-p1)

if __name__ == '__main__':
    n_cases = int(input())

    for i in range(n_cases):
        x_a, x_b, y = map(int, input().split(' '))
        n_obst = int(input())
        obst_starts = []
        obst_ends = []

        for ob in range(n_obst):
            x_o, y_o, r = map(int, input().split(' '))
            d = math.sqrt(x_o**2 + y_o**2)
            theta = math.asin(y_o / d)

            if x_o > 0:  # if on right side, flip theta
                theta = math.pi - theta

            phi = math.asin(r / d)
            alpha = theta - phi
            beta = theta + phi
            obst_starts.append(alpha)
            obst_ends.append(beta)