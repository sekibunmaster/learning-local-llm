# Phase 3 Linux ターミナル基本操作 学習まとめ

---

## 1. ファイル操作

### 基本コマンド

```bash
pwd           # 現在地を表示
ls            # ファイル・フォルダ一覧
ls -la        # 詳細表示（パーミッション・サイズ等）
mkdir 名前    # フォルダを作る
cd 名前       # フォルダを移動
touch 名前    # 空のファイルを作る
cat ファイル  # ファイルの中身を表示
```

### コピー・移動・削除

```bash
cp 元 先      # コピー
mv 元 先      # 移動・名前変更
rm ファイル   # 削除（ゴミ箱なし・即削除）
```

### リダイレクト

```bash
echo "text" > file.txt   # 上書き
echo "text" >> file.txt  # 追記
```

---

## 2. パーミッション

### 見方

```
-rw-r--r--  1  noah  noah  12  Apr 23 16:15  test.txt
│           │  │     │     │
│           │  │     │     └─ ファイルサイズ
│           │  │     └─ グループ名
│           │  └─ 所有者
│           └─ リンク数
└─ パーミッション
```

### パーミッションの構造

```
- rw- r-- r--
│ │   │   └─ その他
│ │   └─ グループ
│ └─ 所有者
└─ ファイル種別（-=ファイル d=フォルダ）
```

### 数字の対応

```
r = 4（読む）
w = 2（書く）
x = 1（実行）

rwx = 7
r-x = 5
r-- = 4
--- = 0
```

### よく使う組み合わせ

```
755  rwxr-xr-x  スクリプトファイル
644  rw-r--r--  通常のファイル
600  rw-------  秘密鍵など
```

### 変更

```bash
chmod 755 ファイル
```

---

## 3. テキスト検索

```bash
grep "文字列" ファイル      # 検索
grep -i "文字列" ファイル   # 大文字小文字を無視
grep -n "文字列" ファイル   # 行番号を表示
grep -v "文字列" ファイル   # 含まない行を表示
```

### パイプ

```bash
ps aux | grep noah   # 左の出力を右に渡す
```

---

## 4. プロセス管理

```bash
ps aux          # 実行中のプロセス一覧
kill PID        # プロセスを終了
sleep 100 &     # バックグラウンドで実行
```

### ps auxの列の意味

```
USER    誰が起動したか
PID     プロセスID
%CPU    CPU使用率
%MEM    メモリ使用率
COMMAND 実行中のコマンド
```

---

## 5. 環境変数

```bash
echo $HOME        # ホームディレクトリ
echo $USER        # 現在のユーザー名
echo $PATH        # コマンドを探す場所の一覧
which コマンド    # コマンドの場所を確認

export 変数名="値"         # 環境変数を設定（一時的）
echo 'export 変数名="値"' >> ~/.bashrc  # 永続化
source ~/.bashrc           # .bashrcを再読み込み
```

### PATHとは

コマンドを入力したとき、Linuxは`$PATH`に書かれたフォルダを順番に探して実行ファイルを見つける。

```bash
which ls   # → /usr/bin/ls
```

---

## 6. 自作コマンド

```bash
# スクリプトを作る
echo '#!/bin/bash' > ~/hello.sh
echo 'echo "hello, $USER"' >> ~/hello.sh

# 実行権限を付与
chmod 755 ~/hello.sh

# PATHの通ったフォルダに移動
sudo mv ~/hello.sh /usr/local/bin/hello.sh

# どこからでも実行できる
hello.sh
```
