import math;

perfect_square_mask = {
    11: "11011100010",
    63: "110010010100000010100010010010000000110000010010010000000010000",
    64: "1100100001000000110000000100000001001000010000000100000001000000",
    65: "11001000011000101000000001100110000110011000000001010001100001001"
}

for n in perfect_square_mask:
    perfect_square_mask[n] = set(map(
        lambda p: p[0],
        filter(lambda p: p[1] == "1", enumerate(perfect_square_mask[n]))
    ))

MAX_SAFE_INTEGER = 1 << 53

def sqrt(n):
    if n <= MAX_SAFE_INTEGER:
        x = math.sqrt(n)
        if x == int(x):
            return int(x)
        else:
            return None

    if (n & 63 not in perfect_square_mask[64]) or (
        n % 11 not in perfect_square_mask[11]) or (
        n % 63 not in perfect_square_mask[63]) or (
        n % 65 not in perfect_square_mask[65]):
        return None

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
        return None

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
