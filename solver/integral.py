import math
from gmpy2 import is_square, isqrt
from expression import Expression
from solver.base import BaseTchisla

__all__ = ["IntegralTchisla"]

class IntegralTchisla(BaseTchisla):
    constructor = int
    MAX = 1 << 128
    MAX_DIGITS = 128
    MAX_CONCAT = 39
    MAX_FACTORIAL = 34

    def __init__(self, n, target, verbose = False):
        super().__init__(n, target, verbose)

    def range_check(self, x):
        return x <= self.MAX

    def integer_check(self, x):
        return True

    def divide(self, p, q, depth):
        if p < q:
            p, q = q, p
        if p % q == 0:
            self.check(p // q, depth, Expression("/", p, q))

    def exponent(self, p, q, depth):
        if p == 1:
            return
        p_digits = math.log2(p)
        exp = Expression("^", p, q)
        while p_digits * q > self.MAX_DIGITS:
            if q & 1 == 0:
                q >>= 1
                exp = Expression("sqrt", exp)
            else:
                return
        self.check(p ** q, depth, exp)

    def sqrt(self, x, depth):
        if is_square(x):
            y = int(isqrt(x))
            self.check(y, depth, Expression("sqrt", x))
