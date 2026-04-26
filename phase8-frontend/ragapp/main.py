from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embedder = SentenceTransformer("all-MiniLM-L6-v2")
db_client = chromadb.Client()
collection = db_client.create_collection("docs")

with open("profile.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

embeddings = embedder.encode(lines).tolist()
collection.add(
    documents=lines,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(lines))]
)

ollama_client = ollama.Client(
    host=os.environ.get("OLLAMA_HOST", "http://localhost:11434")
)

@app.get("/ask")
def ask(q: str):
    query_embedding = embedder.encode([q]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    retrieved = "\n".join(results["documents"][0])

    response = ollama_client.chat(
        model="qwen2.5:1.5b",
        messages=[
            {"role": "system", "content": "You must answer in Japanese only. Never use English. 必ず日本語のみで答えてください。以下のドキュメントに書かれていることだけを元に答えてください。\n" + retrieved},
            {"role": "user", "content": q}
        ]
    )
    return {"answer": response["message"]["content"]}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
