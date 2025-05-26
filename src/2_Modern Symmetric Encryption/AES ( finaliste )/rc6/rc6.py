import math
import os

# Rotate right input x, by n bits
def ROR(x, n, bits=32):
    mask = (2**bits) - 1
    mask_bits = x & mask
    return ((x >> n) | (mask_bits << (bits - n))) & mask

# Rotate left input x, by n bits  
def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)

# Convert input sentence into blocks of binary
# Creates 4 blocks of binary each of 32 bits
def blockConverter(sentence):
    encoded = []
    res = ""
    for i in range(len(sentence)):
        if i % 4 == 0 and i != 0:
            encoded.append(res)
            res = ""
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) < 8:
            temp = "0" * (8 - len(temp)) + temp
        res = res + temp
    encoded.append(res)
    return encoded

# Converts 4 blocks array of long int into string
def deBlocker(blocks):
    s = ""
    for block in blocks:
        temp = bin(block)[2:]
        if len(temp) < 32:
            temp = "0" * (32 - len(temp)) + temp
        for i in range(4):
            byte_str = temp[i*8:(i+1)*8]
            if len(byte_str) == 8:  # Only convert if we have a full byte
                s = s + chr(int(byte_str, 2))
    return s

# Generate key s[0... 2r+3] from given input string userkey
def generateKey(userkey):
    r = 12
    w = 32
    b = len(userkey)
    modulo = 2**32
    s = [0] * (2*r + 4)
    s[0] = 0xB7E15163
    
    for i in range(1, 2*r + 4):
        s[i] = (s[i-1] + 0x9E3779B9) % (2**w)
    
    encoded = blockConverter(userkey)
    enlength = len(encoded)
    l = [0] * enlength
    
    # Fix: Convert binary strings to integers properly
    for i in range(enlength):
        l[i] = int(encoded[i], 2) if encoded[i] else 0
    
    v = 3 * max(enlength, 2*r + 4)
    A = B = i = j = 0
    
    for index in range(v):
        A = s[i] = ROL((s[i] + A + B) % modulo, 3, 32)
        B = l[j] = ROL((l[j] + A + B) % modulo, (A + B) % 32, 32)
        i = (i + 1) % (2*r + 4)
        j = (j + 1) % enlength
    
    return s

