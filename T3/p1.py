# The billboard problem
# https://www.thehindu.com/children/the-billiard-ball-problem/article20314985.ece
# https://en.wikipedia.org/wiki/Arithmetic_billiards

from fractions import Fraction


class BillBoard:
    def __init__(self, n, m, ball, direction):
        self.n = n
        self.m = m
        self.ball = ball
        self.direction = direction
        self.tracking_corners = [
            {"color": "green", "point": (0, 0)},
            {"color": "red", "point": (self.n, 0)},
            {"color": "yellow", "point": (0, self.m)},
            {"color": "blue", "point": (self.n, self.m)},
        ]

    def calc_hit(self, hit, offset=0):

        if self.direction[0] == 0:
            return (hit[0], (self.m if self.direction[1] > 0 else 0))

        def get_y(x):
            return (x - hit[0]) * int(
                self.direction[1] / self.direction[0]
            ) + hit[1]

        # (  1,  1) -> x=n -> y= self.m
        # (  1, -1) -> x=n -> y=0
        # ( -1,  1) -> x=0 -> y= self.m
        # ( -1, -1) -> x=0 -> y=0
        x = hit[0]
        if self.direction[0] == 1:
            x = self.n + offset
        elif self.direction[0] == -1:
            x = 0 - offset
        y = get_y(x)
        return (x, y)

    def create_points(self, last_points):
        new_points = [
            {"color": "green", "point": (0, 0)},
            {"color": "red", "point": (self.n, 0)},
            {"color": "yellow", "point": (0, self.m)},
            {"color": "blue", "point": (self.n, self.m)},
        ]
        if self.direction[1] > 0:
            if self.direction[0] > 0:
                new_points[0] = last_points[3].copy()
                new_points[1] = last_points[2].copy()
                new_points[1]["point"] = tuple(
                    map(sum, zip(last_points[2]["point"], (2 * self.n, 0)))
                )
                new_points[2] = last_points[1].copy()
                new_points[2]["point"] = tuple(
                    map(sum, zip(last_points[1]["point"], (0, 2 * self.m)))
                )
                new_points[3] = last_points[0].copy()
                new_points[3]["point"] = tuple(
                    map(
                        sum,
                        zip(last_points[0]["point"], (2 * self.n, 2 * self.m)),
                    )
                )
            elif self.direction[0] < 0:
                new_points[1] = last_points[2].copy()

                new_points[0] = last_points[3].copy()
                new_points[0]["point"] = tuple(
                    map(sum, zip(last_points[3]["point"], (-2 * self.n, 0)))
                )

                new_points[2] = last_points[1].copy()
                new_points[2]["point"] = tuple(
                    map(
                        sum,
                        zip(
                            last_points[1]["point"], (-2 * self.n, -2 * self.m)
                        ),
                    )
                )

                new_points[3] = last_points[0].copy()
                new_points[3]["point"] = tuple(
                    map(sum, zip(last_points[0]["point"], (0, 2 * self.m)))
                )
        elif self.direction[1] < 0:
            if self.direction[0] > 0:
                new_points[2] = last_points[1].copy()

                new_points[0] = last_points[3].copy()
                new_points[0]["point"] = tuple(
                    map(sum, zip(last_points[3]["point"], (0, -2 * self.m)))
                )

                new_points[1] = last_points[2].copy()
                new_points[1]["point"] = tuple(
                    map(
                        sum,
                        zip(last_points[2]["point"], (2 * self.n, -2 * self.m)),
                    )
                )

                new_points[3] = last_points[0].copy()
                new_points[3]["point"] = tuple(
                    map(sum, zip(last_points[0]["point"], (2 * self.n, 0)))
                )

            elif self.direction[0] < 0:
                new_points[3] = last_points[0].copy()

                new_points[2] = last_points[1].copy()
                new_points[2]["point"] = tuple(
                    map(sum, zip(last_points[1]["point"], (-2 * self.n, 0)))
                )

                new_points[1] = last_points[2].copy()
                new_points[1]["point"] = tuple(
                    map(sum, zip(last_points[2]["point"], (0, -2 * self.m)))
                )

                new_points[0] = last_points[3].copy()
                new_points[0]["point"] = tuple(
                    map(
                        sum,
                        zip(
                            last_points[3]["point"], (-2 * self.n, -2 * self.m)
                        ),
                    )
                )
        return new_points, {i["point"] for i in new_points}

    @staticmethod
    def is_solution(hit, targets):
        return hit in targets

    def prefetch_solution(self, hit):
        if float(hit[0]).is_integer() and float(hit[1]).is_integer():
            pass

    def shot(self):
        offset = 0
        hit = self.calc_hit(ball, offset)
        valid_targets = {i["point"] for i in self.tracking_corners}
        corners = self.tracking_corners.copy()

        if float(hit[0]).is_integer() and float(hit[1]).is_integer():
            while not self.is_solution(hit, valid_targets):
                hit = self.calc_hit(hit, offset=offset)
                offset += self.n
                corners, valid_targets = self.create_points(corners)
                if direction[0] == 0 or direction[1] == 0:
                    return -1
            for corner in corners:
                if corner["point"] == hit:
                    return next(
                        filter(
                            lambda x: x["color"] == corner["color"],
                            self.tracking_corners,
                        )
                    )["point"]
        else:
            return -1


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1 and argv[1] == "-t":
        start_n = 10
        start_m = 10
        ball = (10, -1)
        direction = (-1, 0)
    else:
        start_n = int(input())
        start_m = int(input())

        ball = (int(input()), int(input()))
        direction = (int(input()), int(input()))

    new_fraction = Fraction(start_m, start_n)

    # Calc gcd
    m = new_fraction.numerator
    n = new_fraction.denominator

    change = m / start_m

    ball = (
        ball[0] * change,
        ball[1] * change,
    )

    new_billboard = BillBoard(n, m, ball, direction)
    solution = new_billboard.shot()
    print(f"{solution[0]} {solution[1]}") if isinstance(
        solution, tuple
    ) else print(solution)
