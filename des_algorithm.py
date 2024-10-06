# Tabel Initial Permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Tabel Final Permutation (FP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Tabel Permuted Choice 1 (PC-1)
PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Tabel Permuted Choice 2 (PC-2)
PC_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Shift schedule for each round
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

# Tabel Expansion (E)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# S-Boxes (Hanya S-box pertama sebagai contoh, Anda perlu mendefinisikan semua 8 S-box)
S_BOX = {
    1: [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    # Definisikan S-box 2 hingga 8 di sini...
    # ...
}
# Untuk kesederhanaan, kita hanya menggunakan S_BOX 1 dalam implementasi ini.

# Tabel Permutation P
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

def permute(block, table):
    permuted_bits = [block[i - 1] for i in table]
    return permuted_bits

def text_to_bits(plaintext):
    result = []
    for c in plaintext:
        bits = format(ord(c), '08b')  # Mengonversi karakter ke 8-bit biner
        result += [int(b) for b in bits]  # Menambahkan bit sebagai integer ke list hasil
    return result

def bits_to_text(bits):
    result = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]  # Mengambil 8 bit
        byte_str = ''.join(str(b) for b in byte)  # Mengonversi list bit menjadi string
        result += chr(int(byte_str, 2))  # Mengonversi string bit ke karakter ASCII
    return result

def pad_bits(bits, length):
  if len(bits) < length:
        return bits + [0] * (length - len(bits))
  else:
      return bits[:length]

def shift_left(key_half, n):
    return key_half[n:] + key_half[:n]

def generate_subkeys(key):
    key = permute(key, PC_1)
    C = key[:28]
    D = key[28:]

    subkeys = []
    for shift in SHIFT_SCHEDULE:
        C = shift_left(C, shift)
        D = shift_left(D, shift)
        combine_cd = C + D
        subkey = permute(combine_cd, PC_2)
        subkeys.append(subkey)

    return subkeys

def feistel_function(right, subkey):
    expanded_right = permute(right, E)
    xor_output = [a ^ b for a, b in zip(expanded_right, subkey)]
    sbox_output = []
    for i in range(0, len(xor_output), 6):
        block = xor_output[i:i+6]
        row = int(str(block[0]) + str(block[5]), 2)
        col = int(''.join(map(str, block[1:5])), 2)
        sbox_val = S_BOX[1][row][col]
        sbox_output.extend([int(bit) for bit in bin(sbox_val)[2:].zfill(4)])
    
    return permute(sbox_output, P)

def encrypt(plaintext, key):
    plaintext_bits = text_to_bits(plaintext)
    key_bits = text_to_bits(key)

    plaintext_bits = pad_bits(plaintext_bits, 64)
    key_bits = pad_bits(key_bits, 64)

    initial_permutation = permute(plaintext_bits, IP)
    left_half = initial_permutation[:32]
    right_half = initial_permutation[32:]

    subkeys = generate_subkeys(key_bits)

    for i in range(16):
        temp_right = right_half
        f_output = feistel_function(right_half, subkeys[i])
        new_right = [a ^ b for a, b in zip(left_half, f_output)]
        left_half = temp_right
        right = new_right

    combined_output = left_half + right_half
    final_permutation = permute(combined_output, FP)
    ciphertext = bits_to_text(final_permutation)

    return ciphertext

def decrypt(ciphertext, key):
    ciphertext_bits = text_to_bits(ciphertext)
    key_bits = text_to_bits(key)

    ciphertext_bits = pad_bits(ciphertext_bits, 64)
    key_bits = pad_bits(key_bits, 64)

    initial_permutation = permute(ciphertext_bits, IP)
    left_half = initial_permutation[:32]
    right_half = initial_permutation[32:]

    subkeys = generate_subkeys(key_bits)

    for i in range(15, -1, -1):
        temp_left = left_half
        f_output = feistel_function(left_half, subkeys[i])
        new_left = [a ^ b for a, b in zip(left_half, f_output)]
        left = new_left
        right = temp_left

    combined_output = left_half + right_half
    final_permutation = permute(combined_output, FP)
    plaintext = bits_to_text(final_permutation)

    return plaintext

plaintext = input("Masukkan plaintext (maks 8 karakter): ")
key = input("Masukkan key (maks 8 karakter): ")

# Pastikan plaintext dan key tidak lebih dari 8 karakter
if len(plaintext) > 8 or len(key) > 8:
    print("Error: Plaintext dan key harus maksimal 8 karakter.")

ciphertext = encrypt(plaintext, key)
print(f"Ciphertext (64-bit teks): {ciphertext}")

decrypted_text = decrypt(ciphertext, key)
print(f"Decrypted Text: {decrypted_text}")