def encrypt(sentence, s):
    encoded = blockConverter(sentence)
    # Pad encoded list to have exactly 4 blocks
    while len(encoded) < 4:
        encoded.append("0" * 32)
    
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)
    
    orgi = [A, B, C, D]
    
    r = 12
    w = 32
    modulo = 2**32
    lgw = 5
    
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    
    for i in range(1, r + 1):
        t_temp = (B * (2*B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        u_temp = (D * (2*D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        A = (ROL(A ^ t, umod, 32) + s[2*i]) % modulo
        C = (ROL(C ^ u, tmod, 32) + s[2*i + 1]) % modulo
        (A, B, C, D) = (B, C, D, A)
    
    A = (A + s[2*r + 2]) % modulo
    C = (C + s[2*r + 3]) % modulo
    
    cipher = [A, B, C, D]
    return orgi, cipher

def decrypt(esentence, s):
    encoded = blockConverter(esentence)
    # Pad encoded list to have exactly 4 blocks
    while len(encoded) < 4:
        encoded.append("0" * 32)
    
    A = int(encoded[0], 2)
    B = int(encoded[1], 2)
    C = int(encoded[2], 2)
    D = int(encoded[3], 2)
    
    cipher = [A, B, C, D]
    
    r = 12
    w = 32
    modulo = 2**32
    lgw = 5
    
    C = (C - s[2*r + 3]) % modulo
    A = (A - s[2*r + 2]) % modulo
    
    for j in range(1, r + 1):
        i = r + 1 - j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D * (2*D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        t_temp = (B * (2*B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (ROR((C - s[2*i + 1]) % modulo, tmod, 32) ^ u)
        A = (ROR((A - s[2*i]) % modulo, umod, 32) ^ t)
    
    D = (D - s[1]) % modulo
    B = (B - s[0]) % modulo
    
    orgi = [A, B, C, D]
    return cipher, orgi

def encrypt_main():
    print("ENCRYPTION:")
    key = input("Enter Key (0-16 characters): ")
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    
    print("UserKey:", key)
    s = generateKey(key)
    
    sentence = input("Enter Sentence (0-16 characters): ")
    if len(sentence) < 16:
        sentence = sentence + " " * (16 - len(sentence))
    sentence = sentence[:16]
    
    orgi, cipher = encrypt(sentence, s)
    esentence = deBlocker(cipher)
    
    print("\nInput String:", sentence)
    print("Original String list:", orgi)
    print("Length of Input String:", len(sentence))
    
    print("\nEncrypted String list:", cipher)
    print("Encrypted String:", repr(esentence))  # Use repr to show special characters
    print("Length of Encrypted String:", len(esentence))
    
    # Create directory structure if it doesn't exist
    output_dir = os.path.join("src", "🔐 2. Modern Symmetric Encryption", "AES ( finaliste )", "rc6")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        encrypted_file_path = os.path.join(output_dir, "encrypted.txt")
        with open(encrypted_file_path, "w", encoding='utf-8') as f:
            f.write(esentence)
        print(f"Encrypted data saved to {encrypted_file_path}")
        
        # Also save encryption details
        details_file_path = os.path.join(output_dir, "encryption_details.txt")
        with open(details_file_path, "w", encoding='utf-8') as f:
            f.write(f"RC6 Encryption Results\n")
            f.write(f"===================\n\n")
            f.write(f"Key: {key}\n")
            f.write(f"Original Text: {sentence}\n")
            f.write(f"Original String List: {orgi}\n")
            f.write(f"Encrypted String List: {cipher}\n")
            f.write(f"Encrypted Text Length: {len(esentence)}\n")
        print(f"Encryption details saved to {details_file_path}")
        
    except Exception as e:
        print(f"Error saving file: {e}")

def decrypt_main():
    print("DECRYPTION:")
    key = input("Enter Key (0-16 characters): ")
    if len(key) < 16:
        key = key + " " * (16 - len(key))
    key = key[:16]
    
    print("UserKey:", key)
    s = generateKey(key)
    
    # Look for encrypted file in the specified directory first
    output_dir = os.path.join("src", "🔐 2. Modern Symmetric Encryption", "AES ( finaliste )", "rc6")
    encrypted_file_path = os.path.join(output_dir, "encrypted.txt")
    
    try:
        # Try to read from the specified directory first
        if os.path.exists(encrypted_file_path):
            with open(encrypted_file_path, "r", encoding='utf-8') as f:
                esentence = f.read()
            print(f"Reading encrypted data from {encrypted_file_path}")
        else:
            # Fallback to current directory
            with open("encrypted.txt", "r", encoding='utf-8') as f:
                esentence = f.read()
            print("Reading encrypted data from encrypted.txt")
    except FileNotFoundError:
        print("Encrypted input not found. Please run encryption first.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    cipher, orgi = decrypt(esentence, s)
    sentence = deBlocker(orgi)
    
    print("\nEncrypted String list:", cipher)
    print("Encrypted String:", repr(esentence))
    print("Length of Encrypted String:", len(esentence))
    
    print("\nDecrypted String list:", orgi)
    print("Decrypted String:", sentence)
    print("Length of Decrypted String:", len(sentence))
    
    # Save decryption results
    try:
        decryption_file_path = os.path.join(output_dir, "decrypted.txt")
        with open(decryption_file_path, "w", encoding='utf-8') as f:
            f.write(sentence)
        print(f"Decrypted data saved to {decryption_file_path}")
        
        # Also save decryption details
        details_file_path = os.path.join(output_dir, "decryption_details.txt")
        with open(details_file_path, "w", encoding='utf-8') as f:
            f.write(f"RC6 Decryption Results\n")
            f.write(f"===================\n\n")
            f.write(f"Key: {key}\n")
            f.write(f"Encrypted String List: {cipher}\n")
            f.write(f"Decrypted String List: {orgi}\n")
            f.write(f"Decrypted Text: {sentence}\n")
            f.write(f"Decrypted Text Length: {len(sentence)}\n")
        print(f"Decryption details saved to {details_file_path}")
        
    except Exception as e:
        print(f"Error saving decryption results: {e}")

def main():
    print("RC6 Encryption/Decryption Tool")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose option (1 or 2): ")
    
    if choice == "1":
        encrypt_main()
    elif choice == "2":
        decrypt_main()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()