def word_to_bin(word):
    binary_list = [format(b, '08b') for b in word.encode('utf-8')]
    return binary_list

def bin_to_word(binary_list):
    bytes_from_binary = bytes(int(b, 2) for b in binary_list)
    decoded = bytes_from_binary.decode('utf-8')
    return decoded

def xor_binary_lists(a, b):
    result = []
    for x, y in zip(a, b):
        rx = ''.join('1' if xb != yb else '0' for xb, yb in zip(x, y))
        result.append(rx)
    return result

def main():
    text = input("Введите текст: ")
    gamma1, gamma2, gamma3 = input("Введите гаммы: ").split()

    text_b = word_to_bin(text)
    gamma1_b, gamma2_b, gamma3_b = word_to_bin(gamma1), word_to_bin(gamma2), word_to_bin(gamma3)

    cipher_b = xor_binary_lists(text_b, gamma1_b)
    cipher_b = xor_binary_lists(cipher_b, gamma2_b)
    cipher_b = xor_binary_lists(cipher_b, gamma3_b)

    print(f"Полученный шифротекст: {cipher_b}")

    text_b = xor_binary_lists(cipher_b, gamma2_b)
    text_b = xor_binary_lists(text_b, gamma3_b)
    text_b = xor_binary_lists(text_b, gamma1_b)
    text = bin_to_word(text_b)

    print(f"Расшифрованный текст: {text}")

if __name__ == "__main__":
    main()