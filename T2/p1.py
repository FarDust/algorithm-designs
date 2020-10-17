import math
import cmath


class Polynomial:
    def __init__(self, polynomial, rank=None):
        self.value = list(polynomial)
        self.rank = rank if rank else len(self.value) - 1

    def __mul__(self, other):
        result = list()
        padding = next_potency2(len(other.value) + len(self.value))
        pv_poly_1 = fft(fft_prepare_input(self.value, padding))
        pv_poly_2 = fft(fft_prepare_input(other.value, padding))
        for unit_root in range(padding):
            result.append(pv_poly_1[unit_root] * pv_poly_2[unit_root])
        return Polynomial(
            map(
                lambda number: round_complex(number),
                ifft(fft_prepare_input(result, next_potency2(len(result)))),
            ),
            rank=self.rank+other.rank
        )

    def __repr__(self):
        return " + ".join(
            map(
                lambda i: f"{round_complex(self.value[i])}*X^{i}",
                range(len(self)),
            )
        )
    
    def __len__(self):
        return self.rank + 1

    def __str__(self):
        return repr(self)

    def int_coef_str(self):
        return " ".join(
            map(
                lambda i: f"{int(round_complex(self.value[i]))}",
                range(len(self)),
            )
        )


def next_potency2(number):
    return int(math.ldexp(1, math.ceil(math.log2(number))))


def fft_prepare_input(polynomial, padding):
    zero_padding = [0] * (padding - len(polynomial))
    return polynomial.copy() + zero_padding


def round_complex(number):
    return (
        round(number.real, 14)
        if round(number.imag, 14) * 1j == 0j
        else round(number.real, 14) + round(number.imag, 14) * 1j
    )  # Round base on pi max presition


def dft2(polynomial):
    assert len(polynomial) == 2
    base = [0, 0, 0, 1]
    M = list(map(lambda x: cmath.exp(-1j * cmath.pi * x), base))
    result = [
        (M[0] * polynomial[0] + M[2] * polynomial[1]),
        (M[1] * polynomial[0] + M[3] * polynomial[1]),
    ]
    return result


def fft(polynomial):
    assert len(polynomial) % 2 == 0
    if len(polynomial) == 2:
        return dft2(polynomial)
    even_poly = fft(polynomial[::2])
    odd_poly = fft(polynomial[1::2])
    unit_roots = list(
        map(
            lambda x: cmath.exp(-1j * cmath.pi * x / int(len(polynomial) / 2)),
            range(len(polynomial)),
        )
    )
    last_unit_roots = unit_roots[: int(len(polynomial) / 2)]
    first_unit_roots = unit_roots[int(len(polynomial) / 2) :]
    first_part = map(
        lambda index: (
            even_poly[index] + last_unit_roots[index] * odd_poly[index]
        ),
        range(len(even_poly)),
    )
    second_part = map(
        lambda index: (
            even_poly[index] + first_unit_roots[index] * odd_poly[index]
        ),
        range(len(even_poly)),
    )
    return list(first_part) + list(second_part)


def ifft(pv_polynomial):
    shift_poly = pv_polynomial[0:1] + pv_polynomial[:0:-1]
    return list(
        map(lambda element: element / len(pv_polynomial), fft(shift_poly))
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        polyA = Polynomial([2, 0, 1])
        polyB = Polynomial([2, 0, 1])
    else:
        remap_int = lambda coefficient: int(coefficient)
        polyA = Polynomial(map(remap_int, input().strip().split(" ")[1:]))
        polyB = Polynomial(map(remap_int, input().strip().split(" ")[1:]))

    result = polyA * polyB
    print(f'{result.rank} {result.int_coef_str()}')
