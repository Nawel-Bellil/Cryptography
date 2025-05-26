import struct

# Constants (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

# Initial hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19)
H0 = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
]

def right_rotate(value, bits):
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF

def sha256(message):
    # Preprocessing (Padding)
    message_bytes = message.encode('utf-8')
    orig_len_bits = len(message_bytes) * 8

    # append the bit '1' to the message
    message_bytes += b'\x80'

    # append 0 <= k < 512 bits '0', so that the resulting message length in bits
    # is congruent to 448 mod 512
    while (len(message_bytes) * 8) % 512 != 448:
        message_bytes += b'\x00'

    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message_bytes += struct.pack('>Q', orig_len_bits)

    # Process the message in successive 512-bit chunks:
    chunks = [message_bytes[i:i+64] for i in range(0, len(message_bytes), 64)]

    # Initialize hash values:
    h = H0[:]

    # Main loop
    for chunk in chunks:
        w = [0] * 64

        # Break chunk into sixteen 32-bit big-endian words w[0..15]
        for i in range(16):
            w[i] = struct.unpack('>I', chunk[i*4:i*4+4])[0]

        # Extend the sixteen 32-bit words into sixty-four 32-bit words:
        for i in range(16, 64):
            s0 = (right_rotate(w[i-15], 7) ^ right_rotate(w[i-15], 18) ^ (w[i-15] >> 3))
            s1 = (right_rotate(w[i-2], 17) ^ right_rotate(w[i-2], 19) ^ (w[i-2] >> 10))
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF

        # Initialize working variables to current hash value:
        a, b, c, d, e, f, g, h_var = h

        # Compression function main loop:
        for i in range(64):
            S1 = (right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25))
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h_var + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            S0 = (right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22))
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h_var = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Add the compressed chunk to the current hash value:
        h = [
            (h[0] + a) & 0xFFFFFFFF,
            (h[1] + b) & 0xFFFFFFFF,
            (h[2] + c) & 0xFFFFFFFF,
            (h[3] + d) & 0xFFFFFFFF,
            (h[4] + e) & 0xFFFFFFFF,
            (h[5] + f) & 0xFFFFFFFF,
            (h[6] + g) & 0xFFFFFFFF,
            (h[7] + h_var) & 0xFFFFFFFF,
        ]

    # Produce the final hash value (big-endian) as a 64-character hex string
    return ''.join(f'{value:08x}' for value in h)

# Example usage:
if __name__ == "__main__":
    test_str = input("Enter a string to hash with SHA-512: ")
    if not test_str:
        test_str = "Hello, World!"  # Default test string if none provided
    print(f"SHA-256('{test_str}') = {sha256(test_str)}")
