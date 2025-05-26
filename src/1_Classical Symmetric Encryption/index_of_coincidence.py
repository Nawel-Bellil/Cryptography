def calculate_ic(text):
    """
    Calculates the index of coincidence (IC) for a given text.

    Args:
        text: The input text (string).

    Returns:
        The index of coincidence (float).
    """
    text = ''.join(filter(str.isalpha, text)).lower()
    if not text:
        return 0.0
    n = len(text)
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    ic = 0
    for char in freq:
        ic += freq[char] * (freq[char] - 1)
    
    ic /= (n * (n - 1))
    return ic

# Example usage
text = "this is a sample text to calculate the index of coincidence"
ic = calculate_ic(text)
print(f"The index of coincidence is: {ic}")