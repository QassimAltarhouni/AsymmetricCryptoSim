from crypto.rsa import RSA
from alice.main import main as alice_main

def main():
    # Alice sends the message
    rsa, encrypted_message = alice_main()

    print(f"\nBob received encrypted message: {encrypted_message}")
    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Bob decrypted the message: {decrypted_message}")

if __name__ == "__main__":
    main()


def receive_message(rsa, encrypted_message):
    print("\n[Bob] Received Encrypted Message:")
    print(encrypted_message)
    decrypted = rsa.decrypt(encrypted_message)
    print(f"[Bob] Decrypted Message: {decrypted}")
    return decrypted