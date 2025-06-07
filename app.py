from flask import Flask, request, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
import requests

app = Flask(__name__)

ELEVENLABS_API_KEY = "sk_d3c35b933d0aa0dfa71039d8f46f85059619d878b1383911"
VOICE_ID = "BNtaKAuLDg6H6vma7qm3"

def generar_audio(texto):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "sk_d3c35b933d0aa0dfa71039d8f46f85059619d878b1383911"
    }
    data = {
        "text": texto,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=data)
    with open("respuesta.mp3", "wb") as f:
        f.write(response.content)
    return "respuesta.mp3"

@app.route("/webhook", methods=['POST'])
def voice_webhook():
    # Captura lo que diga la persona que llama (puede variar según cómo configures Twilio)
    speech = request.form.get("SpeechResult", "No entendí lo que dijiste.")

    # Mensaje que responde tu asistente (puedes personalizarlo)
    texto_respuesta = f"Hola. Gracias por llamar. Tú dijiste: {speech}. ¿En qué más te puedo ayudar?"

    # Genera el audio con ElevenLabs
    generar_audio(texto_respuesta)

    # Prepara la respuesta de Twilio
    response = VoiceResponse()
    response.play(request.url_root + "respuesta.mp3")
    return Response(str(response), mimetype='text/xml')

# Ruta para servir el archivo de audio a Twilio
@app.route("/respuesta.mp3")
def serve_audio():
    return send_from_directory('.', 'respuesta.mp3')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
