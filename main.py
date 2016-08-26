#!/usr/bin/python3

import sys
import re
from tchisla import Tchisla

number_re = re.compile("^\\d+$")
tchisla_re = re.compile("^\\d+#\\d$")

def problem_printer(n, target):
    print("{target} # {n}".format(target = target, n = n))

def solve(string):
    if number_re.match(string):
        target = int(string)
        for n in range(1, 10):
            problem_printer(n, target)
            tchisla = Tchisla(n, target)
            tchisla.solve()
            tchisla.print_solution(target, True)
    elif tchisla_re.match(string):
        target, n = tuple(map(int, string.split("#")))
        problem_printer(n, target)
        tchisla = Tchisla(n, target)
        tchisla.solve()
        tchisla.print_solution(target, True)

if __name__ == "__main__":
    for string in sys.argv[1:]:
        solve(string)
