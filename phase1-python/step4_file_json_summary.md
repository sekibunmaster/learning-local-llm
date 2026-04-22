# ファイル操作・JSON 学習まとめ

---

## 1. ファイルの読み書き

### 書き込み（"w"モード）

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("こんにちは\n")
    f.write("世界\n")
```

**出力結果（data.txt の中身）**
```
こんにちは
世界
```

**ポイント**
- `"w"` はwrite（書き込み）の意味
- ファイルが存在しなければ新規作成、存在すれば上書き
- `encoding="utf-8"` で日本語の文字化けを防ぐ
- `with` 文を使うと処理後に自動でファイルを閉じてくれる

---

### 読み込み（"r"モード）

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

**出力結果**
```
こんにちは
世界
```

**ポイント**
- `"r"` はread（読み取り）の意味
- `f.read()` でファイル全体を文字列として取得する

---

### モード一覧

| モード | 意味 | ファイルがない場合 |
|---|---|---|
| `"r"` | 読み取り | エラーになる |
| `"w"` | 書き込み（上書き） | 新規作成 |
| `"a"` | 追記 | 新規作成 |

---

## 2. JSON

### JSONとは

**JavaScript Object Notation** の略。データを保存・やり取りするための形式。
Pythonの辞書（dict）やリスト（list）とほぼ同じ構造で書ける。

```json
{
  "title": "雪国",
  "author": "川端康成",
  "is_checked_out": true
}
```

---

### 辞書 → JSONファイルに保存（json.dump）

```python
import json

data = {"name": "太郎", "age": 25, "scores": [85, 90, 78]}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

**出力結果（data.json の中身）**
```json
{
  "name": "太郎",
  "age": 25,
  "scores": [
    85,
    90,
    78
  ]
}
```

**ポイント**
- `ensure_ascii=False`：日本語をそのまま保存する（ないと文字化けする）
- `indent=2`：見やすく整形して保存する

---

### JSONファイル → 辞書に読み込み（json.load）

```python
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["name"])    # → 太郎
print(loaded["scores"])  # → [85, 90, 78]
```

---

## 3. 例外処理（try-except）

ファイルが存在しない場合などのエラーに対応する。

```python
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("ファイルが見つかりません")
    data = {}
except json.JSONDecodeError:
    print("JSONの形式が正しくありません")
    data = {}
```

**ファイルがない場合の出力結果**
```
ファイルが見つかりません
```

**ポイント**
- `except` を複数書いてエラーの種類ごとに処理を分けられる
- エラーが起きても処理を止めずに続けられる

---

## 4. 今回実装したもの：図書館管理システムへの保存・読み込み

### save()：蔵書リストをJSONに保存

```python
def save(self, filename):
    data = []
    for book in self.books:
        data.append({
            "title": book.title,
            "author": book.author,
            "is_checked_out": book.is_checked_out
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**出力結果（books.json の中身）**
```json
[
  {
    "title": "雪国",
    "author": "川端康成",
    "is_checked_out": true
  },
  {
    "title": "ラプラスの魔女",
    "author": "東野圭吾",
    "is_checked_out": true
  },
  {
    "title": "罪と罰",
    "author": "ドストエフスキー",
    "is_checked_out": false
  }
]
```

**なぜBookオブジェクトをそのまま保存できないのか**
JSONはPythonの辞書・リスト・文字列・数値・真偽値しか扱えない。
`Book`オブジェクトはそのままでは保存できないため、一度辞書に変換する必要がある。

---

### load()：JSONから蔵書リストを復元

```python
def load(self, filename):
    self.books = []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    for d in data:
        book = Book(d["title"], d["author"])
        book.is_checked_out = d["is_checked_out"]
        self.books.append(book)
```

**確認用コード**
```python
lib2 = Library()
lib2.load("books.json")
lib2.show_available()
```

**出力結果**
```
罪と罰, ドストエフスキー, 利用可能
```

JSONから読み込んだデータが正しく`Book`オブジェクトに復元されている。

---

## 5. よくあるミス

| ミス | 原因 | 対処 |
|---|---|---|
| 日本語が文字化けする | `ensure_ascii=False`を忘れた | オプションを追加する |
| `FileNotFoundError` | ファイルが存在しない | `try-except`で処理する |
| ループ変数を上書きしてしまう | `for book in data: book = Book(...)` | 変数名を`d`など別にする |
| `with`を使わずファイルを開く | 閉じ忘れのバグが起きる | 必ず`with`を使う |
