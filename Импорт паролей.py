# -*- coding: utf-8 -*-
"""
Импорт паролей из твоего файла в зашифрованное хранилище МойБота.
Запускаешь ТЫ — пароли не уходят никуда, только шифруются локально.
Поддерживает: CSV (в т.ч. экспорт из Chrome/Edge), и текстовые строки вида
   сервис | логин | пароль     (разделитель : , - | или таб)
"""
import os
import sys
import csv
import getpass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vault

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

print("=== Импорт паролей в защищённое хранилище МойБота ===\n")
path = input("Перетащи сюда файл с паролями и нажми Enter\n(или впиши полный путь): ").strip().strip('"')
if not os.path.isfile(path):
    print("Файл не найден."); input("Enter..."); sys.exit()

master = getpass.getpass("\nМастер-пароль (тот же, что у веба; ввод скрыт): ").strip()
if vault._read(master) is None:
    print("Неверный мастер-пароль (хранилище создано с другим). Отмена."); input("Enter..."); sys.exit()

entries = []   # (service, login, password)

def _clean(s): return (s or "").strip().strip('"').strip()

# 1) Пробуем как CSV (экспорт браузера: колонки name/url/username/password)
try:
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        sample = f.read(2048); f.seek(0)
        if "," in sample or ";" in sample:
            reader = csv.DictReader(f)
            cols = [c.lower() for c in (reader.fieldnames or [])]
            if any("password" in c for c in cols) and any(("username" in c or "login" in c) for c in cols):
                def col(row, *names):
                    for k, v in row.items():
                        if k and k.lower() in names: return v
                    return ""
                for row in reader:
                    svc = _clean(col(row, "name", "title") or col(row, "url", "website"))
                    lg = _clean(col(row, "username", "login", "email", "e-mail"))
                    pw = _clean(col(row, "password", "pass"))
                    if pw and (svc or lg):
                        entries.append((svc or lg, lg, pw))
except Exception:
    pass

# 2) Если CSV не дал — построчно по разделителям
if not entries:
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        parts = None
        for sep in ("|", "\t", ";", " : ", ":", " - ", ",", " "):
            p = [x for x in line.split(sep) if x.strip()]
            if len(p) >= 3:
                parts = p; break
        if not parts and len(line.split()) >= 3:
            parts = line.split()
        if parts and len(parts) >= 3:
            entries.append((_clean(parts[0]), _clean(parts[1]), _clean(parts[-1])))

if not entries:
    print("\nНе смог разобрать формат файла. Покажи первые строки боту в чате "
          "(БЕЗ паролей — просто как выглядит структура), и я поправлю импортёр.")
    input("Enter..."); sys.exit()

print(f"\nНашёл {len(entries)} записей. Проверь (пароли скрыты):")
for svc, lg, pw in entries[:40]:
    print(f"  • {svc:<22} логин: {lg:<28} пароль: {'*' * min(len(pw), 8)}")
if len(entries) > 40:
    print(f"  ... и ещё {len(entries) - 40}")

if input("\nВсё верно? Импортировать? (да/нет): ").strip().lower() not in ("да", "yes", "y", "д"):
    print("Отмена."); input("Enter..."); sys.exit()

ok = 0
for svc, lg, pw in entries:
    if vault.set_credential(master, svc, lg, pw):
        ok += 1
print(f"\n✓ Импортировано {ok} паролей в зашифрованное хранилище.")
print("Сервисы:", ", ".join(vault.list_services(master)))
print("\nТеперь СОВЕТУЮ удалить исходный файл с паролями — он в открытом виде и небезопасен.")
input("Enter — закрыть...")
