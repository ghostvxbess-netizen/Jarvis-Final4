import os
from dotenv import load_dotenv

load_dotenv()

# API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Модели
TEXT_MODEL = "llama-3.3-70b-versatile"
MAX_CONTEXT = 20
MAX_TOKENS = 1500
TEMPERATURE = 0.7

# БД
DATABASE_URL = os.getenv("DATABASE_URL") # Для Postgres на Render
SQLITE_PATH = "jarvis.db"
SESSION_DAYS = 30

# Интерфейс
APP_TITLE = "Jarvis AI"
APP_ICON = "⚡"
PLACEHOLDER = "Спросите Джарвиса..."
SYSTEM_PROMPT = "Ты — Джарвис, продвинутый ИИ-ассистент. Отвечай кратко, по делу и с легким юмором."
