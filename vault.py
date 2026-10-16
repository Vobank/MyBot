# -*- coding: utf-8 -*-
"""
Зашифрованное хранилище паролей аккаунтов (Fernet/AES).
Пароли НИКОГДА не хранятся в открытом виде — только зашифрованными мастер-ключом.
"""
import os
import json
import base64
import hashlib

from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_FILE = os.path.join(BASE_DIR, "vault.enc")

def _key(master):
    raw = hashlib.pbkdf2_hmac("sha256", master.encode("utf-8"), b"moybot-vault-salt-v1", 200_000, 32)
    return base64.urlsafe_b64encode(raw)

def _read(master):
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        data = Fernet(_key(master)).decrypt(open(VAULT_FILE, "rb").read())
        return json.loads(data.decode("utf-8"))
    except Exception:
        return None   # None = неверный мастер-пароль или битый файл

def _write(master, d):
    token = Fernet(_key(master)).encrypt(json.dumps(d, ensure_ascii=False).encode("utf-8"))
    open(VAULT_FILE, "wb").write(token)

def set_credential(master, service, login, password):
    d = _read(master)
    if d is None:
        return False
    d[service.lower()] = {"login": login, "password": password}
    _write(master, d)
    return True

def get_credential(master, service):
    d = _read(master)
    if not d:
        return None
    return d.get(service.lower())

def list_services(master):
    d = _read(master)
    return list(d.keys()) if d else []

def delete_credential(master, service):
    d = _read(master)
    if not d:
        return False
    d.pop(service.lower(), None)
    _write(master, d)
    return True
