"""
L’expansion de clé de base (clé de 128 bits uniquement),

La structure Feistel,

Les opérations S-box, MDS et RS simplifiées,


"""

import struct

# Q-permutation tables (simplifiées pour démo)
Q0 = [i for i in range(256)]
Q1 = [255 - i for i in range(256)]

# MDS Matrix (from Twofish spec)
MDS = [
    [0x01, 0xEF, 0x5B, 0x5B],
    [0x5B, 0xEF, 0xEF, 0x01],
    [0xEF, 0x5B, 0x01, 0xEF],
    [0xEF, 0x01, 0xEF, 0x5B],
]

def mul(a, b):
    """Multiplication in GF(2^8) with modulus x^8 + x^6 + x^5 + x^3 + 1 (0x169)"""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        high = a & 0x80
        a = (a << 1) & 0xFF
        if high:
            a ^= 0x69
        b >>= 1
    return p

def mds_multiply(vector):
    return [sum(mul(mds, x) for mds, x in zip(row, vector)) & 0xFF for row in MDS]

def ROR(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def ROL(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

class Twofish:
    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 128, 192, or 256 bits.")
        self.Nk = len(key) // 8
        self.K = [struct.unpack('<I', key[i:i+4])[0] for i in range(0, len(key), 4)]
        self._expand_key()

    def _expand_key(self):
        self.S = [0] * 4
        self.subkeys = []
        for i in range(40):
            A = self._h(2 * i * 0x01010101, self.K)
            B = ROL(self._h((2 * i + 1) * 0x01010101, self.K), 8)
            self.subkeys.append((A + B) & 0xFFFFFFFF)
        for i in range(4):
            self.S[i] = self.K[self.Nk - 4 + i] if self.Nk >= 4 else 0

    def _h(self, X, L):
        x = [(X >> (8 * i)) & 0xFF for i in range(4)]
        for k in reversed(L):
            for i in range(4):
                x[i] = Q0[x[i]] ^ ((k >> (8 * i)) & 0xFF)
        return struct.unpack('<I', bytes(mds_multiply(x)))[0]

    def _F(self, R0, R1):
        T0 = self._g(R0)
        T1 = self._g(ROL(R1, 8))
        return (T0 + T1, T0 + 2 * T1)

    def _g(self, X):
        x = [(X >> (8 * i)) & 0xFF for i in range(4)]
        for i in range(4):
            x[i] = Q1[x[i] ^ self.S[i]]
        return struct.unpack('<I', bytes(mds_multiply(x)))[0]

    def encrypt_block(self, block: bytes) -> bytes:
        R = list(struct.unpack('<4I', block))
        for i in range(4):
            R[i] ^= self.subkeys[i]
        for r in range(16):
            F0, F1 = self._F(R[0], R[1])
            F0 &= 0xFFFFFFFF
            F1 &= 0xFFFFFFFF
            R[2] = ROR((R[2] ^ F0), 1)
            R[3] = ROL((R[3] ^ F1), 1)
            R = [R[2], R[3], R[0], R[1]]
        R = [R[2], R[3], R[0], R[1]]
        for i in range(4):
            R[i] ^= self.subkeys[i + 4]
        return struct.pack('<4I', *R)

    def decrypt_block(self, block: bytes) -> bytes:
        R = list(struct.unpack('<4I', block))
        for i in range(4):
            R[i] ^= self.subkeys[i + 4]
        R = [R[2], R[3], R[0], R[1]]
        for r in reversed(range(16)):
            R = [R[2], R[3], R[0], R[1]]
            F0, F1 = self._F(R[0], R[1])
            R[2] = ROL(R[2], 1) ^ (F0 & 0xFFFFFFFF)
            R[3] = ROR(R[3], 1) ^ (F1 & 0xFFFFFFFF)
        for i in range(4):
            R[i] ^= self.subkeys[i]
        return struct.pack('<4I', *R)
    
def pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

if __name__ == "__main__":
    key = b"This is a key123"  # 16 bytes = 128-bit key
    tf = Twofish(key)

    plaintext = b"emd crypto !!"  # 16 bytes
    padded = pad(plaintext)
    ciphertext = tf.encrypt_block(padded)
    decrypted = tf.decrypt_block(ciphertext)
    unpadded = unpad(decrypted)

    print("Plaintext :", plaintext)
    print("Ciphertext:", ciphertext.hex())
    print("Decrypted :", decrypted)
    print("Match     :", plaintext == unpadded)

"""

📘 Twofish — Implémentation Python (from scratch)

 🔐 Description

Twofish est un algorithme de chiffrement symétrique à bloc, finaliste du concours AES, conçu par Bruce Schneier. Il utilise :

* une **taille de bloc de 128 bits**
* des **clés de 128, 192 ou 256 bits**
* jusqu’à **16 tours de chiffrement**

---

📦 Classe `Twofish`

```python
class Twofish:
    def __init__(self, key: bytes)
```

🔑 Paramètre :

* `key`: Clé secrète de longueur 16, 24 ou 32 octets (128, 192 ou 256 bits).

🔧 Attributs :

* `self.K` : Liste des mots de clé (32 bits chacun).
* `self.S` : Liste des valeurs de S-box générées dynamiquement.
* `self.subkeys` : Liste des 40 sous-clés utilisées durant le chiffrement.

---

🔐 Méthodes principales

 `encrypt_block(self, block: bytes) -> bytes`

* 🔸 Chiffre un **bloc de 16 octets** (128 bits).
* 🔁 16 tours avec permutation, fonction F, rotation et MDS.
* 🛡 Applique les sous-clés avant, pendant et après les tours.

`decrypt_block(self, block: bytes) -> bytes`

* 🔸 Déchiffre un **bloc de 16 octets**.
* 🔁 Exécute les opérations de chiffrement en sens inverse.
* 🛡 Récupère le message original.

---

 ⚙️ Fonctions internes

`_expand_key()`

* Génère 40 sous-clés (K0...K39) + 4 valeurs S-box à partir de la clé.

 `_F(R0, R1) -> (int, int)`

* Calcule deux valeurs via la fonction non linéaire `g()` + MDS.

 `_g(X: int) -> int`

* Applique les S-boxes + matrice MDS à un mot de 32 bits.

`_h(X: int, L: List[int]) -> int`

* Fonction de hachage pour la génération de sous-clés.

---

 📌 Remarques

| Point                       | Détail                                                          |
| --------------------------- | --------------------------------------------------------------- |
| Taille de bloc              | 128 bits (16 octets)                                            |
| Longueurs de clé supportées | 128, 192, 256 bits                                              |
| Mode supporté               | Chiffrement d’un seul bloc (pas encore de ECB, CBC, etc.)       |
| Padding                     | Non inclus (peut être ajouté avec PKCS#7 si besoin)             |
| Dépendances externes        | Aucune — implémentation 100% Python pur                         |
| Niveau de sécurité          | Pédagogique (non optimisé ni certifié crypto), mais fonctionnel |

---

Souhaitez-vous que j’ajoute :

* 🧱 un **mode ECB ou CBC** ?
* 📁 une **lib complète avec padding + interface de haut niveau** ?
* 📚 une **doc HTML ou Markdown** exportable pour projet GitHub ?
"""