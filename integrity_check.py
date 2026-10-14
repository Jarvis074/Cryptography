def binary_matrix(n):
    bits = n.bit_length()
    mat = [[0]*n for _ in range(bits)]
    for j in range(1, n+1):
        val = j
        for i in range(bits):
            shift = bits - 1 - i
            mat[i][j-1] = (val >> shift) & 1
    return mat

def transpose(mat):
    max_cols = max(len(row) for row in mat)
    transposed = []
    for c in range(max_cols):
        new_row = []
        for r in range(len(mat)):
            row = mat[r]
            if c < len(row):
                new_row.append(row[c])
        transposed.append(new_row)
    return transposed

def multiply_vector_by_mat(mat, vec):
    if not mat:
        return []
    m = len(mat)
    if len(vec) != m:
        raise ValueError("Длина вектора должна равняться числу строк матрицы.")
    max_len = max(len(row) for row in mat)
    # нормализуем вектор в 0/1
    vec_bits = [1 if v else 0 for v in vec]
    result = [0] * max_len
    for r, row in enumerate(mat):
        if vec_bits[r] == 0:
            continue
        # если vec[r] == 1, прибавляем (XOR) строку r к результату по столбцам
        for c, val in enumerate(row):
            if val:
                result[c] ^= 1
    return result

def encode_hamming(bits):
    length = len(bits)

    k = 1
    shift = 0
    while k + shift <= length:
        pos = k + shift
        bits.insert(pos - (1 + shift), 0)
        shift += 1
        k *= 2

    mat = binary_matrix(len(bits))
    mat_t = transpose(mat)

    res = multiply_vector_by_mat(mat_t, bits)
    res.reverse()

    print(f"Полученные контрольные биты: {res}")

    i = 1
    k = 1
    while i < len(bits) and k < len(res):
        bits[i - 1] = res[k - 1]
        i *= 2
        k += 1

    print(f"Битовая строка с добавленными контрольными битами: {"".join(list(map(str, bits)))}")

def decode_hamming(mat, bits):
    res = multiply_vector_by_mat(mat, bits)
    res = list(map(str, res))
    res = "".join(res)

    if res.count("1") != 0:
        error_bit_number = int(res, 2)
        print(f"Номер бита с ошибкой: {error_bit_number}")

        if bits[error_bit_number - 1] == 0:
            bits[error_bit_number - 1] = 1
        else:
            bits[error_bit_number - 1] = 0

        print(f"Исправленная строка: {"".join(list(map(str, bits)))}")
    else:
        print("Последовательность не содержит ошибок.")


def main():
    bits = list(input("Введите битовую последовательность: "))
    bits = list(map(int, bits))

    encode_hamming(bits)

    bits_e = list(input("Введите битовую последовательность с ошибкой: "))
    bits_e = list(map(int, bits_e))

    mat = binary_matrix(len(bits_e))
    mat_t = transpose(mat)

    decode_hamming(mat_t, bits_e)


if __name__ == "__main__":
    main()
