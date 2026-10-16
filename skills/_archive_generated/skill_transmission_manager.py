NAME = "transmission_manager"
DESCRIPTION = "Управляет загрузкой файлов через торрент-клиент Transmission: добавляет, удаляет и показывает список загрузок."
PARAMS = {"action": "действие (add, remove, list)", "torrent_file": "путь к торрент-файлу (для добавления)"}
DANGEROUS = True  # Удаление загрузок может быть опасным

def run(action="list", torrent_file=""):
    import json
    import requests
    import os

    # Настройки для Transmission
    TRANSMISSION_URL = "http://localhost:9091/transmission/rpc"
    USERNAME = "mybot"
    PASSWORD = "securepassword"

    headers = {"x-transmission-session-id": ""}

    def _get_session_id():
        response = requests.get(TRANSMISSION_URL, auth=(USERNAME, PASSWORD))
        if "X-Transmission-Session-Id" in response.headers:
            return response.headers["X-Transmission-Session-Id"]
        else:
            return ""

    def _transmission_request(method, arguments=None):
        if not arguments:
            arguments = {}
        session_id = _get_session_id()
        headers["x-transmission-session-id"] = session_id
        data = {
            "method": method,
            "arguments": arguments,
            "tag": 1
        }
        response = requests.post(TRANSMISSION_URL, headers=headers, auth=(USERNAME, PASSWORD), json=data)
        return response.json()

    if action == "add":
        if not torrent_file or not os.path.exists(torrent_file):
            return "Укажи путь к торрент-файлу."
        with open(torrent_file, 'rb') as f:
            torrent_data = f.read()
        return str(_transmission_request("torrent-add", {"metainfo": torrent_data}))

    elif action == "remove":
        if not torrent_file:
            return "Укажи идентификатор загрузки для удаления."
        return str(_transmission_request("torrent-remove", {"ids": [int(torrent_file)]}))

    elif action == "list":
        response = _transmission_request("torrent-get")
        return "\n".join([f"{torrent['id']}: {torrent['name']} ({torrent['percentDone'] * 100:.2f}%)" for torrent in response['arguments']['torrents']])
    else:
        return "Неизвестное действие. Используй add, remove или list."