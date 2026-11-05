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


def hybrid_encrypt(M, Ks, k, G, Q, a, p):
    """Абонент A шифрует M сеансовым ключом Ks, а Ks — открытым ключом Q."""
    # E_S: симметричное шифрование сообщения — XOR с координатой x ключа Ks.
    C_M = M ^ Ks[0]

    # E_A: асимметричное шифрование сеансового ключа.
    R = multiply(k, G, a, p)   # (x1, y1) = kG передаётся вместе с шифртекстом
    S = multiply(k, Q, a, p)   # (x2, y2) = kQ знает только A

    if R is None or S is None:
        raise ValueError("kG или kQ = O, выберите другое k.")

    x2 = S[0]
    C_K = (Ks[0] ^ x2, Ks[1] ^ x2)

    print(f"C_M = M ⊕ Ks = {M} ⊕ {Ks[0]} = {C_M}")
    print(f"(x1, y1) = kG = {k}·G = {R}")
    print(f"(x2, y2) = kQ = {k}·Q = {S}")
    print(f"C_K = Ks ⊕ x2 = {Ks} ⊕ {x2} = {C_K}")

    return C_M, C_K, R


def hybrid_decrypt(C_M, C_K, R, d, a, p):
    """Абонент B восстанавливает Ks секретным ключом d, затем сообщение M."""
    # D_A: d·(x1, y1) = d·kG = k·Q, поэтому B получает ту же точку, что и A.
    S = multiply(d, R, a, p)
    x2 = S[0]
    Ks = (C_K[0] ^ x2, C_K[1] ^ x2)

    # D_S: обратное к XOR — снова XOR с тем же ключом.
    M = C_M ^ Ks[0]

    print(f"(x2, y2) = d·(x1, y1) = {d}·{R} = {S}")
    print(f"Ks = C_K ⊕ x2 = {C_K} ⊕ {x2} = {Ks}")
    print(f"M = C_M ⊕ Ks = {C_M} ⊕ {Ks[0]} = {M}")

    return M, Ks


def main():
    print("Параметры задаются для эллиптической кривой:")
    print("    y² ≡ x³ + a·x + b (mod p)")
    print()
    print("Введите значения:")
    print("  p      — модуль, указанный после mod;")
    print("  a, b   — коэффициенты уравнения кривой;")
    print("  x, y   — координаты базовой точки G = (x, y);")
    print("  M      — сообщение;")
    print("  d      — секретный ключ абонента B, 1 < d < n - 1;")
    print("  Ks     — сеансовый ключ, точка кривой (x, y);")
    print("  k      — случайное число абонента A, 1 < k < n - 1.")
    print()

    p = int(input("Введите модуль p: "))
    a, b = map(int, input("Введите коэффициенты эллиптической кривой a и b: ").split())
    x, y = map(int, input("Введите координаты точки G, x и y: ").split())
    M = int(input("Введите сообщение M: "))
    d = int(input("Введите секретный ключ d: "))
    kx, ky = map(int, input("Введите сеансовый ключ Ks, x и y: ").split())
    k = int(input("Введите случайное число k: "))

    G = (x % p, y % p)
    Ks = (kx % p, ky % p)

    check_point(G, "G", a, b, p)
    check_point(Ks, "Ks", a, b, p)

    n = point_order(G, a, p)
    Q = multiply(d, G, a, p)

    print()
    print(f"Порядок точки G: n = {n}")
    print(f"Открытый ключ абонента B: Q = d·G = {d}·G = {point_to_str(Q)}")

    print()
    print("Шифрование (абонент A):")
    C_M, C_K, R = hybrid_encrypt(M, Ks, k, G, Q, a, p)
    print(f"Передаётся: C_M = {C_M}, C_K = {C_K}, (x1, y1) = {R}")

    print()
    print("Расшифрование (абонент B):")
    M_dec, Ks_dec = hybrid_decrypt(C_M, C_K, R, d, a, p)

    if M_dec == M and Ks_dec == Ks:
        print(f"Сообщение восстановлено: {M_dec}")
    else:
        print(":(")
        print(f"Сообщения разные: {M}, {M_dec}")


if __name__ == "__main__":
    main()