# Affine Cipher Algorithm Encrypt/Decrypt (Substitution Cipher)
# Leo Martinez III
# Created Sping 2024

#-------------------------------------------------------------------------------
# Encryption
# E(x) = encrypted letter index -> (ax + b) mod 26
# x = plaintext letter index
# a = alpha
# b = beta
# m = alphabet size
# 0 <= a, b <= 25 | 26 letter alphabet for this code

# Create a dictionary (26 letters) to map letters to their corresponding indices
letter_to_index = {chr(i + ord('A')): i for i in range(26)} # A -> 0, B -> 1, ... Z -> 25
index_to_letter = {i: chr(i + ord('A')) for i in range(26)} # 0 -> A, 1 -> B, ... 25 -> Z

# Function to encrypt plaintext using affine cipher
def encryptAffine(plaintext, alpha, beta, m):
    # Filter out spaces from the plaintext (spaces are ignored for encipherment)
    plaintext = "".join(plaintext.split())

    ciphertext = []
    if plaintext.isalpha() and len(plaintext) >= 1: # If plaintext is alphabetic letters and is greater than or equal to 1
      for i in plaintext:
        idx = letter_to_index[i.upper()]  # Convert to uppercase (if not already) for case insensitivity
        x = (alpha * idx + beta) % m # (ax + b) mod m
        ciphertext.append(index_to_letter[x])
      return "".join(ciphertext) # Convert the ciphertext list into a singular string
    else:
        return "An Error has occurred, please double check input used is valid."  # Handle invalid input

#-------------------------------------------------------------------------------
# Decryption
# D(y) = index of decrypted letter -> (y-beta) * (1/alpha)
# y = ciphertext letter index
# a = alpha
# b = beta
# m = alphabet size
# 0 <= a, b <= 25 | 26 letter alphabet for this code

# Function to decrypt ciphertext using affine cipher
def decryptAffine(ciphertext, alpha, beta, m):
    # Filter out spaces from the ciphertext (spaces are ignored for decipherment)
    ciphertext = "".join(ciphertext.split())

    plaintext = []
    if ciphertext.isalpha() and len(ciphertext) >= 1: # If ciphertext is alphabetic letters and is greater than or equal to 1
      # Find the modular multiplicative inverse of alpha
      for a_inv in range(m):
          if (a_inv * alpha) % m == 1:
              break

      for i in ciphertext:
        idx = letter_to_index[i.upper()]  # Convert to uppercase (if not already) for case insensitivity
        x = (a_inv * (idx - beta)) % m # (a_inv * (y - b)) mod m
        plaintext.append(index_to_letter[x])
      return "".join(plaintext) # Convert the plaintext list into a singular string
    else:
        return "An Error has occurred, please double check input used is valid."  # Handle invalid input

#----------------------------------------------------------------------------------------------------------------------------------------------
# Main code (Performs computations and Input/Output operations)
import math # used for GCD in error checking

# User input to perform encryption or decryption
user_input = input("Would you like to perform encryption or decryption?\nPlease Enter 'e' or 'd': ").lower() # In case user uses capital letters
isValid = True
# Check if the user input is 'e' or 'd'
if user_input not in ['e', 'd']:
    print("Invalid input, please enter 'e' for encryption or 'd' for decryption.")
    isValid = False
else:
    # Taking user input for the alpha value
    user_input_alpha = input(f"Enter an alpha value between 1 and {m-1} of type (int): ")
    # Taking user input for the beta value
    user_input_beta = input(f"Enter an beta value between 0 and {m-1} of type (int): ")

    try: # Ensure the user can only use valid whole numbers as the alpha and beta value
        alpha = int(user_input_alpha)
        beta = int(user_input_beta)
        if (alpha < 1) or (alpha > (m-1)) : # Valid range for alpha
            print("Please enter a valid number in proper range for alpha.")
            isValid = False
        elif (beta < 0) or (beta > (m-1)) : # Valid range for beta
            print("Please enter a valid number in proper range for beta.")
            isValid = False
        elif (math.gcd(alpha, m)) != 1:
            print("The GCD of alpha and {m} MUST be equal to 1.")
            isValid = False
    except ValueError:
        print("Invalid numeric input, please enter a valid whole number.")
        isValid = False

# This pair of Ciphertext and Plaintext can be used as input for testing purposes if desired:
# plaintext = "MY FAVORITE CLASS IS COMPUTER SECURITY"
# ciphertext = "GKVCJYZWRMUXCIIWIUYGHARMZIMUAZWRK"
# alpha = 9, beta = 2, m = 26 | Example values, any other valid value can be used
m = 26 # Will be left as 26 (English Alphabet Length) without user input by default


if user_input == 'e' and isValid == True: # If the user chooses to encrypt data and they also have valid input
  user_input_plaintext = input("\nPlease enter the plaintext to encrypt: \n")
  ciphertext = encryptAffine(user_input_plaintext, alpha, beta, m) # Call the encryption method
  print("\nPlaintext (Original): " + user_input_plaintext)
  print("Ciphertext (Generated): " + ciphertext)
  print("Alphabet Size:", m)
  print("Alpha Value Chosen: ", alpha)
  print("Beta Value Chosen: ", beta)

elif user_input == 'd' and isValid == True: # If the user chooses to decrypt data and they also have valid input
  user_input_ciphertext = input("\nPlease enter the ciphertext to decrypt: \n")
  plaintext = decryptAffine(user_input_ciphertext, alpha, beta, m) # Call the decryption method
  print("\nCiphertext (Original): " + user_input_ciphertext)
  print("Plaintext (Generated): " + plaintext)
  print("Alphabet Size: ", m)
  print("Alpha Value Chosen: ", alpha)
  print("Beta Value Chosen: ", beta)

else: # Will only appear if the user has invalid input data somewhere
  print("\nAn error has occured, please try again.")