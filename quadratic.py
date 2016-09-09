import sys
import numbers
import operator
from itertools import starmap
from functools import reduce
from gmpy2 import mpz, mpq as Fraction, is_square, isqrt

__all__ = ["Quadratic"]

primes = (2, 3, 5, 7)

def exp2(n):
    return {1: 0, 3: 1, 7: 2, 15: 3}[n ^ (n - 1)]

_PyHASH_MODULUS = sys.hash_info.modulus

mpz_type = type(mpz())
mpq_type = type(Fraction())

class Quadratic(numbers.Real):
    __slots__ = ("rational_part", "quadratic_power", "quadratic_part")

    def __new__(cls, rational_part = Fraction(), quadratic_power = 0, quadratic_part = None):
        self = super(Quadratic, cls).__new__(cls)
        if type(rational_part) is str:
            rational_part = Fraction(rational_part)
        if isinstance(rational_part, (int, mpz_type, mpq_type)):
            self.rational_part = Fraction(rational_part)
            self.quadratic_power = quadratic_power
            self.quadratic_part = quadratic_part
            return self
        elif isinstance(rational_part, Quadratic):
            self.rational_part = rational_part.rational_part
            self.quadratic_power = rational_part.quadratic_power
            self.quadratic_part = rational_part.quadratic_part
            return self
        else:
            raise NotImplementedError

    def __str__(self):
        if self.quadratic_part:
            q = reduce(operator.mul, starmap(operator.pow, zip(primes, self.quadratic_part)))
            quadratic_part_string = "s" * self.quadratic_power + "qrt(" + str(q) + ")"
            if self.rational_part == 1:
                return quadratic_part_string
            elif self.rational_part == -1:
                return "-" + quadratic_part_string
            else:
                return str(self.rational_part) + "*" + quadratic_part_string
        else:
            return str(self.rational_part)

    __repr__ = __str__

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        def forward(a, b):
            if isinstance(b, (int, mpz_type, mpq_type, Quadratic)):
                return monomorphic_operator(a, Quadratic(b))
            else:
                return NotImplemented

        def reverse(b, a):
            if isinstance(a, (int, mpz_type, mpq_type, Quadratic)):
                return monomorphic_operator(a, Quadratic(b))
            else:
                return NotImplemented

        return forward, reverse

    def _add(x, y):
        if x.quadratic_power == y.quadratic_power and x.quadratic_part == y.quadratic_part:
            if x.rational_part + y.rational_part == 0:
                return Quadratic()
            else:
                return Quadratic(x.rational_part + y.rational_part, x.quadratic_power, x.quadratic_part)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(x, y):
        if x.quadratic_power == y.quadratic_power and x.quadratic_part == y.quadratic_part:
            if x.rational_part == y.rational_part:
                return Quadratic()
            else:
                return Quadratic(x.rational_part - y.rational_part, x.quadratic_power, x.quadratic_part)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(x, y):
        r = x.rational_part * y.rational_part
        if x.quadratic_power == 0:
            return Quadratic(r, y.quadratic_power, y.quadratic_part)
        if y.quadratic_power == 0:
            return Quadratic(r, x.quadratic_power, x.quadratic_part)

        p = x.quadratic_part
        q = y.quadratic_part
        quadratic_power = max(x.quadratic_power, y.quadratic_power)
        exp_quadratic_power = 1 << quadratic_power
        shifts = quadratic_power - x.quadratic_power, quadratic_power - y.quadratic_power
        prime_power_list = []
        mask = 0
        for index in range(len(primes)):
            power = (p[index] << shifts[0]) + (q[index] << shifts[1])
            if power >= exp_quadratic_power:
                r *= primes[index]
                power -= exp_quadratic_power
            prime_power_list.append(power)
            mask |= power
        if mask == 0:
            return Quadratic(r)
        mask_shift = exp2(mask)
        return Quadratic(
            r,
            quadratic_power - mask_shift,
            tuple(n >> mask_shift for n in prime_power_list)
        )

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _div(x, y):
        r = x.rational_part / y.rational_part
        if y.quadratic_power == 0:
            return Quadratic(r, x.quadratic_power, x.quadratic_part)

        p = x.quadratic_part or (0,) * len(primes)
        q = y.quadratic_part
        quadratic_power = max(x.quadratic_power, y.quadratic_power)
        exp_quadratic_power = 1 << quadratic_power
        shifts = quadratic_power - x.quadratic_power, quadratic_power - y.quadratic_power
        prime_power_list = []
        mask = 0
        for index in range(len(primes)):
            power = (p[index] << shifts[0]) - (q[index] << shifts[1])
            if power < 0:
                r /= primes[index]
                power += exp_quadratic_power
            prime_power_list.append(power)
            mask |= power
        if mask == 0:
            return Quadratic(r)
        mask_shift = exp2(mask)
        return Quadratic(
            r,
            quadratic_power - mask_shift,
            tuple(n >> mask_shift for n in prime_power_list)
        )

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def __float__(x):
        raise NotImplementedError

    def __floordiv__(x, y):
        raise NotImplementedError

    def __rfloordiv__(x, y):
        raise NotImplementedError

    def __mod__(x, y):
        raise NotImplementedError

    def __rmod__(x, y):
        raise NotImplementedError

    def inverse(x):
        r = x.rational_part ** -1
        q = x.quadratic_part
        if x.quadratic_power == 0:
            return Quadratic(r)
        prime_base = 1
        prime_power_list = []
        for index in range(len(primes)):
            if q[index]:
                r /= primes[index]
                prime_power_list.append((1 << x.quadratic_power) - q[index])
            else:
                prime_power_list.append(0)
        return Quadratic(r, x.quadratic_power, tuple(prime_power_list))

    def __pow__(x, y):
        power = None
        inverse = False
        if isinstance(y, (int, mpz_type)):
            power = abs(y)
            inverse = y < 0
        elif y.quadratic_power == 0 and y.rational_part.denominator == 1:
            power = abs(y.rational_part.numerator)
            inverse = y.rational_part.numerator < 0
        else:
            raise NotImplementedError

        if power == 0:
            return Quadratic(1)
        r = x.rational_part ** power
        if x.quadratic_power == 0:
            return Quadratic(r ** -1) if inverse else Quadratic(r)
        quadratic_power = x.quadratic_power
        while quadratic_power and power & 1 == 0:
            quadratic_power -= 1
            power >>= 1
        exp_quadratic_power = 1 << quadratic_power
        prime_power_list = []
        for index in range(len(primes)):
            p = x.quadratic_part[index] * power
            r *= primes[index] ** (p // exp_quadratic_power)
            prime_power_list.append(p % exp_quadratic_power)
        result = None
        if quadratic_power == 0:
            result = Quadratic(r)
        else:
            result = Quadratic(r, quadratic_power, tuple(prime_power_list))
        return result.inverse() if inverse else result

    def __rpow__(x, y):
        raise NotImplementedError

    @staticmethod
    def sqrt(x):
        p = x.rational_part
        s, t = p.numerator, p.denominator
        q = x.quadratic_part
        if p == 0:
            return Quadratic()
        elif p < 0:
            raise NotImplementedError
        elif x.quadratic_power == 0:
            if is_square(s) and is_square(t):
                return Quadratic(Fraction(isqrt(s), isqrt(t)))
            else:
                q = (0,) * len(primes)

        r = Fraction(1, t)
        p = s * t
        prime_power_list = []
        for index in range(len(primes)):
            prime = primes[index]
            power = 0
            while p % prime == 0:
                p //= prime
                power += 1
            r *= prime ** (power >> 1)
            prime_power_list.append(((power & 1) << x.quadratic_power) | q[index])
        if not is_square(p):
            return
        return Quadratic(r * isqrt(p), x.quadratic_power + 1, tuple(prime_power_list))

    def __pos__(x):
        return Quadratic(x.rational_part, x.quadratic_power, x.quadratic_part)

    def __neg__(x):
        return Quadratic(-x.rational_part, x.quadratic_power, x.quadratic_part)

    def __abs__(x):
        return Quadratic(abs(x.rational_part), x.quadratic_power, x.quadratic_part)

    def __int__(x):
        if x.quadratic_power == 0 and x.rational_part.denominator == 1:
            return int(x.rational_part.numerator)

    def __trunc__(x):
        raise NotImplementedError

    def __floor__(x):
        raise NotImplementedError

    def __ceil__(x):
        raise NotImplementedError

    def __round__(x):
        raise NotImplementedError

    def __hash__(self):
        if self.quadratic_power == 0:
            return hash(self.rational_part)
        else:
            return hash(self.rational_part) * hash(self.quadratic_power) * hash(self.quadratic_part) % _PyHASH_MODULUS

    def __eq__(x, y):
        if isinstance(y, (int, mpz_type, mpq_type)):
            return x.quadratic_power == 0 and x.rational_part == y
        elif isinstance(y, Quadratic):
            return x.rational_part == y.rational_part and x.quadratic_power == y.quadratic_power and x.quadratic_part == y.quadratic_part
        else:
            return NotImplemented

    def __lt__(x, y):
        raise NotImplementedError

    def __gt__(x, y):
        raise NotImplementedError

    def __le__(x, y):
        raise NotImplementedError

    def __ge__(x, y):
        raise NotImplementedError

    def __bool__(x):
        return x.rational_part != 0

    def __reduce__(self):
        return (self.__class__, (str(self),))

    def __copy__(self):
        if type(self) is Quadratic:
            return self
        return self.__class__(self)

    def __deepcopy__(self):
        if type(self) is Quadratic:
            return self
        return self.__class__(self)
