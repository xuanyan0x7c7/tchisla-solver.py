__all__ = ["Expression"]

tchisla_operators = {
    "+": {"precedence": 1, "abelian": True},
    "-": {"precedence": 1, "abelian": False},
    "negate": {"precedence": 2, "abelian": False},
    "*": {"precedence": 3, "abelian": True},
    "/": {"precedence": 3, "abelian": False},
    "^": {"precedence": 4, "abelian": False},
    "factorial": {"precedence": 5, "abelian": False},
    "sqrt": {"precedence": 6, "abelian": True},
    "number": {"precedence": 7, "abelian": False},
    "concat": {"precedence": 7, "abelian": False}
}

class Expression:
    __slots__ = ("name", "args")

    def __init__(self, name, *args):
        self.name = name
        self.args = tuple(args)

    def __str__(self):
        return Expression.str(self)

    @staticmethod
    def str(expression, *, spaces = False):
        if type(expression) is not Expression:
            return str(expression)
        elif expression.name == "concat":
            return str(expression.args[0])
        elif len(expression.args) == 1:
            arg = expression.args[0]
            string = Expression.str(arg, spaces = spaces)
            if expression.name == "sqrt":
                sqrt_depth = 1
                while Expression.type(arg) == "sqrt":
                    sqrt_depth += 1
                    arg = arg.args[0]
                string = Expression.str(arg, spaces = spaces)
                return "s" * sqrt_depth + "qrt(" + string + ")"
            elif expression.name == "factorial":
                if Expression.type(arg) in ("number", "concat", "sqrt"):
                    return string + "!"
                else:
                    return "(" + string + ")!"
            elif expression.name == "negate":
                if Expression.type(arg) in ("+", "-"):
                    return "-(" + string + ")"
                else:
                    return "-" + string
            else:
                raise NotImplementedError
        else:
            delimiter = " " + expression.name + " " if spaces else expression.name
            op2 = tchisla_operators[expression.name]
            def mapping(arg):
                index, arg = arg
                string = Expression.str(arg, spaces = spaces)
                op1 = tchisla_operators[Expression.type(arg)]
                need_brackets = op1["precedence"] < op2["precedence"]
                if index > 0 and op1["precedence"] == op2["precedence"] and not op2["abelian"]:
                    need_brackets = True
                if need_brackets:
                    return "(" + string + ")"
                else:
                    return string
            return delimiter.join(map(mapping, enumerate(expression.args)))

    @staticmethod
    def type(expression):
        return expression.name if type(expression) is Expression else "number"

    @staticmethod
    def concat(x):
        return Expression("concat", x)

    @staticmethod
    def add(*args):
        return Expression("+", *args)

    @staticmethod
    def subtract(x, y):
        return Expression("-", x, y)

    @staticmethod
    def multiply(*args):
        return Expression("*", *args)

    @staticmethod
    def divide(x, y):
        return Expression("/", x, y)

    @staticmethod
    def power(x, y):
        return Expression("^", x, y)

    @staticmethod
    def negate(x):
        return Expression("negate", x)

    @staticmethod
    def sqrt(x):
        return Expression("sqrt", x)

    @staticmethod
    def factorial(x):
        return Expression("factorial", x)
