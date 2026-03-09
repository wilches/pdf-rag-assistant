from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from indexer import index_pdf
from query import ask
from analyzer import analyze_contract as run_analysis

app = FastAPI(
    title="PDF RAG Assistant",
    description="Upload PDFs and ask questions about them",
    version="1.0.0"
)

# Permite que el frontend (permite conexiones desde otros dominios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # * significa "acepta de cualquier origen"
    allow_methods=["*"], # acepta GET, POST, DELETE, etc.
    allow_headers=["*"] # acepta cualquier header
)

# Modelo para la pregunta (valida que la pregunte llegue con el formato correcto)
class QuestionRequest(BaseModel):
    question: str

# ─────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "PDF RAG Assistant is running..."}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")

    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        index_pdf(file_path)
        return {
            "status": "ok",
            "message": f"{file.filename} indexado exitosamente"
        }
    except Exception as e:
        # Borra el archivo si falló
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"No se pudo leer el PDF. Asegúrate que el documento tenga texto seleccionable y no sea una imagen escaneada."
        )

@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía." )

    try:
        answer = ask(request.question)
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze():
    try:
        result = run_analysis()
        return result #devuelve el JSON con el análisis (diccionario con respuestas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
