# Phase 5 Docker基礎 学習まとめ

---

## 1. Dockerとは

アプリケーションを「コンテナ」という独立した環境でパッケージ化して動かす仕組み。

### 仮想環境との違い

```
venv（Python仮想環境）
└─ Pythonライブラリだけを分離

Docker（コンテナ）
└─ OS・ライブラリ・アプリ全体を分離
```

### なぜDockerを使うか

```
「自分のPCでは動くのに本番では動かない」問題を解決する。
コンテナの中に必要なものをすべて含めるため、
どの環境でも同じように動く。
```

---

## 2. 用語の整理

```
イメージ    コンテナの設計図（テンプレート）
コンテナ    イメージから作った実行環境
Dockerfile  イメージを作るための手順書
Docker Hub  イメージを配布するクラウドサービス
```

---

## 3. Dockerの仕組み

```
Dockerfile（手順書）
    ↓ docker build
イメージ（設計図）
    ↓ docker run
コンテナ（実行環境）  ← ここでアプリが動く
```

---

## 4. Dockerのインストール

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ユーザー名  # sudoなしで使えるようにする
```

---

## 5. 基本コマンド

```bash
docker build -t イメージ名 .   # イメージをビルド
docker run イメージ名          # コンテナを起動
docker run -it イメージ名 bash # インタラクティブに起動
docker images                  # イメージ一覧
docker ps                      # 実行中のコンテナ一覧
docker ps -a                   # 全コンテナ一覧（終了済みも含む）
docker rm コンテナID           # コンテナを削除
docker rmi イメージ名          # イメージを削除
```

---

## 6. Dockerfileの書き方

```dockerfile
FROM python:3.12-slim      # ベースイメージを指定
WORKDIR /app               # コンテナ内の作業フォルダ
COPY requirements.txt .    # ファイルをコンテナにコピー
RUN pip install -r requirements.txt  # コマンドを実行（ビルド時）
COPY . .                   # 残りのファイルをコピー
CMD ["python", "app.py"]   # コンテナ起動時に実行するコマンド
```

### COPYを2回に分ける理由

```
requirements.txtを先にコピーしてpip installすることで
ソースコードを変更してもpip installの結果がキャッシュされる。
→ 再ビルドが速くなる
```

---

## 7. 環境変数の渡し方

```bash
docker run -e 変数名=値 イメージ名
```

```bash
# 例：OllamaのホストをDockerコンテナに渡す
docker run -e OLLAMA_HOST=http://172.25.72.236:11434 ragapp
```

コンテナ内でPythonから読み込む：

```python
import os
host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
```

---

## 8. DockerコンテナとOllamaの接続

コンテナはWSL2とは独立した環境なので`localhost`でOllamaに接続できない。

```
【問題】
Dockerコンテナ → localhost:11434 → 接続できない（コンテナ自身のlocalhostを見る）

【解決】
OllamaをWSL2のIPアドレスで外部公開する
OLLAMA_HOST=0.0.0.0:11434 ollama serve

Dockerコンテナ → 172.25.72.236:11434 → Ollamaに接続できる
```

### 全体のアーキテクチャ

```
[Dockerコンテナ]
  ragapp
  ├─ rag.py
  ├─ profile.txt
  └─ ChromaDB + sentence-transformers
       ↓ HTTP (172.25.72.236:11434)
[WSL2]
  Ollamaサーバー (0.0.0.0:11434)
       ↓
  qwen2.5:1.5b（モデル）
```
