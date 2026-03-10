from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_db():
    print("Loading PDF... this may take a moment.")
    loader = PyPDFLoader("android-14-cdd.pdf")
    documents = loader.load()
    
    # Using Recursive splitter is better for technical manuals
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents)
    
    print(f"Split into {len(docs)} chunks. Creating index...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_android_cdd")
    print("--- SUCCESS: Compliance Knowledge Base Created! ---")

if __name__ == "__main__":
    create_vector_db()