import math
import operator
from itertools import count, product, combinations_with_replacement, chain
from functools import reduce
from abc import ABCMeta, abstractmethod
from gmpy2 import mpq as Fraction, fac as factorial
from expression import Expression

__all__ = ["BaseTchisla"]

class SolutionFoundError(Exception):
    def __init__(self, message):
        self.message = message

class BaseTchisla:
    __metaclass__ = ABCMeta
    __slots__ = ("n", "target", "solutions", "max_depth", "visited", "number_printed")

    def __init__(self, n, target):
        self.n = n
        self.target = self.constructor(target)
        self.solutions = {}
        self.max_depth = None
        self.visited = [None, []]
        self.number_printed = set()

    def insert(self, x, depth, expression):
        self.solutions[x] = depth, expression
        self.visited[depth].append(x)
        if x == self.target:
            raise SolutionFoundError(str(self.target) + "#" + str(self.n))

    @abstractmethod
    def range_check(self, x):
        pass

    @abstractmethod
    def integer_check(self, x):
        pass

    def check(self, x, depth, expression, *, need_sqrt = True):
        if not self.range_check(x) or x in self.solutions:
            return
        self.insert(x, depth, expression)
        if need_sqrt:
            self.sqrt(x, depth)
        if self.integer_check(x):
            self.factorial(x, depth)

    def concat(self, depth):
        if depth <= self.MAX_CONCAT:
            x = self.constructor((10 ** depth - 1) // 9 * self.n)
            self.check(x, depth, Expression("concat", x))

    def add(self, p, q, depth):
        self.check(p + q, depth, Expression("+", p, q))

    def subtract(self, p, q, depth):
        if p == q:
            return
        result = p - q
        if result < 0:
            self.check(-result, depth, Expression("-", q, p))
        else:
            self.check(result, depth, Expression("-", p, q))

    def multiply(self, p, q, depth):
        self.check(p * q, depth, Expression("*", p, q))

    def divide(self, p, q, depth):
        quotient = p / q
        if quotient < 1:
            self.check(quotient ** -1, depth, Expression("/", q, p))
            self.check(quotient, depth, Expression("/", p, q))
        else:
            self.check(quotient, depth, Expression("/", p, q))
            self.check(quotient ** -1, depth, Expression("/", q, p))

    def factorial_divide(self, p, q, depth):
        if p == q or not self.integer_check(p) or not self.integer_check(q):
            return
        x = int(p)
        y = int(q)
        if x < y:
            x, y = y, x
            p, q = q, p
        if x <= self.MAX_FACTORIAL or y <= 2 or x - y == 1 or (x - y) * (math.log2(x) + math.log2(y)) > self.MAX_DIGITS << 1:
            return
        result = reduce(operator.mul, range(x, y, -1))
        p_factorial = Expression("factorial", p)
        q_factorial = Expression("factorial", q)
        self.check(self.constructor(result), depth, Expression("/", p_factorial, q_factorial))
        if depth != self.max_depth and self.solutions[q][0] == 1:
            self.check(self.constructor(result - 1), depth + 1, Expression(
                "/",
                Expression("-", p_factorial, q_factorial),
                q_factorial
            ))
            self.check(self.constructor(result + 1), depth + 1, Expression(
                "/",
                Expression("+", p_factorial, q_factorial),
                q_factorial
            ))

    @abstractmethod
    def exponent(self, p, q, depth):
        pass

    @abstractmethod
    def sqrt(self, x, depth):
        pass

    def factorial(self, x, depth):
        if int(x) <= self.MAX_FACTORIAL:
            y = self.constructor(factorial(int(x)))
            self.check(y, depth, Expression("factorial", x))

    def binary_operation(self, p, q, depth):
        self.add(p, q, depth)
        self.subtract(p, q, depth)
        self.multiply(p, q, depth)
        self.divide(p, q, depth)
        self.exponent(p, q, depth)
        self.exponent(q, p, depth)

    def search(self, depth):
        if depth not in self.visited:
            self.visited.append([])
        self.concat(depth)
        for d1 in range(1, (depth + 1) >> 1):
            d2 = depth - d1
            for p, q in product(self.visited[d1], self.visited[d2]):
                self.binary_operation(p, q, depth)
        if depth & 1 == 0:
            for p, q in combinations_with_replacement(self.visited[depth >> 1], 2):
                self.binary_operation(p, q, depth)
        for d1 in range(1, (depth + 1) >> 1):
            d2 = depth - d1
            for p, q in product(self.visited[d1], self.visited[d2]):
                self.factorial_divide(p, q, depth)
        if depth & 1 == 0:
            for p, q in combinations_with_replacement(self.visited[depth >> 1], 2):
                self.factorial_divide(p, q, depth)

    def solve(self, *, max_depth = None, verbose = False):
        self.max_depth = max_depth
        for depth in count(1):
            if depth - 1 == max_depth:
                return
            if verbose:
                print(depth)
            try:
                self.search(depth)
            except SolutionFoundError:
                return depth


    def printer(self, n):
        depth, expression = self.solutions[n]
        string = str(depth) + ": " + str(n)
        if expression.name == "concat":
            return string
        else:
            return string + " = " + str(expression)

    def solution_prettyprint(self, n, *, force_print = False):
        def requirements(expression):
            if type(expression) is Expression:
                return chain(*map(requirements, expression.args))
            else:
                return (expression,)

        if n in self.number_printed or n not in self.solutions:
            return []
        depth, expression = self.solutions[n]
        if expression.name == "concat" and not force_print:
            return []
        solution_list = [self.printer(n)]
        self.number_printed.add(n)
        for x in requirements(expression):
            solution_list += self.solution_prettyprint(x)
        return solution_list
