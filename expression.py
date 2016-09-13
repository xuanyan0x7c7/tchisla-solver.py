__all__ = ["Expression"]

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
            if expression.name == "sqrt":
                sqrt_depth = 1
                arg = expression.args[0]
                while type(arg) is Expression and arg.name == "sqrt":
                    sqrt_depth += 1
                    arg = arg.args[0]
                return "s" * sqrt_depth + "qrt(" + Expression.str(arg, spaces = spaces) + ")"
            elif expression.name == "factorial":
                return Expression.str(expression.args[0], spaces = spaces) + "!"
            elif expression.name == "-":
                return "-" + Expression.str(expression.args[0], spaces = spaces)
        else:
            delimiter = " " + expression.name + " " if spaces else expression.name
            return delimiter.join(map(
                lambda s: Expression.str(s, spaces = spaces),
                expression.args
            ))

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
        return Expression("-", x)

    @staticmethod
    def sqrt(x):
        return Expression("sqrt", x)

    @staticmethod
    def factorial(x):
        return Expression("factorial", x)
