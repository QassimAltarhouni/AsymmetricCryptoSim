from crypto.rsa import RSA

def main():
    rsa = RSA()
    print(f"Public Key (e, n): ({rsa.e}, {rsa.n})")
    print(f"Private Key (d, n): ({rsa.d}, {rsa.n})")

    message = "Hello Bob!"
    print(f"\nOriginal Message: {message}")

    encrypted = rsa.encrypt(message)
    print(f"Encrypted Message: {encrypted}")

    # Optional: Simulate sending to Bob
    return rsa, encrypted

if __name__ == "__main__":
    main()
