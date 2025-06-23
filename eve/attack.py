import random
import math
import time
from sympy import factorint

def is_perfect_square(n: int) -> bool:
    root = math.isqrt(n)
    return root * root == n

def fermat_factor(n: int, max_iterations: int = 100000):
    a = math.isqrt(n)
    b2 = a * a - n
    count = 0
    while b2 < 0 or not is_perfect_square(b2):
        a += 1
        b2 = a * a - n
        count += 1
        if count > max_iterations:
            return None, None
    b = math.isqrt(b2)
    return a - b, a + b

def _pollards_rho(n: int, max_iterations: int = 10000, max_attempts: int = 5):
    if n % 2 == 0:
        return 2
    for _ in range(max_attempts):
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
    return None

def factorize_pollard(n: int):
    start = time.time()
    if n % 2 == 0:
        return 2, n // 2, time.time() - start
    factor = _pollards_rho(n)
    if factor and 1 < factor < n:
        return factor, n // factor, time.time() - start
    return None, None, -1

def factorize_fermat(n: int):
    start = time.time()
    p, q = fermat_factor(n)
    duration = time.time() - start
    if p and q:
        return p, q, duration
    return None, None, -1

def factorize_gnfs(n: int):
    start = time.time()
    factors = factorint(n)
    if len(factors) == 2:
        p, q = list(factors)
        return p, q, time.time() - start
    return None, None, -1

def factorize_ecm(n: int):
    start = time.time()
    factors = factorint(n)  # Simulated ECM via sympy
    if len(factors) == 2:
        p, q = list(factors)
        return p, q, time.time() - start
    return None, None, -1

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def eve_attack(e, n, ciphertext, method="rho"):
    if method == "rho":
        p, q, time_taken = factorize_pollard(n)
    elif method == "fermat":
        p, q, time_taken = factorize_fermat(n)
    elif method == "gnfs":
        p, q, time_taken = factorize_gnfs(n)
    elif method == "ecm":
        p, q, time_taken = factorize_ecm(n)
    else:
        raise ValueError("Unsupported method")

    if not p or not q:
        return None, method, None, time_taken

    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    decrypted = ''.join(chr(pow(c, d, n)) for c in ciphertext)
    return decrypted, method, (p, q, d), time_taken
