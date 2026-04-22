# ローカルLLM学習 会話まとめ

## あなたのプロフィール
- 学部4年生・大学研究者
- 企業のソフトウェア開発にAIを活用（機密情報扱いのためローカルLLM必須）
- Python：RK4まで自分で実装した経験あり
- Git：GitHub Desktopで触った程度、ほぼAI任せ
- Linux：未経験

---

## ローカルLLMの基礎知識

### ローカルLLMとは
自分のPC上でAIモデルを動かすこと。GPUがなくてもCPUだけで動作可能（速度は遅い）。

### クラウドLLMとの違い
| | クラウドLLM | ローカルLLM |
|---|---|---|
| 例 | ChatGPT, Claude | Llama, Mistral |
| ネット | 必須 | 不要 |
| プライバシー | データが外部に送られる | データが外に出ない |
| 性能 | 現状こちらが上 | モデル次第 |

### HTTPについて
HTTPはインターネット専用ではなく通信ルールの形式。`127.0.0.1`（localhost）宛の通信はPC外に出ない。ローカルLLMはHTTPを使いながらも外部に出ない。

---

## 学習ロードマップ（合計約110時間）

| Phase | 内容 | 時間 |
|---|---|---|
| 1 | Python実務レベル | 約30h |
| 2 | Git/GitHub（CLI） | 約15h |
| 3 | Linuxターミナル | 約20h |
| 4 | ローカルLLM実践・RAG基礎 | 約25h |
| 5 | Docker基礎 | 約20h |

1日2時間ペースで約55日。

---

## 現在の進捗

### 完了済み
- GitHubリポジトリ作成（`learning-local-llm`）
- `phase1-python/error_practice.py` をpush済み
- Step 2（エラー練習）：全問正解で完了

### 学んだGitコマンド
```bash
git init          # Gitの初期化
git remote add origin URL  # GitHubと紐づけ
git add ファイル名  # ステージング
git commit -m "メッセージ"  # コミット
git push          # GitHubにアップロード
git status        # 現在の状態確認
```

### 遭遇したトラブルと解決
| トラブル | 原因 | 解決 |
|---|---|---|
| `failed to push` | READMEを自動生成してしまった | `git pull --allow-unrelated-histories` |
| `src refspec main does not match` | ブランチがmasterだった | `git push -u origin master` |
| Vimが起動した | `-m`なしでcommitした | `Esc` → `:q!`で抜けてやり直し |
| 文字化け | 改行コードがUTF-8でなかった | VSCodeでUTF-8に変換して再push |

---

## Step 2 エラー一覧（習得済み）

| エラー名 | 原因 |
|---|---|
| `SyntaxError` | 文法ミス（コロン忘れなど） |
| `NameError` | 未定義の変数を使用 |
| `TypeError` | 型の不一致（strとintの演算など） |
| `IndexError` | リストの範囲外を指定 |
| `KeyError` | 辞書に存在しないキーを指定 |
| `FileNotFoundError` | ファイルが存在しない |
| `ZeroDivisionError` | 0で除算 |
| `AttributeError` | 存在しないメソッドを呼んだ |
| `ImportError` | ライブラリが存在しない |

---

## 次にやること

**Step 3：クラス・モジュール分割（10時間）**

1. 関数の復習（1時間）→ BMI計算プログラムのお題に取り組み中
2. クラスの学習（4時間）
3. モジュール分割（3時間）
4. 自作：学習記録管理プログラム（2時間）

### Step 3の最終課題
`Record`クラスを作り、JSONファイルへの保存・読み込みを実装してGitHubにpushする。

---

## 学習方針メモ

- AIには「答えを聞く」のではなく「仮説を検証する壁打ち相手」として使う
- エラーが出たらまず自分で原因を考えてから調べる
- コードを書いたら必ず`add`→`commit`→`push`する習慣をつける
- 管理ツール（NotionかObsidian）に「詰まったこと・解決方法」を必ず記録する
