import random
import math
import time

def _pollards_rho(n: int, max_iterations: int = 10_000) -> int | None:
    if n % 2 == 0:
        return 2

    while True:
        x = random.randrange(2, n - 1)
        y = x
        c = random.randrange(1, n - 1)
        d = 1
        for _ in range(max_iterations):
            x = (pow(x, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            d = math.gcd(abs(x - y), n)
            if d == 1:
                continue
            if d == n:
                break
            return d


def factorize(n: int):
    start = time.time()
    if n % 2 == 0:
        return 2, n // 2, time.time() - start

    factor = _pollards_rho(n)
    if factor and 1 < factor < n:
        return factor, n // factor, time.time() - start
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
