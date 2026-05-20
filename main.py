from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
COMET_API_KEY = os.getenv("COMET_API_KEY")
COMET_URL = os.getenv("COMET_URL")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.get("/")
def home():
    return {"status": "Bot funcionando"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        # ENVÍA MENSAJE A COMET
        comet_response = requests.post(
            COMET_URL,
            headers={
                "Authorization": f"Bearer {COMET_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "message": message
            }
        )

        comet_data = comet_response.json()

        # RESPUESTA DE COMET
        reply = comet_data.get("response", "Sin respuesta de Comet")

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
        return {"error": str(e)}
