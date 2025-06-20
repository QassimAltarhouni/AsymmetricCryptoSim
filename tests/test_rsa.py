import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto.rsa import RSA
from eve.attack import eve_attack


def test_rsa_encrypt_decrypt():
    rsa = RSA(key_length=64)
    message = "hello"
    encrypted = rsa.encrypt(message)
    decrypted = rsa.decrypt(encrypted)
    assert decrypted == message


def test_eve_attack_small_modulus():
    rsa = RSA(key_length=32)
    message = "secret"
    ciphertext = rsa.encrypt(message)
    recovered = eve_attack(rsa.e, rsa.n, ciphertext)
    assert recovered == message