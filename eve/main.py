import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from alice.main import main as alice_main


def factorize(n: int):
    """Very naive factorization used for demonstration only."""
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return i, n // i
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
    rsa, encrypted = alice_main()
    e, n = rsa.e, rsa.n

    print(f"\n[Eve] Intercepted Public Key: (e={e}, n={n})")
    print(f"[Eve] Intercepted Encrypted Message: {encrypted}")

    message = decrypt_as_eve(e, n, encrypted)
    if message:
        print(f"[Eve] Decrypted Message: {message}")


if __name__ == "__main__":
    main()