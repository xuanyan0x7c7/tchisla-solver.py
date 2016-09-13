import math
from gmpy2 import mpq as Fraction, is_square, isqrt
from expression import Expression
from solver.base import BaseTchisla

__all__ = ["RationalTchisla"]

class RationalTchisla(BaseTchisla):
    constructor = Fraction
    MAX = 1 << 32
    MAX_DIGITS = 32
    MAX_CONCAT = 20
    MAX_FACTORIAL = 12

    def __init__(self, n, target):
        super().__init__(n, target)

    def range_check(self, x):
        return x.numerator <= self.MAX and x.denominator <= self.MAX

    def integer_check(self, x):
        return x.denominator == 1

    def exponent(self, p, q, depth):
        if q.denominator != 1 or p == 1:
            return
        p_digits = math.log2(max(p.numerator, p.denominator))
        q_int = q.numerator
        exp = Expression.power(p, q), Expression.power(p, Expression.negate(q))
        while p_digits * q_int > self.MAX_DIGITS:
            if q_int & 1 == 0:
                q_int >>= 1
                exp = Expression.sqrt(exp[0]), Expression.sqrt(exp[1])
            else:
                return
        x = p ** q_int
        self.check(x, depth, exp[0])
        self.check(x ** -1, depth, exp[1])

    def sqrt(self, x, depth):
        if is_square(x.numerator) and is_square(x.denominator):
            y = isqrt(x.numerator)
            z = isqrt(x.denominator)
            self.check(Fraction(y, z), depth, Expression.sqrt(x))
