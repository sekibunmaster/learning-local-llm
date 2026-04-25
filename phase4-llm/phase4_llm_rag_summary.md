# Phase 4 ローカルLLM実践 + RAG基礎 学習まとめ

---

## 1. Ollamaとは

ローカルでLLMを動かすためのツール。バックグラウンドでサーバーとして動作し、APIでリクエストを受け付ける。

```
The Ollama API is now available at 127.0.0.1:11434
```

---

## 2. Ollamaのインストール

```bash
sudo apt-get install zstd
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 3. モデルの操作

```bash
ollama run モデル名      # モデルをダウンロードして起動
ollama list             # インストール済みモデル一覧
/bye                    # モデルの終了
```

### 使ったモデル

| モデル | サイズ | 特徴 |
|---|---|---|
| qwen2.5:1.5b | 986MB | Alibaba製、軽量 |
| llama3.2:1b | 1.3GB | Meta製、軽量 |

---

## 4. PythonからOllamaを呼び出す

```python
import ollama

response = ollama.chat(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": "必ず日本語で答えてください。"},
        {"role": "user", "content": "質問内容"}
    ]
)

print(response["message"]["content"])
```

---

## 5. 会話履歴の保持

毎回`messages`の全履歴をOllamaに渡すことで前の会話を覚えさせる。

```python
messages = [
    {"role": "system", "content": "必ず日本語で返答してください。"}
]

while True:
    user_input = input("あなた: ")
    if user_input == "/bye":
        break

    messages.append({"role": "user", "content": user_input})

    response = ollama.chat(model="qwen2.5:1.5b", messages=messages)
    reply = response["message"]["content"]

    messages.append({"role": "assistant", "content": reply})
    print(f"AI: {reply}\n")
```

### messagesのroleの種類

```
system     AIへの指示（言語指定・役割設定など）
user       ユーザーの発言
assistant  AIの返答
```

---

## 6. RAG（Retrieval-Augmented Generation）

### RAGとは

LLMは学習済みの知識しか持っていない。RAGは質問に関連するドキュメントを検索してLLMに渡すことで、外部知識を使って回答させる仕組み。

```
質問
 ↓
ChromaDBでドキュメントを検索
 ↓
質問 + 関連ドキュメント をLLMに渡す
 ↓
回答
```

### 使ったライブラリ

```bash
pip install chromadb sentence-transformers ollama
```

| ライブラリ | 役割 |
|---|---|
| chromadb | ベクトルデータベース（ドキュメントの保存・検索） |
| sentence-transformers | テキストをベクトルに変換（埋め込みモデル） |
| ollama | LLMの呼び出し |

### 埋め込み（Embedding）とは

テキストを数値のベクトルに変換する技術。意味が近いテキストは近いベクトルになるため、類似度で検索できる。

```
「Gitとは何ですか」→ [0.23, -0.14, 0.87, ...]
「Gitはバージョン管理システムです」→ [0.21, -0.12, 0.85, ...]
↑ ベクトルが近い → 関連度が高い
```

### RAGの実装

```python
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("docs")

# ファイルからドキュメントを読み込む
with open("profile.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

embeddings = embedder.encode(lines).tolist()
collection.add(
    documents=lines,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(lines))]
)

# 質問に関連するドキュメントを検索
query = "趣味は何ですか"
query_embedding = embedder.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3  # 取得するドキュメント数
)

retrieved = "\n".join(results["documents"][0])

# LLMに渡す
response = ollama.chat(
    model="qwen2.5:1.5b",
    messages=[
        {"role": "system", "content": "必ず日本語で答えてください。以下のドキュメントに書かれていることだけを元に答えてください。ドキュメントにない情報は答えないでください。\n" + retrieved},
        {"role": "user", "content": query}
    ]
)

print(response["message"]["content"])
```

---

## 7. ハルシネーションへの対処

LLMがドキュメントにない情報を勝手に作り上げる問題。

### 対策1：システムプロンプトで制限する

```python
"ドキュメントに書かれていることだけを元に答えてください。ドキュメントにない情報は答えないでください。"
```

### 対策2：n_resultsを調整する

```python
n_results=1  # 少なすぎると必要な情報が取れない
n_results=3  # 複数取得することで関連情報をカバーできる
```

---

## 8. 全体のアーキテクチャ

```
モデルファイル（データ）
    ↓ Ollamaが読み込む
Ollamaサーバー（127.0.0.1:11434で待ち受け）
    ↓ HTTP通信
Pythonスクリプト
    ↑
ChromaDB（ドキュメントの検索）
    ↑
sentence-transformers（テキストをベクトルに変換）
```
