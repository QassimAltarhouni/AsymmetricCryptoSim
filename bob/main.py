import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crypto.rsa import RSA
from alice.main import main as alice_main


def main():
    # Alice sends the message and generates RSA keys
    rsa, encrypted_message = alice_main()

    print(f"\nBob received encrypted message: {encrypted_message}")
    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Bob decrypted the message: {decrypted_message}")


if __name__ == "__main__":
    main()