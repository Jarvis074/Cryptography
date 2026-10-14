import random

block_size = 16

def make_random_s_box():
    values = list(range(256))

    for i in range(255, 0, -1):
        j = random.randrange(i + 1)
        values[i], values[j] = values[j], values[i]

    s_box = bytes(values)
    inv = [0] * 256

    for i,b in enumerate(s_box):
        inv[b] = i

    inv_s_box = bytes(inv)

    return s_box, inv_s_box

def padding(data):
    pad_len = block_size - (len(data) % block_size)

    return data + bytes([pad_len]) * pad_len

def delete_padding(data):
    pad_len = data[-1]

    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Неверный отступ")

    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Неверный отступ")

    return data[:-pad_len]

def encrypt(s_box, data):
    data = padding(data)
    out = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        out.extend(s_box[b] for b in block)

    return bytes(out)

def decrypt(inv_s_box, data):
    out = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        out.extend(inv_s_box[b] for b in block)

    return delete_padding(bytes(out))

def main():
    text = input("Введите текст для шифрования: ").encode()

    s_box, inv_s_box = make_random_s_box()
    print("S-box (hex):", s_box.hex())

    encrypted = encrypt(s_box, text)
    print("Шифротекст (hex):", encrypted.hex())

    decrypted = decrypt(inv_s_box, encrypted)
    print("Расшифрованный текст:", decrypted.decode())

if __name__ == "__main__":
    main()
