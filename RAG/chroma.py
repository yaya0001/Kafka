from pypdf import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="nomic-embed-text")

def load_db():
    vectordb = Chroma(
        persist_directory="C:/Users/DPQUAI250130/lang_env/Scripts/RAG/kafka_chroma",
        embedding_function=embeddings
    )
    print("DB is ready.")
    return vectordb
