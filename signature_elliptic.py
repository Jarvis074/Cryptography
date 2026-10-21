def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def inverse(x, y):
    gcd, inv, _ = extended_gcd(x % y, y)
    if gcd != 1:
        raise ValueError("Решать нельзя, НОД != 1")
    return inv % y


def add_points(P1, P2, a, p):
    """Складывает две точки эллиптической кривой."""
    if P1 is None:
        return P2

    if P2 is None:
        return P1

    x1, y1 = P1
    x2, y2 = P2

    # Противоположные точки дают точку на бесконечности O.
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
    """Вычисляет nP методом удвоения и сложения."""
    R = None
    for bit in bin(n)[2:]:
        R = add_points(R, R, a, p)
        if bit == "1":
            R = add_points(R, P, a, p)
    return R


def point_order(G, a, p):
    """Порядок точки G: наименьшее n, при котором nG = O."""
    n, R = 1, G
    while R is not None:
        R = add_points(R, G, a, p)
        n += 1
    return n


def check_point(point, name, a, b, p):
    """Проверяет, что точка лежит на кривой y² ≡ x³ + ax + b (mod p)."""
    x, y = point
    if (y**2 - (x**3 + a * x + b)) % p != 0:
        raise ValueError(f"Точка {name} не лежит на заданной эллиптической кривой.")


def point_to_str(P):
    return "O" if P is None else str(P)


def sign(e, d, k, G, n, a, p):
    """Подписывает хеш e секретным ключом d со случайным числом k."""
    kG = multiply(k, G, a, p)
    if kG is None:
        raise ValueError("kG = O, выберите другое k.")

    x1, y1 = kG
    r = (x1 + e) % n
    s = (k - r * d) % n

    if r == 0 or s == 0:
        raise ValueError("r = 0 или s = 0, выберите другое k.")

    print(f"(x1, y1) = kG = {k}·G = {kG}")
    print(f"r = (x1 + e) mod n = ({x1} + {e}) mod {n} = {r}")
    print(f"s = (k - r·d) mod n = ({k} - {r}·{d}) mod {n} = {s}")

    return r, s


def verify(e, r, s, G, Q, n, a, p):
    """Проверяет подпись (r, s) открытым ключом Q.

    sG + rQ = (k - rd)G + rdG = kG, поэтому x этой точки совпадает с x1.
    """
    if not (1 <= r < n and 1 <= s < n):
        return False

    sG = multiply(s, G, a, p)
    rQ = multiply(r, Q, a, p)
    X = add_points(sG, rQ, a, p)

    print(f"s·G = {point_to_str(sG)}, r·Q = {point_to_str(rQ)}")
    print(f"(x1, y1) = s·G + r·Q = {point_to_str(X)}")

    if X is None:
        return False

    r_check = (X[0] + e) % n
    print(f"r' = (x1 + e) mod n = ({X[0]} + {e}) mod {n} = {r_check}")

    return r_check == r


def main():
    print("Параметры задаются для эллиптической кривой:")
    print("    y² ≡ x³ + a·x + b (mod p)")
    print()
    print("Введите значения:")
    print("  p      — модуль, указанный после mod;")
    print("  a, b   — коэффициенты уравнения кривой;")
    print("  x, y   — координаты базовой точки G = (x, y);")
    print("  M      — подписываемое сообщение;")
    print("  c, q   — степень и простой модуль хеш-функции e = M^c mod q;")
    print("  d      — секретный ключ;")
    print("  k      — случайное число от 1 до n - 1.")
    print()

    p = int(input("Введите модуль p: "))
    a, b = map(int, input("Введите коэффициенты эллиптической кривой a и b: ").split())
    x, y = map(int, input("Введите координаты точки G, x и y: ").split())
    M = int(input("Введите сообщение M: "))
    c, q = map(int, input("Введите степень c и простой модуль q хеш-функции: ").split())
    d, k = map(int, input("Введите секретный ключ d и случайное число k: ").split())

    G = (x % p, y % p)

    check_point(G, "G", a, b, p)

    n = point_order(G, a, p)
    Q = multiply(d, G, a, p)
    e = pow(M, c, q)

    print()
    print(f"Порядок точки G: n = {n}")
    print(f"Открытый ключ Q = d·G = {d}·G = {point_to_str(Q)}")
    print(f"Хеш e = M^c mod q = {M}^{c} mod {q} = {e}")

    print()
    print("Подпись:")
    r, s = sign(e, d, k, G, n, a, p)
    print(f"Подпись (r, s) = ({r}, {s})")

    print()
    print("Проверка:")
    if verify(e, r, s, G, Q, n, a, p):
        print("Подпись верна")
    else:
        print(":(")
        print("Подпись неверна")


if __name__ == "__main__":
    main()