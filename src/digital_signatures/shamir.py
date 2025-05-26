import random
import time
from typing import List, Tuple
from math import gcd

class ShamirSecretSharing:
    """
    Implementation of Shamir's Secret Sharing scheme.
    
    This protocol allows splitting a secret into n shares where any k shares
    can reconstruct the original secret, but k-1 shares reveal nothing.
    """
    
    def __init__(self, secret: int = None, k: int = None, n: int = None, prime: int = None):
        """
        Initialize Shamir's Secret Sharing.
        
        Args:
            secret: The secret value to share (will ask for input if None)
            k: Threshold - minimum shares needed to reconstruct (will ask if None)
            n: Total number of shares to generate (will ask if None)
            prime: Prime modulus for calculations (will ask if None)
        """
        self.secret = secret
        self.k = k  # threshold
        self.n = n  # total shares
        self.prime = prime
        self.polynomial_coeffs = []
        self.shares = []
        
        if any(param is None for param in [secret, k, n, prime]):
            self._get_user_parameters()
        
        self._validate_parameters()
        self._generate_polynomial()
        self._generate_shares()
    
    def _get_user_parameters(self):
        """Get scheme parameters from user input."""
        print("\n" + "="*60)
        print("SHAMIR'S SECRET SHARING SETUP")
        print("="*60)
        
        print("\nWelcome to Shamir's Secret Sharing Demo!")
        print("This scheme splits a secret into shares where:")
        print("✅ k shares can reconstruct the secret")
        print("❌ k-1 shares reveal nothing about the secret")
        
        if self.secret is None:
            print("\n📝 Step 1: Enter the secret to share")
            print("   This is the value you want to protect")
            while True:
                try:
                    self.secret = int(input("   Enter secret (positive integer): "))
                    if self.secret > 0:
                        break
                    else:
                        print("   ❌ Secret must be positive. Try again.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        if self.k is None:
            print(f"\n📝 Step 2: Choose threshold (k)")
            print(f"   Minimum number of shares needed to reconstruct secret = {self.secret}")
            print(f"   Recommended: 2-5 for demo purposes")
            while True:
                try:
                    self.k = int(input("   Enter threshold k: "))
                    if 2 <= self.k <= 10:
                        break
                    else:
                        print("   ❌ Please choose k between 2 and 10.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        if self.n is None:
            print(f"\n📝 Step 3: Choose total number of shares (n)")
            print(f"   Must be >= k = {self.k}")
            print(f"   Recommended: {self.k + 1} to {self.k + 3} for demo")
            while True:
                try:
                    self.n = int(input(f"   Enter total shares n (>= {self.k}): "))
                    if self.n >= self.k and self.n <= 15:
                        break
                    elif self.n < self.k:
                        print(f"   ❌ n must be >= k = {self.k}. Try again.")
                    else:
                        print("   ❌ Please choose n <= 15 for demo.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        if self.prime is None:
            print(f"\n📝 Step 4: Choose prime modulus")
            print(f"   Must be larger than both secret ({self.secret}) and n ({self.n})")
            print(f"   Suggested primes: 101, 103, 107, 109, 113")
            
            # Suggest a suitable prime
            min_prime = max(self.secret, self.n) + 1
            suggested_prime = self._next_prime(min_prime)
            
            print(f"   Minimum required: > {max(self.secret, self.n)}")
            print(f"   Suggested: {suggested_prime}")
            
            while True:
                try:
                    user_input = input(f"   Enter prime (or press Enter for {suggested_prime}): ")
                    if user_input.strip() == "":
                        self.prime = suggested_prime
                        break
                    else:
                        self.prime = int(user_input)
                        if self._is_prime(self.prime) and self.prime > max(self.secret, self.n):
                            break
                        elif not self._is_prime(self.prime):
                            print("   ❌ That's not a prime number. Try again.")
                        else:
                            print(f"   ❌ Prime must be > {max(self.secret, self.n)}. Try again.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        print(f"\n✅ Secret sharing parameters set:")
        print(f"   Secret: {self.secret}")
        print(f"   Threshold (k): {self.k}")
        print(f"   Total shares (n): {self.n}")
        print(f"   Prime modulus: {self.prime}")
        print(f"   Scheme: ({self.k}, {self.n})-threshold secret sharing")
        
        input("\n   Press Enter to continue...")
    
    def _is_prime(self, num: int) -> bool:
        """Check if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    def _next_prime(self, n: int) -> int:
        """Find the next prime number >= n."""
        while not self._is_prime(n):
            n += 1
        return n
    
    def _validate_parameters(self):
        """Validate that all parameters are consistent."""
        if self.k > self.n:
            raise ValueError(f"Threshold k={self.k} cannot be greater than total shares n={self.n}")
        if self.prime <= max(self.secret, self.n):
            raise ValueError(f"Prime {self.prime} must be greater than secret and n")
        if not self._is_prime(self.prime):
            raise ValueError(f"{self.prime} is not a prime number")
    
    def _generate_polynomial(self):
        """Generate random polynomial coefficients with user interaction."""
        print("\n" + "="*60)
        print("POLYNOMIAL GENERATION")
        print("="*60)
        
        print(f"\n🔢 Creating polynomial of degree {self.k-1}")
        print(f"   f(x) = a₀ + a₁x + a₂x² + ... + a₍ₖ₋₁₎x^{self.k-1} mod {self.prime}")
        print(f"   Where a₀ = secret = {self.secret}")
        
        # First coefficient is the secret
        self.polynomial_coeffs = [self.secret]
        
        print(f"\n   Coefficient a₀ = {self.secret} (the secret)")
        
        # Generate random coefficients for higher degree terms
        print(f"   Generating {self.k-1} random coefficients...")
        
        for i in range(1, self.k):
            coeff = random.randint(1, self.prime - 1)
            self.polynomial_coeffs.append(coeff)
            print(f"   Coefficient a{i} = {coeff} (random)")
            time.sleep(0.3)
        
        # Display the complete polynomial
        poly_str = f"f(x) = {self.polynomial_coeffs[0]}"
        for i in range(1, len(self.polynomial_coeffs)):
            poly_str += f" + {self.polynomial_coeffs[i]}x"
            if i > 1:
                poly_str += f"^{i}"
        poly_str += f" mod {self.prime}"
        
        print(f"\n✅ Generated polynomial:")
        print(f"   {poly_str}")
        
        input("\n   Press Enter to continue to share generation...")
    
    def _evaluate_polynomial(self, x: int) -> int:
        """Evaluate the polynomial at point x."""
        result = 0
        for i, coeff in enumerate(self.polynomial_coeffs):
            result += coeff * pow(x, i, self.prime)
            result %= self.prime
        return result
    
    def _generate_shares(self):
        """Generate n shares by evaluating polynomial at different points."""
        print("\n" + "="*60)
        print("SHARE GENERATION")
        print("="*60)
        
        print(f"\n📊 Generating {self.n} shares by evaluating f(x) at x = 1, 2, ..., {self.n}")
        print(f"   Each share is a point (x, f(x)) on the polynomial")
        
        for x in range(1, self.n + 1):
            y = self._evaluate_polynomial(x)
            self.shares.append((x, y))
            
            # Show calculation
            calc_str = f"f({x}) = {self.polynomial_coeffs[0]}"
            for i in range(1, len(self.polynomial_coeffs)):
                term = self.polynomial_coeffs[i] * pow(x, i, self.prime) % self.prime
                calc_str += f" + {self.polynomial_coeffs[i]}×{x}"
                if i > 1:
                    calc_str += f"^{i}"
            
            print(f"   Share {x}: f({x}) = {y}")
            print(f"            Calculation: {calc_str} ≡ {y} (mod {self.prime})")
            time.sleep(0.4)
        
        print(f"\n✅ Generated {self.n} shares:")
        for i, (x, y) in enumerate(self.shares, 1):
            print(f"   Share {i}: ({x}, {y})")
        
        input("\n   Press Enter to continue...")
    
    def _wait_for_user(self, prompt: str = "Press Enter to continue..."):
        """Wait for user input with a custom prompt."""
        input(f"\n   {prompt}")
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse using extended Euclidean algorithm."""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd_val, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd_val, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def _lagrange_interpolation(self, points: List[Tuple[int, int]]) -> int:
        """Reconstruct secret using Lagrange interpolation."""
        if len(points) < self.k:
            raise ValueError(f"Need at least {self.k} points, got {len(points)}")
        
        # Use only the first k points
        points = points[:self.k]
        
        print(f"\n🔍 Using Lagrange interpolation with {len(points)} points:")
        for i, (x, y) in enumerate(points, 1):
            print(f"   Point {i}: ({x}, {y})")
        
        result = 0
        
        print(f"\n📊 Lagrange interpolation formula:")
        print(f"   f(0) = Σ yᵢ × ∏(0-xⱼ)/(xᵢ-xⱼ) for i≠j")
        
        for i, (xi, yi) in enumerate(points):
            # Calculate Lagrange basis polynomial at x=0
            numerator = 1
            denominator = 1
            
            print(f"\n   For point ({xi}, {yi}):")
            num_factors = []
            den_factors = []
            
            for j, (xj, _) in enumerate(points):
                if i != j:
                    numerator = (numerator * (0 - xj)) % self.prime
                    denominator = (denominator * (xi - xj)) % self.prime
                    num_factors.append(f"(0-{xj})")
                    den_factors.append(f"({xi}-{xj})")
            
            # Calculate modular inverse of denominator
            denominator_inv = self._mod_inverse(denominator, self.prime)
            
            # Lagrange coefficient
            lagrange_coeff = (numerator * denominator_inv) % self.prime
            
            print(f"     Numerator: {' × '.join(num_factors)} = {numerator}")
            print(f"     Denominator: {' × '.join(den_factors)} = {denominator}")
            print(f"     Coefficient: {numerator} × {denominator}⁻¹ ≡ {lagrange_coeff} (mod {self.prime})")
            
            # Add contribution to result
            contribution = (yi * lagrange_coeff) % self.prime
            result = (result + contribution) % self.prime
            
            print(f"     Contribution: {yi} × {lagrange_coeff} ≡ {contribution} (mod {self.prime})")
        
        print(f"\n   Final result: f(0) ≡ {result} (mod {self.prime})")
        
        return result
    
    def reconstruction_demo(self):
        """Interactive demonstration of secret reconstruction."""
        print("\n" + "="*60)
        print("SECRET RECONSTRUCTION DEMO")
        print("="*60)
        
        print(f"\n🎯 Goal: Reconstruct secret using k = {self.k} shares")
        print(f"📊 Available shares: {self.n}")
        print(f"🔐 Original secret: {self.secret}")
        
        while True:
            print(f"\n📋 Available shares:")
            for i, (x, y) in enumerate(self.shares, 1):
                print(f"   {i}. Share ({x}, {y})")
            
            print(f"\n🎲 Choose how to select {self.k} shares:")
            print(f"   1. Let me choose manually")
            print(f"   2. Use first {self.k} shares")
            print(f"   3. Use random {self.k} shares")
            print(f"   4. Test with insufficient shares ({self.k-1})")
            print(f"   5. Return to main menu")
            
            while True:
                try:
                    choice = int(input(f"\n   Enter choice (1-5): "))
                    if 1 <= choice <= 5:
                        break
                    else:
                        print("   ❌ Please enter a number between 1 and 5.")
                except ValueError:
                    print("   ❌ Please enter a valid number.")
            
            if choice == 1:
                selected_shares = self._manual_share_selection()
            elif choice == 2:
                selected_shares = self.shares[:self.k]
                print(f"   Selected first {self.k} shares: {selected_shares}")
            elif choice == 3:
                selected_shares = random.sample(self.shares, self.k)
                print(f"   Randomly selected {self.k} shares: {selected_shares}")
            elif choice == 4:
                selected_shares = self.shares[:self.k-1]
                print(f"   Selected {self.k-1} shares (insufficient): {selected_shares}")
            elif choice == 5:
                return
            
            self._wait_for_user("Press Enter to start reconstruction...")
            
            # Attempt reconstruction
            try:
                if len(selected_shares) < self.k:
                    print(f"\n❌ INSUFFICIENT SHARES")
                    print(f"   Need {self.k} shares, but only have {len(selected_shares)}")
                    print(f"   Cannot reconstruct the secret!")
                    
                    # Show that we can't determine the secret uniquely
                    print(f"\n🔍 Why this fails:")
                    print(f"   With {len(selected_shares)} points, we can fit multiple polynomials")
                    print(f"   of degree {self.k-1}, each giving different secrets!")
                else:
                    reconstructed = self._lagrange_interpolation(selected_shares)
                    
                    print(f"\n🎉 RECONSTRUCTION RESULT:")
                    print(f"   Reconstructed secret: {reconstructed}")
                    print(f"   Original secret: {self.secret}")
                    
                    if reconstructed == self.secret:
                        print(f"   ✅ SUCCESS! Secrets match!")
                    else:
                        print(f"   ❌ ERROR! Secrets don't match!")
                        print(f"   This shouldn't happen - check implementation!")
            
            except Exception as e:
                print(f"\n❌ Reconstruction failed: {e}")
            
            print(f"\n" + "-"*40)
            choice = input("Try another reconstruction? (y/n): ").lower().strip()
            if choice != 'y':
                break
    
    def _manual_share_selection(self) -> List[Tuple[int, int]]:
        """Allow user to manually select shares."""
        selected = []
        available_indices = list(range(len(self.shares)))
        
        print(f"\n📝 Select {self.k} shares:")
        
        for i in range(self.k):
            print(f"\n   Available shares:")
            for idx in available_indices:
                share_num = idx + 1
                x, y = self.shares[idx]
                print(f"   {share_num}. Share ({x}, {y})")
            
            while True:
                try:
                    choice = int(input(f"   Select share {i+1}/{self.k}: "))
                    if 1 <= choice <= len(self.shares) and (choice-1) in available_indices:
                        selected.append(self.shares[choice-1])
                        available_indices.remove(choice-1)
                        print(f"   ✅ Selected share {choice}: {self.shares[choice-1]}")
                        break
                    else:
                        print(f"   ❌ Invalid choice or already selected. Try again.")
                except ValueError:
                    print(f"   ❌ Please enter a valid number.")
        
        return selected
    
    def security_demo(self):
        """Demonstrate security properties of the scheme."""
        print("\n" + "="*60)
        print("SECURITY DEMONSTRATION")
        print("="*60)
        
        print(f"\n🛡️ Security Property: (k-1) shares reveal NO information")
        print(f"   We'll show that {self.k-1} shares are completely useless!")
        
        # Take k-1 shares
        insufficient_shares = self.shares[:self.k-1]
        print(f"\n📊 Using {self.k-1} shares:")
        for i, (x, y) in enumerate(insufficient_shares, 1):
            print(f"   Share {i}: ({x}, {y})")
        
        print(f"\n🔍 Testing different possible secrets...")
        print(f"   For each guess, we'll see if it's consistent with our {self.k-1} shares")
        
        # Test several possible secrets
        test_secrets = [self.secret]  # Include the real secret
        
        # Add some other random secrets
        for _ in range(4):
            fake_secret = random.randint(1, self.prime - 1)
            if fake_secret != self.secret:
                test_secrets.append(fake_secret)
        
        consistent_secrets = []
        
        for test_secret in test_secrets:
            print(f"\n   Testing secret = {test_secret}:")
            
            # Can we construct a polynomial with this secret that fits our shares?
            # We need to solve a system of linear equations
            consistent = self._check_consistency(test_secret, insufficient_shares)
            
            if consistent:
                consistent_secrets.append(test_secret)
                print(f"   ✅ Consistent! Could be the secret.")
            else:
                print(f"   ❌ Inconsistent with shares.")
        
        print(f"\n📊 SECURITY ANALYSIS:")
        print(f"   Secrets consistent with {self.k-1} shares: {len(consistent_secrets)}")
        print(f"   Consistent secrets: {consistent_secrets}")
        
        if len(consistent_secrets) > 1:
            print(f"   🎉 SUCCESS! Multiple secrets are possible!")
            print(f"   🔐 The {self.k-1} shares reveal nothing about the real secret!")
        else:
            print(f"   ⚠️  Only one consistent secret found.")
            print(f"   This might be due to small parameter choices.")
        
        print(f"\n💡 Key insight:")
        print(f"   With {self.k-1} shares, an attacker cannot distinguish")
        print(f"   between multiple possible secrets - perfect security!")
        
        input(f"\n   Press Enter to continue...")
    
    def _check_consistency(self, test_secret: int, shares: List[Tuple[int, int]]) -> bool:
        """Check if a test secret could generate the given shares."""
        # For a polynomial of degree k-1, we need k coefficients
        # We have k-1 shares plus the secret (which gives us f(0))
        # This gives us exactly k points, which should determine a unique polynomial
        
        # Create the system: we know f(0) = test_secret and f(xi) = yi for each share
        points = [(0, test_secret)] + shares
        
        if len(points) < self.k:
            # With fewer than k points, any secret could work with some polynomial
            return True
        
        # Try to construct a polynomial of degree k-1 that fits these points
        # If we can, then this secret is consistent
        try:
            # Use Lagrange interpolation to see if we get a valid polynomial
            # For this simplified check, we'll just see if the interpolation works
            result = self._lagrange_interpolation_general(points, 0)
            return result == test_secret
        except:
            return False
    
    def _lagrange_interpolation_general(self, points: List[Tuple[int, int]], x: int) -> int:
        """General Lagrange interpolation for any x value."""
        result = 0
        
        for i, (xi, yi) in enumerate(points):
            # Calculate Lagrange basis polynomial at x
            numerator = 1
            denominator = 1
            
            for j, (xj, _) in enumerate(points):
                if i != j:
                    numerator = (numerator * (x - xj)) % self.prime
                    denominator = (denominator * (xi - xj)) % self.prime
            
            # Calculate modular inverse of denominator
            if denominator == 0:
                continue
                
            denominator_inv = self._mod_inverse(denominator, self.prime)
            lagrange_coeff = (numerator * denominator_inv) % self.prime
            contribution = (yi * lagrange_coeff) % self.prime
            result = (result + contribution) % self.prime
        
        return result
    
    def threshold_demo(self):
        """Demonstrate threshold property with different numbers of shares."""
        print("\n" + "="*60)
        print("THRESHOLD PROPERTY DEMONSTRATION")
        print("="*60)
        
        print(f"\n🎯 Demonstrating threshold property:")
        print(f"   k = {self.k} shares: CAN reconstruct")
        print(f"   k-1 = {self.k-1} shares: CANNOT reconstruct")
        
        for num_shares in range(1, min(self.n + 2, 8)):  # Test up to n+1 or 7 shares
            print(f"\n" + "-"*30)
            print(f"Testing with {num_shares} shares:")
            
            if num_shares > self.n:
                print(f"   ⚠️  Only have {self.n} shares available")
                continue
            
            # Select shares
            test_shares = self.shares[:num_shares]
            print(f"   Using shares: {test_shares}")
            
            if num_shares < self.k:
                print(f"   ❌ Insufficient shares ({num_shares} < {self.k})")
                print(f"   🔐 Secret remains protected!")
                
                # Show that multiple secrets are possible
                possible_secrets = []
                for test_val in range(1, min(20, self.prime)):
                    if self._check_consistency(test_val, test_shares):
                        possible_secrets.append(test_val)
                        if len(possible_secrets) >= 5:  # Limit output
                            break
                
                if len(possible_secrets) > 1:
                    print(f"   📊 Multiple possible secrets: {possible_secrets[:5]}...")
                
            elif num_shares >= self.k:
                try:
                    reconstructed = self._lagrange_interpolation(test_shares)
                    print(f"   ✅ Sufficient shares! Reconstructed: {reconstructed}")
                    
                    if reconstructed == self.secret:
                        print(f"   🎉 Correct secret recovered!")
                    else:
                        print(f"   ❌ Wrong secret (implementation error)")
                        
                except Exception as e:
                    print(f"   ❌ Reconstruction failed: {e}")
            
            time.sleep(0.5)
        
        input(f"\n   Press Enter to continue...")

def main_demo():
    """Main demonstration function with menu system."""
    print("\n" + "🔐"*30)
    print("SHAMIR'S SECRET SHARING")
    print("Interactive Terminal Demonstration")
    print("🔐"*30)
    
    # Initialize the scheme with user input
    sss = ShamirSecretSharing()
    
    while True:
        print(f"\n" + "="*60)
        print("DEMO MENU")
        print("="*60)
        print(f"1. 🔄 Secret Reconstruction Demo")
        print(f"2. 🛡️ Security Properties Demo")
        print(f"3. 📊 Threshold Property Demo") 
        print(f"4. 📋 Show Current Parameters & Shares")
        print(f"5. 🔧 Create New Secret Sharing Scheme")
        print(f"6. ❓ Show Scheme Explanation")
        print(f"7. 🚪 Exit")
        
        while True:
            try:
                choice = int(input(f"\nChoose an option (1-7): "))
                if 1 <= choice <= 7:
                    break
                else:
                    print("❌ Please enter a number between 1 and 7.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        if choice == 1:
            sss.reconstruction_demo()
        elif choice == 2:
            sss.security_demo()
        elif choice == 3:
            sss.threshold_demo()
        elif choice == 4:
            show_parameters(sss)
        elif choice == 5:
            sss = ShamirSecretSharing()
        elif choice == 6:
            show_explanation()
        elif choice == 7:
            print(f"\n👋 Thank you for exploring secret sharing!")
            print(f"🔐 Remember: Shared secrets are more secure than stored secrets!")
            break

def show_parameters(sss):
    """Display current scheme parameters and shares."""
    print(f"\n" + "="*60)
    print("CURRENT SCHEME PARAMETERS")
    print("="*60)
    print(f"🔐 Secret: {sss.secret}")
    print(f"🎯 Threshold (k): {sss.k}")
    print(f"📊 Total shares (n): {sss.n}")
    print(f"🔢 Prime modulus: {sss.prime}")
    print(f"📈 Polynomial degree: {sss.k - 1}")
    
    print(f"\n🔢 Polynomial coefficients:")
    poly_str = f"f(x) = {sss.polynomial_coeffs[0]}"
    for i in range(1, len(sss.polynomial_coeffs)):
        poly_str += f" + {sss.polynomial_coeffs[i]}x"
        if i > 1:
            poly_str += f"^{i}"
    poly_str += f" mod {sss.prime}"
    print(f"   {poly_str}")
    
    print(f"\n📋 Generated shares:")
    for i, (x, y) in enumerate(sss.shares, 1):
        print(f"   Share {i}: ({x}, {y})")
    
    input(f"\nPress Enter to return to menu...")

def show_explanation():
    """Show detailed explanation of Shamir's Secret Sharing."""
    print(f"\n" + "="*60)
    print("SHAMIR'S SECRET SHARING EXPLANATION")
    print("="*60)
    
    explanations = [
        ("🎯 What is Secret Sharing?", 
         "A way to split a secret into multiple pieces (shares) such that:\n"
         "✅ k shares can reconstruct the original secret\n"
         "❌ k-1 shares reveal absolutely nothing about the secret\n"
         "Perfect for backup keys, distributed systems, and secure storage!"),
        
        ("🔧 The Mathematical Foundation",
         "Based on polynomial interpolation:\n"
         "• Any k points uniquely determine a polynomial of degree k-1\n"
         "• Secret is hidden as f(0) where f(x) is a random polynomial\n"
         "• Shares are points (x, f(x)) on this polynomial\n"
         "• Lagrange interpolation reconstructs f(0) from k points"),
        
        ("🏗️ Setup Process",
         "1. Choose secret S and parameters (k, n, prime p)\n"
         "2. Create polynomial: f(x) = S + a₁x + a₂x² + ... + aₖ₋₁x^(k-1)\n"
         "3. Generate n shares: (1, f(1)), (2, f(2)), ..., (n, f(n))\n"
         "4. Distribute shares to participants"),
        
        ("🔄 Reconstruction Process",
         "1. Collect k shares from participants\n"
         "2. Use Lagrange interpolation to find f(0)\n"
         "3. Reconstructed value is the original secret S\n"
         "4. Works with ANY k shares - order doesn't matter!"),
        
        ("🛡️ Security Properties",
         "• Information-theoretic security (mathematically proven)\n"
         "• k-1 shares give ZERO information about the secret\n"
         "• Even with unlimited computing power, attackers learn nothing\n"
         "• Perfect secrecy - as secure as one-time pad encryption"),
        
        ("📊 Real-World Applications",
         "• Cryptocurrency wallet backup (split private keys)\n"
         "• Corporate secrets (board decisions, trade secrets)\n"
         "• Military communications and nuclear launch codes\n"
         "• Distributed password management systems\n"
         "• Blockchain governance and multisig alternatives"),
        
        ("⚡ Advantages & Limitations",
         "Advantages:\n"
         "✅ Perfect security guarantee\n"
         "✅ Flexible threshold (any k out of n)\n"
         "✅ No single point of failure\n"
         "✅ Shares can be stored separately\n\n"
         "Limitations:\n"
         "❌ All k shares needed simultaneously\n"
         "❌ Vulnerable to share corruption/loss\n"
         "❌ Requires secure channels for distribution"),
        
        ("🔍 Mathematical Deep Dive",
         "Lagrange Interpolation Formula:\n"
         "f(x) = Σᵢ yᵢ × ∏ⱼ≠ᵢ (x-xⱼ)/(xᵢ-xⱼ)\n\n"
         "For secret reconstruction at x=0:\n"
         "S = f(0) = Σᵢ yᵢ × ∏ⱼ≠ᵢ (-xⱼ)/(xᵢ-xⱼ)\n\n"
         "All arithmetic performed modulo prime p\n"
         "Division replaced by modular inverse multiplication")
    ]
    
    for i, (title, content) in enumerate(explanations, 1):
        print(f"\n{title}")
        print("-" * len(title))
        print(content)
        
        if i < len(explanations):
            input(f"\nPress Enter for next section...")
    
    print(f"\n" + "="*60)
    print("QUICK REFERENCE - KEY FORMULAS")
    print("="*60)
    print("Polynomial: f(x) = a₀ + a₁x + a₂x² + ... + aₖ₋₁x^(k-1) mod p")
    print("Secret: S = a₀ = f(0)")
    print("Shares: (i, f(i)) for i = 1, 2, ..., n")
    print("Reconstruction: S = Σᵢ yᵢ × ∏ⱼ≠ᵢ (-xⱼ)/(xᵢ-xⱼ) mod p")
    print("Security: Any k-1 shares reveal zero information")
    
    print(f"\n💡 Pro Tips:")
    print("• Choose prime p > max(secret, n) for security")
    print("• Use cryptographically secure random coefficients")
    print("• Store shares in different locations/systems")
    print("• Consider error-correcting codes for share integrity")
    print("• Test reconstruction before deploying in production")
    
    input(f"\nPress Enter to return to main menu...")

def advanced_demo():
    """Advanced demonstration with edge cases and attack scenarios."""
    print(f"\n" + "="*60)
    print("ADVANCED SECURITY DEMONSTRATIONS")
    print("="*60)
    
    print("🎓 This section demonstrates advanced concepts:")
    print("• Attack resistance analysis")
    print("• Edge case handling")
    print("• Performance considerations")
    print("• Error detection and recovery")
    
    # Demo with small parameters to show vulnerabilities
    print(f"\n🔬 Creating scheme with small parameters for analysis...")
    
    # Fixed small example for predictable analysis
    sss_small = ShamirSecretSharing(secret=7, k=3, n=5, prime=11)
    
    print(f"\n📊 Small scheme parameters:")
    print(f"   Secret: {sss_small.secret}")
    print(f"   Threshold: {sss_small.k}")
    print(f"   Shares: {sss_small.n}")
    print(f"   Prime: {sss_small.prime}")
    
    # Brute force attack simulation
    print(f"\n🔓 BRUTE FORCE ATTACK SIMULATION")
    print(f"   Attacker has {sss_small.k-1} shares: {sss_small.shares[:sss_small.k-1]}")
    print(f"   Trying all possible secrets from 1 to {sss_small.prime-1}...")
    
    valid_secrets = []
    for candidate in range(1, sss_small.prime):
        if sss_small._check_consistency(candidate, sss_small.shares[:sss_small.k-1]):
            valid_secrets.append(candidate)
    
    print(f"   Valid secrets found: {valid_secrets}")
    print(f"   Real secret: {sss_small.secret}")
    print(f"   🎉 Attacker cannot determine which is real!")
    
    input(f"\n   Press Enter to continue...")

# Test and validation functions
def run_tests():
    """Run comprehensive tests of the implementation."""
    print(f"\n" + "="*60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    tests_passed = 0
    total_tests = 0
    
    def test_case(name, condition, details=""):
        nonlocal tests_passed, total_tests
        total_tests += 1
        if condition:
            print(f"✅ {name}")
            tests_passed += 1
        else:
            print(f"❌ {name}")
            if details:
                print(f"   {details}")
    
    # Test 1: Basic reconstruction
    print(f"\n🧪 Test Suite 1: Basic Functionality")
    try:
        sss = ShamirSecretSharing(secret=42, k=3, n=5, prime=101)
        reconstructed = sss._lagrange_interpolation(sss.shares[:3])
        test_case("Basic reconstruction", reconstructed == 42)
    except Exception as e:
        test_case("Basic reconstruction", False, str(e))
    
    # Test 2: Different share combinations
    try:
        combinations = [
            sss.shares[:3],
            sss.shares[1:4],
            sss.shares[2:5],
            [sss.shares[0], sss.shares[2], sss.shares[4]]
        ]
        all_correct = True
        for combo in combinations:
            if sss._lagrange_interpolation(combo) != 42:
                all_correct = False
                break
        test_case("Multiple share combinations", all_correct)
    except Exception as e:
        test_case("Multiple share combinations", False, str(e))
    
    # Test 3: Edge cases
    print(f"\n🧪 Test Suite 2: Edge Cases")
    try:
        # Minimum threshold (k=2)
        sss_min = ShamirSecretSharing(secret=15, k=2, n=3, prime=17)
        reconstructed = sss_min._lagrange_interpolation(sss_min.shares[:2])
        test_case("Minimum threshold k=2", reconstructed == 15)
    except Exception as e:
        test_case("Minimum threshold k=2", False, str(e))
    
    # Test 4: Large numbers
    try:
        sss_large = ShamirSecretSharing(secret=12345, k=4, n=7, prime=15485867)
        reconstructed = sss_large._lagrange_interpolation(sss_large.shares[:4])
        test_case("Large number handling", reconstructed == 12345)
    except Exception as e:
        test_case("Large number handling", False, str(e))
    
    # Test 5: Prime validation
    print(f"\n🧪 Test Suite 3: Parameter Validation")
    try:
        # This should fail - composite number
        try:
            ShamirSecretSharing(secret=10, k=2, n=3, prime=15)
            test_case("Composite prime rejection", False, "Should reject composite numbers")
        except ValueError:
            test_case("Composite prime rejection", True)
    except Exception as e:
        test_case("Composite prime rejection", False, str(e))
    
    # Test 6: Insufficient shares
    try:
        try:
            sss._lagrange_interpolation(sss.shares[:2])  # Need 3, giving 2
            test_case("Insufficient shares detection", False, "Should reject insufficient shares")
        except ValueError:
            test_case("Insufficient shares detection", True)
    except Exception as e:
        test_case("Insufficient shares detection", False, str(e))
    
    # Summary
    print(f"\n" + "="*60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} PASSED")
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Implementation is robust.")
    else:
        print("⚠️  Some tests failed. Review implementation.")
    print("="*60)
    
    input(f"\nPress Enter to return to main menu...")

# Update main demo to include advanced features
def main_demo():
    """Main demonstration function with enhanced menu system."""
    print("\n" + "🔐"*30)
    print("SHAMIR'S SECRET SHARING")
    print("Interactive Terminal Demonstration")
    print("🔐"*30)
    
    # Initialize the scheme with user input
    sss = ShamirSecretSharing()
    
    while True:
        print(f"\n" + "="*60)
        print("DEMO MENU")
        print("="*60)
        print(f"1. 🔄 Secret Reconstruction Demo")
        print(f"2. 🛡️ Security Properties Demo")
        print(f"3. 📊 Threshold Property Demo") 
        print(f"4. 📋 Show Current Parameters & Shares")
        print(f"5. 🔧 Create New Secret Sharing Scheme")
        print(f"6. ❓ Show Scheme Explanation")
        print(f"7. 🎓 Advanced Security Demonstrations")
        print(f"8. 🧪 Run Comprehensive Tests")
        print(f"9. 🚪 Exit")
        
        while True:
            try:
                choice = int(input(f"\nChoose an option (1-9): "))
                if 1 <= choice <= 9:
                    break
                else:
                    print("❌ Please enter a number between 1 and 9.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        if choice == 1:
            sss.reconstruction_demo()
        elif choice == 2:
            sss.security_demo()
        elif choice == 3:
            sss.threshold_demo()
        elif choice == 4:
            show_parameters(sss)
        elif choice == 5:
            sss = ShamirSecretSharing()
        elif choice == 6:
            show_explanation()
        elif choice == 7:
            advanced_demo()
        elif choice == 8:
            run_tests()
        elif choice == 9:
            print(f"\n👋 Thank you for exploring secret sharing!")
            print(f"🔐 Remember: Shared secrets are more secure than stored secrets!")
            print(f"📚 Consider implementing this in your security systems!")
            break

# Entry point
if __name__ == "__main__":
    try:
        main_demo()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Demo interrupted by user.")
        print(f"👋 Thanks for trying Shamir's Secret Sharing!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print(f"🔧 Please check your input and try again.")