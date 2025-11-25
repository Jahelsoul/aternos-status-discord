import os
import json
import requests

# Configurações
ATERNOS_SERVER = os.getenv("ATERNOS_SERVER")  # ex: "meuserver"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
STATUS_FILE = "last_status.json"

STATUS_URL = f"https://api.mcsrvstat.us/2/{ATERNOS_SERVER}.aternos.me"


def get_last_status():
    if not os.path.exists(STATUS_FILE):
        return None
    with open(STATUS_FILE, "r") as f:
        return json.load(f).get("online")


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump({"online": status}, f)


def send_discord_message(text):
    data = {"content": text}
    r = requests.post(DISCORD_WEBHOOK_URL, json=data)
    r.raise_for_status()


def main():
    if not ATERNOS_SERVER:
        raise RuntimeError("Variável ATERNOS_SERVER não definida")

    if not DISCORD_WEBHOOK_URL:
        raise RuntimeError("Variável DISCORD_WEBHOOK_URL não definida")

    # pega status atual
    r = requests.get(STATUS_URL)
    r.raise_for_status()
    data = r.json()
    online = data.get("online", False)

    last = get_last_status()

    # se nunca rodou, só salva sem notificar
    if last is None:
        save_status(online)
        return

    # se mudou, manda mensagem
    if online != last:
        status_txt = "🟢 **online**" if online else "🔴 **offline**"
        msg = f"Servidor `{ATERNOS_SERVER}` agora está {status_txt}."
        send_discord_message(msg)
        save_status(online)


if __name__ == "__main__":
    main()
