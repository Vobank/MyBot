# -*- coding: utf-8 -*-
"""
МойБот — личный ИИ-агент с онлайн-режимом.
Мозг: локальные модели через Ollama (офлайн, бесплатно, полностью твой).

Умеет:
  - вести диалог, думать вслух и писать код (видно в реальном времени)
  - создавать / читать / редактировать файлы
  - запускать команды и скрипты
  - искать в интернете
  - ВИДЕТЬ ЭКРАН и делать скриншоты (модель зрения qwen2.5vl)
  - УПРАВЛЯТЬ ПК: мышь, клики, ввод текста, горячие клавиши
  - редактировать собственный код и перезапускаться

Режимы (команда /режим):
  безопасный — спрашивает разрешение перед командами и управлением ПК
  авто       — делает всё сам, ничего не спрашивая

Команды в чате:
  /выход      — закрыть бота
  /режим      — переключить безопасный / авто
  /модель     — сменить модель-мозг
  /экран      — бот опишет, что сейчас на экране
  /очистить   — очистить память диалога
  /перезапуск — перезапустить бота
  /помощь     — справка
"""

import os
import re
import io
import sys
import ast
import json
import time
import base64
import threading
import subprocess

import requests

# ----------------------------------------------------------------------------
# Настройки
# ----------------------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:14b-instruct"      # мозг (текст+инструменты). /модель меняет
VISION_MODEL = "qwen2.5vl:7b"       # зрение (анализ экрана/скриншотов)
SELF_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(SELF_PATH)                # папка, где лежит сам бот
WORKDIR = os.path.join(BASE_DIR, "workspace")        # рабочая папка рядом с ботом
MAX_TOOL_OUTPUT = 6000
REQUEST_TIMEOUT = 900

MODE = "безопасный"   # "безопасный" | "авто"
HEADLESS = False      # True в веб-интерфейсе: без консольных запросов (действует сам, самоправку не даём)
VAULT_MASTER = None   # мастер-пароль для хранилища аккаунтов (задаётся при входе)

MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")   # память между запусками
BACKUP_DIR = os.path.join(BASE_DIR, "backups")        # копии кода до самоправок
IMPROVE_LOG = os.path.join(BASE_DIR, "улучшения.log") # журнал самоулучшений
MEMORY_LIMIT = 40                                     # сколько последних сообщений помнить

