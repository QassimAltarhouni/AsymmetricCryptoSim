# 🔐 AsymmetricCryptoSim – RSA Cryptography Simulation

This project simulates asymmetric cryptography using a toy RSA implementation. It includes a full communication chain:
- **Alice** (sender)
- **Bob** (receiver)
- **Eve** (attacker)

You can observe how encrypted communication works and how Eve attempts to break it using factorization (Pollard’s Rho). The system is interactive, configurable, and educational.

---

## 📁 Project Features

- ✅ **Simple Demo:** Alice encrypts a message to Bob using RSA.
- ✅ **Full Simulation:** Eve tries to break the encryption by factoring `n`.
- 🔧 Configurable key lengths and attack methods (extendable).
- 📈 Optional performance comparison across different key sizes.

---

## ⚙️ Setup

Install required dependencies:

```
pip install -r requirements.txt
```

This will also install `pytest` if you want to run tests.

---

## 🚀 Running the Simulation

From the root of the project, run the full simulation (Alice → Bob → Eve):

```
python main.py --key-length 64
```

### Example Key Sizes:
- `--key-length 32` → Eve **will succeed**
- `--key-length 64` → Eve **might succeed**
- `--key-length 128+` → Eve **will likely fail**

Example output:
```
Public Key (e, n): (65537, 1387306693)
Encrypted Message: [806436040, 231302551, ...]
Bob decrypted the message: Hello Bob!
Eve failed to factor n. The encryption is secure.
```

---

## 🧪 Running Tests

Run all unit tests:

```
pytest tests/
```

Tests include:
- Correct encryption/decryption with RSA
- Eve’s ability to break small-key RSA

---

## 📄 Output

When Eve attempts to decrypt, results are saved in `eve_output.txt`:

```
Eve's RSA Attack Simulation Log
===============================
Public Key (e, n): (65537, 1387306693)
Encrypted Message: [806436040, ...]
Decrypted Message: Hello Bob!
Attack Time: 0.00 seconds
```

---

## 🧠 Optional: Extend the Project

Want to go further?
- Add another attack method (Fermat’s factorization, brute-force, etc.)
- Add a timeout limit or performance graph
- Compare RSA with ElGamal
- Build a simple GUI or Flask API

---

## 📅 Deadline

This project is part of Problem Set 4 and is due **June 23**.
