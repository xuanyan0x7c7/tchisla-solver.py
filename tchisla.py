import math
from fractions import Fraction
from itertools import count, product, combinations_with_replacement, chain, islice
from expression import Expression
from utils import sqrt, factorial

__all__ = ["Tchisla"]

MAX = 1 << 128
MAX_DIGITS = 128
MAX_CONCAT = 39
MAX_FACTORIAL = 34

class SolutionFoundError(Exception):
    def __init__(self, message):
        self.message = message

class Tchisla:
    __slots__ = ("n", "target", "solutions", "visited", "number_printed")

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
            raise SolutionFoundError(str(self.target) + "#" + str(self.n))

    def check(self, x, depth, expression):
        if x.numerator > MAX or x.denominator > MAX or x in self.solutions:
            return
        self.insert(x, depth, expression)
        z = sqrt(x.denominator)
        if z is not None:
            y = sqrt(x.numerator)
            if y is not None:
                self.check(Fraction(y, z, False), depth, Expression("sqrt", x))
        if x.denominator == 1 and x <= MAX_FACTORIAL:
            y = Fraction(factorial(int(x)))
            self.check(y, depth, Expression("factorial", x))

    def quotient(self, p, q, depth):
        if p < q:
            p, q = q, p
        quotient = p / q
        self.check(quotient, depth, Expression("/", p, q))
        self.check(quotient ** -1, depth, Expression("/", q, p))

    def exponent(self, p, q, depth):
        if q.denominator != 1 or p == 1:
            return
        p_digits = math.log2(max(p.numerator, p.denominator))
        q_int = q.numerator
        exp = (Expression("^", p, q), Expression("^", p, Expression("-", q)))
        while p_digits * q_int > MAX_DIGITS:
            if q_int & 1 == 0:
                q_int >>= 1
                exp = (Expression("sqrt", exp[0]), Expression("sqrt", exp[1]))
            else:
                return
        x = p ** q_int
        self.check(x, depth, exp[0])
        self.check(x ** -1, depth, exp[1])

    def binary(self, p, q, depth):
        self.check(p + q, depth, Expression("+", p, q))
        if p > q:
            self.check(p - q, depth, Expression("-", p, q))
        elif p < q:
            self.check(q - p, depth, Expression("-", q, p))
        self.check(p * q, depth, Expression("*", p, q))
        self.quotient(p, q, depth)
        self.exponent(p, q, depth)
        self.exponent(q, p, depth)

    def search(self, depth):
        self.visited.append([])
        if depth <= MAX_CONCAT:
            m = Fraction((10 ** depth - 1) // 9 * self.n)
            self.check(m, depth, Expression())
        for d1 in range(1, (depth + 1) >> 1):
            d2 = depth - d1
            for p, q in product(self.visited[d1], self.visited[d2]):
                self.binary(p, q, depth)
        if depth & 1 == 0:
            for p, q in combinations_with_replacement(self.visited[depth >> 1], 2):
                self.binary(p, q, depth)

    def solve(self):
        try:
            for depth in count(1):
                self.search(depth)
        except SolutionFoundError:
            pass

    def printer(self, n):
        depth, expression = self.solutions[n]
        string = str(depth) + ": " + str(n)
        if expression.name is None:
            return string
        else:
            return string + " = " + str(expression)

    @staticmethod
    def number_dfs(expression):
        if type(expression) is Expression:
            return chain.from_iterable(map(Tchisla.number_dfs, expression.args))
        else:
            return (expression,)

    def print_solution(self, n, force_print = False):
        if n in self.number_printed:
            return
        depth, expression = self.solutions[n]
        if expression.name is not None or force_print:
            print(self.printer(n))
            self.number_printed.add(n)
            for x in Tchisla.number_dfs(expression):
                self.print_solution(x)
