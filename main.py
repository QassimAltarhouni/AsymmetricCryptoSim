import os
import sys
from time import time
from datetime import datetime

from eve.attack import eve_attack

# Add paths to modules
sys.path.append(os.path.join(os.path.dirname(__file__), "alice"))
sys.path.append(os.path.join(os.path.dirname(__file__), "bob"))
sys.path.append(os.path.join(os.path.dirname(__file__), "eve"))

from bob.main import main as bob_main



def save_comparison(public_key, encrypted_message, results, key_length):
    with open("eve_output.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"🧪 New Test Run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🔑 Key Length: {key_length} bits\n")
        f.write("=" * 60 + "\n")
        f.write("🔓 RSA Attack Simulation Log (Comparison)\n")
        f.write("=" * 60 + "\n")
        f.write(f"Public Key (e, n):\n{public_key}\n\n")
        f.write("Encrypted Message:\n")
        f.write(", ".join(map(str, encrypted_message)) + "\n\n")

        for method, success, details, duration in results:
            f.write(f"[{method.upper()}] Attack:\n")
            if success:
                p, q, d = details
                f.write(f"  ✅ Success\n")
                f.write(f"  p = {p}\n  q = {q}\n  d = {d}\n")
                f.write(f"  🔓 Decrypted Message: {success}\n")
            else:
                f.write("  ❌ Failed\n")
            f.write(f"  ⏱️ Time: {duration:.4f} seconds\n")
            f.write("-" * 50 + "\n")


def append_summary_to_log(log_path="eve_output.txt", flag_path=".summary_written.flag"):
    if os.path.exists(flag_path):
        return  # Already written

    summary = """
============================================================
📊 Attack Comparison by Key Length
============================================================
| 🔑 Key Length (bits) | ✅ RHO | ✅ FERMAT | ✅ ECM  | ✅ GNFS | 📝 Notes                                         |
|----------------------|--------|-----------|--------|--------|--------------------------------------------------|
| 32                   | ✔️     | ✔️         | ✔️     | ✔️     | Very weak key — broken by all methods easily    |
| 64                   | ✔️     | ❌         | ✔️     | ✔️     | GNFS/ECM succeed where Fermat fails             |
| 96                   | ❌     | ❌         | ❌     | ✔️     | Only GNFS may work occasionally                 |
| 128+                 | ❌     | ❌         | ❌     | ❌     | Too strong for these methods                    |
"""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(summary + "\n")

    with open(flag_path, "w") as f:
        f.write("written")


def full_simulation(key_length: int = 64):
    print("🔐 Simulating RSA Communication: Alice → Bob → Eve\n")
    rsa, encrypted = bob_main(key_length=key_length)
    e, n = rsa.e, rsa.n

    methods = ["rho", "fermat", "ecm", "gnfs"]
    results = []

    for method in methods:
        print(f"🕵️ Eve using {method.upper()}...")
        start = time()
        decrypted, _, info, duration = eve_attack(e, n, encrypted, method=method)
        success = decrypted if decrypted else None
        results.append((method, success, info, duration))

    save_comparison((e, n), encrypted, results, key_length)
    append_summary_to_log()
    print("✅ All results saved to eve_output.txt\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="🔍 RSA Eve Attack Comparison")
    parser.add_argument("-k", "--key-length", type=int, default=64, help="Key length in bits (default: 64)")
    args = parser.parse_args()
    full_simulation(key_length=args.key_length)
