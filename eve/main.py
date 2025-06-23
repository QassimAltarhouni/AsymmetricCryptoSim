import random
import math
from time import time
from datetime import datetime

# Local project imports (adjust if needed)
from alice.main import main as alice_main
from eve.attack import factorize_ecm, factorize_gnfs


# ----------- Attack Implementations -----------

def _pollards_rho(n, max_iterations=10_000, max_attempts=5):
    if n % 2 == 0:
        return 2
    for _ in range(max_attempts):
        x = random.randrange(2, n - 1)
        y = x
        c = random.randrange(1, n - 1)
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

def _fermat_factor(n, max_iter=100000):
    a = math.isqrt(n)
    b2 = a * a - n
    count = 0
    while b2 < 0 or not math.isqrt(b2) ** 2 == b2:
        a += 1
        b2 = a * a - n
        count += 1
        if count > max_iter:
            return None, None
    b = math.isqrt(b2)
    return a - b, a + b

def factorize_pollard(n):
    start = time()
    if n % 2 == 0:
        return 2, n // 2, time() - start
    factor = _pollards_rho(n)
    if factor and 1 < factor < n:
        return factor, n // factor, time() - start
    return None, None, -1

def factorize_fermat(n):
    start = time()
    p, q = _fermat_factor(n)
    duration = time() - start
    if p and q:
        return p, q, duration
    return None, None, -1

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


# ----------- Decrypt + Attack Wrapper -----------

def decrypt_with_method(e, n, ciphertext, method):
    if method == "rho":
        p, q, time_taken = factorize_pollard(n)
    elif method == "fermat":
        p, q, time_taken = factorize_fermat(n)
    elif method == "ecm":
        p, q, time_taken = factorize_ecm(n)
    elif method == "gnfs":
        p, q, time_taken = factorize_gnfs(n)
    else:
        return None, method, None, -1

    if not p or not q:
        return None, method, None, time_taken

    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    decrypted = ''.join(chr(pow(c, d, n)) for c in ciphertext)
    return decrypted, method, (p, q, d), time_taken


# ----------- Output Formatter -----------

def save_to_txt(public_key, encrypted_message, attacks_results):
    with open("eve_output.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"🧪 New Test Run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        f.write("🔓 RSA Attack Simulation Log (Comparison)\n")
        f.write("=" * 60 + "\n")
        f.write(f"🔑 Public Key (e, n):\n{public_key}\n\n")
        f.write("🔐 Encrypted Message:\n")
        f.write(", ".join(map(str, encrypted_message)) + "\n\n")

        for method, success, detail, duration in attacks_results:
            f.write("-" * 60 + "\n")
            f.write(f"[{method.upper()}] Attack\n")
            if success:
                p, q, d = detail
                f.write(f"✅ Success\n")
                f.write(f"  p = {p}\n  q = {q}\n  d = {d}\n")
                f.write(f"🔓 Decrypted Message: {success}\n")
            else:
                f.write("❌ Failed\n")
            f.write(f"⏱️ Time: {duration:.4f} seconds\n")


# ----------- Main Execution -----------

def main():
    rsa, encrypted = alice_main()
    e, n = rsa.e, rsa.n
    methods = ["rho", "fermat", "ecm", "gnfs"]

    attacks_results = []
    for method in methods:
        print(f"[Eve] Trying attack method: {method}")
        decrypted, method_used, detail, duration = decrypt_with_method(e, n, encrypted, method=method)
        success = decrypted if decrypted else None
        attacks_results.append((method_used, success, detail, duration))

    save_to_txt((e, n), encrypted, attacks_results)
    print("✅ Log saved to eve_output.txt")


if __name__ == "__main__":
    main()
