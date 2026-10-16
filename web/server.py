# -*- coding: utf-8 -*-
"""
Веб-интерфейс МойБота: чат с историей, голос, просмотр экрана, скриншоты.
Запуск: python web/server.py
"""
import os
import io
import sys
import json
import time
import base64
import uuid

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import bot

from flask import Flask, request, jsonify, Response, send_file, session, redirect

bot.HEADLESS = True
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
CHATS_FILE = os.path.join(WEB_DIR, "chats.json")
CONFIG_FILE = os.path.join(WEB_DIR, "config.json")
TAILSCALE_IP = "100.73.252.82"

# ——— Пароль хранится в отдельном файле config.json (не в коде) ———
def _load_config():
    cfg = {"password": "bossbot"}
    try:
        cfg.update(json.load(open(CONFIG_FILE, encoding="utf-8")))
    except Exception:
        json.dump(cfg, open(CONFIG_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return cfg

CONFIG = _load_config()
PASSWORD = CONFIG.get("password", "bossbot")
bot.VAULT_MASTER = PASSWORD    # тот же пароль открывает хранилище аккаунтов

app = Flask(__name__)
app.secret_key = CONFIG.get("secret") or os.urandom(16).hex()
if not CONFIG.get("secret"):
    CONFIG["secret"] = app.secret_key
    try:
        json.dump(CONFIG, open(CONFIG_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception:
        pass

# ——— Защита от перебора пароля (анти-взлом) ———
_fails = {}
def _blocked(ip):
    r = _fails.get(ip)
    return bool(r and r[1] > time.time())
def _fail(ip):
    r = _fails.get(ip, [0, 0])
    r[0] += 1
    if r[0] >= 5:
        r[1] = time.time() + 900        # блок на 15 минут
        r[0] = 0
    _fails[ip] = r

_LOGIN_PAGE = """<!doctype html><html lang=ru><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Вход — МойБот</title></head>
<body style="margin:0;height:100vh;display:flex;align-items:center;justify-content:center;
background:#0f1115;color:#e7e9ee;font-family:Segoe UI,system-ui,Arial">
<form method=post style="background:#171a21;border:1px solid #2a2f3a;border-radius:16px;
padding:28px;width:300px;text-align:center">
  <div style="font-size:40px">🤖</div>
  <div style="font-weight:700;font-size:20px;margin:8px 0 4px">Мой<span style=color:#7c5cff>Бот</span></div>
  <div style="color:#9aa3b2;font-size:13px;margin-bottom:16px">Введите пароль</div>
  <input type=password name=password autofocus placeholder=Пароль
   style="width:100%;padding:13px;border-radius:12px;border:1px solid #2a2f3a;
   background:#1e222b;color:#e7e9ee;font-size:16px;margin-bottom:12px">
  <button type=submit style="width:100%;padding:13px;border:none;border-radius:12px;
   background:#7c5cff;color:#fff;font-size:16px;font-weight:600">Войти</button>
  __ERR__
</form></body></html>"""

@app.route("/login", methods=["GET", "POST"])
def login():
    ip = request.remote_addr or "?"
    err = ""
    if request.method == "POST":
        if _blocked(ip):
            err = "Слишком много попыток. Подожди 15 минут."
        elif request.form.get("password", "") == PASSWORD:
            session["auth"] = True
            session.permanent = True
            return redirect("/")
        else:
            _fail(ip); err = "Неверный пароль."
    html = _LOGIN_PAGE.replace("__ERR__",
        f'<div style="color:#e74c3c;font-size:13px;margin-top:12px">{err}</div>' if err else "")
    return Response(html, mimetype="text/html")

@app.before_request
def _require_auth():
    if request.path in ("/login", "/icon.png", "/manifest.json"):
        return
    if not session.get("auth"):
        if request.path.startswith("/api/"):
            return Response("Не авторизован", 401)
        return redirect("/login")

# ——— Хранилище чатов ———
# chats[id] = {"title": str, "messages": [ {role, content}... ] (полная история для модели) }
chats = {}
current_id = None

def _sys_msg():
    return {"role": "system", "content": bot.system_prompt()}

def _save():
    try:
        json.dump({"chats": chats, "current": current_id},
                  open(CHATS_FILE, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception:
        pass

def _load():
    global chats, current_id
    try:
        d = json.load(open(CHATS_FILE, encoding="utf-8"))
        chats = d.get("chats", {})
        current_id = d.get("current")
    except Exception:
        chats, current_id = {}, None

def _new_chat():
    global current_id
    cid = uuid.uuid4().hex[:8]
    chats[cid] = {"title": "Новый чат", "messages": [_sys_msg()]}
    current_id = cid
    _save()
    return cid

def _ensure_current():
    global current_id
    if not current_id or current_id not in chats:
        _new_chat()

def _display(cid):
    """Сообщения для показа (только ты/бот с текстом)."""
    out = []
    for m in chats.get(cid, {}).get("messages", []):
        if m.get("role") in ("user", "assistant") and m.get("content"):
            out.append({"role": m["role"], "content": m["content"]})
    return out

@app.route("/")
def index():
    return send_file(os.path.join(WEB_DIR, "index.html"))

@app.route("/icon.png")
def icon():
    return send_file(os.path.join(WEB_DIR, "icon.png"))

@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "МойБот", "short_name": "МойБот",
        "start_url": "/", "display": "standalone",
        "background_color": "#0f1115", "theme_color": "#7c5cff",
        "icons": [{"src": "/icon.png", "sizes": "512x512", "type": "image/png"}],
    })

@app.route("/api/chats")
def list_chats():
    _ensure_current()
    items = [{"id": k, "title": v.get("title", "Чат")} for k, v in chats.items()]
    items.reverse()
    return jsonify({"chats": items, "current": current_id, "messages": _display(current_id)})

@app.route("/api/chats/new", methods=["POST"])
def new_chat():
    cid = _new_chat()
    return jsonify({"id": cid, "messages": []})

@app.route("/api/chats/select", methods=["POST"])
def select_chat():
    global current_id
    cid = (request.json or {}).get("id")
    if cid in chats:
        current_id = cid
        _save()
    return jsonify({"messages": _display(current_id), "current": current_id})

@app.route("/api/chats/delete", methods=["POST"])
def delete_chat():
    global current_id
    cid = (request.json or {}).get("id")
    if cid in chats:
        del chats[cid]
        if current_id == cid:
            current_id = next(iter(chats), None)
            if not current_id:
                _new_chat()
        _save()
    return jsonify({"ok": True, "current": current_id})

@app.route("/api/chat", methods=["POST"])
def chat():
    _ensure_current()
    text = (request.json or {}).get("message", "").strip()
    if not text:
        return jsonify({"reply": "", "actions": []})
    conv = chats[current_id]
    conv["messages"].append({"role": "user", "content": text})
    if conv["title"] == "Новый чат":
        conv["title"] = text[:40]
    try:
        reply, actions = bot.agent_respond(conv["messages"])
    except Exception as e:
        reply, actions = f"Ошибка: {e}", []
    _save()
    return jsonify({"reply": reply or "(готово)", "actions": actions})

@app.route("/api/monitors")
def monitors():
    try:
        import mss
        with mss.mss() as sct:
            return jsonify({"count": max(1, len(sct.monitors) - 1)})   # без [0] «все вместе»
    except Exception:
        return jsonify({"count": 1})

@app.route("/api/screen")
def screen():
    try:
        import mss
        from PIL import Image
        try:
            n = int(request.args.get("mon", 1))
        except Exception:
            n = 1
        with mss.mss() as sct:
            mons = sct.monitors
            idx = n if 0 <= n < len(mons) else (1 if len(mons) > 1 else 0)
            shot = sct.grab(mons[idx])
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        w = 2048                       # выше разрешение — чётче текст (плюс зум щипком)
        if img.width > w:
            img = img.resize((w, int(img.height * w / img.width)))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        return Response(buf.getvalue(), mimetype="image/jpeg")
    except Exception as e:
        return Response(f"screen error: {e}", status=500)

@app.route("/api/vision", methods=["POST"])
def vision():
    data = request.json or {}
    img_b64 = data.get("image", "")
    question = data.get("question") or "Что на этом изображении? Опиши по-русски."
    if "," in img_b64:
        img_b64 = img_b64.split(",", 1)[1]
    try:
        png = base64.b64decode(img_b64)
        return jsonify({"reply": bot.ask_vision(png, question)})
    except Exception as e:
        return jsonify({"reply": f"Ошибка разбора изображения: {e}"})

def _boot():
    if not bot.check_ollama():
        bot.ensure_ollama()
    try:
        bot.register_skills()
    except Exception:
        pass
    _load()
    _ensure_current()

def _open_browser_when_ready(host):
    import time, webbrowser, urllib.request
    url = f"http://{host}:5000/"
    for _ in range(60):
        try:
            urllib.request.urlopen(url, timeout=1)
            webbrowser.open(url)
            return
        except Exception:
            time.sleep(0.5)

LOG_FILE = os.path.join(WEB_DIR, "last_run.log")
def _log(msg):
    line = time.strftime("%H:%M:%S ") + str(msg)
    print(line)
    try:
        open(LOG_FILE, "a", encoding="utf-8").write(line + "\n")
    except Exception:
        pass

if __name__ == "__main__":
    try:
        open(LOG_FILE, "w", encoding="utf-8").write("")   # очистить лог
    except Exception:
        pass
    try:
        _log("=== запуск веб-сервера ===")
        _log("подготовка (Ollama, навыки, чаты)...")
        _boot()
        _log("подготовка ок")
        host = "127.0.0.1"     # локально; наружу отдаёт Tailscale HTTPS (безопасно)
        import threading
        threading.Thread(target=_open_browser_when_ready, args=(host,), daemon=True).start()
        _log("=" * 40)
        _log(f"МойБот-веб ЗАПУЩЕН. Пароль: {PASSWORD}")
        _log(f"На ЭТОМ ПК:  http://127.0.0.1:5000")
        _log(f"С ТЕЛЕФОНА:  https://vova.tail46eef4.ts.net  (Tailscale вкл, микрофон работает)")
        _log("Не закрывай это окно, пока пользуешься.")
        _log("=" * 40)
        app.run(host=host, port=5000, threaded=True)
    except Exception as e:
        import traceback
        _log("!!! ОШИБКА ЗАПУСКА: " + repr(e))
        _log(traceback.format_exc())
        print("\nЧто-то пошло не так — покажи боту файл web\\last_run.log")
        input("Нажми Enter, чтобы закрыть...")
