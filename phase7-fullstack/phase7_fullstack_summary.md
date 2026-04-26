# Phase 7 FastAPIのDockerコンテナ化 学習まとめ

---

## 1. Phase 7のゴール

FastAPIをDockerコンテナ化して、`docker compose up`だけで全部動く構成を作る。

```
docker compose up
    ↓
ollama（LLMサーバー）  ポート11434
ragapp（RAG + FastAPI） ポート8000
    ↓
ブラウザ・curlからアクセスできる
```

---

## 2. フォルダ構成

```
phase7-fullstack/
├─ docker-compose.yml
└─ ragapp/
    ├─ Dockerfile
    ├─ requirements.txt
    ├─ main.py
    └─ profile.txt
```

---

## 3. Dockerfile（FastAPI用）

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `--host 0.0.0.0`が必要な理由

```
--host 127.0.0.1（デフォルト）
  → コンテナ内からしかアクセスできない

--host 0.0.0.0
  → コンテナ外（ホストPC）からもアクセスできる
```

---

## 4. docker-compose.yml

```yaml
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  ragapp:
    build: ./ragapp
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama
    command: >
      sh -c "sleep 10 && uvicorn main:app --host 0.0.0.0 --port 8000"

volumes:
  ollama_data:
```

---

## 5. 操作手順

```bash
# ollamaだけ先に起動
docker compose up ollama -d

# モデルをダウンロード
docker exec phase7-fullstack-ollama-1 ollama pull qwen2.5:1.5b

# 全体を起動
docker compose up
```

---

## 6. 確認方法

```bash
# Swagger UI（ブラウザ）
http://localhost:8000/docs

# curlでAPIを叩く（日本語はURLエンコードが必要）
curl "http://localhost:8000/ask?q=%E8%B6%A3%E5%91%B3%E3%81%AF%E4%BD%95%E3%81%A7%E3%81%99%E3%81%8B"
```

---

## 7. Phase 4〜7の全体アーキテクチャ

```
[ブラウザ / curl]
    ↓ GET /ask?q=質問
[Dockerコンテナ: ragapp（ポート8000）]
  uvicorn + FastAPI（main.py）
    ├─ ChromaDB（ドキュメント検索）
    └─ sentence-transformers（ベクトル化）
         ↓ HTTP http://ollama:11434
[Dockerコンテナ: ollama（ポート11434）]
  Ollamaサーバー
         ↓
  qwen2.5:1.5b（LLMモデル）
         ↓
[Dockerコンテナ: ragapp]
  {"answer": "回答"} をJSONで返す
         ↓
[ブラウザ / curl]
```
