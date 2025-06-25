from flask import Flask
import threading
import time
import requests
import os

app = Flask(__name__)

# Substitua pelas suas credenciais do Telegram em variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            print("Erro ao enviar para Telegram:", r.text)
    except Exception as e:
        print("Exceção no envio para o Telegram:", e)

def buscar_cotacao_periodicamente():
    while True:
        try:
            response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
            data = response.json()
            dolar = data["USDBRL"]["bid"]
            mensagem = f"💵 Cotação atual do dólar: R$ {dolar}"
            print(mensagem)
            enviar_mensagem_telegram(mensagem)
        except Exception as e:
            print("Erro ao buscar cotação:", e)
        time.sleep(60 * 20)  # Espera 20 minutos

@app.route('/')
def home():
    return "Bot de cotação do dólar rodando com envio via Telegram."

if __name__ == "__main__":
    thread = threading.Thread(target=buscar_cotacao_periodicamente)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=8000)