os.makedirs(WORKDIR, exist_ok=True)
os.makedirs(os.path.join(WORKDIR, "screenshots"), exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# Цвета
# ----------------------------------------------------------------------------
try:
    os.system("")                       # включает ANSI-цвета в Windows
    sys.stdout.reconfigure(encoding="utf-8")   # чтобы не падать на любой консоли
    sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass

class C:
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    BLUE = "\033[94m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
    RED = "\033[91m"; CYAN = "\033[96m"; MAGENTA = "\033[95m"

def say(t):       print(f"{C.GREEN}{C.BOLD}Бот:{C.RESET} {t}")
def info(t):      print(f"{C.DIM}{t}{C.RESET}")
def tool_note(t): print(f"{C.CYAN}  ⚙ {t}{C.RESET}")
def act_note(t):  print(f"{C.MAGENTA}  🖱 {t}{C.RESET}")

# ----------------------------------------------------------------------------
# Ленивая загрузка тяжёлых библиотек
# ----------------------------------------------------------------------------
def grab_screenshot_png():
    """Снимок всего экрана -> PNG-байты."""
    from PIL import ImageGrab
    img = ImageGrab.grab(all_screens=True)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def _pyautogui():
    import pyautogui
    pyautogui.FAILSAFE = True   # увести мышь в угол = аварийный стоп
    return pyautogui

# ----------------------------------------------------------------------------
# Системная инструкция
# ----------------------------------------------------------------------------
def system_prompt():
    return f"""Ты — личный ИИ-агент по имени МойБот. Хозяин (босс) даёт поручения — ты их выполняешь сам, шаг за шагом.

У тебя есть инструменты для реальных действий: файлы, запуск команд, поиск в интернете, ЗРЕНИЕ (видеть экран и скриншоты) и УПРАВЛЕНИЕ ПК (мышь, клавиатура). Ещё ты можешь читать и переписывать собственный код.

Правила:
- Отвечай на русском, коротко и по делу. Рассуждай вслух кратко — босс видит твои мысли.
- На ВОПРОСЫ отвечай текстом. Погода — только через инструмент weather (НЕ открывай сайт погоды). Факты из интернета — web_search/fetch_url, потом дай ответ словами. Сайт (open_url) открывай ТОЛЬКО если явно просят «открой …».
- Пользуйся инструментами сам, не проси разрешения (безопасность решает режим программы).
- ДЕЙСТВУЙ, а не переспрашивай. НЕ задавай вопросов вроде «вы хотите, чтобы я…» — просто бери и делай. Если каких-то мелочей не хватает — разумно предположи сам и выполни. Уточняй ТОЛЬКО когда без ответа совсем никак (например, непонятно, какой именно из нескольких файлов открыть).
- Чтобы ОТКРЫТЬ программу (Epic Games, Steam, Блокнот, Chrome и т.п.) — вызывай open_app с её названием (он сам найдёт её в меню Пуск). Программа — это НЕ папка, не ищи её в проводнике.
- Чтобы ОТКРЫТЬ файл — open_file (по имени). Чтобы найти файлы — find_files. Не пиши команды в терминал для запуска.
- Чтобы НАПЕЧАТАТЬ текст куда-то — сначала кликни в нужное поле (mouse_click), потом type_text с текстом.
- В ответе пиши ТОЛЬКО обычный человеческий текст. НЕ выводи служебное: теги <tool_response>/<tool_call>, слова user/assistant/system, «почему-то ...».
- По-настоящему опасное (удалить файлы, почистить диск, сменить важные настройки) — только с подтверждением: сначала скажи, ЧТО именно сделаешь.
- Прежде чем кликать или печатать по экрану — сначала посмотри на экран инструментом see_screen, чтобы понять, где что находится, и назови координаты.
- Программу сохраняй в файл (write_file), а не просто показывай.
- Рабочая папка: {WORKDIR}
- Текущий режим: {MODE}. В режиме «безопасный» опасные действия подтверждает босс.
- Когда задача готова — кратко скажи, что сделал."""

# ----------------------------------------------------------------------------
# Разрешение на действие (зависит от режима)
# ----------------------------------------------------------------------------
def allowed(action_desc):
    if HEADLESS or MODE == "авто":     # в вебе действуем сами (пользователь видит действия и экран)
        return True
    ans = input(f"{C.YELLOW}  «{action_desc}» — выполнить? [Enter=да / n=нет]: {C.RESET}").strip().lower()
    return ans != "n"

def confirm_always(action_desc):
    """Подтверждение, которое спрашивают ВСЕГДА — даже в режиме «авто».
    Для по-настоящему рискованного (переписать собственный код)."""
    if HEADLESS:                       # без консоли не разрешаем самоправку (некому подтвердить)
        return False
    ans = input(f"{C.RED}  ⚠ {action_desc}. Это может сломать бота. Напиши ДА, чтобы разрешить: {C.RESET}").strip().lower()
    return ans in ("да", "yes", "y", "д")

# ----------------------------------------------------------------------------
# Инструменты: файлы / команды / интернет
# ----------------------------------------------------------------------------
def _resolve(path):
    return path if os.path.isabs(path) else os.path.join(WORKDIR, path)

def tool_write_file(path, content):
    full = _resolve(path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    tool_note(f"записал файл: {full} ({len(content)} симв.)")
    return f"Файл сохранён: {full}"

def tool_read_file(path):
    full = _resolve(path)
    if not os.path.exists(full):
        return f"Файл не найден: {full}"
    with open(full, "r", encoding="utf-8", errors="replace") as f:
        data = f.read()
    tool_note(f"прочитал файл: {full}")
    return data[:MAX_TOOL_OUTPUT]

def tool_list_dir(path="."):
    full = _resolve(path)
    if not os.path.isdir(full):
        return f"Папка не найдена: {full}"
    out = []
    for name in sorted(os.listdir(full)):
        p = os.path.join(full, name)
        out.append(("[папка] " if os.path.isdir(p) else "") + name)
    tool_note(f"список папки: {full}")
    return "\n".join(out) if out else "(пусто)"

def tool_run_command(command):
    tool_note(f"команда: {command}")
    if not allowed(f"выполнить команду: {command}"):
        return "Босс отменил выполнение команды."
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR, capture_output=True,
                           text=True, timeout=300, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (("\n[ошибки]\n" + r.stderr) if r.stderr else "")
        return f"Код возврата: {r.returncode}\n{(out.strip() or '(пусто)')[:MAX_TOOL_OUTPUT]}"
    except subprocess.TimeoutExpired:
        return "Прервано: превышено время (5 мин)."
    except Exception as e:
        return f"Ошибка запуска: {e}"

def tool_web_search(query, count=5):
    tool_note(f"поиск: {query}")
    try:
        r = requests.post("https://html.duckduckgo.com/html/", data={"q": query},
                          headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        res = []
        for m in re.finditer(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S):
            title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if title:
                res.append(f"- {title}\n  {m.group(1)}")
            if len(res) >= count:
                break
        return "\n".join(res) if res else "Ничего не найдено."
    except Exception as e:
        return f"Ошибка поиска: {e}"

def tool_fetch_url(url):
    tool_note(f"страница: {url}")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        t = re.sub(r"(?is)<(script|style).*?</\1>", " ", r.text)
        t = re.sub(r"<[^>]+>", " ", t)
        return re.sub(r"\s+", " ", t).strip()[:MAX_TOOL_OUTPUT]
    except Exception as e:
        return f"Ошибка загрузки: {e}"

# ----------------------------------------------------------------------------
# Инструменты: ЗРЕНИЕ
# ----------------------------------------------------------------------------
def ask_vision(png_bytes, question):
    """Спросить модель зрения про картинку."""
    b64 = base64.b64encode(png_bytes).decode()
    r = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": VISION_MODEL, "stream": False,
        "messages": [{"role": "user", "content": question, "images": [b64]}],
    }, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()

def tool_see_screen(question="Что сейчас на экране? Опиши подробно и укажи заметные элементы."):
    tool_note("смотрю на экран...")
    try:
        png = grab_screenshot_png()
        return ask_vision(png, question)
    except Exception as e:
        return f"Не смог посмотреть на экран: {e}"

def tool_save_screenshot(path="screenshots/screen.png"):
    try:
        png = grab_screenshot_png()
        full = _resolve(path)
        os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
        with open(full, "wb") as f:
            f.write(png)
        tool_note(f"скриншот сохранён: {full}")
        return f"Скриншот сохранён: {full}"
    except Exception as e:
        return f"Ошибка скриншота: {e}"

# ----------------------------------------------------------------------------
# Инструменты: УПРАВЛЕНИЕ ПК
# ----------------------------------------------------------------------------
def tool_mouse_click(x, y, button="left", clicks=1):
    if not allowed(f"клик {button} по ({x},{y})"):
        return "Босс отменил клик."
    try:
        pg = _pyautogui()
        pg.click(x=int(x), y=int(y), clicks=int(clicks), button=button, interval=0.1)
        act_note(f"клик {button} ({x},{y}) x{clicks}")
        return f"Клик выполнен: ({x},{y})"
    except Exception as e:
        return f"Ошибка клика: {e}"

def tool_move_mouse(x, y):
    if not allowed(f"навести мышь на ({x},{y})"):
        return "Босс отменил."
    try:
        _pyautogui().moveTo(int(x), int(y), duration=0.3)
        act_note(f"мышь -> ({x},{y})")
        return "Готово."
    except Exception as e:
        return f"Ошибка: {e}"

def tool_type_text(text):
    if not allowed(f"напечатать текст: {text[:60]}"):
        return "Босс отменил ввод."
    try:
        pg = _pyautogui()
        if _clip_set(text):            # через буфер обмена — печатает ЛЮБЫЕ символы, в т.ч. русские
            pg.hotkey("ctrl", "v")
        else:
            pg.typewrite(text, interval=0.02)
        act_note(f"напечатал {len(text)} симв.")
        return "Напечатано."
    except Exception as e:
        return f"Ошибка ввода: {e}"

def tool_press_keys(keys):
    """keys: 'enter' или комбинация 'ctrl+s' / 'alt+tab'."""
    if not allowed(f"нажать клавиши: {keys}"):
        return "Босс отменил."
    try:
        pg = _pyautogui()
        parts = [k.strip() for k in keys.replace("+", " ").split()]
        if len(parts) > 1:
            pg.hotkey(*parts)
        else:
            pg.press(parts[0])
        act_note(f"клавиши: {keys}")
        return f"Нажато: {keys}"
    except Exception as e:
        return f"Ошибка клавиш: {e}"

def tool_scroll(amount):
    try:
        _pyautogui().scroll(int(amount))
        act_note(f"прокрутка {amount}")
        return "Прокручено."
    except Exception as e:
        return f"Ошибка: {e}"

# ----------------------------------------------------------------------------
# Инструменты: приложения / сайты / почта
# ----------------------------------------------------------------------------
def tool_open_url(url):
    """Открыть сайт в браузере по умолчанию."""
    if not url:
        return "Не указан адрес."
    if not re.match(r"^https?://", url):
        url = "https://" + url
    try:
        import webbrowser
        webbrowser.open(url)
        act_note(f"открыл сайт: {url}")
        return f"Открыл {url}"
    except Exception as e:
        return f"Ошибка: {e}"

def _clip_set(text):
    """Положить текст в буфер обмена (работает с кириллицей/любыми символами)."""
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value $input"],
                       input=text, text=True, encoding="utf-8", timeout=10)
        return True
    except Exception:
        return False

def tool_windows_search(query="", press_enter=True):
    """Открыть поиск Windows (кнопка Пуск), вписать запрос и (по умолчанию) открыть первый результат."""
    if not query:
        return "Что искать в Windows?"
    if not allowed(f"поиск в Windows: {query}"):
        return "Босс отменил."
    try:
        pg = _pyautogui()
        pg.press("win"); time.sleep(0.7)
        if _clip_set(query):
            pg.hotkey("ctrl", "v")            # вставка — печатает любые символы, в т.ч. русские
        else:
            pg.typewrite(query, interval=0.03)
        time.sleep(0.9)
        if press_enter:
            pg.press("enter")
        act_note(f"поиск Windows: {query}")
        return f"Открыл поиск Windows, вписал «{query}»" + (" и открыл первый результат." if press_enter else ".")
    except Exception as e:
        return f"Ошибка: {e}"

def tool_open_file(query=""):
    """Открыть ФАЙЛ или ПАПКУ по имени/пути. Папка откроется в Проводнике."""
    if not query:
        return "Что открыть — файл или папку?"
    q = query.strip().strip('"')
    # 1) прямой путь (файл или папка)
    if os.path.exists(q):
        try:
            os.startfile(q); act_note(f"открыл: {q}"); return f"Открыл: {q}"
        except Exception as e:
            return f"Ошибка: {e}"
    home = os.path.expanduser("~")
    ql = q.lower()
    # 2) известные папки по названию
    known = {"загрузки": "Downloads", "downloads": "Downloads", "рабочий стол": "Desktop",
             "desktop": "Desktop", "документы": "Documents", "documents": "Documents",
             "картинки": "Pictures", "pictures": "Pictures", "музыка": "Music", "видео": "Videos"}
    if ql in known:
        p = os.path.join(home, known[ql])
        if os.path.isdir(p):
            os.startfile(p); act_note(f"открыл папку: {p}"); return f"Открыл папку: {p}"
    # 3) поиск файла ИЛИ папки по имени
    roots = [os.path.join(home, d) for d in ("Desktop", "Downloads", "Documents", "Pictures")] + \
            [home, r"D:\Projects"]
    checked = 0
    for r in roots:
        if not os.path.isdir(r):
            continue
        for root, dirs, files in os.walk(r):
            for name in dirs + files:
                checked += 1
                if ql in name.lower():
                    full = os.path.join(root, name)
                    try:
                        os.startfile(full); act_note(f"открыл: {full}"); return f"Открыл: {full}"
                    except Exception:
                        pass
            if checked > 50000:
                break
    return f"«{query}» не нашёл в обычных папках. Дай точный путь (например D:\\Папка)."

def tool_open_app(name):
    """Открыть программу по имени: сначала ищем ярлык в меню Пуск (там Epic, Steam и т.п.)."""
    if not name:
        return "Не указано имя программы."
    import glob
    q = name.lower().replace(".exe", "").strip()
    dirs = [
        os.path.join(os.environ.get("ProgramData", ""), r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs"),
    ]
    for d in dirs:
        if not d or not os.path.isdir(d):
            continue
        for lnk in glob.glob(os.path.join(d, "**", "*.lnk"), recursive=True):
            base = os.path.splitext(os.path.basename(lnk))[0].lower()
            if q in base:
                try:
                    os.startfile(lnk)
                    act_note(f"запустил ярлык: {os.path.basename(lnk)}")
                    return f"Запускаю: {os.path.splitext(os.path.basename(lnk))[0]}"
                except Exception:
                    pass
    try:
        subprocess.Popen(f'start "" "{name}"', shell=True)
        act_note(f"пробую запустить: {name}")
        return f"Пробую запустить «{name}». Если не открылось — скажи точное название (как в меню Пуск)."
    except Exception as e:
        return f"Ошибка: {e}"

def tool_look_and_act(target="", action="click"):
    """Посмотреть на экран, найти элемент по описанию и кликнуть по нему.
    Медленно и не всегда точно (координаты даёт модель зрения)."""
    try:
        png = grab_screenshot_png()
        from PIL import Image
        W, H = Image.open(io.BytesIO(png)).size
        q = (f"На скриншоте экрана (ширина {W}px, высота {H}px) найди элемент: «{target}». "
             "Ответь СТРОГО двумя целыми числами через пробел — координаты X Y центра этого "
             "элемента в пикселях. Если элемента нет — ответь одним словом: нет.")
        ans = ask_vision(png, q)
        m = re.search(r"(\d{1,5})\D+(\d{1,5})", ans)
        if not m:
            return f"Не нашёл «{target}» на экране (модель: {ans[:100]})."
        x, y = int(m.group(1)), int(m.group(2))
        tool_note(f"нашёл «{target}» ~({x},{y})")
        if action == "move":
            return tool_move_mouse(x, y)
        return tool_mouse_click(x, y)
    except Exception as e:
        return f"Ошибка: {e}"

def tool_find_junk():
    """Просканировать типичные места мусора и показать, что МОЖНО удалить. НЕ удаляет."""
    tool_note("сканирую диск на мусор...")
    home = os.path.expanduser("~")
    targets = {
        "Временные файлы (TEMP)": os.environ.get("TEMP", ""),
        "Кэш Windows Temp": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"),
        "Загрузки": os.path.join(home, "Downloads"),
        "Корзина (примерно)": os.path.join(os.environ.get("SystemDrive", "C:") + "\\", "$Recycle.Bin"),
    }
    lines, total = [], 0
    for name, path in targets.items():
        if not path or not os.path.isdir(path):
            continue
        sz = n = 0
        for root, _, files in os.walk(path):
            for f in files:
                try:
                    sz += os.path.getsize(os.path.join(root, f)); n += 1
                except Exception:
                    pass
            if sz > 5e9:      # хватит считать после 5 ГБ
                break
        total += sz
        lines.append(f"• {name}: {n} файлов, ~{sz/1e9:.2f} ГБ\n    {path}")
    if not lines:
        return "Явного мусора в стандартных местах не нашёл."
    return ("Вот что обычно можно почистить (я НИЧЕГО не удалил — только показал). "
            f"Всего примерно {total/1e9:.2f} ГБ:\n" + "\n".join(lines) +
            "\n\nЕсли скажешь удалить что-то конкретное — сначала переспрошу.")

def tool_fill_login(service=""):
    """Ввести сохранённые логин и пароль для сервиса (из шифрованного хранилища).
    Пароль НЕ показывается и НЕ попадает в переписку."""
    if not VAULT_MASTER:
        return "Хранилище паролей заблокировано (не введён мастер-пароль при входе)."
    try:
        import vault
        cred = vault.get_credential(VAULT_MASTER, service)
    except Exception as e:
        return f"Ошибка хранилища: {e}"
    if not cred:
        return (f"Для «{service}» нет сохранённого пароля. Добавь его через программу "
                "«Добавить пароль» (пароли туда вводятся безопасно, не через чат).")
    if not allowed(f"ввести логин и пароль для {service}"):
        return "Босс отменил ввод данных."
    try:
        pg = _pyautogui()
        pg.typewrite(cred["login"], interval=0.03)
        pg.press("tab"); time.sleep(0.4)
        pg.typewrite(cred["password"], interval=0.03)
        act_note(f"ввёл логин и пароль для {service}")
        return (f"Ввёл логин и пароль для {service} в текущие поля. "
                "Если поля не те — сначала кликни по полю логина и повтори. Затем «Войти».")
    except Exception as e:
        return f"Ошибка ввода: {e}"

def tool_weather(city=""):
    """Погода текстом (через wttr.in) — чтобы ОТВЕЧАТЬ, а не открывать сайт."""
    from urllib.parse import quote
    c = quote(city or "")
    try:
        r = requests.get(f"https://wttr.in/{c}?format=3&lang=ru",
                         headers={"User-Agent": "curl/8"}, timeout=15)
        line = r.text.strip()
        if r.ok and line and "html" not in line.lower():
            act_note(f"узнал погоду: {city or 'тек. место'}")
            return line
        return "Не удалось получить погоду. Уточни город."
    except Exception as e:
        return f"Ошибка погоды: {e}"

def tool_send_gmail(to="", subject="", body=""):
    """Открыть окно написания письма в Gmail с уже заполненными полями."""
    from urllib.parse import quote
    url = ("https://mail.google.com/mail/?view=cm&fs=1"
           f"&to={quote(to)}&su={quote(subject)}&body={quote(body)}")
    try:
        import webbrowser
        webbrowser.open(url)
        act_note(f"открыл письмо в Gmail для {to or '(без адреса)'}")
        return ("Открыл окно письма в Gmail с заполненным текстом. "
                "Осталось нажать «Отправить» (или Ctrl+Enter).")
    except Exception as e:
        return f"Ошибка: {e}"

# ----------------------------------------------------------------------------
# Инструменты: САМОПРАВКА
# ----------------------------------------------------------------------------
def tool_read_own_code():
    tool_note("читаю собственный код")
    with open(SELF_PATH, "r", encoding="utf-8") as f:
        return f.read()[:MAX_TOOL_OUTPUT * 4]

def tool_update_own_code(content):
    # ВСЕГДА спрашиваем подтверждение — даже в режиме «авто» (это самое рискованное действие).
    if not confirm_always("переписать собственный код bot.py"):
        return "Босс не подтвердил — самоправка отменена."
    # Проверяем, что новый код вообще валиден, иначе бот сломается.
    try:
        ast.parse(content)
    except SyntaxError as e:
        return f"Отклонено: в новом коде синтаксическая ошибка (строка {e.lineno}). Бот не тронут."
    if "def main(" not in content or "def run_agent(" not in content:
        return "Отклонено: в новом коде потеряны важные части (main/run_agent). Бот не тронут."
    backup = SELF_PATH + ".bak"
    try:
        with open(SELF_PATH, "r", encoding="utf-8") as f:
            open(backup, "w", encoding="utf-8").write(f.read())
        with open(SELF_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        tool_note(f"код обновлён (бэкап: {backup}). Нужен /перезапуск.")
        return "Код обновлён. Скажи боссу перезапустить бота командой /перезапуск."
    except Exception as e:
        return f"Ошибка самоправки: {e}"

# ----------------------------------------------------------------------------
# Карта инструментов и их описания
# ----------------------------------------------------------------------------
TOOL_FUNCS = {
    "write_file": lambda a: tool_write_file(a["path"], a["content"]),
    "read_file": lambda a: tool_read_file(a["path"]),
    "list_dir": lambda a: tool_list_dir(a.get("path", ".")),
    "run_command": lambda a: tool_run_command(a["command"]),
    "web_search": lambda a: tool_web_search(a["query"]),
    "fetch_url": lambda a: tool_fetch_url(a["url"]),
    "see_screen": lambda a: tool_see_screen(a.get("question", "Что на экране? Опиши подробно.")),
    "save_screenshot": lambda a: tool_save_screenshot(a.get("path", "screenshots/screen.png")),
    "mouse_click": lambda a: tool_mouse_click(a["x"], a["y"], a.get("button", "left"), a.get("clicks", 1)),
    "move_mouse": lambda a: tool_move_mouse(a["x"], a["y"]),
    "type_text": lambda a: tool_type_text(a["text"]),
    "press_keys": lambda a: tool_press_keys(a["keys"]),
    "scroll": lambda a: tool_scroll(a["amount"]),
    "open_url": lambda a: tool_open_url(a.get("url", "")),
    "open_app": lambda a: tool_open_app(a.get("name", "")),
    "open_file": lambda a: tool_open_file(a.get("query", "")),
    "windows_search": lambda a: tool_windows_search(a.get("query", ""), a.get("press_enter", True)),
    "weather": lambda a: tool_weather(a.get("city", "")),
    "look_and_act": lambda a: tool_look_and_act(a.get("target", ""), a.get("action", "click")),
    "find_junk": lambda a: tool_find_junk(),
    "fill_login": lambda a: tool_fill_login(a.get("service", "")),
    "send_gmail": lambda a: tool_send_gmail(a.get("to", ""), a.get("subject", ""), a.get("body", "")),
    "read_own_code": lambda a: tool_read_own_code(),
    "update_own_code": lambda a: tool_update_own_code(a["content"]),
}

def _fn(name, desc, props, req=None):
    return {"type": "function", "function": {
        "name": name, "description": desc,
        "parameters": {"type": "object", "properties": props, "required": req or []}}}

TOOLS = [
    _fn("write_file", "Создать/перезаписать файл.",
        {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"]),
    _fn("read_file", "Прочитать файл.", {"path": {"type": "string"}}, ["path"]),
    _fn("list_dir", "Список файлов в папке.", {"path": {"type": "string"}}),
    _fn("run_command", "Выполнить команду в терминале Windows.", {"command": {"type": "string"}}, ["command"]),
    _fn("web_search", "Поиск в интернете (заголовки+ссылки).", {"query": {"type": "string"}}, ["query"]),
    _fn("fetch_url", "Открыть страницу и вернуть текст.", {"url": {"type": "string"}}, ["url"]),
    _fn("see_screen", "ПОСМОТРЕТЬ на экран и получить описание. Задай конкретный вопрос про экран.",
        {"question": {"type": "string"}}),
    _fn("save_screenshot", "Сделать и сохранить скриншот в файл.", {"path": {"type": "string"}}),
    _fn("mouse_click", "Клик мышью по координатам экрана.",
        {"x": {"type": "integer"}, "y": {"type": "integer"},
         "button": {"type": "string", "description": "left/right/middle"},
         "clicks": {"type": "integer"}}, ["x", "y"]),
    _fn("move_mouse", "Навести курсор на координаты.",
        {"x": {"type": "integer"}, "y": {"type": "integer"}}, ["x", "y"]),
    _fn("type_text", "Напечатать текст с клавиатуры.", {"text": {"type": "string"}}, ["text"]),
    _fn("press_keys", "Нажать клавишу или комбинацию, напр. 'enter' или 'ctrl+s'.",
        {"keys": {"type": "string"}}, ["keys"]),
    _fn("scroll", "Прокрутить колесо мыши (число: + вверх, - вниз).", {"amount": {"type": "integer"}}, ["amount"]),
    _fn("open_url", "Открыть сайт в браузере (например google.com, youtube.com).",
        {"url": {"type": "string"}}, ["url"]),
    _fn("open_app", "Запустить программу на ПК по имени (например notepad, calc, chrome, epic games, steam).",
        {"name": {"type": "string"}}, ["name"]),
    _fn("open_file", "Открыть ФАЙЛ или ПАПКУ по имени или пути (папка откроется в Проводнике). "
        "Понимает «Загрузки», «Рабочий стол», «Документы».",
        {"query": {"type": "string"}}, ["query"]),
    _fn("windows_search", "Открыть поиск Windows (кнопка Пуск), вписать запрос и открыть первый результат. "
        "Годится для поиска настроек и того, чего нет в open_app/open_file.",
        {"query": {"type": "string"}}, ["query"]),
    _fn("weather", "Узнать ПОГОДУ и ответить текстом (не открывая сайт). Укажи город.",
        {"city": {"type": "string"}}),
    _fn("look_and_act", "Посмотреть на экран, найти элемент по описанию и кликнуть по нему "
        "(медленно). target — что искать, action — click или move.",
        {"target": {"type": "string"}, "action": {"type": "string"}}, ["target"]),
    _fn("find_junk", "Просканировать диск и показать, что можно удалить (мусор/временные). Не удаляет.", {}),
    _fn("fill_login", "Ввести сохранённые логин и пароль для сервиса (epicgames, steam, gmail...) "
        "в текущие поля входа. Пароль берётся из шифрованного хранилища.",
        {"service": {"type": "string"}}, ["service"]),
    _fn("send_gmail", "Открыть окно написания письма в Gmail с заполненными адресом, темой и текстом.",
        {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}),
    _fn("read_own_code", "Прочитать собственный исходный код бота.", {}),
    _fn("update_own_code", "Переписать собственный код (нужен перезапуск).", {"content": {"type": "string"}}, ["content"]),
]

# ----------------------------------------------------------------------------
# Общение с Ollama (со стримингом — видно, как бот думает)
# ----------------------------------------------------------------------------
def chat_stream(messages):
    """Стримим ответ модели. Печатаем текст по мере генерации.
    Возвращаем собранное сообщение с content и tool_calls."""
    resp = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL, "messages": messages, "tools": TOOLS, "stream": True,
    }, stream=True, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    content = ""
    tool_calls = []
    printed_prefix = False
    for line in resp.iter_lines():
        if not line:
            continue
        chunk = json.loads(line.decode("utf-8"))
        msg = chunk.get("message", {})
        delta = msg.get("content", "")
        if delta:
            if not printed_prefix:
                print(f"{C.GREEN}{C.BOLD}Бот:{C.RESET} ", end="", flush=True)
                printed_prefix = True
            print(delta, end="", flush=True)
            content += delta
        if msg.get("tool_calls"):
            tool_calls.extend(msg["tool_calls"])
        if chunk.get("done"):
            break
    if printed_prefix:
        print()
    return {"role": "assistant", "content": content, "tool_calls": tool_calls}

def run_agent(messages):
    for _ in range(30):
        msg = chat_stream(messages)
        # для истории убираем пустые tool_calls, чтобы не смущать модель
        stored = {"role": "assistant", "content": msg["content"]}
        if msg["tool_calls"]:
            stored["tool_calls"] = msg["tool_calls"]
        messages.append(stored)

        if not msg["tool_calls"]:
            return
        for call in msg["tool_calls"]:
            fn = call["function"]["name"]
            args = call["function"].get("arguments", {})
            if isinstance(args, str):
                try: args = json.loads(args)
                except Exception: args = {}
            try:
                result = TOOL_FUNCS[fn](args) if fn in TOOL_FUNCS else f"Неизвестный инструмент: {fn}"
            except Exception as e:
                result = f"Ошибка инструмента {fn}: {e}"
            messages.append({"role": "tool", "name": fn, "content": str(result)})
    say("Слишком много шагов — остановился. Уточни задачу.")

def chat_once(messages):
    """Ответ модели без стрима (для веб-интерфейса)."""
    r = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL, "messages": messages, "tools": TOOLS, "stream": False,
    }, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()["message"]

# краткие человеческие подписи действий для веб-интерфейса
_ACTION_LABEL = {
    "open_url": "открываю сайт", "open_app": "запускаю программу", "send_gmail": "пишу письмо",
    "run_command": "выполняю команду", "write_file": "пишу файл", "read_file": "читаю файл",
    "list_dir": "смотрю папку", "web_search": "ищу в интернете", "fetch_url": "читаю страницу",
    "see_screen": "смотрю на экран", "save_screenshot": "делаю скриншот",
    "mouse_click": "кликаю мышью", "move_mouse": "двигаю мышь", "type_text": "печатаю",
    "press_keys": "жму клавиши", "scroll": "прокручиваю",
}

def _clean_reply(t):
    """Убрать из ответа служебный мусор модели (теги, роли, «почему-то ...»)."""
    if not t:
        return t
    t = re.sub(r"(?is)<tool_response>.*?</tool_response>", "", t)
    t = re.sub(r"(?is)<tool_call>.*?</tool_call>", "", t)
    t = re.sub(r"(?im)^\s*</?(tool_response|tool_call)>\s*$", "", t)
    t = re.sub(r"(?im)^\s*(user|assistant|system)\s*:?\s*$", "", t)
    t = re.sub(r"(?im)^\s*почему[-\s]?то\b.*$", "", t)     # навязчивое «почему-то ...»
    t = re.sub(r"(?m)^\s*[A-Za-z]+Operation:?\s*", "", t)  # «CloseOperation:» и т.п.
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t

def agent_respond(messages, max_steps=12):
    """Headless-прогон агента для веба. Возвращает (текст_ответа, список_действий)."""
    actions = []
    for _ in range(max_steps):
        msg = chat_once(messages)
        stored = {"role": "assistant", "content": msg.get("content", "")}
        calls = msg.get("tool_calls") or []
        if calls:
            stored["tool_calls"] = calls
        messages.append(stored)
        if not calls:
            return _clean_reply((msg.get("content", "") or "").strip()) or "Готово.", actions
        for call in calls:
            fn = call["function"]["name"]
            args = call["function"].get("arguments", {})
            if isinstance(args, str):
                try: args = json.loads(args)
                except Exception: args = {}
            label = _ACTION_LABEL.get(fn, fn)
            detail = args.get("url") or args.get("name") or args.get("command") \
                or args.get("query") or args.get("to") or ""
            actions.append((label + (f": {detail}" if detail else "")))
            try:
                result = TOOL_FUNCS[fn](args) if fn in TOOL_FUNCS else f"Неизвестный инструмент: {fn}"
            except Exception as e:
                result = f"Ошибка инструмента {fn}: {e}"
            messages.append({"role": "tool", "name": fn, "content": str(result)})
    return "Слишком много шагов — остановился. Уточни задачу.", actions

# ----------------------------------------------------------------------------
# Память между запусками
# ----------------------------------------------------------------------------
def load_memory():
    try:
        with open(MEMORY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def save_memory(messages):
    hist = [{"role": m["role"], "content": m.get("content", "")}
            for m in messages
            if m.get("role") in ("user", "assistant") and m.get("content")]
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist[-MEMORY_LIMIT:], f, ensure_ascii=False, indent=1)
    except Exception:
        pass

# ----------------------------------------------------------------------------
# Самоулучшение (безопасное): бот придумывает НОВЫЕ маленькие навыки-модули в
# папку skills\ (умной моделью 32b). Живой код бота НЕ меняется — навыки лишь
# добавляются и после /перезапуск становятся новыми инструментами.
# ----------------------------------------------------------------------------
SKILLS_DIR = os.path.join(BASE_DIR, "skills")          # сюда бот пишет навыки
IMPROVE_MODEL = "qwen2.5:32b-instruct"                 # умная модель для придумывания
GOAL_FILE = os.path.join(BASE_DIR, "цель.txt")         # миссия саморазвития (можно править)

DEFAULT_GOAL = (
    "Стать автономным локальным ИИ-агентом уровня Claude Code и добавлять "
    "возможности, которых нет у облачных ассистентов (работа офлайн, полный "
    "доступ к ПК, зрение, автоматизация)."
)

def _improve_goal():
    try:
        with open(GOAL_FILE, encoding="utf-8") as f:
            text = f.read().strip()
        return text or DEFAULT_GOAL
    except Exception:
        return DEFAULT_GOAL

def _log_improve(line):
    try:
        with open(IMPROVE_LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + line + "\n")
    except Exception:
        pass

def _extract_code(text):
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip()

# Контракт навыка (модуль в skills\):
#   NAME = "имя_латиницей"
#   DESCRIPTION = "что делает, по-русски"
#   PARAMS = {"path": "описание параметра", ...}   # необязательно
#   DANGEROUS = True                                # необязательно (опасные — с подтверждением)
#   def run(**kwargs) -> str  (или def run(text="") — тоже поддерживается)

# Модули стандартной библиотеки, которые считаем всегда доступными:
_STDLIB = {
    "os", "sys", "re", "io", "json", "time", "subprocess", "shutil", "datetime",
    "math", "random", "glob", "pathlib", "collections", "platform", "socket",
    "hashlib", "base64", "tempfile", "itertools", "string", "textwrap", "difflib",
    "csv", "sqlite3", "threading", "urllib", "functools", "statistics", "zipfile",
    "ctypes", "shlex", "fnmatch", "html", "uuid", "typing", "traceback", "requests",
}
# Признаки опасного навыка (нужно подтверждение в режиме «безопасный»):
_DANGER_TOKENS = ("taskkill", "shutil.rmtree", "os.remove", "os.rmdir", "os.unlink",
                  "os.system", "stop-process", ".terminate(", ".kill(", "format ",
                  "del /", "rmdir", "rd /s", "reg delete", "diskpart",
                  # перемещение/переименование файлов — тоже опасно (может раскидать файлы)
                  "shutil.move", "os.rename", "os.replace", "os.renames")

# Признаки кода, который не заработает на Windows (юникс-команды) — отклоняем сразу:
_UNIX_TOKENS = ("source ", "| grep", "|grep", " xargs", "/dev/", "#!/bin", "chmod ", "sudo ")

def _looks_unix(code):
    low = code.lower()
    return any(tok in low for tok in _UNIX_TOKENS)

def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def _kw(s):
    return set(re.findall(r"[a-zа-яё]{4,}", (s or "").lower()))

def _skill_field(code, field):
    m = re.search(field + r'\s*=\s*["\']([^"\']+)["\']', code)
    return m.group(1) if m else None

def _skill_name(code):
    n = _skill_field(code, "NAME")
    return re.sub(r"[^0-9A-Za-z_]", "", n) if n else None

def _imports_available(code):
    """Отклоняем навык, если он тянет незнакомую/неустановленную библиотеку."""
    import importlib.util
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"синтаксис (строка {e.lineno})"
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods.add(node.module.split(".")[0])
    for m in mods:
        if m in _STDLIB:
            continue
        try:
            if importlib.util.find_spec(m) is None:
                return False, f"нет библиотеки {m}"
        except Exception:
            return False, f"нет библиотеки {m}"
    return True, "ок"

def _too_similar(name, desc, existing):
    """existing: список (name, desc). True — если навык почти дублирует имеющийся."""
    nn, nk = _norm(name), _kw(desc)
    for en, ed in existing:
        if nn and nn == _norm(en):
            return True
        ek = _kw(ed)
        if nk and ek and len(nk & ek) / len(nk | ek) >= 0.5:
            return True
    return False

def load_skills():
    """Читаем навыки из skills\\. Возвращаем список словарей.
    Битые (не импортируются) переносим в skills\\_broken\\, чтобы не мешали."""
    loaded = []
    if not os.path.isdir(SKILLS_DIR):
        return loaded
    if SKILLS_DIR not in sys.path:
        sys.path.insert(0, SKILLS_DIR)
    import importlib
    broken = os.path.join(SKILLS_DIR, "_broken")
    for fn in sorted(os.listdir(SKILLS_DIR)):
        if not fn.endswith(".py") or fn.startswith("_"):
            continue
        path = os.path.join(SKILLS_DIR, fn)
        try:
            code = open(path, encoding="utf-8").read()
            mod = importlib.import_module(fn[:-3])
            importlib.reload(mod)
            name, run = getattr(mod, "NAME", None), getattr(mod, "run", None)
            if not (name and callable(run)):
                continue
            dangerous = bool(getattr(mod, "DANGEROUS", False)) or \
                any(tok in code.lower() for tok in _DANGER_TOKENS)
            loaded.append({
                "name": name,
                "desc": getattr(mod, "DESCRIPTION", "навык"),
                "run": run,
                "params": getattr(mod, "PARAMS", None),
                "dangerous": dangerous,
                "file": fn,
            })
        except Exception as e:
            # битый навык — в карантин, чтобы не спамил ошибками каждый раз
            try:
                os.makedirs(broken, exist_ok=True)
                os.replace(path, os.path.join(broken, fn))
                info(f"  навык {fn} битый ({e}) — убрал в _broken\\")
            except Exception:
                info(f"  навык {fn} не загрузился: {e}")
    return loaded

def _run_skill(entry, a):
    a = a or {}
    if entry["dangerous"] and not allowed(f"навык «{entry['name']}»"):
        return "Босс отменил навык."
    run = entry["run"]
    for attempt in (lambda: run(**a), lambda: run(text=a.get("text", "")), lambda: run()):
        try:
            return str(attempt())
        except TypeError:
            continue
        except Exception as e:
            return f"Ошибка навыка {entry['name']}: {e}"
    return f"Навык {entry['name']}: параметры не подошли."

def register_skills():
    """Подключаем навыки как инструменты модели (с их параметрами и защитой)."""
    existing = {t["function"]["name"] for t in TOOLS}
    n = 0
    for entry in load_skills():
        name = entry["name"]
        if name in existing:
            continue
        params = entry["params"] if isinstance(entry["params"], dict) else {"text": "входной текст"}
        props = {k: {"type": "string", "description": str(v)} for k, v in params.items()}
        desc = entry["desc"] + (" [ОПАСНЫЙ]" if entry["dangerous"] else "")
        TOOL_FUNCS[name] = (lambda a, _e=entry: _run_skill(_e, a))
        TOOLS.append(_fn(name, desc, props))
        existing.add(name)
        n += 1
    return n

def _validate_skill(code, existing):
    """Строгая проверка навыка перед сохранением (качество важнее количества)."""
    if "def run(" not in code or "NAME" not in code:
        return False, "нет NAME или run()"
    if len(code) > 12000:
        return False, "слишком длинный"
    ok, why = _imports_available(code)   # включает проверку синтаксиса
    if not ok:
        return False, why
    if _looks_unix(code):
        return False, "юникс-команды (не работают на Windows)"
    name = _skill_name(code) or ""
    desc = _skill_field(code, "DESCRIPTION") or ""
    if not name:
        return False, "нет корректного NAME"
    if _too_similar(name, desc, existing):
        return False, "дубликат существующего"
    return True, "ок"

# Пример-образец в промпте — задаёт модели правильный стиль и контракт:
_SKILL_EXAMPLE = '''NAME = "grep_text"
DESCRIPTION = "Ищет строки по шаблону в файлах папки (как grep)."
PARAMS = {"pattern": "что искать", "path": "папка (по умолчанию текущая)"}
def run(pattern="", path="."):
    import os, re
    if not pattern:
        return "Укажи, что искать."
    hits = []
    for root, _, files in os.walk(path or "."):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                for i, line in enumerate(open(fp, encoding="utf-8", errors="ignore"), 1):
                    if re.search(pattern, line):
                        hits.append(f"{fp}:{i}: {line.strip()[:200]}")
            except Exception:
                pass
            if len(hits) >= 100:
                return "\\n".join(hits) + "\\n... (обрезано)"
    return "\\n".join(hits) if hits else "Ничего не найдено."'''

def propose_skill(existing):
    """Умная модель придумывает НОВЫЙ навык. existing: список (name, desc).
    Возвращаем (описание, код|None, причина)."""
    model = IMPROVE_MODEL if has_model(IMPROVE_MODEL) else MODEL
    have = "\n".join(f"- {n}: {d}" for n, d in existing) or "(пока ничего)"
    prompt = [
        {"role": "system", "content":
         f"ЦЕЛЬ РАЗВИТИЯ БОТА: {_improve_goal()}\n\n"
         "Ты придумываешь ОДИН новый навык (модуль Python), который приближает бота к цели "
         "и НЕ дублирует уже имеющиеся. Думай о качестве, а не количестве.\n\n"
         "Формат ответа: СНАЧАЛА строка 'НАВЫК: <что умеет, одним предложением>', затем "
         "модуль в блоке ```python ...``` строго по контракту:\n"
         'NAME = "короткое_имя_латиницей"\n'
         'DESCRIPTION = "что делает, по-русски"\n'
         'PARAMS = {"имя_параметра": "пояснение"}   # если нужны параметры\n'
         'DANGEROUS = True   # только если навык что-то удаляет/убивает процессы/меняет систему\n'
         "def run(<параметры со значениями по умолчанию>):\n    ...\n    return \"результат строкой\"\n\n"
         "Требования к качеству:\n"
         "- используй ТОЛЬКО стандартную библиотеку Python или requests (никаких сторонних вроде graphviz, psutil, pandas);\n"
         "- навык должен быть законченным, обрабатывать пустой ввод и ошибки (try/except);\n"
         "- возвращай осмысленную строку-результат;\n"
         "- НЕ повторяй темы уже имеющихся навыков (git, diff, venv, пакеты и т.п. если они уже есть);\n"
         "- бери НОВУЮ полезную область.\n\n"
         "Пример хорошего навыка:\n```python\n" + _SKILL_EXAMPLE + "\n```"},
        {"role": "user", "content":
         f"Уже есть навыки:\n{have}\n\nПридумай ОДИН НОВЫЙ навык из ДРУГОЙ области, "
         "которого ещё нет. Соблюдай контракт и требования качества."},
    ]
    r = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": model, "messages": prompt, "stream": False,
        "options": {"num_ctx": 8192, "temperature": 0.8},
    }, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    reply = r.json()["message"]["content"]
    nm = re.search(r"НАВЫК:\s*(.+)", reply)
    desc = nm.group(1).strip() if nm else "новый навык"
    code = _extract_code(reply)
    ok, why = _validate_skill(code, existing)
    return desc, (code if ok else None), why

def _existing_pairs():
    return [(e["name"], e["desc"]) for e in load_skills()]

# --- Темы (чтобы не плодить 12 «отчётов») и лимит на тему ---
THEME_CAP = 6          # максимум навыков на одну ТЕМУ (кроме «other» — тот не ограничен)
_THEMES = [
    ("git",      r"git|коммит|diff|репозитор"),
    ("backup",   r"backup|бэкап|резерв|архив|archive|version|верси|копи"),
    ("network",  r"network|сет[еиь]|wifi|порт|port|соединени|подключени|трансмиш|torrent|transmission"),
    ("schedule", r"schedul|расписан|задач|task|cron|планировщ"),
    ("process",  r"process|процесс|kill|service|сервис"),
    ("window",   r"window|окн|дисплей|display|яркост|brightness|разрешени"),
    ("system",   r"system|систем|cpu|gpu|memory|памят|диск|disk|ресурс|обновлени|update|программ|установлен"),
    ("note",     r"note|заметк|sticky|clipboard|буфер"),
    ("venv",     r"venv|pip|пакет|package|окружени|environment|переменн"),
    ("file",     r"файл|file|папк|folder|директор|rename|переименов|sort|group|integrity|пиксел|screenshot|снимок"),
    ("text",     r"текст|text|строк|content|содержим|grep|поиск|search|replace|замен"),
]

def _theme(name, desc):
    s = (str(name) + " " + str(desc)).lower()
    for label, pat in _THEMES:
        if re.search(pat, s):
            return label
    return "other"

def _theme_counts(entries):
    c = {}
    for e in entries:
        t = _theme(e["name"], e["desc"])
        c[t] = c.get(t, 0) + 1
    return c

def commit_skill(desc, code):
    """Сохранить навык, если тема не переполнена (проверки только статические —
    НИЧЕГО не выполняем, чтобы сгенерённый код не мог навредить). (принят, заметка)."""
    entries = load_skills()
    name = _skill_name(code) or f"skill_{int(time.time())}"
    th = _theme(name, desc)
    cap = 999 if th == "other" else THEME_CAP   # «прочее» не ограничиваем — туда падает всё новое
    if _theme_counts(entries).get(th, 0) >= cap:
        return False, f"тема «{th}» уже заполнена"
    path = os.path.join(SKILLS_DIR, f"skill_{name}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    _log_improve(f"НАВЫК {name} [{th}]: {desc}")
    return True, name

def self_improve_loop():
    """Интерактивно: пока не «стоп», придумываем новые качественные навыки в skills\\."""
    os.makedirs(SKILLS_DIR, exist_ok=True)
    model = IMPROVE_MODEL if has_model(IMPROVE_MODEL) else MODEL
    stop = threading.Event()
    def listener():
        while not stop.is_set():
            try:
                line = sys.stdin.readline()
            except Exception:
                break
            if line.strip().lower() in ("стоп", "stop", "/стоп", "/stop"):
                print(f"{C.YELLOW}  ...приму «стоп» после текущего шага...{C.RESET}")
                stop.set(); return
    threading.Thread(target=listener, daemon=True).start()

    say(f"Самоулучшение запущено (модель {model}). Придумываю НОВЫЕ навыки в skills\\ "
        "(проверяю запуском, без дублей и без перекоса по темам). Пиши «стоп».")
    if model.startswith("qwen2.5:32b"):
        info("  (32b умнее, но медленнее — шаг может идти минуту-другую)")
    made = 0; step = 0; skips = 0
    MAX_SKIPS = 8    # столько пропусков подряд = идеи кончились, стоп
    while not stop.is_set():
        step += 1
        info(f"  шаг {step}: придумываю навык...")
        try:
            desc, code, why = propose_skill(_existing_pairs())
        except Exception as e:
            info(f"  шаг {step}: ошибка ({e}) — пробую дальше")
            time.sleep(2); continue
        note = why
        ok = False
        if code:
            ok, note = commit_skill(desc, code)
        if ok:
            made += 1; skips = 0
            print(f"{C.GREEN}  ✓ шаг {step}: {note} — {desc}{C.RESET}")
        else:
            skips += 1
            print(f"{C.DIM}  ✗ шаг {step}: {desc} — пропустил ({note}){C.RESET}")
            if skips >= MAX_SKIPS:
                say("Похоже, новых полезных идей в рамках текущих тем не осталось "
                    "(много пропусков подряд). Останавливаюсь сам. Чтобы копать дальше — "
                    "поменяй/расширь цель.txt.")
                break
    say(f"Остановился. Новых навыков: {made} (шагов: {step}). Список — /навыки. "
        "Заработают после /перезапуск.")

def run_improve_unattended(max_new=20, minutes=120):
    """Фоновая генерация без участия человека: до max_new навыков или minutes минут.
    Остановить досрочно — создать файл skills\\_stop. Прогресс — в улучшения.log."""
    os.makedirs(SKILLS_DIR, exist_ok=True)
    stop_file = os.path.join(SKILLS_DIR, "_stop")
    deadline = time.time() + minutes * 60
    model = IMPROVE_MODEL if has_model(IMPROVE_MODEL) else MODEL
    _log_improve(f"=== ФОНОВАЯ ГЕНЕРАЦИЯ старт (модель {model}, цель {max_new} навыков / {minutes} мин) ===")
    made = 0; step = 0; skips = 0
    MAX_SKIPS = 10
    while made < max_new and time.time() < deadline:
        if os.path.exists(stop_file):
            _log_improve("остановлено файлом _stop")
            break
        step += 1
        try:
            desc, code, why = propose_skill(_existing_pairs())
        except Exception as e:
            _log_improve(f"шаг {step}: ошибка {e}")
            time.sleep(3); continue
        note = why; ok = False
        if code:
            ok, note = commit_skill(desc, code)
        if ok:
            made += 1; skips = 0
            _log_improve(f"[{made}/{max_new}] шаг {step}: {note} — {desc}")
        else:
            skips += 1
            _log_improve(f"шаг {step}: пропуск — {note}")
            if skips >= MAX_SKIPS:
                _log_improve("идеи кончились (много пропусков подряд) — авто-стоп")
                break
    _log_improve(f"=== ФОНОВАЯ ГЕНЕРАЦИЯ конец: новых навыков {made}, шагов {step} ===")
    return made

def cleanup_skills(theme_cap=4, verbose=True):
    """Разовая чистка: оставить только рабочие, непохожие навыки, с лимитом по темам.
    Остальное — в _archive_generated. Возвращает (оставлено, убрано)."""
    if not os.path.isdir(SKILLS_DIR):
        return 0, 0
    archive = os.path.join(SKILLS_DIR, "_archive_generated")
    os.makedirs(archive, exist_ok=True)
    foundation = {"git_status", "git_log", "git_diff", "find_files", "grep_text",
                  "disk_usage", "system_info", "list_processes", "kill_process", "backup_folder"}
    files = [f for f in os.listdir(SKILLS_DIR) if f.endswith(".py") and not f.startswith("_")]
    files.sort(key=lambda f: (0 if f[6:-3] in foundation else 1, f))  # базовые первыми
    kept_pairs = []
    theme_n = {}
    kept = removed = 0
    for f in files:
        path = os.path.join(SKILLS_DIR, f)
        try:
            code = open(path, encoding="utf-8").read()
        except Exception:
            continue
        name = _skill_name(code) or f[6:-3]
        desc = _skill_field(code, "DESCRIPTION") or ""
        reason = None
        ok, why = _validate_skill(code, kept_pairs)   # синтаксис + библиотеки + юникс + дубль
        th = _theme(name, desc)
        if not ok:
            reason = why
        elif theme_n.get(th, 0) >= theme_cap:
            reason = f"тема «{th}» заполнена"
        if reason:
            os.replace(path, os.path.join(archive, f))
            removed += 1
            if verbose:
                print(f"  ✗ убрал {name}: {reason}")
        else:
            kept_pairs.append((name, desc))
            theme_n[th] = theme_n.get(th, 0) + 1
            kept += 1
            if verbose:
                print(f"  ✓ оставил {name} [{th}]")
    if verbose:
        print(f"\nИтог: оставлено {kept}, убрано {removed}.")
    return kept, removed

def list_skills_cmd():
    sk = load_skills()
    if not sk:
        say("Навыков пока нет. Скажи «улучшай себя» — придумаю новые."); return
    print(f"{C.CYAN}Навыки бота (skills\\):{C.RESET}")
    for i, e in enumerate(sk, 1):
        mark = f" {C.RED}[опасный]{C.RESET}" if e["dangerous"] else ""
        print(f"  {i}. {e['name']} — {e['desc']}{mark}")

# ----------------------------------------------------------------------------
# Стартовый экран
# ----------------------------------------------------------------------------
BANNER = r"""
  ╔════════════════════════════════════════════════════╗
  ║                М О Й   Б О Т   🤖                    ║
  ║        личный ИИ-агент • работает на твоём ПК        ║
  ╚════════════════════════════════════════════════════╝"""

def startup_screen():
    global MODE
    try:
        os.system("cls")
    except Exception:
        pass
    print(f"{C.CYAN}{C.BOLD}{BANNER}{C.RESET}")
    print(f"""{C.DIM}  Я умею:
   • писать код, работать с файлами, запускать команды
   • искать в интернете и отвечать на вопросы (погода, факты)
   • ВИДЕТЬ экран, делать скриншоты, кликать и печатать сам
   • открывать сайты/программы, писать письма, вводить пароли из хранилища
   • находить на диске мусор, придумывать себе новые навыки{C.RESET}
{C.CYAN}  Примеры:{C.RESET}{C.DIM} «какая погода в Москве», «открой ютуб»,
   «найди что можно удалить», «посмотри на экран и нажми Играть»{C.RESET}""")
    while True:
        print(f"\n{C.BOLD}  Меню:{C.RESET}   {C.DIM}режим: {MODE} | мозг: {MODEL}{C.RESET}")
        print(f"   1. Начать разговор")
        print(f"   2. Сменить режим (безопасный/авто)")
        print(f"   3. Сменить модель-мозг")
        print(f"   4. Помощь")
        raw = input(f"{C.YELLOW}  Выбор (Enter — начать): {C.RESET}").strip()
        sel = raw.lower()
        if sel in ("", "1", "начать"):
            break
        elif sel == "2":
            MODE = "авто" if MODE == "безопасный" else "безопасный"
            say(f"Режим теперь «{MODE}».")
        elif sel == "3":
            choose_model()
        elif sel == "4":
            print(HELP)
        else:
            # не пункт меню — это уже задача/команда: уходим в чат и выполним её
            print(f"{C.GREEN}  Поехали!{C.RESET}")
            return raw
    print(f"{C.GREEN}  Поехали! Пиши задачу или /помощь.{C.RESET}")
    return ""

# ----------------------------------------------------------------------------
# Служебное
# ----------------------------------------------------------------------------
def check_ollama():
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).raise_for_status()
        return True
    except Exception:
        return False

def start_ollama():
    """Пробуем запустить Ollama, если она не отвечает."""
    os.environ.setdefault("OLLAMA_MODELS", r"D:\Ollama\models")
    candidates = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Ollama\ollama app.exe"),
    ]
    exe = next((p for p in candidates if os.path.exists(p)), None)
    flags = getattr(subprocess, "DETACHED_PROCESS", 0)
    try:
        if exe:
            subprocess.Popen([exe], creationflags=flags, close_fds=True)
        else:
            import shutil
            o = shutil.which("ollama")
            if not o:
                return False
            subprocess.Popen([o, "serve"], creationflags=flags, close_fds=True)
        return True
    except Exception:
        return False

def ensure_ollama():
    """Гарантируем, что Ollama работает: запускаем и ждём до 30 сек."""
    if check_ollama():
        return True
    info("Ollama не запущена — запускаю сам...")
    if not start_ollama():
        return False
    for _ in range(30):
        time.sleep(1)
        if check_ollama():
            info("Ollama запущена.")
            return True
    return False

def has_model(name):
    try:
        tags = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).json()["models"]
        return any(t["name"] == name for t in tags)
    except Exception:
        return False

