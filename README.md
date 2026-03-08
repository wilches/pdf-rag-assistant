# 📄 PDF RAG Assistant

Chat with your PDF documents using RAG (Retrieval Augmented Generation).

## 🛠️ Tech Stack
- **LLM:** Google Gemini 1.5 Flash
- **Embeddings:** Google Gemini Embeddings
- **Vector DB:** ChromaDB
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Orchestration:** LangChain

## 🏗️ Architecture
PDF → Chunks → Embeddings → ChromaDB
Question → Embedding → ChromaDB Search → Gemini → Answer

## 🚀 Run locally

### 1. Clone the repo
git clone https://github.com/tuusuario/pdf-rag-assistant

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up environment variables
Create a .env file:
GOOGLE_API_KEY=your_api_key_here

### 5. Run the API
uvicorn api:app --reload

### 6. Run the frontend
streamlit run frontend.py

## 📁 Project Structure
pdf-rag-assistant/

├── indexer.py      # PDF processing and ChromaDB indexing

├── query.py        # RAG query pipeline

├── api.py          # FastAPI REST endpoints

├── frontend.py     # Streamlit UI

├── data/           # PDF uploads

└── .env            # API keys (not in repo)
