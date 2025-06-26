from flask import Flask
import threading
import time
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__)

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensagem_telegram(mensagem, alerta_forte=False):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    if alerta_forte:
        mensagem = (
            "🚨🚨🚨<b>ALERTA: Dólar abaixo de R$5,41!</b>\n"
            f"{mensagem}\n"
            "🔊📱 <b>Verifique agora!</b>"
        )
        parse_mode = "HTML"
    else:
        parse_mode = None

    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": parse_mode
    }

    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            print("Erro ao enviar para Telegram:", r.text)
    except Exception as e:
        print("Exceção no envio para o Telegram:", e)

def buscar_cotacao_periodicamente():
    while True:
        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        hora = agora.hour

        if 7 <= hora < 22:
            try:
                response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
                data = response.json()
                dolar = float(data["USDBRL"]["bid"])
                mensagem = f"💵 Cotação atual do dólar: R$ {dolar}"

                print(f"[{agora.strftime('%H:%M:%S')}] {mensagem}")

                if dolar < 5.41:
                    enviar_mensagem_telegram(mensagem, alerta_forte=True)
                else:
                    enviar_mensagem_telegram(mensagem)

            except Exception as e:
                print("Erro ao buscar cotação:", e)
        else:
            print(f"[{agora.strftime('%H:%M:%S')}] Fora do horário de operação (07h–22h BR).")

        time.sleep(60 * 60)  # Espera 1 hora

@app.route('/')
def home():
    return "Bot de cotação do dólar rodando com envio via Telegram."

if __name__ == "__main__":
    thread = threading.Thread(target=buscar_cotacao_periodicamente)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=8000)
