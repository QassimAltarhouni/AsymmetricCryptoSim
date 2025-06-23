import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crypto.rsa import RSA
from alice.main import main as alice_main


def main(key_length: int = 64):
    """Run the Alice → Bob exchange and return the RSA context."""
    # Alice sends the message and generates RSA keys
    rsa, encrypted_message = alice_main(key_length=key_length)

    print(f"\nBob received encrypted message: {encrypted_message}")
    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Bob decrypted the message: {decrypted_message}")

    return rsa, encrypted_message


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the simple Alice/Bob demo")
    parser.add_argument(
        "-k",
        "--key-length",
        type=int,
        default=64,
        help="RSA key length in bits (default: 64 for quick demo)",
    )
    args = parser.parse_args()

    main(key_length=args.key_length)