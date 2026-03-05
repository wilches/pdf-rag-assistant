from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

import os
from pathlib import Path

load_dotenv()

# 1. Embeddings (same model we have been using)
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Load the database
vector_store = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings_model
)

# 3. LLM response
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3 #less creativity, more precision
)
# 4. Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k":1})

# 5. Personalized propmt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Use the following context to answer the question.
    If you don't know the answer, say you don't know.

    Context: {context}"""),
    ("human", "Question: {input}")
])
# 6. Full RAG chain
combine_docs_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

# 7. Ask
pregunta = "What is the main contribution of this paper?"
print(f"Pregunta: {pregunta}")
print(f"\nRespuesta:")
respuesta = retrieval_chain.invoke({"input": pregunta})
print(respuesta["answer"])
