import os
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

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

query = "趣味は何ですか"
query_embedding = embedder.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

retrieved = "\n".join(results["documents"][0])
print("取得したドキュメント:", retrieved)

ollama_client = ollama.Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

response = ollama_client.chat(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": "必ず日本語で答えてください。以下のドキュメントに書かれていることだけを元に答えてください。ドキュメントにない情報は答えないでください。\n" + retrieved},
        {"role": "system", "content": "You must answer in Japanese only. Never use English. 必ず日本語のみで答えてください。英語は使わないでください。\n" + retrieved},
        {"role": "user", "content": query}
    ]
)

print(response["message"]["content"])
