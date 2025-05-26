import struct
import hashlib

class SimpleMARS:
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long.")
        self.round_keys = self._expand_key(key)

    def _expand_key(self, key: bytes) -> list:
        # Génère 16 sous-clés de 32 bits à partir de la clé initiale
        hash_key = hashlib.sha256(key).digest()
        return list(struct.unpack('<8I', hash_key[:32]))

    def _F(self, x: int, k: int) -> int:
        # Fonction non-linéaire simple
        return self._rotl((x ^ k) + 0x9e3779b9, 5)

    def _rotl(self, x: int, r: int) -> int:
        return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

    def _rotr(self, x: int, r: int) -> int:
        return ((x >> r) | (x << (32 - r))) & 0xFFFFFFFF

    def _encrypt_block(self, block: bytes) -> bytes:
        L, R = struct.unpack('<2Q', block)  # 2x 64-bit
        for i in range(8):  # 8 rounds
            temp = self._F(R & 0xFFFFFFFF, self.round_keys[i])
            L, R = R, L ^ temp
        return struct.pack('<2Q', L, R)

    def _decrypt_block(self, block: bytes) -> bytes:
        L, R = struct.unpack('<2Q', block)
        for i in reversed(range(8)):
            L, R = R ^ self._F(L & 0xFFFFFFFF, self.round_keys[i]), L
        return struct.pack('<2Q', L, R)

    def encrypt(self, plaintext: bytes) -> bytes:
        if len(plaintext) % 16 != 0:
            raise ValueError("Plaintext must be a multiple of 16 bytes.")
        ciphertext = b''
        for i in range(0, len(plaintext), 16):
            ciphertext += self._encrypt_block(plaintext[i:i+16])
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext must be a multiple of 16 bytes.")
        plaintext = b''
        for i in range(0, len(ciphertext), 16):
            plaintext += self._decrypt_block(ciphertext[i:i+16])
        return plaintext
    
    
def pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if not 1 <= pad_len <= 16:
        raise ValueError("Invalid padding.")
    return data[:-pad_len]

mars = SimpleMARS(key=b'Sixteen byte key')

# Bloc de 16 octets
plaintext = b'ana nawel!!'  # 16 octets exactement
padded = pad(plaintext)
ciphertext = mars.encrypt(padded)
decrypted = mars.decrypt(ciphertext)
unpadded = unpad(decrypted)

print("Original :", plaintext)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", decrypted)
print("Match    :", plaintext == unpadded)
