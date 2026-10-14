def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

def mod_inverse(x, y):
    gcd, inv, _ = extended_gcd(x, y)
    if gcd != 1:
        raise ValueError("Решать нельзя, НОД != 1")
    return inv % y

p = int(input("Введите число p: "))
x1, y1 = map(int, input("Введите числа x1 и y1: ").split())
X1 = int(input("Введите число X1: "))

x2 = mod_inverse(x1, p - 1)
y2 = mod_inverse(y1, p - 1)

Y1 = (X1 ** y1) % p
X2 = (Y1 ** x2) % p

Y2 = (X2 ** y2) % p

print(f"Результат: {Y2}")

# 16, 21, 8, 27, 31