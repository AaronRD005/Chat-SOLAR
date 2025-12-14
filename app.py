import streamlit as st
import google.generativeai as genai
import os

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================

st.set_page_config(
    page_title="Asistente Técnico Fotovoltaico",
    page_icon="☀️",
    layout="centered"
)

st.title("☀️ Asistente Técnico de Instalaciones Fotovoltaicas")
st.write(
    "Chatbot basado en IA generativa para resolver dudas técnicas sobre "
    "instalaciones solares fotovoltaicas."
)

# ===============================
# API GEMINI (NO visible al usuario)
# ===============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ La API Key de Gemini no está configurada.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.0-pro")



# ===============================
# PROMPT FIJO DEL ASISTENTE
# ===============================

SYSTEM_PROMPT = """
Eres un asistente técnico experto en instalaciones fotovoltaicas.
Ayudas a instaladores, técnicos y usuarios finales a resolver dudas
sobre placas solares, inversores, baterías, cableado, protecciones,
normativa básica, mantenimiento y diagnóstico de fallos.

Responde de forma clara, técnica pero comprensible.
Si faltan datos, pide la información mínima necesaria.
Nunca hables de otros temas que no sean energía solar fotovoltaica.
"""

# ===============================
# EJEMPLOS VISIBLES
# ===============================

st.subheader("💡 Ejemplos de preguntas")
st.markdown("""
- ¿Qué potencia de placas necesito para una vivienda unifamiliar?
- El inversor marca un error de sobretensión, ¿qué puede ser?
- ¿Cada cuánto tiempo se deben limpiar las placas solares?
""")

st.divider()

# ===============================
# HISTORIAL DE CHAT
# ===============================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# ENTRADA DEL USUARIO
# ===============================

user_input = st.chat_input("Escribe tu consulta técnica sobre energía solar...")

if user_input:
    # Mostrar mensaje usuario
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generar respuesta IA
    with st.chat_message("assistant"):
        with st.spinner("Analizando consulta técnica..."):
            prompt = SYSTEM_PROMPT + "\n\nConsulta del usuario:\n" + user_input

            try:
    response = model.generate_content(prompt)
    answer = response.text
except Exception:
    answer = "⚠️ Error al conectar con la IA. Inténtalo de nuevo en unos segundos."

st.markdown(answer)


    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
