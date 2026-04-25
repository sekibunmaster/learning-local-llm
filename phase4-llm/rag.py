import chromadb
from sentence_transformers import SentenceTransformer
import ollama

embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("docs")

# ファイルから読み込む
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

response = ollama.chat(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": "必ず日本語で答えてください。以下のドキュメントを参考に答えてください。\n" + retrieved},
        {"role": "system", "content": "必ず日本語で答えてください。以下のドキュメントに書かれていることだけを元に答えてください。ドキュメントにない情報は答えないでください。\n" + retrieved},
        {"role": "user", "content": query}
    ]
)
