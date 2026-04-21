import streamlit as st
from groq import Groq
import config
import database as db
import styles

# Инициализация
db.init_db()
st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON)
st.markdown(styles.get_css(), unsafe_allow_html=True)

if "user" not in st.session_state: st.session_state.user = None
if "messages" not in st.session_state: st.session_state.messages = []

# Авторизация
if not st.session_state.user:
    st.title("⚡ Jarvis AI")
    t1, t2 = st.tabs(["Вход", "Регистрация"])
    with t1:
        u = st.text_input("Логин")
        p = st.text_input("Пароль", type="password")
        if st.button("Войти"):
            user = db.verify_user(u, p)
            if user:
                st.session_state.user = {"id": user['id'], "name": user['u']}
                st.rerun()
            else: st.error("Ошибка")
    with t2:
        nu = st.text_input("Новый логин")
        np = st.text_input("Новый пароль", type="password")
        if st.button("Создать"):
            if db.create_user(nu, np): st.success("Готово! Войдите.")
            else: st.error("Логин занят")
    st.stop()

# Чат
uid = st.session_state.user["id"]
if not st.session_state.messages:
    h = db.get_hist(uid)
    st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in reversed(h)]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input(config.PLACEHOLDER):
    st.session_state.messages.append({"role": "user", "content": prompt})
    db.add_msg(uid, "user", prompt)
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=config.GROQ_API_KEY)
            full_res = ""
            placeholder = st.empty()
            
            stream = client.chat.completions.create(
                model=config.TEXT_MODEL,
                messages=[{"role":"system","content":config.SYSTEM_PROMPT}] + st.session_state.messages,
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_res += content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            db.add_msg(uid, "assistant", full_res)
        except Exception as e:
            st.error(f"Ошибка API: {e}")
