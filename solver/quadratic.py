import math
from gmpy2 import mpq as Fraction, is_square, isqrt
from quadratic import Quadratic
from expression import Expression
from solver.base import BaseTchisla

__all__ = ["QuadraticTchisla"]

class QuadraticTchisla(BaseTchisla):
    constructor = Quadratic
    MAX = 1 << 16
    MAX_DIGITS = 16
    MAX_CONCAT = 5
    MAX_FACTORIAL = 8

    def __init__(self, n, target):
        super().__init__(n, target)

    def range_check(self, x):
        x = x.rational_part
        return x.numerator <= self.MAX and x.denominator <= self.MAX

    def integer_check(self, x):
        return x.quadratic_power == 0 and x.rational_part.denominator == 1

    def add(self, p, q, depth):
        result = p + q
        if result is not None:
            self.check(result, depth, Expression("+", p, q))

    def subtract(self, p, q, depth):
        if p == q:
            return
        if p.rational_part < q.rational_part:
            p, q = q, p
        result = p - q
        if result is not None:
            if result.rational_part < 0:
                result = -result
                p, q = q, p
            self.check(result, depth, Expression("-", p, q))

    def multiply(self, p, q, depth):
        self.check(p * q, depth, Expression("*", p, q))

    def divide(self, p, q, depth):
        quotient = p / q
        self.check(quotient, depth, Expression("/", p, q))
        self.check(quotient ** -1, depth, Expression("/", q, p))

    def exponent(self, p, q, depth):
        if not self.integer_check(q) or p == 1:
            return
        base = math.log2(max(p.rational_part.numerator, p.rational_part.denominator))
        q_max = q.rational_part.numerator
        while base * (q_max - p.quadratic_power) > self.MAX_DIGITS:
            if q_max & 1 == 0:
                q_max >>= 1
            else:
                return
        q_min = q_max
        exp = (Expression("^", p, q), Expression("^", p, Expression("-", q)))
        while q_min & 1 == 0:
            q_min >>= 1
            exp = (Expression("sqrt", exp[0]), Expression("sqrt", exp[1]))
        q = q_min
        x = p ** q
        while q <= q_max:
            if not self.range_check(x):
                break
            self.check(x, depth, exp[0], need_sqrt = q == q_min)
            self.check(x ** -1, depth, exp[1], need_sqrt = q == q_min)
            q <<= 1
            x **= 2
            if type(exp[0]) is Expression:
                exp = exp[0].args[0], exp[1].args[0]

    def sqrt(self, x, depth):
        if x.quadratic_power < 3:
            y = Quadratic.sqrt(x)
            if y is not None:
                self.check(y, depth, Expression("sqrt", x))
