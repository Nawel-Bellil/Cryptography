import os
import struct

# AES constants
Nb = 4  # block size in 32-bit words
Nk = 4  # key length in 32-bit words (4 for AES-128)
Nr = 10  # number of rounds (10 for AES-128)

# S-box and Inverse S-box
s_box = [
    # 0     1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]
inv_s_box = [s_box.index(x) for x in range(256)]

Rcon = [0x01]
for _ in range(1, 10):
    Rcon.append(Rcon[-1] << 1 ^ (0x11B if Rcon[-1] & 0x80 else 0))

def sub_bytes(state):
    return [s_box[b] for b in state]

def inv_sub_bytes(state):
    return [inv_s_box[b] for b in state]

def shift_rows(state):
    return [
        state[0], state[5], state[10], state[15],
        state[4], state[9], state[14], state[3],
        state[8], state[13], state[2], state[7],
        state[12], state[1], state[6], state[11],
    ]

def inv_shift_rows(state):
    return [
        state[0], state[13], state[10], state[7],
        state[4], state[1], state[14], state[11],
        state[8], state[5], state[2], state[15],
        state[12], state[9], state[6], state[3],
    ]

def mix_columns(state):
    def xtime(a): return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1
    def mix_column(column):
        t = column[0] ^ column[1] ^ column[2] ^ column[3]
        return [
            column[0] ^ t ^ xtime(column[0] ^ column[1]),
            column[1] ^ t ^ xtime(column[1] ^ column[2]),
            column[2] ^ t ^ xtime(column[2] ^ column[3]),
            column[3] ^ t ^ xtime(column[3] ^ column[0]),
        ]
    return sum([mix_column(state[i::4]) for i in range(4)], [])

def inv_mix_columns(state):
    def mul(a, b):
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit = a & 0x80
            a = (a << 1) ^ (0x1B if hi_bit else 0)
            b >>= 1
        return p & 0xFF
    def inv_mix_column(col):
        return [
            mul(col[0], 14) ^ mul(col[1], 11) ^ mul(col[2], 13) ^ mul(col[3], 9),
            mul(col[0], 9) ^ mul(col[1], 14) ^ mul(col[2], 11) ^ mul(col[3], 13),
            mul(col[0], 13) ^ mul(col[1], 9) ^ mul(col[2], 14) ^ mul(col[3], 11),
            mul(col[0], 11) ^ mul(col[1], 13) ^ mul(col[2], 9) ^ mul(col[3], 14),
        ]
    return sum([inv_mix_column(state[i::4]) for i in range(4)], [])

def add_round_key(state, round_key):
    return [s ^ rk for s, rk in zip(state, round_key)]

def key_expansion(key):
    key_symbols = list(key)
    w = [key_symbols[i:i + 4] for i in range(0, 16, 4)]
    for i in range(4, Nb * (Nr + 1)):
        temp = w[i - 1][:]
        if i % Nk == 0:
            temp = temp[1:] + temp[:1]
            temp = [s_box[b] for b in temp]
            temp[0] ^= Rcon[i // Nk - 1]
        w.append([wi ^ ti for wi, ti in zip(w[i - Nk], temp)])
    return sum(w, [])

def encrypt_block(block, key_schedule):
    state = list(block)
    state = add_round_key(state, key_schedule[:16])
    for r in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_schedule[16*r:16*(r+1)])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule[16*Nr:])
    return bytes(state)

def decrypt_block(block, key_schedule):
    state = list(block)
    state = add_round_key(state, key_schedule[16*Nr:])
    for r in range(Nr-1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key_schedule[16*r:16*(r+1)])
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, key_schedule[:16])
    return bytes(state)

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    return data[:-data[-1]]

def aes_encrypt_ecb(plaintext, key):
    key_schedule = key_expansion(key)
    plaintext = pad(plaintext)
    return b''.join(encrypt_block(plaintext[i:i+16], key_schedule) for i in range(0, len(plaintext), 16))

def aes_decrypt_ecb(ciphertext, key):
    key_schedule = key_expansion(key)
    plaintext = b''.join(decrypt_block(ciphertext[i:i+16], key_schedule) for i in range(0, len(ciphertext), 16))
    return unpad(plaintext)

def increment_counter(counter):
    return counter[:-1] + bytes([(counter[-1] + 1) % 256])

def aes_encrypt_ctr(plaintext, key, nonce):
    key_schedule = key_expansion(key)
    ciphertext = b''
    counter = nonce + b'\x00' * 8
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        keystream = encrypt_block(counter, key_schedule)
        ciphertext += bytes(a ^ b for a, b in zip(block, keystream))
        counter = increment_counter(counter)
    return ciphertext

def aes_decrypt_ctr(ciphertext, key, nonce):
    return aes_encrypt_ctr(ciphertext, key, nonce)  # symmetric

# Example usage
if __name__ == "__main__":
    key = b"Th1s1sA128bitKey"
    nonce = b"NONCE123"  # 8 bytes
    plaintext = b"Example message that needs to be encrypted."

    print("== ECB Mode ==")
    ct = aes_encrypt_ecb(plaintext, key)
    pt = aes_decrypt_ecb(ct, key)
    print("Ciphertext:", ct.hex())
    print("Decrypted :", pt)

    print("\n== CTR Mode ==")
    ct = aes_encrypt_ctr(plaintext, key, nonce)
    pt = aes_decrypt_ctr(ct, key, nonce)
    print("Ciphertext:", ct.hex())
    print("Decrypted :", pt)
