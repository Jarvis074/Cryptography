def euler_totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def fast_exponentiation_euler(a, b, m):
    if m == 1:
        return 0  # любое число по модулю 1 равно 0

    # Вычисляем φ(m)
    phi_m = euler_totient(m)

    # Сокращаем b с помощью φ(m)
    b = b % phi_m

    # Базовое быстрое возведение в степень
    result = 1
    a = a % m  # Применяем модуль к основанию

    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        b //= 2

    return result

p, g = map(int, input("Введите числа p и g: ").split())
x, y = map(int, input("Введите числа x и y: ").split())

A = fast_exponentiation_euler(g, x, p)
B = fast_exponentiation_euler(g, y, p)

print(f"Передаваемые числа A и B: {A}, {B}")

key_a = fast_exponentiation_euler(A, y, p)
key_b = fast_exponentiation_euler(B, x, p)

if key_a == key_b:
    key = key_a
    print(f"Ключи совпали: {key}")
else:
    print(":(")
    print(f"Ключи разные: {key_a}, {key_b}")
