# https://medium.com/@techclaw/hill-cipher-in-python-encrypting-your-data-with-matrix-magic-6cecfb339627
import numpy as np
def encrypt_hill_cipher(plaintext, key_matrix):
    block_size = len(key_matrix)
    # Convert plaintext to numerical values
    plaintext_num = [ord(char) - ord('A') for char in plaintext]
    
    ciphertext = ""
    for i in range(0, len(plaintext_num), block_size):
        block = np.array(plaintext_num[i:i+block_size])
        encrypted_block = np.dot(key_matrix, block) % 26
        ciphertext += "".join(chr(val + ord('A')) for val in encrypted_block)
    
    return ciphertext
# Example usage
plaintext = "HELLOHILL"
key_matrix = np.array([[6, 24], [13, 16]])
ciphertext = encrypt_hill_cipher(plaintext, key_matrix)
print("Ciphertext:", ciphertext)