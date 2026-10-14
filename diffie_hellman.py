p, g = map(int, input("Введите числа p и g: ").split())
x, y = map(int, input("Введите числа x и y: ").split())

A = g ** x % p
B = g ** y % p

print(f"Передаваемые числа A и B: {A}, {B}")

key_a = A ** y % p
key_b = B ** x % p

if key_a == key_b:
    key = key_a
    print(f"Ключи совпали: {key}")
else:
    print(":(")
    print(f"Ключи разные: {key_a}, {key_b}")
