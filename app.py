import streamlit as st
import os
import base64
from groq import Groq
import config
import database as db
import styles

# 1. Инициализация базы данных
db.init_db()

# 2. Настройка страницы
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="centered"
)

# Применяем стили и JS (фикс для мобильных и дизайн)
st.markdown(f"<style>{styles.get_css()}</style>", unsafe_allow_html=True)
st.markdown(styles.PWA_JS, unsafe_allow_html=True)

# 3. Управление сессией (Авторизация)
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ФУНКЦИЯ ВХОДА ---
def login_screen():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.title("⚡ Jarvis AI")
    auth_tab1, auth_tab2 = st.tabs(["Вход", "Регистрация"])
    
    with auth_tab1:
        u = st.text_input("Логин", key="l_user")
        p = st.text_input("Пароль", type="password", key="l_pass")
        if st.button("Войти", use_container_width=True):
            user = db.verify_user(u, p)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Неверный логин или пароль")
                
    with auth_tab2:
        nu = st.text_input("Придумайте логин", key="r_user")
        np = st.text_input("Придумайте пароль", type="password", key="r_pass")
        if st.button("Создать аккаунт", use_container_width=True):
            if db.create_user(nu, np):
                st.success("Аккаунт создан! Теперь войдите.")
            else:
                st.error("Этот логин уже занят")
    st.markdown('</div>', unsafe_allow_html=True)

# Если не залогинен — показываем вход и стопаем код
if not st.session_state.user:
    login_screen()
    st.stop()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ДЖАРВИСА ---
user_id = st.session_state.user["id"]
username = st.session_state.user["username"]

# Загружаем историю из БД, если сессия пуста
if not st.session_state.messages:
    history = db.get_history(user_id, limit=config.MAX_CONTEXT)
    st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in reversed(history)]

# Боковая панель
with st.sidebar:
    st.title(f"Привет, {username}!")
    if st.button("Очистить историю"):
        db.clear_history(user_id)
        st.session_state.messages = []
        st.rerun()
    if st.button("Выйти"):
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

# Отображение чата
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ввод сообщения
if prompt := st.chat_input(config.PLACEHOLDER):
    # Добавляем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})
    db.add_message(user_id, "user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерация ответа через Groq
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Используем ключ из переменных окружения (Render Environment)
            client = Groq(api_key=config.GROQ_API_KEY)
            
            # Собираем контекст: системный промпт + последние сообщения
            messages_for_api = [{"role": "system", "content": config.SYSTEM_PROMPT}] + \
                               st.session_state.messages[-config.MAX_CONTEXT:]

            stream = client.chat.completions.create(
                model=config.TEXT_MODEL,
                messages=messages_for_api,
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Сохраняем ответ ассистента
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            db.add_message(user_id, "assistant", full_response)
            
        except Exception as e:
            st.error(f"Ошибка API: {str(e)}")
