import random
import math

def extended_euler(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_euler(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

def mod_inverse(x, y):
    gcd, inv, _ = extended_euler(x, y)
    if gcd != 1:
        raise ValueError("Решать нельзя, НОД != 1")
    return inv % y

def inverse(x, y):
    gcd, inv, _ = extended_euler(x, y)
    if gcd != 1:
        raise ValueError("Решать нельзя, НОД != 1")
    return inv

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    gcd, _, _ = extended_euler(e, phi)
    while gcd != 1:
        e = random.randint(2, phi - 1)
        gcd, _, _ = extended_euler(e, phi)

    d = mod_inverse(e, phi)

    return (e, n), (d, n)  # (public_key, private_key)

def encrypt(public_key, m):
    e, n = public_key
    c = pow(m, e, n)
    return c

def decrypt(private_key, c):
    d, n = private_key
    m = pow(c, d, n)
    return m

def run_normal():
    p, q = map(int, input("Введите простые числа p и q: ").split())

    public_key, private_key = generate_keypair(p, q)
    print(f"public_key, private_key")

    m = int(input("Введите число M: "))

    c = encrypt(public_key, m)

    print(f"Шифрограмма: {c}")

    m = decrypt(private_key, c)

    print(f"Расшифрованный текст: {m}")

def attack_without_key():
    n = int(input("Введите общее простое число n:"))
    e1, e2 = map(int, input("Введите простые числа e1 и e2: ").split())
    c1, c2 = map(int, input("Введите простые числа e1 и e2: ").split())

    _, r, s = extended_euler(e1, e2)

    print(r, s)

    if r > 0:
        m_finded = pow(c1, r, n) * (inverse(c2, n) ** -s) % n
    else:
        m_finded = (inverse(c1, n) ** -r) % n * pow(c2, s, n)

    print(m_finded)

def chinese_attack():
    c1, N1 = map(int, input("Введите простые числа c1 и n1: ").split())
    c2, N2 = map(int, input("Введите простые числа c2 и n2: ").split())
    c3, N3 = map(int, input("Введите простые числа c3 и n3: ").split())

    Y = N1 * N2 * N3

    y1 = N2 * N3
    y2 = N1 * N3
    y3 = N1 * N2

    n1 = mod_inverse(y1, N1)
    n2 = mod_inverse(y2, N2)
    n3 = mod_inverse(y3, N3)

    S = c1 * n1 * y1 + c2 * n2 * y2 + c3 * n3 * y3
    C = S % Y

    print(math.cbrt(C))

def ferm_attack():
    n = int(input("Введите число N: "))

    t1 = math.ceil(math.sqrt(n))

    v = math.sqrt((t1 ** 2) - n)
    while v % 1 != 0:
        t1 += 1
        v = math.sqrt((t1 ** 2) - n)

    p = t1 + v
    q = t1 - v

    print(f"Число t: {t1}")
    print(f"Числа p и q: {p}, {q}")
    if p * q == n:
        print(f"Произведение p и q равно N: {p * q} = {n}")
    else:
        print(f"Произведение p и q не равно N! {p * q} = {n}")

def main():
    ferm_attack()

if __name__ == "__main__":
    main()
