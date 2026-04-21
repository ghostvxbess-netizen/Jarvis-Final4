import streamlit as st
import os
from groq import Groq

# 1. Сначала настройки страницы (обязательно первой строкой!)
st.set_page_config(page_title="Jarvis AI", page_icon="⚡")

# 2. Проверка ключа (если его нет, мы увидим текст, а не белый экран)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ ОШИБКА: GROQ_API_KEY не найден в настройках Render!")
    st.info("Зайдите в Render -> Environment и добавьте переменную GROQ_API_KEY")
    st.stop()

# 3. Минимальные стили прямо здесь (чтобы не зависеть от других файлов)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    </style>
""", unsafe_allow_html=True)

# 4. Инициализация чата
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ Jarvis AI")

# Отображение истории
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Ввод сообщения
if prompt := st.chat_input("Спроси Джарвиса..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=api_key)
            placeholder = st.empty()
            full_res = ""
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True
            )
            
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_res += content
                    placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"Ошибка API: {e}")
