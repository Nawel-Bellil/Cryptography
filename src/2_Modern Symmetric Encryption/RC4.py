def encryption():
    global key, plain_text, n

    # Entrée manuelle du texte clair et de la clé
    plain_text = input("Entrez le texte clair (binaire)    : ").strip()
    key = input("Entrez la clé (binaire)              : ").strip()
    n = int(input("Entrez la taille des blocs (bits) n : "))

    print("\nPlain text : ", plain_text)
    print("Key        : ", key)
    print("n          : ", n)

    # État initial
    S = [i for i in range(0, 2**n)]

    key_list = [key[i:i + n] for i in range(0, len(key), n)]
    key_list = [int(k, 2) for k in key_list]

    global pt
    pt = [plain_text[i:i + n] for i in range(0, len(plain_text), n)]
    pt = [int(p, 2) for p in pt]

    # Adapter la longueur de la clé
    while len(key_list) < len(S):
        key_list.append(key_list[len(key_list) % len(key_list)])

    print("\nKSA iterations:")
    def KSA():
        j = 0
        for i in range(len(S)):
            j = (j + S[i] + key_list[i]) % len(S)
            S[i], S[j] = S[j], S[i]
            print(f"{i} -> {S}")
        print("\nInitial permutation array:", S)
    KSA()

    print("\nPGRA iterations:")
    global key_stream
    key_stream = []
    def PGRA():
        i = j = 0
        for k in range(len(pt)):
            i = (i + 1) % len(S)
            j = (j + S[i]) % len(S)
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % len(S)
            key_stream.append(S[t])
            print(f"{k} -> {S}")
    PGRA()

    print("\nKey stream:", key_stream)

    global cipher_text
    cipher_text = [key_stream[i] ^ pt[i] for i in range(len(pt))]

    encrypted_bits = ''.join(f'{c:0{n}b}' for c in cipher_text)
    print("\nCipher text :", encrypted_bits)

def decryption():
    S = [i for i in range(0, 2**n)]

    key_list = [key[i:i + n] for i in range(0, len(key), n)]
    key_list = [int(k, 2) for k in key_list]

    pt = [plain_text[i:i + n] for i in range(0, len(plain_text), n)]
    pt = [int(p, 2) for p in pt]

    while len(key_list) < len(S):
        key_list.append(key_list[len(key_list) % len(key_list)])

    print("\nKSA iterations:")
    def KSA():
        j = 0
        for i in range(len(S)):
            j = (j + S[i] + key_list[i]) % len(S)
            S[i], S[j] = S[j], S[i]
            print(f"{i} -> {S}")
        print("\nInitial permutation array:", S)
    KSA()

    print("\nPGRA iterations:")
    global key_stream
    key_stream = []
    def PGRA():
        i = j = 0
        for k in range(len(pt)):
            i = (i + 1) % len(S)
            j = (j + S[i]) % len(S)
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % len(S)
            key_stream.append(S[t])
            print(f"{k} -> {S}")
    PGRA()

    print("\nKey stream:", key_stream)

    global original_text
    original_text = [key_stream[i] ^ cipher_text[i] for i in range(len(cipher_text))]

    decrypted_bits = ''.join(f'{b:0{n}b}' for b in original_text)
    print("\nDecrypted text :", decrypted_bits)

# Lancer les fonctions
encryption()
print("\n" + "-"*60 + "\n")
decryption()
