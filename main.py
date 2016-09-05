#!/usr/bin/python3

import sys
import re
from gmpy2 import mpq as Fraction
from solver.integral import IntegralTchisla
from solver.rational import RationalTchisla

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
    "incremental": [
        {"regex": integral_re, "constructor": int, "solver": IntegralTchisla},
        {"regex": rational_re, "constructor": Fraction, "solver": RationalTchisla}
    ]
}

def general_solver(n, target, solver_type):
    depth = None
    solution = None
    for solver in solvers[solver_type]:
        if not solver["regex"].match(target):
            continue
        current_target = solver["constructor"](target)
        tchisla = solver["solver"](n, current_target)
        max_depth = depth
        original_solution = solution
        depth = tchisla.solve(max_depth)
        solution = tchisla.solution_prettyprint(current_target, True)
        if not solution:
            depth = max_depth
            solution = original_solution
            continue
        if original_solution:
            print("=" * 20)
        for string in solution:
            print(string)

def solve(string, solver_type):
    if "#" in string:
        array = string.split("#")
        if len(array) == 2:
            target = array[0]
            n = array[1]
            if integral_re.match(n) and number_re.match(target):
                n = int(n)
                print(str(target) + " # " + str(n))
                general_solver(n, target, solver_type)
    elif number_re.match(string):
        for n in range(1, 10):
            print(str(string) + " # " + str(n))
            general_solver(n, string, solver_type)

def main(argv):
    if argv[0][:2] == "--":
        for string in argv[1:]:
            solve(string, argv[0][2:])
    else:
        for string in argv:
            solve(string, "incremental")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
