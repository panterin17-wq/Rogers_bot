from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

# CARGAR VARIABLES
load_dotenv()

# INICIAR FASTAPI
app = FastAPI()

# VARIABLES
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
COMET_API_KEY = os.getenv("COMET_API_KEY")
COMET_URL = os.getenv("COMET_URL")

# API TELEGRAM
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# RUTA PRINCIPAL
@app.get("/")
def home():
    return {"status": "Bot funcionando correctamente"}

# WEBHOOK TELEGRAM
@app.post("/webhook")
async def webhook(request: Request):

    # RECIBE DATOS TELEGRAM
    data = await request.json()

    print("MENSAJE RECIBIDO:")
    print(data)

    try:

        # MENSAJE
        message = data["message"]["text"]

        # CHAT ID
        chat_id = data["message"]["chat"]["id"]

        print("MENSAJE USUARIO:")
        print(message)

        # ENVÍA MENSAJE A COMET
        comet_response = requests.post(
            COMET_URL,
            headers={
                "Authorization": f"Bearer {COMET_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
        )

        # RESPUESTA COMET
        print("STATUS COMET:")
        print(comet_response.status_code)

        print("RESPUESTA COMET:")
        print(comet_response.text)

        # CONVIERTE RESPUESTA JSON
        comet_data = comet_response.json()

        # EXTRAE TEXTO
        reply = comet_data["choices"][0]["message"]["content"]

        # ENVÍA RESPUESTA A TELEGRAM
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

        return {"ok": True}

    except Exception as e:

        print("ERROR:")
        print(str(e))

        return {"error": str(e)}
