# 🤖 Bot Simple con ChatGPT Assistant

Un bot de WhatsApp simple que integra tu asistente personalizado de ChatGPT para respuestas inteligentes, basado en tu código original.

## 🚀 Características

- **Estructura Simple**: Basada en tu código original
- **ChatGPT Assistant**: Usa tu asistente personalizado configurado
- **Conversaciones Persistentes**: Mantiene el contexto de cada usuario
- **Comandos Especiales**: Mantiene las funciones de quotes y cat pics
- **Fácil Configuración**: Solo necesitas tu API key y Assistant ID

## 📋 Prerrequisitos

- Python 3.8 o superior
- Cuenta de OpenAI con API key
- Asistente de OpenAI configurado
- **Opcional**: Cuenta de Twilio con WhatsApp habilitado

## 🛠️ Instalación

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno**
   Crea un archivo `.env` con:
   ```env
   OPENAI_API_KEY=tu_openai_api_key_aqui
   OPENAI_ASSISTANT_ID=tu_assistant_id_aqui
   FLASK_ENV=development
   ```

## 🚀 Ejecución

```bash
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

## 📡 Endpoints

### Bot Webhook
- **URL**: `/bot`
- **Método**: `POST`
- **Descripción**: Recibe mensajes y responde con tu asistente

### Health Check
- **URL**: `/health`
- **Método**: `GET`
- **Descripción**: Verifica que el bot esté funcionando

## 🎯 Funcionalidades

### Comandos Especiales
- **"quote"** - Devuelve una cita famosa aleatoria
- **"cat"** - Devuelve una imagen de gato aleatoria

### ChatGPT Assistant
- **Cualquier otro mensaje** - Responde usando tu asistente personalizado
- **Conversaciones persistentes** - Cada usuario mantiene su contexto

## 📱 Configuración con Twilio (Opcional)

Si quieres usar con WhatsApp:

1. **Configurar webhook en Twilio**
   - URL: `https://tu-dominio.ngrok.io/bot`
   - Método: `POST`

2. **Usar ngrok para desarrollo local**
   ```bash
   ngrok http 5000
   ```

## 🔧 Personalización

### Tu Asistente Personalizado
El bot usa tu asistente configurado en `OPENAI_ASSISTANT_ID`. Puedes personalizar:
- Instrucciones del asistente
- Herramientas y funciones
- Modelo de IA
- Comportamiento específico

### Agregar más comandos especiales
En la función `bot()`, agrega más condiciones:
```python
if 'tu_comando' in incoming_msg:
    # Tu lógica aquí
    msg.body('Tu respuesta')
    responded = True
```

## 🐛 Solución de Problemas

### Error: "OPENAI_API_KEY no está configurada"
- Verifica que el archivo `.env` existe
- Asegúrate de que `OPENAI_API_KEY` esté configurada correctamente

### Error: "OPENAI_ASSISTANT_ID no está configurado"
- Verifica que `OPENAI_ASSISTANT_ID` esté en tu archivo `.env`
- Asegúrate de que el ID del asistente sea correcto

### Error: "Error al procesar mensaje con ChatGPT"
- Verifica que tu API key sea válida
- Revisa que tengas créditos en tu cuenta de OpenAI
- Verifica que tu asistente esté configurado correctamente

## 📊 Estructura del Proyecto

```
Quici/
├── app.py              # Bot principal con asistente
├── requirements.txt    # Dependencias
├── .env               # Variables de entorno (crear manualmente)
└── README.md          # Esta documentación
```

## 🎉 ¡Listo!

Tu bot ahora:
- ✅ Mantiene la estructura simple de tu código original
- ✅ Usa tu asistente personalizado de ChatGPT
- ✅ Mantiene conversaciones persistentes por usuario
- ✅ Conserva los comandos especiales (quote, cat)
- ✅ Solo necesita tu API key y Assistant ID

¡Disfruta usando tu bot con tu asistente personalizado! 🚀