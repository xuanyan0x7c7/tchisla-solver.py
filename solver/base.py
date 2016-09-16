import math
import operator
from itertools import count, product, combinations_with_replacement, chain
from functools import reduce
from abc import ABCMeta, abstractmethod
from config import global_config
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

    def insert(self, x, digits, expression):
        self.solutions[x] = digits, expression
        self.visited[digits].append(x)
        if x == self.target:
            raise SolutionFoundError(str(self.target) + "#" + str(self.n))

    @abstractmethod
    def range_check(self, x):
        pass

    @abstractmethod
    def integer_check(self, x):
        pass

    def check(self, x, digits, expression, *, need_sqrt = True):
        if not self.range_check(x) or x in self.solutions:
            return
        self.insert(x, digits, expression)
        if need_sqrt:
            self.sqrt(x, digits)
        if self.integer_check(x):
            self.factorial(x, digits)

    def concat(self, digits):
        if digits <= self.MAX_CONCAT:
            x = self.constructor((10 ** digits - 1) // 9 * self.n)
            self.check(x, digits, Expression.concat(x))

    def add(self, p, q, digits):
        self.check(p + q, digits, Expression.add(p, q))

    def subtract(self, p, q, digits):
        if p == q:
            return
        result = p - q
        if result < 0:
            self.check(-result, digits, Expression.subtract(q, p))
        else:
            self.check(result, digits, Expression.subtract(p, q))

    def multiply(self, p, q, digits):
        self.check(p * q, digits, Expression.multiply(p, q))

    def divide(self, p, q, digits):
        quotient = p / q
        if quotient < 1:
            self.check(quotient ** -1, digits, Expression.divide(q, p))
            self.check(quotient, digits, Expression.divide(p, q))
        else:
            self.check(quotient, digits, Expression.divide(p, q))
            self.check(quotient ** -1, digits, Expression.divide(q, p))

    def factorial_divide(self, p, q, digits):
        if p == q or not self.integer_check(p) or not self.integer_check(q):
            return
        x = int(p)
        y = int(q)
        if x < y:
            x, y = y, x
            p, q = q, p
        if x <= self.MAX_FACTORIAL or y <= 2 or x - y == 1 or (
            (x - y) * (math.log2(x) + math.log2(y)) > self.MAX_DIGITS << 1
        ):
            return
        result = reduce(operator.mul, range(x, y, -1))
        p_factorial = Expression.factorial(p)
        q_factorial = Expression.factorial(q)
        self.check(self.constructor(result), digits, Expression.divide(p_factorial, q_factorial))
        if digits != self.max_depth and self.solutions[q][0] == 1:
            self.check(self.constructor(result - 1), digits + 1, Expression.divide(
                Expression.subtract(p_factorial, q_factorial),
                q_factorial
            ))
            self.check(self.constructor(result + 1), digits + 1, Expression.divide(
                Expression.add(p_factorial, q_factorial),
                q_factorial
            ))

    @abstractmethod
    def exponent(self, p, q, digits):
        pass

    @abstractmethod
    def sqrt(self, x, digits):
        pass

    def factorial(self, x, digits):
        if int(x) <= self.MAX_FACTORIAL:
            y = self.constructor(factorial(int(x)))
            self.check(y, digits, Expression.factorial(x))

    def binary_operation(self, p, q, digits):
        self.add(p, q, digits)
        self.subtract(p, q, digits)
        self.multiply(p, q, digits)
        self.divide(p, q, digits)
        self.exponent(p, q, digits)
        self.exponent(q, p, digits)

    def binary_generator(self, digits):
        for d1 in range(1, (digits + 1) >> 1):
            d2 = digits - d1
            yield from product(self.visited[d1], self.visited[d2])
        if digits & 1 == 0:
            yield from combinations_with_replacement(self.visited[digits >> 1], 2)

    def search(self, digits):
        if digits not in self.visited:
            self.visited.append([])
        self.concat(digits)
        for p, q in self.binary_generator(digits):
            self.binary_operation(p, q, digits)
        for p, q in self.binary_generator(digits):
            self.factorial_divide(p, q, digits)

    def solve(self, *, max_depth = None):
        self.max_depth = max_depth
        for digits in count(1):
            if digits - 1 == max_depth:
                return
            if global_config["verbose"]:
                print(digits)
            try:
                self.search(digits)
            except SolutionFoundError:
                return digits

    def printer(self, n):
        digits, expression = self.solutions[n]
        string = str(digits) + ": " + str(n)
        if expression.name == "concat":
            return string
        else:
            return string + " = " + Expression.str(expression, spaces = True)

    def solution_prettyprint(self, n, *, force_print = False):
        def requirements(expression):
            if type(expression) is Expression:
                return chain(*map(requirements, expression.args))
            else:
                return (expression,)

        if n in self.number_printed or n not in self.solutions:
            return []
        digits, expression = self.solutions[n]
        if expression.name == "concat" and not force_print:
            return []
        solution_list = [self.printer(n)]
        self.number_printed.add(n)
        for x in requirements(expression):
            solution_list += self.solution_prettyprint(x)
        return solution_list

    def full_expression(self, n):
        if type(n) is Expression:
            return Expression(n.name, *map(self.full_expression, n.args))
        _, expression = self.solutions[n]
        if expression.name == "concat":
            return n
        else:
            return Expression(expression.name, *map(self.full_expression, expression.args))
