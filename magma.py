S_box = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
]

def rotl32(x, n):
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

def u32(x):
    return x & 0xFFFFFFFF

def apply_s_box(x):
    out = 0

    for i in range(8):
        nibble = (x >> (4 * i)) & 0xF
        s = S_box[i][nibble] & 0xF
        out |= (s << (4 * i))

    return out

def f_round(n, k):
    t = u32(n + k)
    t = apply_s_box(t)
    t = rotl32(t, 11)

    return t

def form_keys(key64):
    mk = key64 * 4

    words = []

    for i in range(0, 32, 4):
        w = int.from_bytes(mk[i:i + 4], byteorder='little')
        words.append(w)

    return words

def encrypt_block(block, round_keys):
    n1 = int.from_bytes(block[0:4], byteorder='little')
    n2 = int.from_bytes(block[4:8], byteorder='little')

    for r in range(1, 33):
        if r <= 24:
            k = round_keys[(r - 1) % 8]
        else:
            k = round_keys[32 - r]

        t = f_round(n1, k)
        t = u32(n2 ^ t)

        n2, n1 = n1, t

    out = n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

    return out

def decrypt_block(block, round_keys):
    n1 = int.from_bytes(block[0:4], byteorder='little')
    n2 = int.from_bytes(block[4:8], byteorder='little')

    ek = []

    for i in range(24):
        ek.append(round_keys[i % 8])
    for i in range(8):
        ek.append(round_keys[7 - i])

    for k in reversed(ek):
        t = f_round(n1, k)
        t = u32(n2 ^ t)
        n2, n1 = n1, t

    out = n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

    return out

def padding(data):
    pad_len = 8 - (len(data) % 8)

    return data + bytes([pad_len]) * pad_len

def delete_padding(data):
    pad_len = data[-1]

    if pad_len < 1 or pad_len > 8:
        raise ValueError("Неверный отступ")

    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Неверный отступ")

    return data[:-pad_len]


def encrypt(data, key64):
    round_keys = form_keys(key64)
    ek = []

    for _ in range(3):
        ek.extend(round_keys)
    ek.extend(reversed(round_keys))

    data = padding(data)

    out = bytearray()
    for i in range(0, len(data), 8):
        out += encrypt_block(data[i:i + 8], round_keys)

    return bytes(out)

def decrypt(data, key64):
    round_keys = form_keys(key64)

    out = bytearray()
    for i in range(0, len(data), 8):
        out += decrypt_block(data[i:i + 8], round_keys)

    return delete_padding(bytes(out))

def main():
    text = input("Введите сообщение для шифрования: ")
    key = input("Введите 8-ти байтовый ключ: ").encode()

    while len(key) != 8:
        key = input("Длина ключа должна быть 8 байт, введите ключ повторно: ").encode()

    print("Открытый текст:", text)

    encrypted = encrypt(text.encode("utf-8"), key)
    print("Шифротекст (hex):", encrypted.hex())

    decrypted = decrypt(encrypted, key)
    print("Расшифрованный текст:", decrypted.decode("utf-8"))

if __name__ == "__main__":
    main()
