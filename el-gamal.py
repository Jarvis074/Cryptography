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

def el_gamal_decrypt():
    p, g = map(int, input("Введите числа p и g: ").split())
    x = int(input("Введите числа y: "))
    r, s = map(int, input("Введите числа r и s: ").split())

    y = (g ** x) % p
    power = p - 1 - x

    if power >= 0:
        M = (s * (r ** power)) % p
    else:
        M = (s * (inverse(r, p) ** -power)) % p

    print(f"Криптограмма: ({y}, {M})")

def el_gamal_encrypt():
    p, g = map(int, input("Введите числа p и g: ").split())
    y = int(input("Введите числа y: "))
    M, k = map(int, input("Введите числа M и k: ").split())

    r = (g ** k) % p
    s = M * (y ** k) % p

    print(f"Криптограмма: ({r}, {s})")

el_gamal_encrypt()
el_gamal_decrypt()