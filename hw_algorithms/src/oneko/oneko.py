from fractions import Fraction

if __name__ == '__main__':
    n_onekos = int(input())

    correct = True
    slope_found = False

    for o in range(n_onekos):
        o_x, o_y = map(int, input().split(' '))
        # print(o_coords)

        if o_x == 0 and o_y == 0:
            continue

        if not slope_found:
            if o_x == 0:
                slope = "infty"
            else:
                slope = Fraction(o_y, o_x)
            slope_found = True
            continue

        if slope != "infty":
            if Fraction(o_y, o_x) != slope:
                correct = False
                break
        else:
            if o_x != 0:
                correct = False
                break

    if correct:
        print("yes")
    else:
        print("no")
