from math import gcd
import time

def factorize(n, limit=100000):
    start = time.time()
    for i in range(2, limit):
        if n % i == 0:
            end = time.time()
            return i, n // i, end - start
    return None, None, -1

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def eve_attack(e, n, ciphertext):
    p, q, time_taken = factorize(n)
    if not p:
        print("[Eve] Failed to factor n.")
        return None

    print(f"[Eve] Factored n in {time_taken:.4f} seconds: p={p}, q={q}")
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    print(f"[Eve] Calculated private key: d={d}")
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])
