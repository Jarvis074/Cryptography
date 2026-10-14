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


def make_operations(n):
    """Создаёт последовательность удвоений и сложений для вычисления nP."""
    if n < 1:
        raise ValueError("Число n должно быть положительным.")

    reversed_operations = []

    while n > 1:
        if n % 2 == 0:
            reversed_operations.append("double")
            n //= 2
        else:
            reversed_operations.append("add_P")
            reversed_operations.append("double")
            n = (n - 1) // 2

    return list(reversed(reversed_operations))


def one_iteration(R, operation, P, a, p, multiplier):
    """Выполняет одну итерацию и возвращает новую точку и множитель."""
    if operation == "double":
        R = add_points(R, R, a, p)
        multiplier *= 2
    elif operation == "add_P":
        R = add_points(R, P, a, p)
        multiplier += 1

    return R, multiplier


def calculate(n, P, a, p):
    if n == 0:
        print("Итог: 0P = O")
        return None

    if n < 0:
        raise ValueError("Число n должно быть неотрицательным.")

    if n == 1:
        print(f"Итог: 1P = {P}")
        return P

    R = P
    multiplier = 1
    operations = make_operations(n)

    for iteration, operation in enumerate(operations, start=1):
        R, multiplier = one_iteration(
            R, operation, P, a, p, multiplier
        )

        point_value = "O" if R is None else str(R)
        print(f"R_{iteration}: {multiplier}P = {point_value}")

    point_value = "O" if R is None else str(R)
    print(f"Итог: {n}P = {point_value}")

    return R


print("Параметры задаются для эллиптической кривой:")
print("    y² ≡ x³ + a·x + b (mod p)")
print()
print("Введите значения:")
print("  n      — число, на которое умножается точка P в выражении nP;")
print("  p      — модуль, указанный после mod;")
print("  a, b   — коэффициенты уравнения кривой;")
print("  x, y   — координаты точки P = (x, y).")
print()

n = int(input("Введите n: "))
p = int(input("Введите модуль p: "))
a, b = map(int, input("Введите коэффициенты эллиптической кривой a и b: ").split())
x, y = map(int, input("Введите координаты точки P, x и y: ").split())

P = (x % p, y % p)

# Проверка, что точка лежит на кривой y² ≡ x³ + ax + b (mod p).
if (P[1]**2 - (P[0]**3 + a * P[0] + b)) % p != 0:
    raise ValueError("Точка P не лежит на заданной эллиптической кривой.")

calculate(n, P, a, p)
