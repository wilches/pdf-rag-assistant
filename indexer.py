from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

load_dotenv()

def index_pdf(pdf_path: str):
    print(f"Indexando: {pdf_path}")

    # 1. Load
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print(f"Páginas encontradas: {len(pages)}")

    # 2.Chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(pages)
    print(f"Chunks generados: {len(chunks)}")

    # 3.Embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_ley=os.getenv("GOOGLE_API_KEY")
    )

    # 4.Save on Chroma DB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory="data/chroma_db"
    )

    print(f"Indexado Exitosamente! Total chunks guardados: {vector_store._collection.count()}")
    return True

if __name__=="__main__":
    index_pdf("data/sample.pdf")
