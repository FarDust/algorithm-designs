# The billboard problem
# https://www.thehindu.com/children/the-billiard-ball-problem/article20314985.ece

from fractions import Fraction

start_m = 154812
start_n = 123522

ball = (512, 0)
direction = (1, 1)

new_fraction = Fraction(start_m, start_n)

# Calc gcd
m = new_fraction.numerator
n = new_fraction.denominator

change = m / start_m

ball = (
    ball[0] * change,
    ball[1] * change,
)

tracking_corners = [
    {"color": "green", "point": (0, 0)},
    {"color": "red", "point": (n, 0)},
    {"color": "yellow", "point": (0, m)},
    {"color": "blue", "point": (n, m)},
]


def calc_hit(hit, direction, offset=0):

    if direction[0] == 0:
        return (hit[0], (m if direction[1] > 0 else 0))

    def get_y(x):
        return (x - hit[0]) * int(direction[1] / direction[0]) + hit[1]

    # (  1,  1) -> x=n -> y=m
    # (  1, -1) -> x=n -> y=0
    # ( -1,  1) -> x=0 -> y=m
    # ( -1, -1) -> x=0 -> y=0
    x = hit[0]
    if direction[0] == 1:
        x = n + offset
    elif direction[0] == -1:
        x = 0 - offset
    y = get_y(x)
    return (x, y)


def create_points(last_points):
    new_points = [
        {"color": "green", "point": (0, 0)},
        {"color": "red", "point": (n, 0)},
        {"color": "yellow", "point": (0, m)},
        {"color": "blue", "point": (n, m)},
    ]
    if direction[1] > 0:
        if direction[0] > 0:
            new_points[0] = last_points[3].copy()
            new_points[1] = last_points[2].copy()
            new_points[1]["point"] = tuple(
                map(sum, zip(last_points[2]["point"], (2 * n, 0)))
            )
            new_points[2] = last_points[1].copy()
            new_points[2]["point"] = tuple(
                map(sum, zip(last_points[1]["point"], (0, 2 * m)))
            )
            new_points[3] = last_points[0].copy()
            new_points[3]["point"] = tuple(
                map(sum, zip(last_points[0]["point"], (2 * n, 2 * m)))
            )
        elif direction[0] < 0:
            new_points[1] = last_points[2].copy()

            new_points[0] = last_points[3].copy()
            new_points[0]["point"] = tuple(
                map(sum, zip(last_points[3]["point"], (-2 * n, 0)))
            )

            new_points[2] = last_points[1].copy()
            new_points[2]["point"] = tuple(
                map(sum, zip(last_points[1]["point"], (-2 * n, -2 * m)))
            )

            new_points[3] = last_points[0].copy()
            new_points[3]["point"] = tuple(
                map(sum, zip(last_points[0]["point"], (0, 2 * m)))
            )
    elif direction[1] < 0:
        if direction[0] > 0:
            new_points[2] = last_points[1].copy()

            new_points[0] = last_points[3].copy()
            new_points[0]["point"] = tuple(
                map(sum, zip(last_points[3]["point"], (0, -2 * m)))
            )

            new_points[1] = last_points[2].copy()
            new_points[1]["point"] = tuple(
                map(sum, zip(last_points[2]["point"], (2 * n, -2 * m)))
            )

            new_points[3] = last_points[0].copy()
            new_points[3]["point"] = tuple(
                map(sum, zip(last_points[0]["point"], (2 * n, 0)))
            )

        elif direction[0] < 0:
            new_points[3] = last_points[0].copy()

            new_points[2] = last_points[1].copy()
            new_points[2]["point"] = tuple(
                map(sum, zip(last_points[1]["point"], (-2 * n, 0)))
            )

            new_points[1] = last_points[2].copy()
            new_points[1]["point"] = tuple(
                map(sum, zip(last_points[2]["point"], (0, -2 * m)))
            )

            new_points[0] = last_points[3].copy()
            new_points[0]["point"] = tuple(
                map(sum, zip(last_points[3]["point"], (-2 * n, -2 * m)))
            )
    new_points
    return new_points, {i["point"] for i in new_points}


def is_solution(hit, targets):
    return hit in targets


def prefetch_solution():
    if float(hit[0]).is_integer() and float(hit[1]).is_integer():
        pass


offset = 0
hit = calc_hit(ball, direction, offset)
valid_targets = {i["point"] for i in tracking_corners}
corners = tracking_corners.copy()
result = True

if float(hit[0]).is_integer() and float(hit[1]).is_integer():
    while not is_solution(hit, valid_targets):
        hit = calc_hit(hit, direction, offset=offset)
        offset += n
        corners, valid_targets = create_points(corners)
        if direction[0] == 0 or direction[1] == 0:
            result = False
            print(-1)
            break
    if result:
        print(hit)
        print(valid_targets)

        print("")

        [print(i) for i in corners]

        print("")

        for corner in corners:
            if corner["point"] == hit:
                print(
                    next(
                        filter(
                            lambda x: x["color"] == corner["color"],
                            tracking_corners,
                        )
                    )["point"]
                )
                print(f"final_corner: {corner['color']}")

                break
else:
    print(-1)
