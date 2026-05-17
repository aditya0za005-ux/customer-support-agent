# rag.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

print("LOADING RAG...")

with open("data/faq.txt", "r", encoding="utf-8") as f:

    faq_text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = splitter.split_documents([
    Document(page_content=faq_text)
])

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = FAISS.from_documents(
    docs,
    embedding_model
)

print("RAG READY")


def search_docs(query):

    print("SEARCHING FAQ")

    results = vectorstore.similarity_search(
        query,
        k=3
    )

    return [
        doc.page_content
        for doc in results
    ]