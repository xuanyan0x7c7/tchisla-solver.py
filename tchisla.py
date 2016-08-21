import math
from itertools import count, product
from utils import sqrt, factorial

MAX = 1 << 128
MAX_DIGITS = 128
MAX_CONCAT = 39
MAX_FACTORIAL = 34

formatters = {
    "print": "{depth}: {n}",
    "sqrt": "{depth}: {n} = sqrt({op1})",
    "factorial": "{depth}: {n} = {op1}!",
    "binary": "{depth}: {n} = {op1} {method} {op2}"
}

class Tchisla:
    def __init__(self, n, target):
        self.n = n
        self.target = target
        self.solutions = {}
        self.visited = [[]]
        self.number_printed = set()

    def insert(self, x, depth, method, op1, op2):
        self.solutions[x] = depth, method, op1, op2
        self.visited[depth].append(x)
        if x == self.target:
            self.solution_found(self.target, True)
            return True

    def check(self, x, depth, method, op1, op2):
        if x > MAX or x in self.solutions:
            return
        if self.insert(x, depth, method, op1, op2):
            return True
        y = sqrt(x)
        if y and self.check(y, depth, "sqrt", x, None):
            return True
        if x <= MAX_FACTORIAL:
            y = factorial(x)
            if self.check(y, depth, "factorial", x, None):
                return True

    def binary(self, p, q, depth):
        if self.check(p + q, depth, "+", p, q):
            return True
        if p > q:
            if self.check(p - q, depth, "-", p, q):
                return True
        elif p < q:
            if self.check(q - p, depth, "-", q, p):
                return True
        if self.check(p * q, depth, "*", p, q):
            return True
        if p % q == 0 and self.check(p // q, depth, "/", p, q):
            return True
        if q % p == 0 and self.check(q // p, depth, "/", q, p):
            return True
        if math.log2(p) * q <= MAX_DIGITS:
            if self.check(p ** q, depth, "^", p, q):
                return True
        if math.log2(q) * p <= MAX_DIGITS:
            if self.check(q ** p, depth, "^", q, p):
                return True

    def search(self, depth = 1):
        self.visited.append([])
        if depth <= MAX_CONCAT:
            m = (10 ** depth - 1) // 9 * self.n
            if self.check(m, depth, "concat", None, None):
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

    def printer(self, n, style):
        depth, method, op1, op2 = self.solutions[n]
        print(formatters[style].format(
            n = n, depth = depth, method = method, op1 = op1, op2 = op2
        ))

    def solution_found(self, n, force_print = False):
        if n in self.number_printed:
            return
        _, method, op1, op2 = self.solutions[n]
        if method == "concat" and not force_print:
            return
        else:
            self.number_printed.add(n)
        if method == "concat":
            self.printer(n, "print")
        elif method in ("sqrt", "factorial"):
            self.printer(n, method)
            self.solution_found(op1)
        else:
            self.printer(n, "binary")
            self.solution_found(op1)
            self.solution_found(op2)
