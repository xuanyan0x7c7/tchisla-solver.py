#!/usr/bin/python3

import sys
import re
from fractions import Fraction
from solver.base import Tchisla

number_re = re.compile("^\\d+(/\\d+)?$")
tchisla_re = re.compile("^\\d+(/\\d+)?#\\d$")

def problem_printer(n, target):
    print("{target} # {n}".format(target = target, n = n))

def solve(string):
    if number_re.match(string):
        target = Fraction(string)
        for n in range(1, 10):
            problem_printer(n, target)
            tchisla = Tchisla(n, target)
            tchisla.solve()
            tchisla.print_solution(target, True)
    elif tchisla_re.match(string):
        array = string.split("#")
        target = Fraction(array[0])
        n = int(array[1])
        problem_printer(n, target)
        tchisla = Tchisla(n, target)
        tchisla.solve()
        tchisla.print_solution(target, True)

if __name__ == "__main__":
    for string in sys.argv[1:]:
        solve(string)
