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


def check_point(point, name, a, b, p):
    """Проверяет, что точка лежит на кривой y² ≡ x³ + ax + b (mod p)."""
    x, y = point
    if (y**2 - (x**3 + a * x + b)) % p != 0:
        raise ValueError(f"Точка {name} не лежит на заданной эллиптической кривой.")


def find_points(a, b, p):
    """Находит все точки кривой перебором x и y от 0 до p - 1."""
    # Квадраты по модулю p: какому y соответствует каждый остаток y².
    squares = {}
    for y in range(p):
        squares.setdefault(y**2 % p, []).append(y)

    points = []
    for x in range(p):
        right = (x**3 + a * x + b) % p
        ys = squares.get(right, [])

        if ys:
            print(f"x = {x}: x³ + ax + b ≡ {right}, y = {', '.join(map(str, ys))}")
        else:
            print(f"x = {x}: x³ + ax + b ≡ {right}, точек нет")

        for y in ys:
            points.append((x, y))

    print()
    print("Точки кривой:", ", ".join(map(str, points)), "и ∞")
    print(f"Итог: порядок кривой = {len(points) + 1}")

    return points


def main():
    print("Режимы работы:")
    print("  1 — умножение точки на число nP;")
    print("  2 — сложение двух точек P + Q;")
    print("  3 — нахождение всех точек кривой.")
    mode = input("Выберите режим (1, 2 или 3): ").strip()

    if mode not in ("1", "2", "3"):
        raise ValueError("Неизвестный режим. Введите 1, 2 или 3.")

    print()
    print("Параметры задаются для эллиптической кривой:")
    print("    y² ≡ x³ + a·x + b (mod p)")
    print()
    print("Введите значения:")
    if mode == "1":
        print("  n      — число, на которое умножается точка P в выражении nP;")
    print("  p      — модуль, указанный после mod;")
    print("  a, b   — коэффициенты уравнения кривой;")
    if mode in ("1", "2"):
        print("  x, y   — координаты точки P = (x, y).")
    if mode == "2":
        print("  x, y   — координаты точки Q = (x, y).")
    print()

    if mode == "1":
        n = int(input("Введите n: "))
    p = int(input("Введите модуль p: "))
    a, b = map(int, input("Введите коэффициенты эллиптической кривой a и b: ").split())

    if mode == "3":
        print()
        find_points(a, b, p)
        return

    x, y = map(int, input("Введите координаты точки P, x и y: ").split())

    P = (x % p, y % p)

    check_point(P, "P", a, b, p)

    if mode == "1":
        calculate(n, P, a, p)
    else:
        x, y = map(int, input("Введите координаты точки Q, x и y: ").split())
        Q = (x % p, y % p)

        check_point(Q, "Q", a, b, p)

        R = add_points(P, Q, a, p)
        point_value = "∞" if R is None else str(R)
        print(f"Итог: P + Q = {P} + {Q} = {point_value}")


if __name__ == "__main__":
    main()