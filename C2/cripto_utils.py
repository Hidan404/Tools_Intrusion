# crypto_utils.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

KEY = b'minhachavesecreta'  # 16 bytes (AES-128); pode ser 24 ou 32 para AES-192/256

def encrypt_data(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted).decode()

def decrypt_data(enc_data):
    raw = base64.b64decode(enc_data)
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted), AES.block_size).decode()

def encrypt_bytes(data_bytes):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data_bytes, AES.block_size))
    return base64.b64encode(iv + encrypted)

def decrypt_bytes(enc_data_b64):
    raw = base64.b64decode(enc_data_b64)
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted), AES.block_size)