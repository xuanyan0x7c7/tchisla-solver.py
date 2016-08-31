import math;

__all__ = ["sqrt", "factorial"]

perfect_square_mask = {
    11: "11011100010",
    63: "110010010100000010100010010010000000110000010010010000000010000",
    64: "1100100001000000110000000100000001001000010000000100000001000000",
    65: "11001000011000101000000001100110000110011000000001010001100001001"
}

for n in perfect_square_mask:
    perfect_square_mask[n] = tuple(x == "1" for x in perfect_square_mask[n])

MAX_SAFE_INTEGER = 1 << 53

def sqrt(n):
    if n <= MAX_SAFE_INTEGER:
        x = int(math.sqrt(n))
        if x ** 2 == n:
            return x
        else:
            return

    if not perfect_square_mask[64][n & 63]:
        return
    m = n % 45045
    if (not perfect_square_mask[11][m % 11]) or (
        not perfect_square_mask[63][m % 63]) or (
        not perfect_square_mask[65][m % 65]):
        return

    l = n.bit_length()
    if l & 1 and n & (n - 1) == 0:
        return 1 << (l >> 1)
    x = n
    y = 1 << ((l + 1) >> 1)
    while x > y:
        x, y = y, (y + n // y) >> 1
    if x ** 2 == n:
        return x
    else:
        return

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
