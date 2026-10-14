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

def form_keys(key16: bytes):
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

def encrypt(key16, iv, data):
    data = padding(data)
    out = bytearray()
    feedback = bytes(iv)

    for i in range(0, len(data), block_size):
        gamma = encrypt_block(key16, feedback)
        block = data[i:i + block_size]

        xored = bytes(a ^ b for a, b in zip(block, gamma[:len(block)]))
        out.extend(xored)

        feedback = gamma

    return bytes(out)

def decrypt(key16, iv, ciphertext):
    out = bytearray()
    feedback = bytes(iv)

    for i in range(0, len(ciphertext), block_size):
        gamma = encrypt_block(key16, feedback)
        block = ciphertext[i:i + block_size]

        xored = bytes(a ^ b for a, b in zip(block, gamma[:len(block)]))
        out.extend(xored)

        feedback = gamma

    return delete_padding(bytes(out))

def main():
    text = input("Введите текст для шифрования: ").encode()

    key = random.randbytes(block_size)
    iv = random.randbytes(block_size)
    print("Key (hex):", key.hex())
    print("IV (hex):", iv.hex())

    encrypted = encrypt(key, iv, text)
    print("Шифротекст (hex):", encrypted.hex())

    decrypted = decrypt(key, iv, encrypted)
    print("Расшифрованный текст:", decrypted.decode())

if __name__ == "__main__":
    main()