from fastapi import FastAPI
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI()
model = OllamaLLM(model="llama3.2")

# Load the Compliance Knowledge Base
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.load_local(
    "faiss_android_cdd", 
    embeddings, 
    allow_dangerous_deserialization=True
)

@app.get("/")
def home():
    return {"status": "SentinAI Online"}

@app.post("/audit")
def audit_app(data: dict):
    app_name = data.get("app_name")
    permissions = data.get("permissions")

    # RAG Search
    search_query = f"Android compliance rules for {permissions}"
    relevant_docs = vector_db.similarity_search(search_query, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
    Context: {context}
    App: {app_name}
    Permissions: {permissions}
    
    Task: Provide a security verdict based on the CDD context. 
    Cite a Section number if applicable. Answer in 2 sentences.
    """

    response = model.invoke(prompt)
    print(f"\n[AUDITING]: {app_name}")
    print(f"[VERDICT]: {response}")
    print("-" * 40)
    
    return {"verdict": str(response)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)