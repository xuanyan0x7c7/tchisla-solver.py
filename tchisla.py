import math
from fractions import Fraction
from itertools import count, product, combinations_with_replacement, chain, islice
from functools import reduce
from utils import sqrt, factorial

__all__ = ["Tchisla"]

MAX = 1 << 128
MAX_DIGITS = 128
MAX_CONCAT = 39
MAX_FACTORIAL = 34

class Tchisla:
    def __init__(self, n, target):
        self.n = n
        self.target = target
        self.solutions = {}
        self.visited = [[]]
        self.number_printed = set()

    def insert(self, x, depth, expression):
        self.solutions[x] = depth, expression
        self.visited[depth].append(x)
        if x == self.target:
            self.solution_found(self.target, True)
            return True

    def check(self, x, depth, expression):
        if x.numerator > MAX or x.denominator > MAX or x in self.solutions:
            return
        if self.insert(x, depth, expression):
            return True
        z = sqrt(x.denominator)
        if z is not None:
            y = sqrt(x.numerator)
            if y is not None and self.check(Fraction(y, z, False), depth, ("sqrt", x)):
                return True
        if x.denominator == 1 and x <= MAX_FACTORIAL:
            y = Fraction(factorial(int(x)))
            if self.check(y, depth, ("factorial", x)):
                return True

    def exponent(self, p, q, depth):
        if q.denominator != 1 or p == 1:
            return
        p_digits = math.log2(max(p.numerator, p.denominator))
        q_int = q.numerator
        exp = (("^", p, q), ("^", p, ("-", q)))
        while p_digits * q_int > MAX_DIGITS:
            if q_int & 1 == 0:
                q_int >>= 1
                exp = (("sqrt", exp[0]), ("sqrt", exp[1]))
            else:
                return
        x = p ** q_int
        if self.check(x, depth, exp[0]):
            return True
        if self.check(x ** -1, depth, exp[1]):
            return True

    def binary(self, p, q, depth):
        if self.check(p + q, depth, ("+", p, q)):
            return True
        if p > q and self.check(p - q, depth, ("-", p, q)):
            return True
        elif p < q and self.check(q - p, depth, ("-", q, p)):
            return True
        if self.check(p * q, depth, ("*", p, q)):
            return True
        quotient = p / q
        if self.check(quotient, depth, ("/", p, q)):
            return True
        if self.check(quotient ** -1, depth, ("/", q, p)):
            return True
        if self.exponent(p, q, depth):
            return True
        if self.exponent(q, p, depth):
            return True

    def search(self, depth):
        self.visited.append([])
        if depth <= MAX_CONCAT:
            m = Fraction((10 ** depth - 1) // 9 * self.n)
            if self.check(m, depth, ()):
                return True
        for d1 in range(1, (depth + 1) >> 1):
            d2 = depth - d1
            for p, q in product(self.visited[d1], self.visited[d2]):
                if self.binary(p, q, depth):
                    return True
        if depth & 1 == 0:
            for p, q in combinations_with_replacement(self.visited[depth >> 1], 2):
                if self.binary(p, q, depth):
                    return True

    def solve(self):
        for depth in count(1):
            if self.search(depth):
                return

    @staticmethod
    def number_printer(n):
        if type(n) is tuple:
            if len(n) == 2:
                if n[0] == "sqrt":
                    return "sqrt(" + Tchisla.number_printer(n[1]) + ")"
                elif n[0] == "-":
                    return "-" + Tchisla.number_printer(n[1])
            elif len(n) == 3:
                return Tchisla.number_printer(n[1]) + n[0] + Tchisla.number_printer(n[2])
        else:
            return str(n)

    def printer(self, n):
        depth, expression = self.solutions[n]
        string = str(depth) + ": " + str(n)
        if expression == ():
            return string
        string += " = "
        if len(expression) == 2:
            method, operator = expression
            if method == "sqrt":
                return string + "sqrt(" + Tchisla.number_printer(operator) + ")"
            elif method == "factorial":
                return string + str(operator) + "!"
        elif len(expression) == 3:
            method, op1, op2 = expression
            return string + Tchisla.number_printer(op1) + " " + method + " " + Tchisla.number_printer(op2)

    @staticmethod
    def number_dfs(expression):
        if type(expression) is tuple:
            return chain.from_iterable(map(Tchisla.number_dfs, islice(expression, 1, None)))
        else:
            return (expression,)

    def solution_found(self, n, force_print = False):
        if n in self.number_printed:
            return
        depth, expression = self.solutions[n]
        if expression or force_print:
            print(self.printer(n))
            self.number_printed.add(n)
            for x in Tchisla.number_dfs(expression):
                self.solution_found(x)
