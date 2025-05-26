import random
import hashlib
import time
from typing import List, Tuple
from math import gcd

class FeigeFiatShamir:
    """
    Implementation of the Feige-Fiat-Shamir zero-knowledge identification protocol.
    
    This protocol allows a prover to demonstrate knowledge of square roots modulo n
    without revealing the actual square roots.
    """
    
    def __init__(self, p: int = None, q: int = None, k: int = None):
        """
        Initialize the FFS protocol.
        
        Args:
            p, q: Two large prime numbers (will ask for input if None)
            k: Security parameter (number of secrets) (will ask for input if None)
        """
        self.p = p
        self.q = q
        self.k = k
        self.n = None
        self.secrets = []
        self.public_values = []
        
        if p is None or q is None or k is None:
            self._get_user_parameters()
        
        self.n = self.p * self.q
        self._generate_keys()
    
    def _get_user_parameters(self):
        """Get protocol parameters from user input."""
        print("\n" + "="*60)
        print("FEIGE-FIAT-SHAMIR PROTOCOL SETUP")
        print("="*60)
        
        print("\nWelcome to the Feige-Fiat-Shamir Zero-Knowledge Proof Demo!")
        print("This protocol allows proving knowledge of secrets without revealing them.")
        
        if self.p is None:
            print("\n📝 Step 1: Choose the first prime number (p)")
            print("   For demo purposes, use a small prime like 17, 19, 23, etc.")
            while True:
                try:
                    self.p = int(input("   Enter prime p: "))
                    if self._is_prime(self.p):
                        break
                    else:
                        print("   ❌ That's not a prime number. Try again.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        if self.q is None:
            print(f"\n📝 Step 2: Choose the second prime number (q)")
            print(f"   Choose a different prime from p={self.p}")
            while True:
                try:
                    self.q = int(input("   Enter prime q: "))
                    if self._is_prime(self.q) and self.q != self.p:
                        break
                    elif self.q == self.p:
                        print("   ❌ q must be different from p. Try again.")
                    else:
                        print("   ❌ That's not a prime number. Try again.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        if self.k is None:
            print(f"\n📝 Step 3: Choose security parameter (k)")
            print(f"   This is the number of secret values (typically 2-5 for demo)")
            while True:
                try:
                    self.k = int(input("   Enter k: "))
                    if 1 <= self.k <= 10:
                        break
                    else:
                        print("   ❌ Please choose k between 1 and 10.")
                except ValueError:
                    print("   ❌ Please enter a valid integer.")
        
        print(f"\n✅ Protocol parameters set:")
        print(f"   p = {self.p}")
        print(f"   q = {self.q}")
        print(f"   n = p × q = {self.p * self.q}")
        print(f"   k = {self.k}")
        
        input("\n   Press Enter to continue...")
    
    def _is_prime(self, n: int) -> bool:
        """Simple primality test for small numbers."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def _generate_keys(self):
        """Generate the secret and public key pairs with user interaction."""
        print("\n" + "="*60)
        print("KEY GENERATION PHASE")
        print("="*60)
        
        print(f"\n🔐 Generating {self.k} secret-public key pairs...")
        print(f"   Each secret sᵢ will have a corresponding public value vᵢ = sᵢ² mod {self.n}")
        
        for i in range(self.k):
            print(f"\n   Generating key pair {i+1}/{self.k}:")
            
            # Generate a random secret s_i
            while True:
                s = random.randint(2, self.n - 1)
                if gcd(s, self.n) == 1:
                    break
            
            # Compute public value v_i = s_i^2 mod n
            v = pow(s, 2, self.n)
            
            self.secrets.append(s)
            self.public_values.append(v)
            
            print(f"   🔑 Secret s�{i+1} = {s}")
            print(f"   🌐 Public v₁ = s₁² mod {self.n} = {v}")
            
            time.sleep(0.5)  # Brief pause for readability
        
        print(f"\n✅ Key generation complete!")
        print(f"   Secrets (kept private): {self.secrets}")
        print(f"   Public values (shared): {self.public_values}")
        
        input("\n   Press Enter to continue to the proof phase...")
    
    def _wait_for_user(self, prompt: str = "Press Enter to continue..."):
        """Wait for user input with a custom prompt."""
        input(f"\n   {prompt}")
    
    def interactive_proof_demo(self):
        """Run an interactive proof demo with step-by-step explanation."""
        print("\n" + "="*60)
        print("INTERACTIVE ZERO-KNOWLEDGE PROOF")
        print("="*60)
        
        print("\n🎯 Goal: Prove knowledge of secrets without revealing them")
        print("📋 Protocol: 3-move interactive proof")
        print("   1. Commitment (Prover → Verifier)")
        print("   2. Challenge (Verifier → Prover)")
        print("   3. Response (Prover → Verifier)")
        
        # Ask for number of rounds
        print(f"\n🔄 How many rounds would you like to run?")
        print(f"   (Each round reduces the chance of cheating by 50%)")
        while True:
            try:
                rounds = int(input("   Enter number of rounds (1-10): "))
                if 1 <= rounds <= 10:
                    break
                else:
                    print("   ❌ Please choose between 1 and 10 rounds.")
            except ValueError:
                print("   ❌ Please enter a valid integer.")
        
        print(f"\n🚀 Starting {rounds} rounds of zero-knowledge proof...")
        self._wait_for_user()
        
        all_passed = True
        
        for round_num in range(rounds):
            print(f"\n" + "-"*40)
            print(f"ROUND {round_num + 1} of {rounds}")
            print("-"*40)
            
            # Phase 1: Commitment
            print(f"\n📤 PHASE 1: COMMITMENT")
            print(f"   Prover generates random r and computes x = r² mod {self.n}")
            
            r, x = self.prover_commitment()
            print(f"   🎲 Random r = {r}")
            print(f"   📨 Commitment x = {x}")
            print(f"   (Prover keeps r secret, sends x to Verifier)")
            
            self._wait_for_user("Press Enter for Challenge phase...")
            
            # Phase 2: Challenge
            print(f"\n❓ PHASE 2: CHALLENGE")
            print(f"   Verifier generates random binary challenge vector of length {self.k}")
            
            # Ask user if they want to choose challenge or use random
            print(f"   Would you like to:")
            print(f"   1. Let the system generate a random challenge")
            print(f"   2. Choose your own challenge manually")
            
            while True:
                try:
                    choice = int(input("   Enter choice (1 or 2): "))
                    if choice in [1, 2]:
                        break
                    else:
                        print("   ❌ Please enter 1 or 2.")
                except ValueError:
                    print("   ❌ Please enter a valid number.")
            
            if choice == 1:
                challenge = self.verifier_challenge()
                print(f"   🎲 Random challenge: {challenge}")
            else:
                challenge = []
                print(f"   Enter {self.k} binary values (0 or 1):")
                for i in range(self.k):
                    while True:
                        try:
                            bit = int(input(f"   Challenge bit {i+1}: "))
                            if bit in [0, 1]:
                                challenge.append(bit)
                                break
                            else:
                                print("   ❌ Please enter 0 or 1.")
                        except ValueError:
                            print("   ❌ Please enter 0 or 1.")
                print(f"   📝 Your challenge: {challenge}")
            
            self._wait_for_user("Press Enter for Response phase...")
            
            # Phase 3: Response
            print(f"\n💬 PHASE 3: RESPONSE")
            print(f"   Prover computes y = r × ∏(sᵢᵉⁱ) mod {self.n}")
            print(f"   Where eᵢ are the challenge bits")
            
            y = self.prover_response(r, challenge)
            
            # Show the computation step by step
            print(f"   📊 Computation breakdown:")
            print(f"      Starting with r = {r}")
            for i, e in enumerate(challenge):
                if e == 1:
                    print(f"      Multiply by s₁ = {self.secrets[i]} (since e₁ = 1)")
                else:
                    print(f"      Skip s₁ = {self.secrets[i]} (since e₁ = 0)")
            print(f"   📤 Response y = {y}")
            
            self._wait_for_user("Press Enter for Verification...")
            
            # Phase 4: Verification
            print(f"\n✅ VERIFICATION")
            print(f"   Verifier checks: y² ≟ x × ∏(vᵢᵉⁱ) mod {self.n}")
            
            is_valid = self.verifier_check(x, challenge, y)
            
            # Show verification computation
            left = pow(y, 2, self.n)
            right = x
            print(f"   📊 Left side: y² mod {self.n} = {y}² mod {self.n} = {left}")
            
            print(f"   📊 Right side computation:")
            print(f"      Starting with x = {x}")
            for i, e in enumerate(challenge):
                if e == 1:
                    print(f"      Multiply by v₁ = {self.public_values[i]} (since e₁ = 1)")
                    right = (right * self.public_values[i]) % self.n
                else:
                    print(f"      Skip v₁ = {self.public_values[i]} (since e₁ = 0)")
            print(f"      Final right side = {right}")
            
            print(f"\n   🔍 Verification: {left} ≟ {right}")
            
            if is_valid:
                print(f"   ✅ ROUND {round_num + 1}: PASS")
            else:
                print(f"   ❌ ROUND {round_num + 1}: FAIL")
                all_passed = False
            
            if round_num < rounds - 1:
                self._wait_for_user("Press Enter for next round...")
        
        print(f"\n" + "="*60)
        print("PROOF SUMMARY")
        print("="*60)
        
        if all_passed:
            print(f"🎉 SUCCESS! All {rounds} rounds passed!")
            print(f"📊 Soundness: Probability of cheating ≤ (1/2)^{rounds} = {1/(2**rounds):.6f}")
            print(f"🔐 The prover has demonstrated knowledge of the secrets")
            print(f"🤐 without revealing any information about them!")
        else:
            print(f"❌ FAILURE! At least one round failed.")
            print(f"🚫 The proof is invalid.")
        
        return all_passed
    
    def non_interactive_demo(self):
        """Demonstrate non-interactive proof using Fiat-Shamir heuristic."""
        print(f"\n" + "="*60)
        print("NON-INTERACTIVE PROOF (FIAT-SHAMIR HEURISTIC)")
        print("="*60)
        
        print(f"\n🎯 Goal: Create a proof that doesn't require interaction")
        print(f"💡 Method: Use hash function to generate 'random' challenges")
        print(f"📝 Useful for: Digital signatures, blockchain applications")
        
        # Get message from user
        print(f"\n📄 Enter a message to sign/prove:")
        message = input("   Message: ")
        
        self._wait_for_user("Press Enter to generate non-interactive proof...")
        
        print(f"\n🔄 Generating non-interactive proof...")
        
        commitments, challenges, responses = self.non_interactive_proof(message)
        
        print(f"\n📊 Proof components generated:")
        print(f"   📤 Commitments: {commitments}")
        print(f"   🎲 Challenges (from hash): {challenges}")
        print(f"   💬 Responses: {responses}")
        
        # Show how challenge was generated
        hash_input = message + "".join(map(str, commitments + self.public_values))
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()
        print(f"\n🔍 Challenge generation:")
        print(f"   Hash input: message + commitments + public_values")
        print(f"   SHA256 hash: {hash_digest[:32]}...")
        print(f"   Extracted challenge bits: {challenges}")
        
        self._wait_for_user("Press Enter to verify the proof...")
        
        # Verify the proof
        print(f"\n✅ Verifying non-interactive proof...")
        is_valid = self.verify_non_interactive_proof(commitments, challenges, responses, message)
        
        if is_valid:
            print(f"   ✅ NON-INTERACTIVE PROOF: VALID")
            print(f"   🎉 Message authenticity confirmed!")
        else:
            print(f"   ❌ NON-INTERACTIVE PROOF: INVALID")
        
        # Test with wrong message
        print(f"\n🧪 Testing with tampered message...")
        wrong_message = message + "TAMPERED"
        is_valid_tampered = self.verify_non_interactive_proof(commitments, challenges, responses, wrong_message)
        
        print(f"   Original message: '{message}'")
        print(f"   Tampered message: '{wrong_message}'")
        print(f"   Verification result: {'VALID' if is_valid_tampered else 'INVALID'}")
        
        if not is_valid_tampered:
            print(f"   ✅ Good! Tampering was detected.")
        else:
            print(f"   ❌ Warning! Tampering was not detected.")
        
        return is_valid
    
    def prover_commitment(self) -> Tuple[int, int]:
        """Prover generates a random commitment."""
        while True:
            r = random.randint(2, self.n - 1)
            if gcd(r, self.n) == 1:
                break
        x = pow(r, 2, self.n)
        return r, x
    
    def verifier_challenge(self) -> List[int]:
        """Verifier generates a random challenge."""
        return [random.randint(0, 1) for _ in range(self.k)]
    
    def prover_response(self, r: int, challenge: List[int]) -> int:
        """Prover computes response to the challenge."""
        y = r
        for i, e in enumerate(challenge):
            if e == 1:
                y = (y * self.secrets[i]) % self.n
        return y
    
    def verifier_check(self, x: int, challenge: List[int], y: int) -> bool:
        """Verifier checks if the proof is valid."""
        left = pow(y, 2, self.n)
        right = x
        for i, e in enumerate(challenge):
            if e == 1:
                right = (right * self.public_values[i]) % self.n
        return left == right
    
    def non_interactive_proof(self, message: str = "") -> Tuple[List[int], List[int], List[int]]:
        """Generate a non-interactive proof using the Fiat-Shamir heuristic."""
        commitments = []
        challenges = []
        responses = []
        random_values = []
        
        for _ in range(self.k):
            r, x = self.prover_commitment()
            commitments.append(x)
            random_values.append(r)
        
        hash_input = message + "".join(map(str, commitments + self.public_values))
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()
        
        for i in range(self.k):
            bit_index = i % len(hash_digest)
            challenges.append(int(hash_digest[bit_index], 16) % 2)
        
        for i in range(self.k):
            y = self.prover_response(random_values[i], [challenges[i]])
            responses.append(y)
        
        return commitments, challenges, responses
    
    def verify_non_interactive_proof(self, commitments: List[int], challenges: List[int], 
                                   responses: List[int], message: str = "") -> bool:
        """Verify a non-interactive proof."""
        hash_input = message + "".join(map(str, commitments + self.public_values))
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()
        
        expected_challenges = []
        for i in range(self.k):
            bit_index = i % len(hash_digest)
            expected_challenges.append(int(hash_digest[bit_index], 16) % 2)
        
        if challenges != expected_challenges:
            return False
        
        for i in range(self.k):
            if not self.verifier_check(commitments[i], [challenges[i]], responses[i]):
                return False
        
        return True


def main_demo():
    """Main demonstration function with menu system."""
    print("\n" + "🔐"*30)
    print("FEIGE-FIAT-SHAMIR ZERO-KNOWLEDGE PROOF")
    print("Interactive Terminal Demonstration")
    print("🔐"*30)
    
    # Initialize the protocol with user input
    ffs = FeigeFiatShamir()
    
    while True:
        print(f"\n" + "="*60)
        print("DEMO MENU")
        print("="*60)
        print(f"1. 🔄 Run Interactive Proof Demo")
        print(f"2. 📝 Run Non-Interactive Proof Demo") 
        print(f"3. 📊 Show Current Parameters")
        print(f"4. 🔧 Reset with New Parameters")
        print(f"5. ❓ Show Protocol Explanation")
        print(f"6. 🚪 Exit")
        
        while True:
            try:
                choice = int(input(f"\nChoose an option (1-6): "))
                if 1 <= choice <= 6:
                    break
                else:
                    print("❌ Please enter a number between 1 and 6.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        if choice == 1:
            ffs.interactive_proof_demo()
        elif choice == 2:
            ffs.non_interactive_demo()
        elif choice == 3:
            show_parameters(ffs)
        elif choice == 4:
            ffs = FeigeFiatShamir()
        elif choice == 5:
            show_explanation()
        elif choice == 6:
            print(f"\n👋 Thank you for exploring zero-knowledge proofs!")
            print(f"🔐 Remember: Knowledge can be proven without being revealed!")
            break

def show_parameters(ffs):
    """Display current protocol parameters."""
    print(f"\n" + "="*60)
    print("CURRENT PROTOCOL PARAMETERS")
    print("="*60)
    print(f"🔢 Prime p: {ffs.p}")
    print(f"🔢 Prime q: {ffs.q}")
    print(f"🔢 Modulus n = p × q: {ffs.n}")
    print(f"🔢 Security parameter k: {ffs.k}")
    print(f"🔐 Secret values: {ffs.secrets}")
    print(f"🌐 Public values: {ffs.public_values}")
    
    input(f"\nPress Enter to return to menu...")

def show_explanation():
    """Show detailed explanation of the protocol."""
    print(f"\n" + "="*60)
    print("FEIGE-FIAT-SHAMIR PROTOCOL EXPLANATION")
    print("="*60)
    
    explanations = [
        ("🎯 What is Zero-Knowledge?", 
         "A way to prove you know something without revealing what you know.\n"
         "Like proving you know a password without saying the password!"),
        
        ("🔧 Setup Phase",
         "1. Choose two large primes p and q\n"
         "2. Compute n = p × q (public)\n" 
         "3. Generate k secret values s₁, s₂, ..., sₖ\n"
         "4. Compute public values vᵢ = sᵢ² mod n"),
        
        ("🔄 Interactive Protocol",
         "1. COMMITMENT: Prover sends x = r² mod n\n"
         "2. CHALLENGE: Verifier sends random bits e₁, e₂, ..., eₖ\n"
         "3. RESPONSE: Prover sends y = r × ∏(sᵢᵉⁱ) mod n\n"
         "4. VERIFY: Check if y² ≡ x × ∏(vᵢᵉⁱ) mod n"),
        
        ("📝 Non-Interactive Version",
         "Uses Fiat-Shamir heuristic:\n"
         "- Challenge = Hash(message + commitments + public_keys)\n"
         "- No interaction needed, perfect for digital signatures!"),
        
        ("🛡️ Security Properties",
         "- COMPLETENESS: Honest prover always convinces verifier\n"
         "- SOUNDNESS: Cheating prover fails (except with tiny probability)\n"
         "- ZERO-KNOWLEDGE: Verifier learns nothing about secrets")
    ]
    
    for title, content in explanations:
        print(f"\n{title}")
        print("-" * len(title))
        print(content)
        input(f"\nPress Enter to continue...")
    
    print(f"\n🎉 That's the Feige-Fiat-Shamir protocol in a nutshell!")
    input(f"Press Enter to return to menu...")


if __name__ == "__main__":
    main_demo()