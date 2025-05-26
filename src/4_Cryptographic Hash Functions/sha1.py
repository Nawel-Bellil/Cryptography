#!/usr/bin/env python
from __future__ import print_function
import struct
import io
import sys
import os
import argparse
import unittest
import random
import hashlib

### --- SHA-1 ALGORITHM IMPLEMENTATION --- ###

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def _process_chunk(chunk, h0, h1, h2, h3, h4):
    assert len(chunk) == 64
    w = [0] * 80
    for i in range(16):
        w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]
    for i in range(16, 80):
        w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
    a, b, c, d, e = h0, h1, h2, h3, h4
    for i in range(80):
        if 0 <= i <= 19:
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                         a, _left_rotate(b, 30), c, d)
    return [(h + v) & 0xffffffff for h, v in zip((h0, h1, h2, h3, h4), (a, b, c, d, e))]

class Sha1Hash:
    digest_size = 20
    block_size = 64

    def __init__(self):
        self._h = [0x67452301, 0xEFCDAB89, 0x98BADCFE,
                   0x10325476, 0xC3D2E1F0]
        self._unprocessed = b''
        self._message_byte_length = 0

    def update(self, arg):
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)
        chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))
        while len(chunk) == 64:
            self._h = _process_chunk(chunk, *self._h)
            self._message_byte_length += 64
            chunk = arg.read(64)
        self._unprocessed = chunk
        return self

    def digest(self):
        return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

    def hexdigest(self):
        return ''.join('%08x' % h for h in self._produce_digest())

    def _produce_digest(self):
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)
        message += b'\x80'
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)
        h = _process_chunk(message[:64], *self._h)
        if len(message) == 64:
            return h
        return _process_chunk(message[64:], *h)

def sha1(data):
    return Sha1Hash().update(data).hexdigest()

### --- UNIT TESTS --- ###

def get_random_bytes():
    size = random.randrange(1, 1000)
    for _ in range(size):
        yield random.getrandbits(8)

class TestSha1(unittest.TestCase):
    def test_similar(self):
        msg = bytearray(get_random_bytes())
        modified_msg = bytearray(msg)
        index = random.randrange(len(msg))
        modified_msg[index] ^= 0x01  # Flip 1 bit
        self.assertNotEqual(sha1(msg), sha1(modified_msg))

    def test_repeatable(self):
        msg = bytearray(get_random_bytes())
        self.assertEqual(sha1(msg), sha1(msg))

    def test_comparison(self):
        msg = bytearray(get_random_bytes())
        self.assertEqual(sha1(msg), hashlib.sha1(msg).hexdigest())

    def test_associativity(self):
        msg1 = bytearray(get_random_bytes())
        msg2 = bytearray(get_random_bytes())
        digest1 = sha1(msg1 + msg2)
        sha = Sha1Hash()
        sha.update(msg1)
        sha.update(msg2)
        digest2 = sha.hexdigest()
        self.assertEqual(digest1, digest2)

### --- CLI ENTRYPOINT --- ###
    def test_known_value(self):
        """Test SHA-1 against a known test vector"""
        print('\n>>> running: test_known_value')
        msg = b"The quick brown fox jumps over the lazy dog"
        expected_digest = "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12"

        result_digest = sha1(msg)

        print(f"... input: {msg}")
        print(f"... expected: {expected_digest}")
        print(f"... got:      {result_digest}")

        self.assertEqual(result_digest, expected_digest)
        print('... test_known_value: success')

    def test_gradual(self):
        """Ensure gradual hashing gives same result as single pass"""
        print('\n>>> running: test_gradual')
        data = bytearray(get_random_bytes())

        # Hash all at once
        full_digest = sha1(data)

        # Hash gradually
        hasher = Sha1Hash()
        for i in range(0, len(data), 17):  # chunk size = 17 (arbitrary)
            hasher.update(data[i:i+17])
        gradual_digest = hasher.hexdigest()

        print(f"... full_digest:     {full_digest}")
        print(f"... gradual_digest:  {gradual_digest}")

        self.assertEqual(full_digest, gradual_digest)
        print("... test_gradual: success")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="*", help="File(s) to hash or use stdin")
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    args = parser.parse_args()

    if args.test:
        print("Running SHA-1 unit tests...\n")
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSha1)
        unittest.TextTestRunner(verbosity=2).run(suite)
        return

    if not args.input:
        try:
            print(" Enter data to hash :")
            data = sys.stdin.readline().strip().encode()
            print("sha1-digest:", sha1(data))
        except KeyboardInterrupt:
            print("Input interrupted.")
    else:
        for arg in args.input:
            if os.path.isfile(arg):
                with open(arg, 'rb') as f:
                    print(f"{arg}: sha1-digest: {sha1(f)}")
            else:
                print(f"Error: could not find {arg}")
 


    

if __name__ == "__main__":
    main()
