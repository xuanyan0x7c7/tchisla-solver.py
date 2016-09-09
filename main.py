#!/usr/bin/env python3

import re
from argparse import ArgumentParser
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

def general_solver(n, target, options):
    max_depth = options.max_depth
    solver_type = options.solver
    verbose = options.verbose
    depth = max_depth and max_depth + 1
    solution = None
    for solver in solvers[solver_type]:
        if not solver["regex"].match(target):
            continue
        current_target = solver["constructor"](target)
        tchisla = solver["solver"](n, current_target, verbose)
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

def solve(string, options):
    if "#" in string:
        array = string.split("#")
        if len(array) == 2:
            target = array[0]
            n = array[1]
            if integral_re.match(n) and number_re.match(target):
                n = int(n)
                print(str(target) + " # " + str(n))
                general_solver(n, target, options)
    elif number_re.match(string):
        for n in range(1, 10):
            print(str(string) + " # " + str(n))
            general_solver(n, string, options)

def main():
    parser = ArgumentParser()
    parser.add_argument('--solver',
        default='incremental',
        type=str,
        choices=list(solvers.keys()),
        help='choose a solver'
    )
    parser.add_argument('-d', '--max-depth',
        type=int,
        help='max search depth'
    )
    parser.add_argument('-v', '--verbose',
        action='store_true',
        default=False,
        help='enable detailed output'
    )
    parser.add_argument('problem',
        nargs='+',
        help='problem to solve'
    )
    options = parser.parse_args()
    problem_list = options.problem
    for problem in problem_list:
        solve(problem, options)

if __name__ == "__main__":
    main()
