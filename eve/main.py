import os
import sys
import random
import math
from time import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from alice.main import main as alice_main


def _pollards_rho(n: int, max_iterations: int = 10_000) -> int | None:
    """Return a non-trivial factor of n using Pollard's rho algorithm."""
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


def factorize(n: int) -> tuple[int | None, int | None]:
    """Attempt to factor n using Pollard's rho."""
    if n % 2 == 0:
        return 2, n // 2

    factor = _pollards_rho(n)
    if factor and 1 < factor < n:
        return factor, n // factor
    return None, None


def modinv(a: int, m: int) -> int:
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def decrypt_as_eve(e: int, n: int, ciphertext: list[int]):
    p, q = factorize(n)
    if not p or not q:
        print("Eve failed to factor n.")
        return None

    print(f"[Eve] Factored n: p={p}, q={q}")
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    print(f"[Eve] Computed private key d={d}")
    return ''.join(chr(pow(c, d, n)) for c in ciphertext)




def main():
    start = time()
    rsa, encrypted = alice_main()
    e, n = rsa.e, rsa.n
    message = decrypt_as_eve(e, n, encrypted)
    duration = time() - start

    if message:
        save_to_txt((e, n), encrypted, message, duration)
        print("[✔] Output saved to eve_output.txt")


def save_to_txt(public_key, encrypted_message, decrypted_message, duration):
    with open("eve_output.txt", "w", encoding="utf-8") as f:
        f.write("🔓 Eve's RSA Attack Simulation Log\n")
        f.write("=" * 40 + "\n")
        f.write(f"Public Key (e, n):\n{public_key}\n\n")
        f.write("Encrypted Message:\n")
        f.write(", ".join(map(str, encrypted_message)) + "\n\n")
        f.write(f"Decrypted Message:\n{decrypted_message}\n")
        f.write(f"\nAttack Time: {duration:.2f} seconds\n")



if __name__ == "__main__":
    main()