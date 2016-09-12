__all__ = ["Expression"]

class Expression:
    __slots__ = ("name", "args")

    def __init__(self, name, *args):
        self.name = name
        self.args = tuple(args)

    def __str__(self):
        if self.name == "concat":
            return str(self.args[0])
        elif len(self.args) == 1:
            if self.name == "sqrt":
                sqrt_depth = 1
                arg = self.args[0]
                while type(arg) is Expression and arg.name == "sqrt":
                    sqrt_depth += 1
                    arg = arg.args[0]
                return "s" * sqrt_depth + "qrt(" + str(arg) + ")"
            elif self.name == "factorial":
                return str(self.args[0]) + "!"
            elif self.name == "-":
                return "-" + str(self.args[0])
        else:
            return (" " + self.name + " ").join(map(str, self.args))
