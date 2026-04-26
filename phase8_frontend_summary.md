# Phase 8 チャットUI 学習まとめ

---

## 1. Phase 8のゴール

HTMLとJavaScriptでチャット画面を作り、ブラウザからRAGアプリに質問できるようにする。

---

## 2. 発生した問題と解決

### CORSエラー

```
Access to fetch at 'http://localhost:8000/ask' from origin 'null' 
has been blocked by CORS policy
```

`file://`プロトコルからAPIにアクセスするとブラウザがブロックする。

**解決1：FastAPIにCORSミドルウェアを追加**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**解決2：index.htmlをFastAPIから配信する**

`file://`ではなく`http://localhost:8000/`からHTMLを配信することで問題を根本解決。

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
```

---

## 3. フォルダ構成

```
phase7-fullstack/
├─ docker-compose.yml
└─ ragapp/
    ├─ Dockerfile
    ├─ requirements.txt
    ├─ main.py
    └─ static/
        └─ index.html
```

---

## 4. index.html

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>RAG Chat</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; }
    #chat { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
    .user { text-align: right; color: blue; margin: 8px 0; }
    .ai { text-align: left; color: green; margin: 8px 0; }
    #input { width: 80%; padding: 8px; }
    #send { padding: 8px 16px; }
  </style>
</head>
<body>
  <h1>RAG Chat</h1>
  <div id="chat"></div>
  <input id="input" type="text" placeholder="質問を入力してください">
  <button id="send">送信</button>

  <script>
    const chat = document.getElementById("chat");
    const input = document.getElementById("input");
    const send = document.getElementById("send");

    send.addEventListener("click", async () => {
      const q = input.value.trim();
      if (!q) return;

      chat.innerHTML += `<div class="user">あなた: ${q}</div>`;
      input.value = "";

      const res = await fetch(`http://localhost:8000/ask?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      chat.innerHTML += `<div class="ai">AI: ${data.answer}</div>`;
      chat.scrollTop = chat.scrollHeight;
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") send.click();
    });
  </script>
</body>
</html>
```

---

## 5. 最終アーキテクチャ

```
ブラウザ（http://localhost:8000/）
    ↓ GET /ask?q=質問
FastAPI（ragapp コンテナ：ポート8000）
  ├─ static/index.html を配信
  ├─ ChromaDB（ドキュメント検索）
  └─ sentence-transformers（ベクトル化）
       ↓ http://ollama:11434
Ollama（ollamaコンテナ：ポート11434）
       ↓
  qwen2.5:1.5b
       ↓
{"answer": "回答"} をJSONで返す
       ↓
ブラウザのチャット画面に表示
```
