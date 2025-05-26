import math

print("\n=== Démo interactive : Calcul du hash MD5 ===\n")
print("⚠️  MD5 n'est plus sécurisé pour les usages cryptographiques !\n"
      "Mais il reste utile pour des vérifications d'intégrité rapides.\n")

# Étapes de rotation
rotate_by = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

# Constantes dérivées des sinus
constants = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

def pad(msg_bytes):
    print("🔧 Étape 1 : Padding du message...")
    msg_len_bits = (8 * len(msg_bytes)) & 0xFFFFFFFFFFFFFFFF
    print(f"Longueur initiale : {len(msg_bytes)} octets ({msg_len_bits} bits)")
    msg_bytes.append(0x80)
    while len(msg_bytes) % 64 != 56:
        msg_bytes.append(0)
    msg_bytes += msg_len_bits.to_bytes(8, byteorder='little')
    print(f"Longueur après padding : {len(msg_bytes)} octets")
    input("➡️  Appuyez sur Entrée pour continuer...\n")
    return msg_bytes

def leftRotate(x, amount):
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def processMessage(msg_bytes):
    print("🔧 Étape 2 : Traitement par blocs de 512 bits...")
    A, B, C, D = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    for offset in range(0, len(msg_bytes), 64):
        a, b, c, d = A, B, C, D
        block = msg_bytes[offset:offset + 64]
        print(f"🧱 Traitement du bloc {offset // 64 + 1}:")
        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            to_add = int.from_bytes(block[4 * g:4 * g + 4], byteorder='little')
            f = (f + a + constants[i] + to_add) & 0xFFFFFFFF
            rotated = leftRotate(f, rotate_by[i])
            a, d, c, b = d, c, b, (b + rotated) & 0xFFFFFFFF

            print(f"  ➤ Opération {i+1:02d} | f = {hex(f)} | g = {g:2d} | rot = {rotate_by[i]:2d} | b = {hex(b)}")

            if (i + 1) % 16 == 0:
                input(f"🔁 Fin du round {i // 16 + 1}. Appuyez sur Entrée...\n")

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF
        print(f"🔚 Bloc terminé → A,B,C,D = {hex(A)}, {hex(B)}, {hex(C)}, {hex(D)}\n")

    digest = (A.to_bytes(4, 'little') + B.to_bytes(4, 'little') +
              C.to_bytes(4, 'little') + D.to_bytes(4, 'little'))
    return digest

def md5(message):
    print(f"📩 Message original : '{message}'\n")
    msg_bytes = bytearray(message, 'ascii')
    msg_bytes = pad(msg_bytes)
    digest_bytes = processMessage(msg_bytes)
    hex_result = ''.join(f'{byte:02x}' for byte in digest_bytes)
    print(f"✅ Résultat final (MD5) : {hex_result}\n")
    return hex_result
def run_tests():
    print("\n=== 🎯 Lancement des tests standards MD5 ===\n")
    test_vectors = {
        "": "d41d8cd98f00b204e9800998ecf8427e",
        "a": "0cc175b9c0f1b6a831c399e269772661",
        "abc": "900150983cd24fb0d6963f7d28e17f72",
        "message digest": "f96b697d7cb7938d525a2f31aaf161d0",
        "abcdefghijklmnopqrstuvwxyz": "c3fcd3d76192e4007dfb496cca67e13b",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            "d174ab98d277d9f5a5611c2c9f419d9f",
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890":
            "57edf4a22be3c955ac49da2e2107b67a"
    }

    for i, (msg, expected) in enumerate(test_vectors.items(), 1):
        print(f"\n🔍 Test {i} : '{msg}'")
        result = md5(msg)
        if result == expected:
            print(f"✅ MATCH : {result}")
        else:
            print(f"❌ FAIL\nAttendu : {expected}\nObtenu : {result}")
        print("-" * 50)

if __name__ == "__main__":
    # Pour tester rapidement les vecteurs classiques :
    # run_tests()
    choix = input("Mode (1=Interactif | 2=Tests auto) : ")
    if choix.strip() == "1":
        message = input("✍️  Entrez un message à hacher avec MD5 :\n> ")
        md5(message)
    else:
        run_tests()
