from flask import Flask, request, jsonify
import requests
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# === OpenAI con Assistants v2 ===
# Nota clave: agregamos default_headers={"OpenAI-Beta": "assistants=v2"}
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
if not ASSISTANT_ID:
    raise RuntimeError("Falta OPENAI_ASSISTANT_ID en el .env")

# Diccionario: thread por usuario
user_threads = {}  # dict[user_phone] = thread_id

def _get_or_create_thread(user_phone: str) -> str:
    """Crea un thread para el usuario si no existe; retorna thread_id."""
    thread_id = user_threads.get(user_phone)
    if thread_id:
        return thread_id
    thread = client.beta.threads.create()
    user_threads[user_phone] = thread.id
    logger.info(f"Thread creado para {user_phone}: {thread.id}")
    return thread.id

def _append_user_message(thread_id: str, content: str):
    """Adjunta el mensaje del usuario al thread."""
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def _run_assistant(thread_id: str):
    """Inicia un Run del assistant en el thread."""
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
        # instructions="(opcional) Instrucciones dinámicas por mensaje"
    )

def _wait_run_completion(thread_id: str, run_id: str, timeout_seconds: int = 14) -> str:
    """
    Espera a que el Run termine (polling). Devuelve el texto de la última respuesta del asistente.
    timeout_seconds ~14s para ajustarnos al tiempo típico de Twilio (≈15s).
    """
    terminal = {"completed", "failed", "cancelled", "expired", "requires_action"}
    start = time.time()

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status in terminal:
            break
        if (time.time() - start) > timeout_seconds:
            logger.warning(f"Timeout esperando run {run_id} (status={run.status})")
            return ""
        time.sleep(0.4)

    if run.status != "completed":
        logger.error(f"Run no completado. status={run.status}")
        return ""

    # Obtener la última respuesta del asistente
    msgs = client.beta.threads.messages.list(thread_id=thread_id, order="desc", limit=8)
    for m in msgs.data:
        if m.role == "assistant":
            parts = []
            for c in m.content:
                if getattr(c, "type", None) == "text":
                    t = getattr(c, "text", None)
                    if t and getattr(t, "value", None):
                        parts.append(t.value)
            text = "\n".join(parts).strip()
            if text:
                return text
    return ""

def get_chatgpt_response(user_message, user_phone):
    """Obtener respuesta usando el Assistant (assistant_id) con hilos por usuario."""
    try:
        logger.info(f"Procesando mensaje para {user_phone}: {user_message}")

        # 1) Thread por usuario
        thread_id = _get_or_create_thread(user_phone)

        # 2) Agregar mensaje del usuario
        _append_user_message(thread_id, user_message)

        # 3) Ejecutar Run
        run = _run_assistant(thread_id)

        # 4) Esperar resultado con timeout corto
        answer = _wait_run_completion(thread_id, run.id, timeout_seconds=14)

        if not answer:
            return "Estoy procesando tu mensaje. ¿Podrías intentarlo de nuevo en un momento?"

        logger.info(f"Respuesta del asistente para {user_phone}: {answer[:200]}")
        return answer

    except Exception as e:
        logger.exception(f"Error al procesar mensaje con Assistant: {str(e)}")
        return "Lo siento, hubo un error procesando tu mensaje. Inténtalo de nuevo."

@app.route('/bot', methods=['POST'])
def bot():
    logger.info("=== NUEVO MENSAJE RECIBIDO ===")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Form data: {dict(request.form)}")

    incoming_msg = request.values.get('Body', '')
    user_phone = request.values.get('From', 'unknown_user')

    logger.info(f"Mensaje de {user_phone}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    logger.info("Usando Assistant (assistants=v2) para responder")
    chatgpt_response = get_chatgpt_response(incoming_msg, user_phone)
    msg.body(chatgpt_response)

    response_xml = str(resp)
    logger.info(f"Respuesta enviada: {response_xml}")
    return response_xml

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY no está configurada en el archivo .env")
        exit(1)
    if not os.getenv('OPENAI_ASSISTANT_ID'):
        print("❌ Error: OPENAI_ASSISTANT_ID no está configurada en el archivo .env")
        exit(1)

    print("🤖 Bot iniciado con Assistant de OpenAI (v2)")
    print("📱 Endpoint: /bot")
    app.run(debug=True, host='0.0.0.0', port=5000)