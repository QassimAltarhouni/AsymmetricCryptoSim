import random
from math import gcd

# Miller-Rabin primality test for probabilistic prime checking
# This allows generating primes with configurable bit lengths

def _is_probable_prime(n: int, k: int = 40) -> bool:
    """Return True if n is probably prime using Miller-Rabin."""
    if n < 2:
        return False
    # handle small primes
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % p == 0:
            return n == p
    # find r and s such that n-1 = 2^r * s with s odd
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _generate_prime_candidate(bits: int) -> int:
    candidate = random.getrandbits(bits)
    candidate |= 1 << (bits - 1)  # ensure high bit is set
    candidate |= 1  # ensure odd
    return candidate


def generate_large_prime(bits: int) -> int:
    """Generate a prime number of the given bit length."""
    while True:
        candidate = _generate_prime_candidate(bits)
        if _is_probable_prime(candidate):
            return candidate


class RSA:
    """Basic RSA implementation with configurable key length."""

    def __init__(self, key_length: int = 512):
        half = key_length // 2
        self.p = generate_large_prime(half)
        self.q = generate_large_prime(half)
        while self.q == self.p:
            self.q = generate_large_prime(half)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self._find_e()
        self.d = self._modinv(self.e, self.phi)

    def _find_e(self) -> int:
        # common choice for e is 65537
        e = 65537
        if gcd(e, self.phi) == 1:
            return e
        e = 3
        while gcd(e, self.phi) != 1:
            e += 2
        return e

    @staticmethod
    def _egcd(a: int, b: int):
        if a == 0:
            return b, 0, 1
        g, y, x = RSA._egcd(b % a, a)
        return g, x - (b // a) * y, y

    def _modinv(self, a: int, m: int) -> int:
        g, x, _ = self._egcd(a, m)
        if g != 1:
            raise ValueError("Inverse doesn't exist")
        return x % m

    def encrypt(self, plaintext: str) -> list[int]:
        return [pow(ord(ch), self.e, self.n) for ch in plaintext]
    def decrypt(self, ciphertext: list[int]) -> str:
        return "".join(chr(pow(c, self.d, self.n)) for c in ciphertext)