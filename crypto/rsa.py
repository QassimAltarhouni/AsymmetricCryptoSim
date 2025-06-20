import random
from math import gcd

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def generate_large_prime(start=100, end=300):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

class RSA:
    def __init__(self):
        self.p = generate_large_prime()
        self.q = generate_large_prime()
        while self.q == self.p:
            self.q = generate_large_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.find_e()
        self.d = self.modinv(self.e, self.phi)

    def find_e(self):
        e = 3
        while gcd(e, self.phi) != 1:
            e += 2
        return e

    def modinv(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            a, m = m, a % m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encrypt(self, plaintext):
        return [pow(ord(char), self.e, self.n) for char in plaintext]

    def decrypt(self, ciphertext):
        return ''.join([chr(pow(char, self.d, self.n)) for char in ciphertext])
