import math
from expression import Expression
from utils import sqrt
from solver.base import BaseTchisla

__all__ = ["IntegerTchisla"]

MAX = 1 << 128
MAX_DIGITS = 128
MAX_CONCAT = 39
MAX_FACTORIAL = 34

class IntegerTchisla(BaseTchisla):
    constructor = int
    MAX = 1 << 128
    MAX_DIGITS = 128
    MAX_CONCAT = 39
    MAX_FACTORIAL = 34

    def __init__(self, n, target):
        super().__init__(n, target)

    def range_check(self, x):
        return x <= self.MAX

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
        y = sqrt(x)
        if y is not None:
            self.check(y, depth, Expression("sqrt", x))
