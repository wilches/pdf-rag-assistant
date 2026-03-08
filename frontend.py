import streamlit as st
import requests
import os

# URL de API para localhost
#API_URL = "http://localhost:8000"

#URL de API para deploy
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ─────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────
st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF RAG Assistant")
st.caption("Sube un PDF y hazle preguntas")

# ─────────────────────────────────────
# SECCIÓN 1: SUBIR PDF
# ─────────────────────────────────────
st.header("1. Sube tu documento")

uploaded_file = st.file_uploader(
    "Selecciona un PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    # Botón para indexar
    if st.button("Indexar PDF"):
        with st.spinner("Procesando documento..."):
            # Manda el archivo a la API
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/upload", files=files)

            if response.status_code == 200:
                st.success(f"✅ {response.json()['message']}")
                # Guarda en session_state que ya hay un PDF indexado
                st.session_state["pdf_indexed"] = True
                st.session_state["pdf_name"] = uploaded_file.name
            else:
                st.error(f"❌ Error: {response.json()['detail']}")

# ─────────────────────────────────────
# SECCIÓN 2: HACER PREGUNTAS
# ─────────────────────────────────────
st.header("2. Hazle preguntas al documento")

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Muestra el historial
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input de pregunta
question = st.chat_input("Escribe tu pregunta aquí...")

if question:
    # Muestra la pregunta del usuario
    with st.chat_message("user"):
        st.write(question)
    st.session_state["messages"].append({
        "role": "user",
        "content": question
    })

    # Llama a la API y muestra respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
                st.write(answer)
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                st.error(f"❌ Error: {response.json()['detail']}")
