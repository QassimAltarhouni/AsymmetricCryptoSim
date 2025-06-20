import os
import sys
from time import time

# Add internal module paths
sys.path.append(os.path.join(os.path.dirname(__file__), "alice"))
sys.path.append(os.path.join(os.path.dirname(__file__), "bob"))
sys.path.append(os.path.join(os.path.dirname(__file__), "eve"))

from alice.main import main as alice_main
from bob.main import main as bob_main
from eve.main import decrypt_as_eve, save_to_txt


def full_simulation():
    print("🔐 Starting Full RSA Simulation: Alice → Bob → Eve\n")

    # Step 1: Alice generates keys and encrypts message
    print("📡 Alice is encrypting the message...")
    rsa, encrypted_message = alice_main()

    # Step 2: Bob receives and decrypts the message
    print("\n📥 Bob is receiving and decrypting the message...")
    bob_main()

    # Step 3: Eve intercepts and attempts to decrypt
    print("\n🕵️ Eve is attempting to break the encryption...")
    e, n = rsa.e, rsa.n

    start = time()
    decrypted_by_eve = decrypt_as_eve(e, n, encrypted_message)
    duration = time() - start

    if decrypted_by_eve:
        save_to_txt((e, n), encrypted_message, decrypted_by_eve, duration)
        print("[✔] Eve successfully decrypted the message! Report saved to eve_output.txt")
    else:
        print("[❌] Eve failed to factor n. The encryption is secure.")


if __name__ == "__main__":
    full_simulation()
