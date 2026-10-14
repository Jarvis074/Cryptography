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

def word32_from_bytes(b, offset):
    return int.from_bytes(b[offset:offset + 4], 'big')

def word32_to_bytes(w):
    return w.to_bytes(4, 'big')

def process_round(round_key, data):
    data = (data + round_key) & 0xFFFFFFFF
    data = (data ^ ((data * 0x9E3779B1) & 0xFFFFFFFF)) & 0xFFFFFFFF
    return ((data << 7) | (data >> (32 - 7))) & 0xFFFFFFFF

def form_keys(key16):
    keys = [word32_from_bytes(key16, i * 4) for i in range(4)]

    for i in range(4, 8):
        keys.append(((keys[i - 1] ^ keys[i - 4]) + 0x01010101) & 0xFFFFFFFF)

    return keys[:4]

def encrypt_block(key16, block16):
    keys = form_keys(key16)
    words = [word32_from_bytes(block16, i*4) for i in range(4)]

    for rnd in range(4):
        round_key = keys[rnd % len(keys)]

        f0 = process_round(round_key, words[0])
        words[1] ^= f0

        f1 = process_round(round_key ^ 0xA5A5A5A5, words[2])
        words[3] ^= f1

        words[0], words[2] = words[2], words[0]
        words[1], words[3] = words[3], words[1]

    return b''.join(word32_to_bytes(w) for w in words)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def compute_mac(key16, iv, message):
    padded = padding(message)
    state = bytes(iv)

    for i in range(0, len(padded), block_size):
        block = padded[i:i + block_size]
        state = encrypt_block(key16, xor_bytes(state, block))

    return state

def verify_mac(key16, iv, message, mac):
    return compute_mac(key16, iv, message) == mac

def main():
    text = input("Введите сообщение для шифрования/подписи: ").encode()

    key = random.randbytes(16)
    iv = random.randbytes(16)
    print("Key (hex):", key.hex())
    print("IV (hex):", iv.hex())

    mac = compute_mac(key, iv, text)
    print("MAC (hex):", mac.hex)

    # демонстрация проверки
    ok = verify_mac(key, iv, text, mac)
    print("Проверка MAC:", "OK" if ok else "FAIL")

    # демонстрация, что изменение сообщения ломает проверку
    tampered = text + b"!"
    ok2 = verify_mac(key, iv, tampered, mac)
    print("Проверка MAC для изменённого сообщения:", "OK" if ok2 else "FAIL")

if __name__ == "__main__":
    main()
