from pypdf import PdfReader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectordb = Chroma(
    embedding_function=embeddings,
    persist_directory="./kafka_chroma"
)
lc_semantic_chunker = SemanticChunker(
    embeddings=embeddings)
Work = ["the hunger artist", "A-country-doctor-by-Franz-Kafka", "AN_IMPERIAL_MESSAGE", 
     "Before the law", "in-the-penal-colony", 
     "Jackals and Arabs", "Metamorphosis", 
     "oceanofpdf.com_letters_to_milena_-_franz_kafka", "The Trial - Franz Kafka"]
personal=["oceanofpdf.com_letters_to_milena_-_franz_kafka",'letters-to-felice','Kafka_life','max interview','Dearest Father','the-diaries_text','Kafkaesque']

def add_to_db(docs,author,source,typ):
    for i in docs:
        reader = PdfReader(f"data for RAG/{i}.pdf")
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        # قراءة الـ PDF وتجميع النص ...
        
        # تقسيم أولي آمن
        initial_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,       # ~400–600 توكن، آمن
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", "!", "?", " ", ""]
        )
        initial_chunks = initial_splitter.split_text(text)
        
        # الآن طبق SemanticChunker على كل جزء
        all_semantic_chunks = []
        
        for init_chunk in initial_chunks:
            semantic_chunks = lc_semantic_chunker.create_documents([init_chunk])
            all_semantic_chunks.extend(semantic_chunks)
        
        # أضف metadata
        for j, doc in enumerate(all_semantic_chunks):
            doc.metadata = {
                "author": author,
                "source": source,
                "type": typ,
                "work": i,
                "chunk_id": j,
                "original_file": i + ".pdf"
            }
        
        # أضف واحد واحد عشان أمان إضافي
        for doc in all_semantic_chunks:
            vectordb.add_documents([doc])
        print("Finished processing:", i, "Total chunks added:", len(all_semantic_chunks))
    print(f"Total documents: {vectordb._collection.count()}")
add_to_db(personal,"Franz Kafka","Personal Papers","Personal")