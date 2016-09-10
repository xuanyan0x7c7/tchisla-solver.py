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

problems_re = re.compile("^(?:\[(?P<targets>[^\]]*)\]|(?P<target>[1-9]\d*(?:\/[1-9]\d*)?))(?:#(?:\[(?P<digits>[^\]]*)\]|(?P<digit>[1-9])))?$")
targets_re = re.compile("^(?:(?P<target>[1-9]\d*(?:\/[1-9]\d*)?)|(?P<start>[1-9]\d*)-(?P<end>[1-9]\d*))$")
digits_re = re.compile("^(?P<first>[1-9])(?:-(?P<last>[1-9]))?$")

solvers = {
    "integral": {
        "regex": integral_re, "constructor": int, "solver": IntegralTchisla
    },
    "rational": {
        "regex": rational_re, "constructor": Fraction, "solver": RationalTchisla
    },
    "quadratic": {
        "regex": rational_re, "constructor": Quadratic, "solver": QuadraticTchisla
    }
}

def general_solver(n, target, options):
    max_depth = options.max_depth
    verbose = options.verbose
    depth = max_depth and max_depth + 1
    solution = None
    for solver_key in options.solvers:
        solver = solvers[solver_key]
        if not solver["regex"].match(str(target)):
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

def solve(problem, options):
    print(problem[0], '#', problem[1])
    general_solver(problem[1], problem[0], options)

def parse_problems(problems):
    problem_list = []
    for each in problems:
        m = problems_re.match(each)
        if not m:
            continue

        targets = m.group('targets')
        targets = parse_targets(targets) if targets else [to_number(m.group('target'))]

        digits = m.group('digits')
        digit = m.group('digit')
        digits = parse_digits(digits) if digits else [int(digit)] if digit else list(range(1, 10))

        for target in targets:
            for digit in digits:
                problem_list.append((target, digit))
    problem_list = sorted(set(problem_list))

    return problem_list

def to_number(string):
    number = Fraction(string)
    if number.denominator == 1:
        number = int(number)
    return number

def parse_digits(digits):
    digit_list = []
    digits = digits.split(',')
    for each in digits:
        m = digits_re.match(each)
        if not m:
            continue
        first = int(m.group('first'))
        last = m.group('last')
        if last:
            last = int(last)
        if not last:
            last = first
        if first > last:
            first, last = last, first
        digit_list = digit_list + list(range(first, last + 1))
    digit_list = sorted(set(digit_list))
    return digit_list


def parse_targets(targets):
    target_list = []
    targets = targets.split(',')
    for each in targets:
        m = targets_re.match(each)
        if not m:
            continue
        target = m.group('target')
        if target:
            target_list.append(to_number(target))
            continue
        start = int(m.group('start'))
        end = int(m.group('end'))
        if start > end:
            start, end = end, start
        target_list = target_list + list(range(start, end + 1))
    target_list = sorted(set(target_list))
    return target_list



def main():
    default_solvers = ['integral', 'rational']
    parser = ArgumentParser()
    parser.add_argument('-s', '--add-solver',
        dest='solvers',
        action='append',
        choices=list(solvers.keys()),
        help='set solvers list, add one solver each time, the default set is ' + str(default_solvers)
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
        help='problem to solve, examples: "2", "2#5", "[1,3]#8", "[2-4]#[6,7]", "[3-6,125,127]#[2-9]"'
    )
    options = parser.parse_args()
    if not options.solvers:
        options.solvers=default_solvers
    problem_list = parse_problems(options.problem)
    for problem in problem_list:
        solve(problem, options)

if __name__ == "__main__":
    main()
