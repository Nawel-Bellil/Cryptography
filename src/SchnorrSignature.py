#!/usr/bin/env python3
"""
Schnorr Signature Implementation from Scratch
============================================

This implementation includes:
- Elliptic curve operations over secp256k1
- Schnorr signature generation and verification
- Interactive terminal demo with step-by-step visualization

Author: Claude
Date: 2025
"""

import hashlib
import secrets
import time
import os
from typing import Tuple, Optional


class EllipticCurve:
    """Elliptic curve operations over secp256k1"""
    
    def __init__(self):
        # secp256k1 parameters
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.a = 0
        self.b = 7
        self.Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        self.Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.G = (self.Gx, self.Gy)
    
    def mod_inverse(self, a: int, m: int) -> int:
        """Extended Euclidean Algorithm for modular inverse"""
        if a < 0:
            a = (a % m + m) % m
        g, x, _ = self.extended_gcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        return x % m
    
    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Extended Euclidean Algorithm"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def point_add(self, P: Optional[Tuple[int, int]], Q: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Add two points on the elliptic curve"""
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                s = (3 * x1 * x1 + self.a) * self.mod_inverse(2 * y1, self.p) % self.p
            else:
                # Points are inverses
                return None
        else:
            # Point addition
            s = (y2 - y1) * self.mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def point_multiply(self, k: int, P: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Multiply point P by scalar k using double-and-add"""
        if k == 0:
            return None
        if k == 1:
            return P
        
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result
    
    def is_on_curve(self, P: Tuple[int, int]) -> bool:
        """Check if point P is on the curve"""
        x, y = P
        return (y * y) % self.p == (x * x * x + self.a * x + self.b) % self.p


class SchnorrSignature:
    """Schnorr Signature implementation"""
    
    def __init__(self):
        self.curve = EllipticCurve()
    
    def hash_function(self, message: bytes) -> int:
        """Hash function H(m) -> Zn"""
        return int.from_bytes(hashlib.sha256(message).digest(), 'big') % self.curve.n
    
    def hash_challenge(self, R: Tuple[int, int], P: Tuple[int, int], message: bytes) -> int:
        """Challenge hash H(R || P || m)"""
        Rx_bytes = R[0].to_bytes(32, 'big')
        Px_bytes = P[0].to_bytes(32, 'big')
        Py_bytes = P[1].to_bytes(32, 'big')
        combined = Rx_bytes + Px_bytes + Py_bytes + message
        return int.from_bytes(hashlib.sha256(combined).digest(), 'big') % self.curve.n
    
    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """Generate a private/public key pair"""
        # Private key: random integer in [1, n-1]
        private_key = secrets.randbelow(self.curve.n - 1) + 1
        
        # Public key: P = private_key * G
        public_key = self.curve.point_multiply(private_key, self.curve.G)
        
        return private_key, public_key
    
    def sign(self, message: bytes, private_key: int) -> Tuple[Tuple[int, int], int]:
        """
        Sign a message using Schnorr signature
        Returns: (R, s) where R is a point and s is an integer
        """
        # Generate random nonce k
        k = secrets.randbelow(self.curve.n - 1) + 1
        
        # Compute R = k * G
        R = self.curve.point_multiply(k, self.curve.G)
        
        # Compute public key P = private_key * G
        P = self.curve.point_multiply(private_key, self.curve.G)
        
        # Compute challenge e = H(R || P || m)
        e = self.hash_challenge(R, P, message)
        
        # Compute s = k + e * private_key (mod n)
        s = (k + e * private_key) % self.curve.n
        
        return (R, s)
    
    def verify(self, message: bytes, signature: Tuple[Tuple[int, int], int], public_key: Tuple[int, int]) -> bool:
        """
        Verify a Schnorr signature
        signature: (R, s)
        Returns: True if valid, False otherwise
        """
        R, s = signature
        
        # Compute challenge e = H(R || P || m)
        e = self.hash_challenge(R, public_key, message)
        
        # Verify: s * G = R + e * P
        left_side = self.curve.point_multiply(s, self.curve.G)
        right_side = self.curve.point_add(R, self.curve.point_multiply(e, public_key))
        
        return left_side == right_side


class SchnorrDemo:
    """Interactive demo for Schnorr signatures"""
    
    def __init__(self):
        self.schnorr = SchnorrSignature()
        self.delay = 1.5  # seconds between steps
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("=" * 60)
        print(f"  {title}")
        print("=" * 60)
        print()
    
    def print_step(self, step: int, description: str):
        """Print step with formatting"""
        print(f"📍 STEP {step}: {description}")
        print("-" * 40)
    
    def format_number(self, num: int, name: str, max_length: int = 64) -> str:
        """Format large numbers for display"""
        hex_str = hex(num)[2:].upper()
        if len(hex_str) > max_length:
            return f"{name}: {hex_str[:32]}...{hex_str[-32:]}"
        return f"{name}: {hex_str}"
    
    def format_point(self, point: Tuple[int, int], name: str) -> str:
        """Format elliptic curve point for display"""
        x, y = point
        x_str = hex(x)[2:].upper()
        y_str = hex(y)[2:].upper()
        return f"{name}:\n  x = {x_str[:32]}...{x_str[-32:]}\n  y = {y_str[:32]}...{y_str[-32:]}"
    
    def wait_for_continue(self):
        """Wait for user input to continue"""
        input("\n⏸️  Press Enter to continue...")
        time.sleep(0.5)
    
    def run_demo(self):
        """Run the complete Schnorr signature demo"""
        self.clear_screen()
        self.print_header("🔐 SCHNORR SIGNATURE DEMONSTRATION")
        
        print("Welcome to the Schnorr Signature interactive demo!")
        print("This will demonstrate the complete process of:")
        print("• Key generation")
        print("• Message signing")
        print("• Signature verification")
        print()
        print("The demo uses the secp256k1 elliptic curve (same as Bitcoin)")
        
        self.wait_for_continue()
        
        # Step 1: Key Generation
        self.clear_screen()
        self.print_step(1, "KEY GENERATION")
        print("Generating a private/public key pair...")
        time.sleep(self.delay)
        
        private_key, public_key = self.schnorr.generate_keypair()
        
        print("✅ Keys generated successfully!")
        print()
        print(self.format_number(private_key, "Private Key (d)"))
        print()
        print(self.format_point(public_key, "Public Key (P = d * G)"))
        
        self.wait_for_continue()
        
        # Step 2: Message Input
        self.clear_screen()
        self.print_step(2, "MESSAGE PREPARATION")
        
        message = input("Enter a message to sign: ").encode('utf-8')
        if not message:
            message = b"Hello, Schnorr signatures!"
            print(f"Using default message: {message.decode()}")
        
        print(f"\n📝 Message: '{message.decode()}'")
        print(f"📊 Message bytes: {message.hex().upper()}")
        
        message_hash = self.schnorr.hash_function(message)
        print(f"🔢 Message hash: {hex(message_hash)[2:].upper()}")
        
        self.wait_for_continue()
        
        # Step 3: Signature Generation
        self.clear_screen()
        self.print_step(3, "SIGNATURE GENERATION")
        print("Generating Schnorr signature...")
        print()
        
        print("🎲 Generating random nonce k...")
        time.sleep(self.delay)
        
        print("🔢 Computing R = k * G...")
        time.sleep(self.delay)
        
        print("🧮 Computing challenge e = H(R || P || m)...")
        time.sleep(self.delay)
        
        print("🔐 Computing s = k + e * d (mod n)...")
        time.sleep(self.delay)
        
        signature = self.schnorr.sign(message, private_key)
        R, s = signature
        
        print("✅ Signature generated successfully!")
        print()
        print(self.format_point(R, "R (commitment)"))
        print()
        print(self.format_number(s, "s (response)"))
        
        self.wait_for_continue()
        
        # Step 4: Signature Verification
        self.clear_screen()
        self.print_step(4, "SIGNATURE VERIFICATION")
        print("Verifying the signature...")
        print()
        
        print("🔢 Recomputing challenge e = H(R || P || m)...")
        time.sleep(self.delay)
        
        # Show the challenge computation
        e = self.schnorr.hash_challenge(R, public_key, message)
        print(f"📊 Challenge e: {hex(e)[2:].upper()}")
        print()
        
        print("🧮 Computing s * G...")
        time.sleep(self.delay)
        
        print("🧮 Computing R + e * P...")
        time.sleep(self.delay)
        
        print("🔍 Checking if s * G = R + e * P...")
        time.sleep(self.delay)
        
        is_valid = self.schnorr.verify(message, signature, public_key)
        
        if is_valid:
            print("✅ SIGNATURE IS VALID! 🎉")
            print()
            print("The signature verification equation holds:")
            print("s * G = R + e * P")
        else:
            print("❌ SIGNATURE IS INVALID!")
        
        self.wait_for_continue()
        
        # Step 5: Security Properties
        self.clear_screen()
        self.print_step(5, "SECURITY PROPERTIES")
        print("Schnorr signatures provide:")
        print()
        print("🔒 UNFORGEABILITY")
        print("   → Cannot create valid signatures without the private key")
        print()
        print("🔄 NON-MALLEABILITY") 
        print("   → Cannot modify existing signatures to create new valid ones")
        print()
        print("🎯 PROVABLE SECURITY")
        print("   → Security proven under discrete logarithm assumption")
        print()
        print("⚡ EFFICIENCY")
        print("   → Linear signature aggregation possible")
        print("   → Smaller signatures than ECDSA in some contexts")
        
        self.wait_for_continue()
        
        # Step 6: Mathematical Details
        self.clear_screen()
        self.print_step(6, "MATHEMATICAL FOUNDATION")
        print("Schnorr signatures work because:")
        print()
        print("1️⃣  SIGNING: s = k + e*d (mod n)")
        print("   • k = random nonce")  
        print("   • e = H(R || P || m) = challenge")
        print("   • d = private key")
        print()
        print("2️⃣  VERIFICATION: s*G = R + e*P")
        print("   • Substitute: (k + e*d)*G = R + e*P")
        print("   • Expand: k*G + e*d*G = R + e*P")
        print("   • Since R = k*G and P = d*G:")
        print("   • R + e*P = R + e*P ✓")
        print()
        print("The security relies on the difficulty of solving")
        print("the discrete logarithm problem on elliptic curves.")
        
        self.wait_for_continue()
        
        # Demo completion
        self.clear_screen()
        self.print_header("🎊 DEMO COMPLETE")
        print("You have successfully completed the Schnorr signature demo!")
        print()
        print("Summary of what we demonstrated:")
        print("✅ Generated cryptographically secure key pairs")
        print("✅ Created a Schnorr signature for your message")
        print("✅ Verified the signature mathematically")
        print("✅ Explored the security properties")
        print()
        print("The implementation is ready for educational use and")
        print("demonstrates the core concepts of Schnorr signatures.")
        print()
        print("Thank you for exploring cryptography! 🔐")


def main():
    """Main function to run the demo"""
    try:
        demo = SchnorrDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your Python environment and try again.")


if __name__ == "__main__":
    main()