def choose_model():
    global MODEL
    try:
        names = [t["name"] for t in requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).json()["models"]]
    except Exception:
        names = [MODEL]
    print(f"{C.CYAN}Модели:{C.RESET}")
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n}" + (" (текущая)" if n == MODEL else ""))
    pick = input("Номер (Enter — оставить): ").strip()
    if pick.isdigit() and 1 <= int(pick) <= len(names):
        MODEL = names[int(pick) - 1]
        say(f"Теперь думаю моделью {MODEL}.")

def restart():
    say("Перезапускаюсь...")
    time.sleep(0.5)
    os.execl(sys.executable, sys.executable, SELF_PATH)

HELP = """Команды:
  /выход      — закрыть
  /режим      — безопасный (спрашивает) / авто (делает сам)
  /модель     — сменить мозг
  /экран      — описать, что на экране
  /очистить   — очистить текущий диалог
  /забыть     — стереть память прошлых разговоров
  /улучшай    — режим самоулучшения: придумывает новые навыки (пиши «стоп»)
  /навыки     — список наработанных навыков
  /перезапуск — перезапустить бота (подхватить новые навыки)
  /помощь     — справка
Пиши задачу — выполню. «улучшай себя» — начну улучшаться, «стоп» — остановлюсь."""

def wants_self_improve(low):
    """Распознаём просьбу «улучшай себя» терпимо к опечаткам (улудшай/улутшай и т.п.)."""
    t = low.strip()
    if t in ("/улучшай", "/improve"):
        return True
    # стем «улу..ша» ловит улучшай / улудшай / улутшай / улучшайся
    if re.search(r"улу\w{0,3}ша", t):
        return True
    # «улучши/улучшить себя» — только когда речь про СЕБЯ (не «улучши поиск в файле»)
    if ("себя" in t or "сам" in t) and re.search(r"улу\w{0,2}ш", t):
        return True
    if any(w in t for w in ("прокачай себя", "развивай себя", "пиши себя", "создавай навыки", "придумывай навыки")):
        return True
    return False

