import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crypto.rsa import RSA


def main(message: str = "Hello Bob!", key_length: int = 512):
    rsa = RSA(key_length=key_length)
    print(f"Public Key (e, n): ({rsa.e}, {rsa.n})")
    print(f"Private Key (d, n): ({rsa.d}, {rsa.n})")

    print(f"\nOriginal Message: {message}")
    encrypted = rsa.encrypt(message)
    print(f"Encrypted Message: {encrypted}")

    # Optional: Simulate sending to Bob
    return rsa, encrypted

if __name__ == "__main__":
    main()
