# 学習進捗管理

## ステータス凡例
- ✅ 完了
- 🔄 進行中
- ⬜ 未着手

---

## Phase 1｜Python実務レベル（約30時間）

| ステップ | 内容 | 状態 | メモ |
|---|---|---|---|
| Step 1 | 基礎文法 | ✅ | RK4実装経験ありのためスキップ |
| Step 2 | エラーを読む練習 | ✅ | 全9種類習得・テスト全問正解 |
| Step 3 | クラス・モジュール分割 | 🔄 | BMI計算プログラムに取り組み中 |
| Step 4 | ファイル操作・JSON・例外処理 | ⬜ | |
| Step 5 | 仮想環境・ライブラリ管理 | ⬜ | |
| Step 6 | 自作プログラム | ⬜ | テーマ：学習記録管理 |

## Phase 2｜Git/GitHub CLI（約15時間）

| ステップ | 内容 | 状態 | メモ |
|---|---|---|---|
| リポジトリ作成 | GitHub + ターミナルで作成 | ✅ | `learning-local-llm` |
| 基本操作 | add/commit/push | ✅ | 実際にファイルをpush済み |
| ブランチ・PR | ブランチ・マージ・コンフリクト | ⬜ | |

## Phase 3｜Linuxターミナル（約20時間）

| ステップ | 内容 | 状態 |
|---|---|---|
| 基本コマンド | cd/ls/grep/chmod/ssh | ⬜ |
| プロセス管理 | ps/kill/systemctl | ⬜ |
| 環境変数 | export/PATH | ⬜ |

## Phase 4｜ローカルLLM実践・RAG（約25時間）

| ステップ | 内容 | 状態 |
|---|---|---|
| Ollamaでモデルを動かす | | ⬜ |
| 量子化の違いを体感 | | ⬜ |
| RAG概念理解 | | ⬜ |
| ChromaDB + LangChain実装 | | ⬜ |

## Phase 5｜Docker基礎（約20時間）

| ステップ | 内容 | 状態 |
|---|---|---|
| コンテナ・イメージの概念 | | ⬜ |
| 基本コマンド | | ⬜ |
| Dockerfile作成 | | ⬜ |
| LLMをコンテナで動かす | | ⬜ |

---

## 学習記録

### 2026-04-22
- GitHubリポジトリ作成（`learning-local-llm`）
- `error_practice.py`をpush
- Step 2完了・テスト全問正解
- Step 3開始（BMI計算プログラムに取り組み中）

---

## 詰まったこと・解決方法ログ

| 日付 | 詰まったこと | 解決方法 |
|---|---|---|
| 2026-04-22 | `failed to push` | `git pull --allow-unrelated-histories` |
| 2026-04-22 | `src refspec main does not match` | `git push -u origin master` |
| 2026-04-22 | Vimが起動した | `Esc` → `:q!` で抜けて `-m` をつけてcommit |
| 2026-04-22 | README文字化け | VSCodeでUTF-8に変換して再push |