def main():
    global MODE
    if not ensure_ollama():
        print(f"{C.RED}Не удалось запустить Ollama. Запусти приложение Ollama вручную.{C.RESET}")
        sys.exit(1)

    first_task = startup_screen()

    if not has_model(VISION_MODEL):
        info(f"⚠ Модель зрения {VISION_MODEL} не установлена — «зрение» не будет работать.")

    nsk = register_skills()
    if nsk:
        info(f"Подключено навыков: {nsk} (список — /навыки).")

    messages = [{"role": "system", "content": system_prompt()}]
    prior = load_memory()
    if prior:
        messages += prior
        info(f"Помню прошлые разговоры ({len(prior)} сообщений). /забыть — очистить память.")

    while True:
        if first_task:                       # задача, введённая прямо в стартовом меню
            user = first_task.strip()
            first_task = None
            print(f"\n{C.YELLOW}{C.BOLD}Ты:{C.RESET} {user}")
        else:
            try:
                user = input(f"\n{C.YELLOW}{C.BOLD}Ты:{C.RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                print(); break
        if not user:
            continue
        low = user.lower()

        if low in ("/выход", "/exit", "/quit"):
            break
        if low in ("/помощь", "/help"):
            print(HELP); continue
        if low in ("/модель", "/model"):
            choose_model(); messages[0] = {"role": "system", "content": system_prompt()}; continue
        if low.startswith("/режим"):
            arg = low.replace("/режим", "").replace("/mode", "").strip()
            if arg in ("авто", "auto"):
                MODE = "авто"
            elif arg in ("безопасный", "safe"):
                MODE = "безопасный"
            else:
                MODE = "авто" if MODE == "безопасный" else "безопасный"
            messages[0] = {"role": "system", "content": system_prompt()}
            say(f"Режим: {MODE}." + (" Действую без вопросов!" if MODE == "авто" else " Опасное — с подтверждением.")); continue
        if low in ("/экран", "/screen"):
            print(f"{C.DIM}  ...смотрю на экран...{C.RESET}")
            say(tool_see_screen()); continue
        if low in ("/очистить", "/clear"):
            messages = [{"role": "system", "content": system_prompt()}]
            say("Память текущего диалога очищена."); continue
        if low in ("/забыть", "/forget"):
            messages = [{"role": "system", "content": system_prompt()}]
            try:
                if os.path.exists(MEMORY_FILE):
                    os.remove(MEMORY_FILE)
            except Exception:
                pass
            say("Забыл все прошлые разговоры."); continue
        if low in ("/перезапуск", "/restart"):
            save_memory(messages); restart(); continue
        if wants_self_improve(low):
            self_improve_loop(); continue
        if low in ("/навыки", "/skills"):
            list_skills_cmd(); continue

        messages.append({"role": "user", "content": user})
        try:
            print(f"{C.DIM}  ...думаю...{C.RESET}")
            run_agent(messages)
            save_memory(messages)           # помним разговор между запусками
        except requests.exceptions.RequestException as e:
            print(f"{C.RED}Ошибка связи с Ollama: {e}{C.RESET}")
        except Exception as e:
            print(f"{C.RED}Ошибка: {e}{C.RESET}")

    save_memory(messages)
    say("Пока, босс!")

if __name__ == "__main__":
    main()
