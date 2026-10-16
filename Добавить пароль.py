# -*- coding: utf-8 -*-
"""Безопасное добавление пароля аккаунта в зашифрованное хранилище."""
import sys, getpass
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import vault

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

print("=== Добавление пароля в защищённое хранилище МойБота ===")
print("Мастер-пароль — общий ключ ко всем аккаунтам (запомни его!).")
master = getpass.getpass("Мастер-пароль (ввод скрыт): ").strip()
if not master:
    print("Пусто — отмена."); sys.exit()

# проверим, что мастер верный (если хранилище уже есть)
if vault._read(master) is None:
    print("Неверный мастер-пароль (хранилище уже создано с другим). Отмена.")
    sys.exit()

while True:
    print("\n--- новый аккаунт (Enter в названии — выход) ---")
    service = input("Сервис (напр. epicgames, steam, gmail): ").strip()
    if not service:
        break
    login = input("Логин / почта: ").strip()
    password = getpass.getpass("Пароль (ввод скрыт): ").strip()
    if vault.set_credential(master, service, login, password):
        print(f"✓ Сохранено: {service}")
    else:
        print("Ошибка сохранения.")

print("\nГотово. Сервисы в хранилище:", ", ".join(vault.list_services(master)) or "(пусто)")
input("Enter — закрыть...")
