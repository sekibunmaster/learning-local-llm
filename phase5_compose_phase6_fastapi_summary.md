# Phase 5（docker-compose）+ Phase 6（FastAPI）学習まとめ

---

## Phase 5 追加：docker-compose

### docker-composeとは

複数のDockerコンテナを一括管理するツール。`docker-compose.yml`に構成を書いておくことで`docker compose up`一発で全コンテナが起動する。

### 昨日との違い

```
昨日（docker単体）
  ・IPアドレスを手動で調べた（ip addr show eth0）
  ・Ollamaを別ターミナルで手動起動
  ・docker runに毎回IPを指定した

今日（docker-compose）
  ・docker compose up だけで完結
  ・コンテナ同士はサービス名で通信（IPアドレス不要）
```

### docker-compose.ymlの書き方

```yaml
services:
  ollama:
    image: ollama/ollama          # Docker Hubのイメージを使う
    ports:
      - "11434:11434"             # ホスト:コンテナ のポートマッピング
    volumes:
      - ollama_data:/root/.ollama # データを永続化する

  ragapp:
    build: ./ragapp               # Dockerfileからビルドする
    environment:
      - OLLAMA_HOST=http://ollama:11434  # サービス名で接続
    depends_on:
      - ollama                    # ollamaが先に起動する
    command: >
      sh -c "sleep 10 && python rag.py"  # 起動を少し待つ

volumes:
  ollama_data:                    # 名前付きボリューム
```

### 重要ポイント

```
コンテナ同士の通信はサービス名を使う
  ✗ http://172.25.72.236:11434  （IPアドレス直指定）
  ○ http://ollama:11434          （サービス名）
```

### コンテナにモデルをダウンロードする

```bash
# ollamaコンテナをバックグラウンドで起動
docker compose up ollama -d

# コンテナ内でollamaコマンドを実行
docker exec コンテナ名 ollama pull qwen2.5:1.5b
```

### 基本コマンド

```bash
docker compose up          # 全コンテナを起動（フォアグラウンド）
docker compose up -d       # バックグラウンドで起動
docker compose up サービス名 -d  # 特定のサービスだけ起動
docker compose down        # 全コンテナを停止・削除
docker compose logs        # ログを確認
```

---

## Phase 6：FastAPI

### FastAPIとは

PythonでWeb APIを作るフレームワーク。シンプルに書けて、ドキュメントが自動生成される。

### Web APIとローカルの関係

```
Web API  → データをHTTPで受け渡しする仕組み（形式の話）
ローカル  → 自分のPC内で動いている（場所の話）

→ ローカルで動くWeb APIは外部に公開されていない
  localhost:8000 は同じPC内からしかアクセスできない
```

### インストール

```bash
pip install fastapi uvicorn
```

`uvicorn`はFastAPIを動かすHTTPサーバー。

### 基本的な書き方

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")          # GETリクエストを受け付けるエンドポイント
def ask(q: str):          # URLパラメータをそのまま引数で受け取れる
    return {"answer": "回答"}  # dictを返すと自動でJSONになる
```

### 起動方法

```bash
uvicorn main:app --reload
# main.py の app オブジェクトを起動
# --reload でコード変更時に自動再起動
```

### エンドポイントへのアクセス

```bash
# curlでアクセス（日本語はURLエンコードが必要）
curl "http://localhost:8000/ask?q=%E8%B6%A3%E5%91%B3%E3%81%AF%E4%BD%95%E3%81%A7%E3%81%99%E3%81%8B"

# ブラウザでもアクセスできる
http://localhost:8000/ask?q=...
```

### Swagger UI（自動ドキュメント）

```
http://localhost:8000/docs
```

FastAPIが自動生成するドキュメントページ。ブラウザ上でAPIを試せる。

### 今回作ったRAG APIの構成

```python
from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

app = FastAPI()

# 起動時にドキュメントを読み込んでベクトル化
embedder = SentenceTransformer("all-MiniLM-L6-v2")
collection = ...  # ChromaDBに登録

@app.get("/ask")
def ask(q: str):
    # 1. 質問をベクトル化して関連ドキュメントを検索
    # 2. OllamaにドキュメントとともにリクエストをHTTPで送る
    # 3. 回答をJSONで返す
    return {"answer": response["message"]["content"]}
```

### 全体のアーキテクチャ

```
ブラウザ / curl
    ↓ GET /ask?q=質問
uvicorn（HTTPサーバー）
    ↓
FastAPI（main.py）
    ├─ ChromaDB（関連ドキュメント検索）
    └─ Ollama（http://localhost:11434）
           ↓
       qwen2.5:1.5b
    ↓
{"answer": "回答"} をJSON形式で返す
```
