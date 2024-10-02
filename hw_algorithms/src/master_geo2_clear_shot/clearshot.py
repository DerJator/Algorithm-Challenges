from collections import defaultdict
import heapq
import math

class ClearShot:
    def __init__(self, line_start, line_end, line_y, obst_starts, obst_ends):
        self.line_start = line_start
        self.line_end = line_end
        self.line_y = line_y
        self.min_angle = math.asin(line_y / math.sqrt(line_start**2 + line_y**2))
        if line_start > 0:
            self.min_angle = math.pi - self.min_angle
        self.max_angle = math.asin(line_y / math.sqrt(line_end**2 + line_y**2))
        if line_end > 0:
            self.max_angle = math.pi - self.max_angle
        #print(f"{self.min_angle=} {self.max_angle=}")

        self.obst_starts = sorted(obst_starts)  # SORT: O(n logn)
        self.obst_ends = sorted(obst_ends)  # SORT: O(n logn)
        self.active_obstacles = 0
        self.viewpoints = [-1, -1]  # ?
        self.clear_shots = []
        self.viewing = False

        # heapq.heapify(self.clear_shots)  # Maybe too slow, I don't know

    def obst_start(self, angle):
        if self.viewing and angle >= self.min_angle:
            self.viewpoints[1] = angle
            self.calc_view()
        self.active_obstacles += 1
        self.viewing = False

    def obst_end(self, angle):
        self.active_obstacles -= 1
        #print(self.active_obstacles, angle, self.min_angle)
        if self.active_obstacles == 0 and angle >= self.min_angle:
            self.viewing = True
            self.viewpoints[0] = angle

    def clear_start(self):
        pass

    def clear_end(self):
        pass

    def calc_view(self):
        #print(f"Calculating viewpoints from {360 * self.viewpoints[0] / (2*math.pi)} to {360 * self.viewpoints[1] / (2*math.pi)}")
        # if self.viewpoints[0] < math.pi / 2 and self.viewpoints[1] < math.pi / 2:
        #
        #     p1 = self.line_y * math.atan(math.pi / 2 - self.viewpoints[0])
        #     p2 = self.line_y * math.atan(math.pi / 2 - self.viewpoints[1])
        #     self.clear_shots.append(p2-p1)

        # theta = asin(y/d)

        x1 = self.line_y / math.tan(self.viewpoints[0])
        # x1 = -x1 if self.viewpoints[0] <= math.pi / 2 else x1  # Left of origin
        x2 = self.line_y / math.tan(self.viewpoints[1])
        # x2 = -x2 if self.viewpoints[1] <= math.pi / 2 else x2  # Left of origin
        #print(f"{x1=}, {x2=}")

        self.clear_shots.append(abs(x2 - x1))
        #print(f"{self.clear_shots=}")

    def shot_analysis(self):
        track_angles = [self.min_angle, self.max_angle]
        o_a_ix, o_b_ix = 0, 0
        finished = False

        while not finished:
            next_options = [self.obst_starts[o_a_ix], self.obst_ends[o_b_ix], *track_angles]
            #print(f"{next_options=}")
            next_event = min(next_options)
            #print(f"{next_event=}")

            if next_event == self.obst_starts[o_a_ix]:
                #print("Object starts")
                self.active_obstacles += 1
                self.obst_start(next_event)
                o_a_ix += 1
            elif next_event == self.obst_ends[o_b_ix]:
                #print("Object ends")
                self.active_obstacles -= 1
                self.obst_end(next_event)
                o_b_ix += 1
            elif next_event == self.min_angle:
                #print("Minimum angle")
                if self.active_obstacles == 0:
                    self.viewpoints[0] = self.min_angle
                track_angles.pop(0)
            elif next_event == self.max_angle:
                #print("Maximum angle")
                finished = True
                if self.viewing:
                    self.viewpoints[1] = self.max_angle
                    self.calc_view()
                track_angles.pop(0)

        if len(self.clear_shots) == 0 or max(self.clear_shots) < 1e-4:
            return "IMPOSSIBLE"
        else:
            return max(self.clear_shots)


if __name__ == '__main__':
    n_cases = int(input())

    for i in range(n_cases):
        #print("\n\n########\n\n")
        x_a, x_b, y = map(int, input().split(' '))
        #print(f"{x_a=}, {x_b=}, {y=}")
        n_obst = int(input())
        obst_starts = []
        obst_ends = []

        for ob in range(n_obst):
            x_o, y_o, r = map(int, input().split(' '))

            if y_o - r >= y:
                continue
            #print(f"{x_o=}, {y_o=}, {r=}")
            d = math.sqrt(x_o**2 + y_o**2)
            theta = math.asin(y_o / d)

            if x_o > 0:  # if on right side, flip theta
                theta = math.pi - theta

            phi = math.asin(r / d)
            alpha = theta - phi
            beta = theta + phi
            obst_starts.append(alpha)
            obst_ends.append(beta)

        obst_starts.append(math.inf)
        obst_ends.append(math.inf)

        #print(f"{obst_starts=}")
        #print(f"{obst_ends=}")
        shot_obj = ClearShot(x_a, x_b, y, obst_starts, obst_ends)
        result = shot_obj.shot_analysis()
        print(result)
