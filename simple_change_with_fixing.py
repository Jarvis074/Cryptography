import random

block_size = 16

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

def encrypt_block(s_box, block):
    return bytes(s_box[b] for b in block)

def decrypt_block(inv_s_box, block):
    return bytes(inv_s_box[b] for b in block)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt(s_box, iv, data):
    data = padding(data)
    out = bytearray()
    prev = iv

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        x = xor_bytes(block, prev)

        cblock = encrypt_block(s_box, x)
        out.extend(cblock)
        prev = cblock

    return bytes(out)

def decrypt(inv_s_box, iv, data):
    out = bytearray()
    prev = iv

    for i in range(0, len(data), block_size):
        cblock = data[i:i + block_size]
        x = decrypt_block(inv_s_box, cblock)

        pblock = xor_bytes(x, prev)
        out.extend(pblock)
        prev = cblock

    return delete_padding(bytes(out))

def main():
    text = input("Введите текст для шифрования: ").encode()

    s_box, inv_s_box = make_random_s_box()
    iv = random.randbytes(block_size)
    print("S-box (hex):", s_box.hex())
    print("IV (hex):", iv.hex())

    encrypted = encrypt(s_box, iv, text)
    print("Шифротекст (hex):", encrypted.hex())

    decrypted = decrypt(inv_s_box, iv, encrypted)
    print("Расшифрованный текст:", decrypted.decode())

if __name__ == "__main__":
    main()