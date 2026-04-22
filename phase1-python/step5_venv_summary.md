# 仮想環境・ライブラリ管理 学習まとめ

---

## 1. 仮想環境とは

プロジェクトごとに独立したPython環境を作る仕組み。

**なぜ必要か**
プロジェクトAは`requests 2.28`、プロジェクトBは`requests 2.31`を使いたい場合、
同じ環境にインストールするとどちらかが壊れる。
仮想環境を使えばプロジェクトごとに別々の環境を持てる。

---

## 2. 基本コマンド

### 仮想環境を作る

```bash
python -m venv venv
```

`venv/`フォルダが作られる。

---

### 有効化

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**有効化されると左に`(venv)`が表示される**
```
(venv) PS C:\Users\ssyyi\learning-local-llm>
```

---

### 無効化

```bash
deactivate
```

左の`(venv)`が消えれば仮想環境から抜けている。

---

## 3. ライブラリ管理

### インストール

```bash
pip install requests
```

### 依存関係とは

`requests`をインストールしたのに複数のライブラリが入る。
これは`requests`が動くために必要な他のライブラリが自動でインストールされるため。

```
certifi==2026.4.22
charset-normalizer==3.4.7
idna==3.12
requests==2.33.1
urllib3==2.6.3
```

---

## 4. requirements.txt

### 作り方

```bash
pip freeze > requirements.txt
```

インストール済みのライブラリとバージョンを記録する。

**requirements.txtの中身**
```
certifi==2026.4.22
charset-normalizer==3.4.7
idna==3.12
requests==2.33.1
urllib3==2.6.3
```

### 使い方

```bash
pip install -r requirements.txt
```

このコマンド1つで`requirements.txt`に書かれたライブラリを全部インストールできる。
チームで開発するときに全員が同じ環境を再現できる。

---

## 5. .gitignore

Gitで管理しないファイル・フォルダを指定するファイル。

### 作り方

```bash
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
```

### .gitignoreの中身

```
venv/
__pycache__/
```

**なぜvenv/を除外するか**
仮想環境はPCごとに異なる。GitHubにpushする必要はなく、
`requirements.txt`があれば誰でも同じ環境を再現できる。

---

## 6. よくあるミス

| ミス | 原因 | 対処 |
|---|---|---|
| `pip install`しても反映されない | 仮想環境を有効化していない | `(venv)`が表示されているか確認する |
| `venv/`がGitHubにpushされる | `.gitignore`を作っていない | `.gitignore`に`venv/`を追加する |
| 環境が壊れる | 複数プロジェクトで同じ環境を使っている | プロジェクトごとに仮想環境を作る |

---

## 7. 毎回の作業フロー

```bash
# 1. プロジェクトフォルダに移動
cd learning-local-llm

# 2. 仮想環境を有効化
venv\Scripts\activate

# 3. 作業する

# 4. ライブラリを追加したらrequirements.txtを更新
pip freeze > requirements.txt

# 5. 仮想環境を無効化
deactivate
```
