import streamlit as st
from groq import Groq
import config
import database as db
import styles

db.init_db()

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON)
st.markdown(styles.get_css(), unsafe_allow_html=True)
st.markdown(styles.PWA_JS, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def login():
    st.title("⚡ Jarvis System")
    menu = ["Вход", "Регистрация"]
    choice = st.tabs(menu)
    
    with choice[0]:
        u = st.text_input("Логин")
        p = st.text_input("Пароль", type='password')
        if st.button("Войти"):
            user = db.verify_user(u, p)
            if user:
                st.session_state.user = user
                st.rerun()
            else: st.error("Ошибка входа")
            
    with choice[1]:
        nu = st.text_input("Новый логин")
        np = st.text_input("Новый пароль", type='password')
        if st.button("Создать аккаунт"):
            if db.create_user(nu, np): st.success("Аккаунт создан!")
            else: st.error("Логин занят")

if not st.session_state.user:
    login()
    st.stop()

# Основной чат
user_id = st.session_state.user["id"]
if not st.session_state.messages:
    hist = db.get_history(user_id)
    st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in reversed(hist)]

with st.sidebar:
    st.write(f"Пользователь: **{st.session_state.user['username']}**")
    if st.button("Выйти"):
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input(config.PLACEHOLDER):
    st.session_state.messages.append({"role": "user", "content": prompt})
    db.add_message(user_id, "user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=config.GROQ_API_KEY)
            res_area = st.empty()
            full_res = ""
            
            stream = client.chat.completions.create(
                model=config.TEXT_MODEL,
                messages=[{"role": "system", "content": config.SYSTEM_PROMPT}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_res += content
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            db.add_message(user_id, "assistant", full_res)
        except Exception as e:
            st.error(f"Ошибка API: {e}")
