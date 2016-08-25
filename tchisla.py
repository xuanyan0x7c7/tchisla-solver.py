import math
from fractions import Fraction
from itertools import count, product
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
        if z:
            y = sqrt(x.numerator)
            if y and self.check(Fraction(y, z, False), depth, ("sqrt", x)):
                return True
        if x.denominator == 1 and x <= MAX_FACTORIAL:
            y = Fraction(factorial(int(x)))
            if self.check(y, depth, ("factorial", x)):
                return True

    def binary(self, p, q, depth):
        if self.check(p + q, depth, ("+", p, q)):
            return True
        if p > q:
            if self.check(p - q, depth, ("-", p, q)):
                return True
        elif p < q:
            if self.check(q - p, depth, ("-", q, p)):
                return True
        if self.check(p * q, depth, ("*", p, q)):
            return True
        if self.check(p / q, depth, ("/", p, q)):
            return True
        if self.check(q / p, depth, ("/", q, p)):
            return True
        if q.denominator == 1 and p != 1:
            p_digits = math.log2(max(p.numerator, p.denominator))
            q_int = q.numerator
            exp = (("^", p, q), ("^", p, -q))
            q2 = q
            while p_digits * q_int > MAX_DIGITS:
                if q_int & 1 == 0:
                    q_int >>= 1
                    exp = (("sqrt", exp[0]), ("sqrt", exp[1]))
                else:
                    break
            else:
                x = p ** q_int
                if self.check(x, depth, exp[0]):
                    return True
                if self.check(x ** -1, depth, exp[1]):
                    return True
        if p.denominator == 1 and q != 1:
            q_digits = math.log2(max(q.numerator, q.denominator))
            p_int = p.numerator
            exp = (("^", q, p), ("^", q, -p))
            while q_digits * p_int > MAX_DIGITS:
                if p_int & 1 == 0:
                    p_int >>= 1
                    exp = (("sqrt", exp[0]), ("sqrt", exp[1]))
                else:
                    break
            else:
                x = q ** p_int
                if self.check(x, depth, exp[0]):
                    return True
                if self.check(x ** -1, depth, exp[1]):
                    return True

    def search(self, depth = 1):
        self.visited.append([])
        if depth <= MAX_CONCAT:
            m = Fraction((10 ** depth - 1) // 9 * self.n)
            if self.check(m, depth, ("concat",)):
                return True
        for d1 in range(1, (depth + 1) >> 1):
            d2 = depth - d1
            for p, q in product(self.visited[d1], self.visited[d2]):
                if self.binary(p, q, depth):
                    return True
        if depth & 1 == 0:
            v = self.visited[depth >> 1]
            length = len(v)
            for i in range(length):
                for j in range(i, length):
                    if self.binary(v[i], v[j], depth):
                        return True

    def solve(self):
        for depth in count(1):
            if self.search(depth):
                return

    def number_printer(self, n):
        if type(n) is tuple:
            if len(n) == 2:
                if n[0] == "sqrt":
                    return "sqrt(" + self.number_printer(n[1]) + ")"
                elif n[0] == "-":
                    return "-" + self.number_printer(n[1])
            else:
                return self.number_printer(n[1]) + n[0] + self.number_printer(n[2])
        else:
            return str(n)

    def printer(self, n):
        if type(n) is tuple:
            return self.number_printer(n)
        else:
            depth, expression = self.solutions[n]
            string = str(depth) + ": " + str(n)
            if len(expression) == 1:
                return string
            elif len(expression) == 2:
                method, operator = expression
                if method == "sqrt":
                    return string + " = sqrt(" + self.number_printer(operator) + ")"
                elif method == "factorial":
                    return string + " = " + str(operator) + "!"
            else:
                method, op1, op2 = expression
                return string + " = " + self.number_printer(op1) + " " + method + " " + self.number_printer(op2)

    def number_dfs(self, expression):
        if type(expression) is tuple:
            l = []
            for operator in expression[1:]:
                l += self.number_dfs(operator)
            return l
        else:
            return [expression]

    def solution_found(self, n, force_print = False):
        if n in self.number_printed:
            return
        depth, expression = self.solutions[n]
        if len(expression) > 1 or force_print:
            print(self.printer(n))
            self.number_printed.add(n)
            for x in self.number_dfs(expression):
                self.solution_found(x)
