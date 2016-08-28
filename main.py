#!/usr/bin/python3

import sys
import re
from fractions import Fraction
from solver.integer import IntegerTchisla
from solver.rational import RationalTchisla

integer_re = re.compile("^\\d+")
rational_re = re.compile("^\\d+(/\\d+)?$")

def integer_solver(n, target):
    if not integer_re.match(target):
        return
    target = int(target)
    print(str(target) + " # " + str(n))
    tchisla = IntegerTchisla(n, target)
    tchisla.solve()
    for string in tchisla.solution_prettyprint(target, True):
        print(string)

def rational_solver(n, target):
    if not rational_re.match(target):
        return
    target = Fraction(target)
    print(str(target) + " # " + str(n))
    tchisla = RationalTchisla(n, target)
    tchisla.solve()
    for string in tchisla.solution_prettyprint(target, True):
        print(string)

def incremental_solver(n, target):
    if not rational_re.match(target):
        return
    target = Fraction(target)
    print(str(target) + " # " + str(n))
    max_depth = None
    solution_list = []
    if target.denominator == 1:
        integer_target = int(target)
        tchisla = IntegerTchisla(n, integer_target)
        max_depth = tchisla.solve()
        solution_list = tchisla.solution_prettyprint(integer_target, True)
        for string in solution_list:
            print(string)
    tchisla = RationalTchisla(n, target)
    max_depth = tchisla.solve(max_depth)
    rational_solution_list = tchisla.solution_prettyprint(target, True)
    if rational_solution_list:
        if solution_list:
            print("=" * 20)
        solution_list = rational_solution_list
        for string in solution_list:
            print(string)

def general_solver(n, target, solver_type):
    solver_map = {
        "integer": integer_solver,
        "rational": rational_solver,
        "incremental": incremental_solver
    }
    solver_map[solver_type](n, target)

def solve(string, solver_type):
    if "#" in string:
        array = string.split("#")
        general_solver(int(array[1]), array[0], solver_type)
    else:
        for n in range(1, 10):
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
