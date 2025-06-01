# AWS サービス名タイピングゲーム

Pygame を使用した AWS サービス名のタイピングゲームです。

## 概要

このゲームは AWS のサービス名を含むユーモアのある英語文をタイピングする練習ができるゲームです。
制限時間内にできるだけ多くの文章を正確にタイプして、高いスコアを目指しましょう。
80種類以上の AWS サービスが出題されます。

## 機能

- 60秒の制限時間内でのタイピングゲーム
- 80種類以上の AWS サービスを含むユーモアのある英語文が出題される
- サービス名が色付きで表示され、わかりやすく
- スコアとミスのカウント
- ハイスコアの記録
- 回答したサービスの概要を確認できる機能
- タイピング速度に応じた評価システム（Hero, Specialty, Professional, Associate, Foundational）

## 必要条件

- Python 3.x
- uv (推奨) または pip

## インストール方法

### uv を使用する場合（推奨）

1. uv のインストール（まだインストールしていない場合）:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. 仮想環境の作成とパッケージのインストール:

```bash
# リポジトリをクローン
git clone https://github.com/ShinichiOkimoto/aws_typing.git
cd aws_typing

# 仮想環境を作成してパッケージをインストール
uv venv
uv pip install -r requirements.txt
```

### pip を使用する場合

```bash
# リポジトリをクローン
git clone https://github.com/ShinichiOkimoto/aws_typing.git
cd aws_typing

# 仮想環境を作成してパッケージをインストール
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# または
# .venv\Scripts\activate  # Windows

pip install pygame
```

## 実行方法

### uv を使用する場合（推奨）

```bash
uv run aws_typing_game.py
```

### 従来の方法

```bash
# 仮想環境を有効化している場合
python aws_typing_game.py

# または直接実行
python3 aws_typing_game.py
```

## 操作方法

- スペースキー: ゲーム開始/リスタート
- ESCキー: メニューに戻る
- 表示された AWS サービス名を含む文章を入力し、Enter キーで確定
- ゲーム終了後:
  - Iキー: 回答したサービスの情報を表示
  - サービス情報画面で:
    - Aキー: 前のサービス
    - Dキー: 次のサービス
    - ESCキー: 結果画面に戻る

## ゲームルール

- 表示された AWS サービス名を含む文章を正確にタイプして Enter キーを押す
- 正解すると文章の文字数に応じたスコアが加算される
- 間違えるとミスカウントが増える
- 60秒の制限時間が終了するとゲームオーバー
- ゲーム終了後、回答したサービスの概要を確認できる

## 評価システム

タイピング速度（CPM: Characters Per Minute）に応じて以下の評価が表示されます：

- **Hero** (金色): 300文字/分以上
- **Specialty** (紫色): 250～300文字/分
- **Professional** (エメラルド色): 200～250文字/分
- **Associate** (青色): 100～200文字/分
- **Foundational** (灰色): 100文字/分未満

## ライセンス

このプロジェクトはオープンソースであり、制限なく自由に利用、変更、配布することができます。

商用利用、私的利用、修正、配布のいずれも許可されています。ソースコードの再配布時にも特別な条件はありません。

このソフトウェアは「現状のまま」提供されており、明示または黙示を問わず、いかなる保証もありません。
