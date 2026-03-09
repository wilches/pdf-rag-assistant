from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
import json
import os

load_dotenv()

# ─────────────────────────────────────────────────────
# MODELOS DE DATOS
# Definen la estructura exacta que esperamos del LLM
# ─────────────────────────────────────────────────────

class ClauseRisk(BaseModel):
    """Representa el análisis de riesgo de una cláusula"""
    clause_title: str = Field(description="Título o número de la cláusula")
    clause_text: str = Field(description="Texto relevante de la cláusula")
    risk_level: Literal["HIGH", "MEDIUM", "LOW"] = Field(description="Nivel de riesgo")
    reason: str = Field(description="Por qué esta cláusula es riesgosa")
    recommendation: str = Field(description="Qué hacer al respecto")

class ContractAnalysis(BaseModel):
    """Análisis completo del contrato"""
    summary: str = Field(description="Resumen ejecutivo del contrato en 2-3 oraciones")
    contract_type: str = Field (description="Tipo de contrato (servicios, laboral, etc)")
    overall_risk: Literal["HIGH", "MEDIUM", "LOW"] = Field(description="Riesgo general")
    clauses: list[ClauseRisk] = Field(description="Lista de cláusulas analizadas")
    general_recommendation: str = Field(description="Recomendación general antes de firmar")

# ─────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# ─────────────────────────────────────────────────────

def analyze_contract() -> dict:
    """
    Recupera el contrato de ChromaDB y lo analiza
    Devuelve un diccionario con el análisis estructurado
    """

    # 1. Carga el modelo de embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 2. Conecta con ChromaDB y trae TODOS los chunks
    vector_store = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings_model
    )

    # Traemos mas chunks para tener más contexto del contrato
    # k=15 porque necesitamos leer la mayor parte del documento
    retriever = vector_store.as_retriever(search_kwargs={"k":15})

    # Buscamos con una query general para traer las partes más importantes
    docs = retriever.invoke("clauses obligations penalties termination payment risk")

    # 3. Une todos los chunksen un solo texto
    full_context = "\n\n".join([doc.page_content for doc in docs])

    # 4. El LLM con structured output
    # Esto le dice al LLM que debe responder en formato JSON
    # siguiendo exactamente la estructura de ContractAnalysis
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1  # muy bajo para análisis preciso
    )

    #with_structured_output le dice al LLM:
    #"responde EXACTAMENTE con esta estructura JSON"
    structured_llm = llm.with_structured_output(ContractAnalysis)

    # 5. El prompt de análisis
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert contract lawyer with 20 years of experience.
        Analyze the following contract text and identify risky clauses.

        Focus on:
        - Penalty clauses and their limits
        - Termination conditions
        - Payment obligations
        - Liability and indemnification
        - Intellectual property ownership
        - Confidentiality obligations
        - Automatic renewal clauses

        Be specific about WHY each clause is risky and WHAT to do about it.
        If the text seems to not be a contract, set overall_risk as LOW
        and explain in the summary."""),
        ("human", "Contract text:\n\n{context}")
    ])

    # 6. Ejecuta el análisis
    chain = prompt | structured_llm
    result = chain.invoke({"context":full_context})

    # 7. Convierte a diccionario y devuelve
    return result.model_dump()

# Test directo
if __name__ == "__main__":
    print("Analizando contrato...")
    result = analyze_contract()
    print(json.dumps(result, indent=2, ensure_ascii=False))
