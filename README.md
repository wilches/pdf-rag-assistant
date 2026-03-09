# ⚖️ Contract Risk Analyzer

Aplicación web con IA que analiza contratos legales, identifica cláusulas riesgosas y genera recomendaciones usando RAG (Retrieval Augmented Generation).

🔗 **Demo:** [contract-risk-analyzer.streamlit.app](https://pdf-rag-assistant-5ewrmktvkhu8y3zygkwc9j.streamlit.app/)

---

## 🎯 El Problema

Todos hemos firmado contratos sin leerlos completamente. Un contrato de 40 páginas puede esconder:

- Cláusulas de penalización sin límite
- Condiciones de terminación abusivas
- Renovaciones automáticas no deseadas

**Esta app lee el contrato por ti y te dice qué negociar.**

---

## ✨ Funcionalidades

- 📄 **Carga de PDF** — Sube cualquier contrato en PDF
- 🔍 **Análisis automático** — Detecta y clasifica cláusulas riesgosas
- 🚦 **Clasificación de riesgo** — ALTO 🔴 / MEDIO 🟡 / BAJO 🟢
- 💡 **Recomendaciones** — Te dice exactamente qué negociar
- 💬 **Chat con el contrato** — Haz preguntas específicas

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | Google Gemini Embeddings |
| Vector DB | ChromaDB |
| Orquestación | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deploy API | Render |
| Deploy UI | Streamlit Cloud |
---

## 📁 Estructura del Proyecto

    contract-risk-analyzer/
    ├── analyzer.py      # Pipeline de análisis RAG
    ├── indexer.py       # Procesamiento de PDFs
    ├── query.py         # Pipeline de consultas
    ├── api.py           # Endpoints FastAPI
    ├── frontend.py      # Interfaz Streamlit
    ├── data/            # PDFs (gitignored)
    └── .env             # API keys (gitignored)

---

## 🚀 Correr Localmente

**1. Clona el repositorio**

    git clone https://github.com/tuusuario/pdf-rag-assistant.git
    cd pdf-rag-assistant

**2. Crea el entorno virtual**

    python -m venv venv
    venv\Scripts\activate

**3. Instala dependencias**

    pip install -r requirements.txt

**4. Configura variables de entorno**

Crea un archivo `.env`:

    GOOGLE_API_KEY=tu_api_key_aqui

**5. Corre la API**

    uvicorn api:app --reload

**6. Corre el frontend**

    streamlit run frontend.py

---

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/` | Health check |
| POST | `/upload` | Subir e indexar PDF |
| POST | `/analyze` | Analizar riesgos |
| POST | `/ask` | Preguntar sobre el contrato |
---

## ⚠️ Limitaciones

- Funciona mejor con PDFs de texto, no escaneados
- El análisis es generado por IA y no reemplaza asesoría legal
- El free tier puede tener demoras de inicio (~30 segundos)

---

## 📬 Contacto

**Juan Camilo Herrera Wilches**
- GitHub: [@wilches](https://github.com/wilches)
- LinkedIn: [Juan Wilches](https://www.linkedin.com/in/juan-wilches/)
