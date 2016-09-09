#!/usr/bin/env python3

import sys
import re
from gmpy2 import mpq as Fraction
from quadratic import Quadratic
from solver.integral import IntegralTchisla
from solver.rational import RationalTchisla
from solver.quadratic import QuadraticTchisla

integral_re = re.compile("^\\d+$")
rational_re = re.compile("^\\d+(/\\d+)?$")
number_re = rational_re

solvers = {
    "integral": [
        {"regex": integral_re, "constructor": int, "solver": IntegralTchisla}
    ],
    "rational": [
        {"regex": rational_re, "constructor": Fraction, "solver": RationalTchisla}
    ],
    "quadratic": [
        {"regex": rational_re, "constructor": Quadratic, "solver": QuadraticTchisla}
    ],
    "incremental": [
        {"regex": integral_re, "constructor": int, "solver": IntegralTchisla},
        {"regex": rational_re, "constructor": Fraction, "solver": RationalTchisla}
    ]
}

def general_solver(n, target, solver_type, max_depth = None):
    depth = max_depth and max_depth + 1
    solution = None
    for solver in solvers[solver_type]:
        if not solver["regex"].match(target):
            continue
        current_target = solver["constructor"](target)
        tchisla = solver["solver"](n, current_target)
        max_depth = depth
        depth = tchisla.solve(max_depth)
        if depth is None:
            depth = max_depth
            continue
        if solution:
            print("=" * 20)
        solution = tchisla.solution_prettyprint(current_target, True)
        for string in solution:
            print(string)

def solve(string, solver_type, max_depth = None):
    if "#" in string:
        array = string.split("#")
        if len(array) == 2:
            target = array[0]
            n = array[1]
            if integral_re.match(n) and number_re.match(target):
                n = int(n)
                print(str(target) + " # " + str(n))
                general_solver(n, target, solver_type, max_depth)
    elif number_re.match(string):
        for n in range(1, 10):
            print(str(string) + " # " + str(n))
            general_solver(n, string, solver_type, max_depth)

def main(argv):
    solver = "incremental"
    max_depth = None
    problem_list = []
    for arg in argv:
        if arg[:9] == "--solver=":
            solver = arg[9:]
        elif arg[:12] == "--max-depth=":
            max_depth = int(arg[12:])
        else:
            problem_list.append(arg)
    for problem in problem_list:
        solve(problem, solver, max_depth)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
