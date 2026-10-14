import random

block_size = 16  # 128 бит

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

def encrypt_block_with_s_box(s_box, block):
    return bytes(s_box[b] for b in block)

def increment_counter(counter):
    for i in range(len(counter)-1, -1, -1):
        if counter[i] == 0xFF:
            counter[i] = 0
        else:
            counter[i] += 1
            break

def generate_gamma_stream(s_box, iv, n_bytes):
    stream = bytearray()
    counter = bytearray(iv)

    while len(stream) < n_bytes:
        gamma_block = encrypt_block_with_s_box(s_box, bytes(counter))

        stream.extend(gamma_block)
        increment_counter(counter)

    return bytes(stream[:n_bytes])

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt(s_box, data, iv):
    data = padding(data)

    gamma = generate_gamma_stream(s_box, iv, len(data))
    out = xor_bytes(data, gamma)

    return out

def decrypt(s_box, data, iv):
    gamma = generate_gamma_stream(s_box, iv, len(data))
    data = xor_bytes(data, gamma)

    return delete_padding(data)

def main():
    text = input("Введите текст для шифрования: ").encode()

    s_box, inv_s_box = make_random_s_box()
    iv = random.randbytes(block_size)

    print("S-box (hex):", s_box.hex())
    print("IV (hex):", iv.hex())

    encrypted = encrypt(s_box, text, iv)

    print("Шифротекст (hex):", encrypted.hex())

    decrypted = decrypt(s_box, encrypted, iv)
    print("Расшифрованный текст:", decrypted.decode())

if __name__ == "__main__":
    main()