# https://github.com/sdsunjay/kasiski/blob/master/asgn2.pdf
# usage: python kasiski.py [ -v ] [ -m length ] [ infile [ outfile ] ]
# python kasiski.py krypton4.in | awk '{print $4}' | tail -n+3 | sort -nu | factor

from sys import argv
import re
import math

is_debug = False
debug = lambda *args, **kwargs: is_debug and print(*args, **kwargs)

def normalize(s):
    s = s.strip().upper()
    s = re.sub(r'[^A-Z]+', '', s)
    return s

def kasiski(s, min_num=3):
    s = normalize(s)
    out = ''

    matches = []
    found = {}
    for k in range(min_num, len(s) // 2 + 1):  # +1 to include half length
        found[k] = {}
        shouldbreak = True
        for i in range(0, len(s) - k + 1):  # +1 to include last possible substring
            v = s[i:i+k]
            if v not in found[k]:
                found[k][v] = 1
            else:
                found[k][v] += 1
                shouldbreak = False

        if shouldbreak:
            break

        for v in found[k]:
            # use >1 instead of >2 to catch repeated substrings appearing at least twice
            if found[k][v] > 1:
                matches.append(v)

    out += "Length  Count  Word        Factor  Location (distance)\n"
    out += "======  =====  ==========  ======  ===================\n"
    for v in matches:
        k = len(v)
        positions = []
        for i in range(len(s) - k + 1):
            if s[i:i+k] == v:
                positions.append(i)

        # Calculate gcd of distances between repeated positions
        factor = 0
        for i in range(1, len(positions)):
            diff = positions[i] - positions[i-1]
            factor = diff if factor == 0 else math.gcd(factor, diff)

        locations = ""
        for i, pos in enumerate(positions):
            locations += f"{pos} "
            if i > 0:
                locations += f"({positions[i] - positions[i-1]}) "

        out += f"{k:6d}  {found[k][v]:5d}  {v:10s}  {factor:6d}  {locations}\n"

    return out

def main():
    global is_debug
    i, k = 1, 0
    min_num = 3
    infile, outfile = None, None
    while i < len(argv):
        if argv[i] == '-v':
            is_debug = True
            debug("Debug enabled")
        elif argv[i] == '-m':
            i += 1
            if i >= len(argv):
                print("Error: -m requires a length argument")
                return
            min_num = int(argv[i])
            debug(f"min_num: {min_num}")
        elif argv[i][0] != '-':
            if k == 0:
                infile = argv[i]
                debug(f"infile: {infile}")
            elif k == 1:
                outfile = argv[i]
                debug(f"outfile: {outfile}")
            k += 1
        else:
            print(f"Unknown option: {argv[i]}")
            return
        i += 1

    if infile is None:
        s = input("Enter the ciphertext: ")
    else:
        with open(infile, 'r') as f:
            s = f.read()

    out = kasiski(s, min_num)

    if outfile is None:
        print(out)
    else:
        with open(outfile, 'w') as f:
            f.write(out)

if __name__ == "__main__":
    main()
