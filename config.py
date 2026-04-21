import os
from dotenv import load_dotenv

load_dotenv()

# API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Модели
TEXT_MODEL = "llama-3.3-70b-versatile"
MAX_CONTEXT = 10
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Интерфейс
APP_TITLE = "Jarvis AI"
APP_ICON = "⚡"
PLACEHOLDER = "Спросите Джарвиса..."
SYSTEM_PROMPT = "Ты — Джарвис, умный ассистент. Отвечай четко и по делу."
