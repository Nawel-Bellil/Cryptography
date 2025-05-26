import os
import shutil

base = "src"

folders = {
    "classical_symmetric_encryption": ["affine.py", "caesar.py", "hill-cipher.py", "index_of_coincidence.py", "kasiski.py", "playfair.py", "vigenere.py"],
    "modern_symmetric_encryption": ["AES.py", "DES.py", "RC4.py", "rc4.png"],
    "asymmetric_encryption": ["diffie_hellman.py", "ecc.py", "ELGamal.py", "rsa.py"],
    "digital_signatures": ["SchnorrSignature.py", "Feight-Fiat-Shamir-0idf.py", "shamir.py", "signature_num.py"],
    "hash_functions": ["MD5_Hash.py", "sha-256.py", "sha-512.py", "sha1.py"],
    "message_authentication": []
}

# Move each file to the correct subfolder
for folder, files in folders.items():
    target = os.path.join(base, folder)
    os.makedirs(target, exist_ok=True)
    for file in files:
        src_path = os.path.join(base, file)
        if os.path.exists(src_path):
            shutil.move(src_path, os.path.join(target, file.lower().replace("-", "_")))

# Move AES finalist folder
if os.path.exists(os.path.join(base, "AES ( finaliste )")):
    shutil.move(os.path.join(base, "AES ( finaliste )"), os.path.join(base, "modern_symmetric_encryption", "aes_finalist"))

# Move diagram images
diagrams = [
    "elliptic-curve-cryptography-diagram.png",
    "elliptic-curve-cryptography.png",
    "rsa vs ecc - key length.png",
    "rsa vs ecc.png"
]
diagram_dir = os.path.join(base, "asymmetric_encryption", "diagrams")
os.makedirs(diagram_dir, exist_ok=True)

for img in diagrams:
    img_path = os.path.join(base, img)
    if os.path.exists(img_path):
        new_name = img.lower().replace(" ", "_").replace("-", "_")
        shutil.move(img_path, os.path.join(diagram_dir, new_name))

print("✅ Reorganization complete.")
