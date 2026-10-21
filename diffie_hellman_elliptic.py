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


def check_point(point, name, a, b, p):
    """Проверяет, что точка лежит на кривой y² ≡ x³ + ax + b (mod p)."""
    x, y = point
    if (y**2 - (x**3 + a * x + b)) % p != 0:
        raise ValueError(f"Точка {name} не лежит на заданной эллиптической кривой.")


def point_to_str(P):
    return "O" if P is None else str(P)


def main():
    print("Параметры задаются для эллиптической кривой:")
    print("    y² ≡ x³ + a·x + b (mod p)")
    print()
    print("Введите значения:")
    print("  p      — модуль, указанный после mod;")
    print("  a, b   — коэффициенты уравнения кривой;")
    print("  x, y   — координаты базовой точки G = (x, y);")
    print("  kA, kB — секретные ключи абонентов A и B.")
    print()

    p = int(input("Введите модуль p: "))
    a, b = map(int, input("Введите коэффициенты эллиптической кривой a и b: ").split())
    x, y = map(int, input("Введите координаты точки G, x и y: ").split())
    kA, kB = map(int, input("Введите секретные ключи kA и kB: ").split())

    G = (x % p, y % p)

    check_point(G, "G", a, b, p)

    QA = multiply(kA, G, a, p)
    QB = multiply(kB, G, a, p)

    print(f"Передаваемые точки QA и QB: {point_to_str(QA)}, {point_to_str(QB)}")

    key_a = multiply(kA, QB, a, p)
    key_b = multiply(kB, QA, a, p)

    if key_a == key_b:
        key = key_a
        print(f"Ключи совпали: {point_to_str(key)}")
    else:
        print(":(")
        print(f"Ключи разные: {point_to_str(key_a)}, {point_to_str(key_b)}")


if __name__ == "__main__":
    main()