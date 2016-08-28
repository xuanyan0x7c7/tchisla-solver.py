__all__ = ["Expression"]

class Expression:
    __slots__ = ("name", "args")

    def __init__(self, name = None, *args):
        self.name = name
        self.args = tuple(args)

    def __str__(self):
        if not self.args:
            return ""
        elif len(self.args) == 1:
            arg = str(self.args[0])
            if self.name == "sqrt":
                return "sqrt(" + arg + ")"
            elif self.name == "factorial":
                return arg + "!"
            elif self.name == "-":
                return "-" + arg
        else:
            return (" " + self.name + " ").join(map(str, self.args))
