
# 🔐 Cryptography Project

This repository offers an educational, hands-on implementation of cryptographic algorithms. It covers classical symmetric encryption, modern symmetric and asymmetric encryption, cryptographic hash functions, and digital signatures. Designed for learning and demonstration purposes only.

---

## 📁 Project Structure

```

Cryptography/
├── src/
│   ├── 1. Classical Symmetric Encryption/
│   ├── 2. Modern Symmetric Encryption/
│   ├── 3. Asymmetric Encryption (Public-Key Cryptography)/
│   ├── 4. Cryptographic Hash Functions/
│   └── 5. Digital Signatures/
├── README.md
└── .gitignore

````

---

## 🔐 1. Classical Symmetric Encryption

Basic historical ciphers and cryptanalysis tools:

- `caesar.py` – Caesar Cipher
- `affine.py` – Affine Cipher
- `hill-cipher.py` – Hill Cipher
- `playfair.py` – Playfair Cipher
- `vigenere.py` – Vigenère Cipher
- `kasiski.py` – Kasiski Examination
- `index_of_coincidence.py` – Frequency analysis for cryptanalysis

---

## 🔐 2. Modern Symmetric Encryption

Standard and finalist modern block/stream ciphers:

- `AES.py` – Advanced Encryption Standard (AES)
- `DES.py` – Data Encryption Standard (obsolete)
- `RC4.py` – RC4 Stream Cipher
- `AES (finaliste)/`:
  - `mars.py` – MARS Algorithm
  - `twofish.py` – Twofish Algorithm
  - `rc6/rc6.py` – RC6 Cipher
  - `serpent/` – Serpent Cipher with test and utility modules

---

## 🔐 3. Asymmetric Encryption (Public-Key Cryptography)

Public-key cryptographic algorithms:

- `rsa.py` – RSA Encryption
- `ELGamal.py` – ElGamal Encryption
- `ecc.py` – Elliptic Curve Cryptography (ECC)
- `diffie_hellman.py` – Diffie-Hellman Key Exchange

📊 Visual aids:
- ECC diagrams
- RSA vs ECC comparison images

---

## 🔐 4. Cryptographic Hash Functions

Hashing algorithms for data integrity and fingerprinting:

- `MD5_Hash.py` – MD5 (insecure, educational use only)
- `sha1.py` – SHA-1 (deprecated)
- `sha-256.py` – SHA-256 (secure)
- `sha-512.py` – SHA-512 (secure)

---

## 🔐 5. Digital Signatures & Authentication

Authentication protocols, secret sharing, and digital signatures:

- `feight_fiat_shamir_0idf.py` – Fiat–Shamir Zero-Knowledge Proof
- `schnorrsignature.py` – Schnorr Digital Signature
- `shamir.py` – Shamir's Secret Sharing Scheme
- `signature_num.py` – Example of numerical digital signature

---

## ▶️ Getting Started


### 🔧 Usage

Run any algorithm by navigating to its directory and executing it:

```bash
cd src/1. Classical Symmetric Encryption
python caesar.py
````

> Some scripts include user input prompts or pre-defined test cases.


---

## 🧠 Author & Purpose

Developed by students passionate about cryptography, this project is built to strengthen theoretical understanding through practical implementation.
All code is written from scratch and intended solely for educational purposes — **not for production use**.

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE).

```

