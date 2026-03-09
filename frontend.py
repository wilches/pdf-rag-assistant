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
    page_title="Contract Risk Analyzer",
    page_icon="⚖️",
    layout="centered"
)

st.title("📄 PDF RAG Assistant")
st.caption("Sube un contrato y analiza sus riesgos automáticamente")

# ─────────────────────────────────────
# SECCIÓN 1: SUBIR CONTRATO
# ─────────────────────────────────────
st.header("1. Sube tu contrato")

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
# SECCIÓN 1.2: ANALIZAR CONTRATO
# ─────────────────────────────────────


# Inicializar estado si no existe
if 'analizado' not in st.session_state:
    st.session_state.analizado = False

# 2. Funcion que se ejecuta solo al hacer clic
def iniciar_analisis():
    st.session_state.analizado = True

# 3. Cambio de estado al presionar el botón
st.button("Analizar", on_click=iniciar_analisis)

# 4. Si el estado es True, ejecutamos la logica
if st.session_state.analizado:
    with st.spinner("Analizando documento..."):
        # Manda el archivo a la API
        response = requests.post(f"{API_URL}/analyze")

        if response.status_code == 200:
            st.success(f"✅ Análisis completado!")
            st.session_state["analysis"] = response.json() # guardar el análisis completo
        else:
            st.error(f"❌ Error: {response.json()['detail']}")

# ─────────────────────────────────────
# SECCIÓN 2: ANÁLISIS DE RIESGO
# ─────────────────────────────────────

st.header("2. Análisis de Riesgo")


if "analysis" in st.session_state:
    analysis = st.session_state["analysis"] #response.json()  <- donde estan todos los datos

    st.write(f"**Tipo**: {analysis['contract_type']}")
    st.write(f"**Resumen**: {analysis['summary']}")
    st.write(f"**Riesgo General**: {analysis['overall_risk']}")
    st.space("small")
    st.write(f"**Cláusulas**:")
    st.space("small")

    risk_colors = {
        "HIGH": st.error,
        "MEDIUM": st.warning, #guardando la funcion como objeto
        "LOW": st.success
    }
    risk_emojis = {
    "HIGH": "🔴",
    "MEDIUM": "🟡",
    "LOW": "🟢"
    }

    for clause in analysis["clauses"]:
        risk_level = clause["risk_level"]

        # Titutlo con color y emoji dinamico
        risk_colors[risk_level](f"{risk_emojis[risk_level]} {clause['clause_title']} - {risk_level}")

        # Detalles de la cláusula
        st.write(f"📌 **Texto:** {clause['clause_text']}")
        st.write(f"⚠️ **Razón:** {clause['reason']}")
        st.write(f"💡 **Recomendación:** {clause['recommendation']}")

        st.divider()  # separador entre cláusulas



# ─────────────────────────────────────
# SECCIÓN 3: PREGUNTALE AL CONTRATO
# ─────────────────────────────────────

st.header("3. Pregúntale al contrato")
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
