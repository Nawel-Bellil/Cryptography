import hashlib
from typing import Tuple

# === Helper functions ===
def modinv(a, m):
    """Modular inverse via extended Euclidean algorithm"""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m

def extended_gcd(a, b):
    """Extended GCD algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def hash_message(msg: str, r: int, q: int) -> int:
    """Hash function H(m || r) mod q"""
    input_string = msg + str(r)
    print(f"🔍 Hash input: '{input_string}'")
    hasher = hashlib.sha256()
    hasher.update(input_string.encode())
    h = int(hasher.hexdigest(), 16) % q
    print(f"🧮 Hash output (mod q): {h}")
    return h

def schnorr_keygen(p: int, q: int, g: int, x: int) -> int:
    """Compute public key y = g^x mod p"""
    return pow(g, x, p)

def schnorr_sign(msg: str, x: int, p: int, q: int, g: int, k: int) -> Tuple[int, int]:
    r = pow(g, k, p)
    print(f"🌀 r = g^k mod p = {r}")
    e = hash_message(msg, r, q)
    s = (k + x * e) % q
    print(f"📝 Signature: e = {e}, s = {s}")
    return e, s

def schnorr_verify(msg: str, e: int, s: int, y: int, p: int, q: int, g: int) -> bool:
    try:
        y_e_inv = modinv(pow(y, e, p), p)
        r_ = (pow(g, s, p) * y_e_inv) % p
        print(f"🔁 Recomputed r' = {r_}")
        e_ = hash_message(msg, r_, q)
        print(f"🔁 Recomputed e' = {e_}")
        return e == e_
    except Exception as ex:
        print(f"❗ Verification failed: {ex}")
        return False

# === Generator finder ===
def find_generator(p, q):
    """Find a generator of order q modulo p"""
    for g in range(2, p):
        if pow(g, q, p) == 1:
            # Ensure it's of exact order q
            if all(pow(g, q // d, p) != 1 for d in range(2, q) if q % d == 0):
                return g
    raise Exception("No valid generator g found")

# === Main interactive demo ===
def main():
    print("🔐 Schnorr Signature Demo (Manual Inputs)\n")

    # STEP 1
    print("📌 STEP 1: System Parameters (p, q, g)")
    default_p, default_q = 607, 101
    p_input = input(f"Enter a large prime p (default {default_p}): ")
    q_input = input(f"Enter a prime q such that q | (p - 1) (default {default_q}): ")

    p = int(p_input) if p_input.strip() else default_p
    q = int(q_input) if q_input.strip() else default_q

    if (p - 1) % q != 0:
        print("❌ Error: q does not divide (p - 1). Exiting.")
        return

    print("🔍 Finding generator g of order q mod p...")
    try:
        g = find_generator(p, q)
        print(f"✅ Found valid generator: g = {g}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # STEP 2
    print("\n🔑 STEP 2: Key Generation")
    x_input = input(f"Enter private key x ∈ [1, {q-1}] (default 5): ")
    x = int(x_input) if x_input.strip() else 5
    y = schnorr_keygen(p, q, g, x)
    print("✅ Public key y = g^x mod p =", y)

    # STEP 3
    print("\n📝 STEP 3: Signing")
    msg = input("Enter the message to sign: ").strip() or "hello schnorr"
    k_input = input(f"Choose random nonce k ∈ [1, {q-1}] (default 13): ")
    k = int(k_input) if k_input.strip() else 13
    e, s = schnorr_sign(msg, x, p, q, g, k)
    print(f"\n🖊️ Signature generated:\ne = {e}\ns = {s}")

    # STEP 4
    print("\n🔎 STEP 4: Verification")
    print(f"Verifying signature for message: '{msg}'")
    valid = schnorr_verify(msg, e, s, y, p, q, g)
    print("✅ Signature VALID" if valid else "❌ Signature INVALID")

if __name__ == "__main__":
    main()
