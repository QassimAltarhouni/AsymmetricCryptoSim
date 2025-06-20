# AsymmetricCryptoSim

This repository provides a toy RSA implementation with two levels of demos:

* **Simple demo** – shows Alice sending an encrypted message to Bob.
* **Advanced demos** – a collection of interactive examples located under
  `RSA-CryptoSystem-main/src/scripts`.

## Setup

Install the dependencies before running any demos:

```bash
pip install -r requirements.txt
```

## Running the simple demo

From the repository root, execute Bob's script which imports Alice's logic:

```bash
PYTHONPATH=. python bob/main.py
```

Expected output includes printing of the generated public/private RSA keys,
Alice's encrypted message, and Bob decrypting that message, for example:

```
Public Key (e, n): (5, 17113)
Private Key (d, n): (10109, 17113)

Original Message: Hello Bob!
Encrypted Message: [2061, 14647, 7629, ...]

Bob received encrypted message: [2061, 14647, 7629, ...]
Bob decrypted the message: Hello Bob!
```

Numbers will differ each run since new keys are generated every time.

## Advanced interactive demos

Inside `RSA-CryptoSystem-main/src/scripts/` you will find several more
feature‑rich demonstrations:

* `interactive_demo.py` – run with `-t receiver` or `-t sender` in two
  separate terminals. Start the receiver first so it can generate a key pair
  and share its public key with the sender.
* `performance_stats.py` – executes non‑interactive benchmarks and saves
  timing graphs to `src/stats/rsa_stats`.
* `chosen_cipher_text_attack_demo.py` – simulates a chosen ciphertext attack
  on RSA. Configure options in `src/configurations.yaml` then run the script.
* `bruteforce_demo.py` – measures brute‑force attacks by factoring `n` and
  stores graphs in `src/stats/bruteforce_stats`.

For details on configuration parameters, consult
`RSA-CryptoSystem-main/README.md` in the subdirectory.