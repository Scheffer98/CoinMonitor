from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

def buscar_cotacao_periodicamente():
    while True:
        try:
            response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
            data = response.json()
            dolar = data["USDBRL"]["bid"]
            print(f"Cotação do dólar: R$ {dolar}")
            # Aqui você pode incluir envio via Telegram, salvar em banco, etc.
        except Exception as e:
            print("Erro ao buscar cotação:", e)
        time.sleep(60 * 5)  # Executa a cada 5 minutos

@app.route('/')
def home():
    return "Bot de cotação rodando!"

if __name__ == "__main__":
    thread = threading.Thread(target=buscar_cotacao_periodicamente)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=8000)
