import random


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def inverse(x, y):
    gcd, inv, _ = extended_gcd(x, y)
    if gcd != 1:
        raise ValueError("Решать нельзя, НОД != 1")
    return inv


def add_points(P1, P2, a, p):
    if P1 is None:
        return P2

    if P2 is None:
        return P1

    x1, y1 = P1
    x2, y2 = P2

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P1 == P2:
        denominator = (2 * y1) % p
        if denominator == 0:
            return None
        numerator = (3 * x1**2 + a) % p
    else:
        denominator = (x2 - x1) % p
        numerator = (y2 - y1) % p

    slope = (numerator * inverse(denominator, p)) % p

    x3 = (slope**2 - x1 - x2) % p
    y3 = (-y1 + slope * (x1 - x3)) % p

    return x3, y3


def multiply(n, P, a, p):
    R = None
    for bit in bin(n)[2:]:
        R = add_points(R, R, a, p)
        if bit == "1":
            R = add_points(R, P, a, p)
    return R


def point_order(G, a, p):
    n, R = 1, G
    while R is not None:
        R = add_points(R, G, a, p)
        n += 1
    return n


def el_gamal_encrypt(Pm, k, G, Q, a, p):
    return multiply(k, G, a, p), add_points(Pm, multiply(k, Q, a, p), a, p)


def el_gamal_decrypt(C1, C2, d, a, p):
    S = multiply(d, C1, a, p)
    return C2 if S is None else add_points(C2, (S[0], -S[1] % p), a, p)


def main():
    p = int(input("Введите модуль p: "))
    a, b = map(int, input("Введите коэффициенты a и b: ").split())
    G = tuple(map(int, input("Введите точку G, x и y: ").split()))
    coords = list(map(int, input("Введите точки Pm: x1 y1 x2 y2 ...: ").split()))
    messages = list(zip(coords[::2], coords[1::2]))

    n = point_order(G, a, p)
    d = random.randint(2, n - 1)
    Q = multiply(d, G, a, p)

    encrypted = [el_gamal_encrypt(Pm, random.randint(2, n - 1), G, Q, a, p) for Pm in messages]
    decrypted = [el_gamal_decrypt(C1, C2, d, a, p) for C1, C2 in encrypted]

    print("Зашифровано:", encrypted)
    print("Расшифровано:", decrypted)


if __name__ == "__main__":
    main()