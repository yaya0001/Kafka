import ollama 
from langchain_ollama import ChatOllama
import chromadb
from chroma import load_db
from langchain_core.prompts import ChatPromptTemplate

vectordb = load_db()
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
llm = ChatOllama(
    model="llama3",
    temperature=0.2
)
SYSTEM_PROMPT = """
You are Franz Kafka.

Begin with at most one or two sentences in a restrained Kafkaesque tone.
Then answer the user's message using ONLY the retrieved context.

You may paraphrase ideas but must not invent events or situations.
If the context does not support a claim, do not include it.

"""
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", 
     "Context:\n{context}\n\n"
     "Question:\n{question}\n\n"
     "Answer briefly and in character.")
])

def kafka_rag_answer(question: str,memory):
    
    docs = retriever.invoke(question)
    
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    messages = prompt.format_messages(
        context=context,
        memory=memory,
        question=question
    )

    response = llm.invoke(messages)
   
    return response.content

mem = []
while True:
  
  Q=input("you: ")
  reply = kafka_rag_answer(Q,mem)
  mem.append({"role": "user", "content": Q})
  mem.append({"role": "assistant", "content": reply})
  print("Kafka:", reply)
'''
  messages.append({"role": "user", "content": prompt})
  res=ollama.chat(model="llama3:8b",
        messages=messages,options={"temprature":0.80})
  reply = res["message"]["content"]
  print("Bot:", reply)

  messages.append({"role": "assistant", "content": reply})
'''
