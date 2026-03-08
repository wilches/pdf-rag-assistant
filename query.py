from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os

load_dotenv()

def get_rag_chain():
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model = "gemini-embedding-001",
        google_api_key = os.getenv("GOOGLE_API_KEY")
    )

    vector_store = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings_model
    )

    model = ChatGoogleGenerativeAI(
        model = "gemini-3-flash-preview",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )

    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Use the following context to answer the question.
        If you don't know the answer, say you don't know.
        Context: {context}"""),
        ("human", "Question: {input}")
    ])

    combine_docs_chain = create_stuff_documents_chain(model, prompt)
    return create_retrieval_chain(retriever, combine_docs_chain)

def ask(question: str) -> str:
    chain = get_rag_chain()
    respuesta = chain.invoke({"input": question})
    return respuesta["answer"]

if __name__ == "__main__":
    while True:
        pregunta = input("\nPregunta (o 'salir'): ")
        if pregunta.lower() == "salir":
            break
        print(f"\nRespuesta: {ask(pregunta)}")
