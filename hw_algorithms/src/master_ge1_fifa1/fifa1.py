# from matplotlib import pyplot as plt


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            # print(Vector3D(self.x * other, self.y * other, self.z * other))
            return Vector3D(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError(f"Multiplication with {type(other)} not implemented")


# def plot_opponents(opponents, positions, projections=None):
#     fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(widthx_field/10, heighty_field/10))
#     for opp in opponents:
#         height, width, x, y = opp
#         # axs.add_patch(plt.Rectangle((x, y), width, height, fill=False))
#         # plot opponents as horizontal lines inside of the football field
#         axs.hlines(y, x - width / 2, x + width / 2, color='red')
#
#     for pos in positions:
#         axs.plot(pos.x, pos.y, 'o', color='green')
#
#     if projections:
#         for proj in projections:
#             axs.plot(proj[0].x, proj[0].y, 'o', color='blue')
#             axs.plot(proj[1].x, proj[1].y, 'o', color='blue')
#     # plot goal
#     axs.hlines(105, widthx_field / 2 - goal_widthx / 2, widthx_field / 2 + goal_widthx / 2, color='blue')
#     axs.set_ylim([0, 105.2])
#     axs.set_xlim([0, 68])
#     plt.show()
#
# def plot_projections_in_goal(projections):
#     fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(widthx_field/10, 4))
#     # plot goal
#     axs.add_patch(plt.Rectangle((widthx_field / 2 - goal_widthx / 2, 0), goal_widthx, goal_heightz, fill=False, edgecolor='blue'))
#     for proj in projections:
#         # plot proj as rectangle
#         axs.add_patch(plt.Rectangle((proj[0].x, proj[0].z), proj[1].x - proj[0].x, proj[1].z - proj[0].z, alpha=0.2, fill=True, edgecolor='red'))
#     axs.set_ylim([0, 3])
#     axs.set_xlim([27, 40])
#     plt.show()
#
def projection(P: Vector3D, v: Vector3D):
    # k = Fraction(105 - P.y, v.y)
    k = (105 - P.y) / v.y
    return P + v * k


def projections_opponent(height, width, x_opp, y_opp, orig):
    p_lower_left = Vector3D(x_opp, y_opp, 0)
    p_upper_right = Vector3D(x_opp + width, y_opp, height)

    proj_ll = projection(orig, p_lower_left - orig)
    proj_ur = projection(orig, p_upper_right - orig)
    return proj_ll, proj_ur


widthx_field = 68
heighty_field = 105

goal_widthx = 7.32
goal_heightz = 2.44

goal_l = Vector3D(widthx_field / 2 - goal_widthx / 2, 0, 0)
goal_r = Vector3D(widthx_field / 2 + goal_widthx / 2, 0, 0)

goal_l_top = Vector3D(widthx_field / 2 - goal_widthx / 2, 0, goal_heightz)
goal_r_top = Vector3D(widthx_field / 2 + goal_widthx / 2, 0, goal_heightz)

area_goal = goal_heightz * goal_widthx

case_num = 1
while True:
    try:
        num_pos, num_op = map(int, input().split(" "))
    except EOFError:
        break
    if num_pos == 0:
        print(f"Case #{case_num}: No positions given.")
    else:
        print(f"Case #{case_num}")

    positions = []
    for _ in range(num_pos):
        inp = input()
        if "." in inp:
            x, y = map(float, inp.split(" "))
        else:
            x, y = map(int, inp.split(" "))
        pos = Vector3D(x, y, 0)
        positions.append(pos)

    opponents = []
    for _ in range(num_op):
        inp = input().split(" ")
        while "" in inp:
            inp.remove("")
        height, width = map(float, inp[:2])
        if "." in inp[2] or "." in inp[3]:
            x, y = map(float, inp[2:])
        else:
            x, y = map(int, inp[2:])
        x = x - width / 2
        opponents.append((height, width, x, y))
    # plot_opponents(opponents, positions)

    if num_op == 0:
        for i in range(3):
            print(f"100% with id {i + 1}")
        print()
        case_num += 1
        continue

    ratings = []
    for id, pos in enumerate(positions, 1):
        rating = 100

        projections = []
        for opp in opponents:
            if pos.y > opp[3]:
                # print(f"Opponent {opp} is below the ball at {pos}. Skipping.")
                continue

            proj_ll, proj_ur = projections_opponent(*opp, pos)
            # print("Projection:", proj_ll, proj_ur)

            # proj left of goal
            if proj_ur.x <= goal_l.x:
                # print("Projection is left of goal. Skipping.")
                continue

            # proj right of goal
            if proj_ll.x >= goal_r.x:
                # print("Projection is right of goal. Skipping.")
                continue

            # proj on left side of goal
            if proj_ll.x < goal_l.x:
                # print(f"Projection touches left side of goal. Adjusting x from {proj_ll.x} to {goal_l.x}")
                proj_ll.x = goal_l.x

            # proj on right side of goal
            if proj_ur.x > goal_r.x:
                # print(f"Projection touches right side of goal. Adjusting x from {proj_ur.x} to {goal_r.x}")
                proj_ur.x = goal_r.x

            # proj above goal
            if proj_ur.z >= goal_heightz:
                # print("Projection is above goal. Adjusting z from", proj_ur.z, "to", goal_heightz)
                proj_ur.z = goal_heightz

            projections.append((proj_ll, proj_ur))
        # plot_opponents(opponents, positions, projections)
        # plot_projections_in_goal(projections)

        if len(projections) == 0:
            ratings.append((id, 100))
        elif len(projections) == 1:
            proj_ll, proj_ur = projections[0]
            total_area = (proj_ur.x - proj_ll.x) * (proj_ur.z - proj_ll.z)
            rating = 100 * (1 - total_area / area_goal)
            # print(f"Rating for position {id} is {rating}%")
            ratings.append((id, rating))
        else:
            # do a linesweep algo to calculate the total area of the projections
            events = []
            for proj in projections:
                events.append((proj[0].x, 'start', proj))
                events.append((proj[1].x, 'end', proj))

            events.sort(key=lambda x: x[0])

            active_projs = set()
            total_area = 0
            curr_z = 0
            prev_x = 0

            for x, event_type, proj in events:
                if event_type == 'start':
                    total_area += (x - prev_x) * curr_z
                    prev_x = x
                    curr_z = max(curr_z, proj[1].z)
                    active_projs.add(proj)
                else:
                    if curr_z == proj[1].z:
                        total_area += (x - prev_x) * curr_z
                        prev_x = x
                        curr_z = 0
                        active_projs.remove(proj)
                        for p in active_projs:
                            if p[1].z > curr_z:
                                curr_z = p[1].z
                    else:
                        active_projs.remove(proj)

            rating = 100 * (1 - total_area / area_goal)
            # print(f"Rating for position {id} is {rating}%")
            ratings.append((id, rating))

    sorted_ratings = sorted(ratings, key=lambda x: round(x[1]), reverse=True)
    for id, rating in sorted_ratings[:3]:
        print(f"{round(rating)}% with id {id}")

    print()
    case_num += 1


