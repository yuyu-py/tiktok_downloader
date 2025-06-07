# TikTok動画ダウンローダー

## プロジェクト内容

TikTokの動画URLから動画ファイルを直接ダウンロードできるツールです。WebスクレイピングとHTTP通信を使用して、TikTokの動画情報を取得し、ローカルに保存する機能を実装しています。PythonによるWeb API連携、HTMLパース、ファイル操作技術を学習することを目的として開発しました。

## プロジェクト構成

```
tiktok_downloader/
├── src/
│   └── video_downloader.py    # メインプログラム
├── downloaded_videos/         # ダウンロード動画保存フォルダ
├── requirements.txt           # 依存関係管理
├── README.md                  # プロジェクト説明書
└── .gitignore                # Git除外ファイル設定
```

## 必要要件/開発環境

- **Python 3.7以上**
- **VSCode** (開発環境)
- **Git** (バージョン管理)
- **インターネット接続** (動画ダウンロード用)

### 使用ライブラリ

- **requests** HTTP通信とAPI連携処理
- **beautifulsoup4** HTML解析とWebスクレイピング
- **os** ファイルシステム操作

## 機能

- **TikTokURL検証** 入力されたURLの形式確認と妥当性チェック
- **動画情報取得** WebスクレイピングによるダウンロードURL抽出
- **動画ダウンロード** 取得したURLからの動画ファイル取得
- **ファイル自動保存** ダウンロード動画の自動命名と保存
- **対話式インターフェース** ユーザーフレンドリーなコマンドライン操作
- **エラーハンドリング** 通信エラーやファイル操作エラーの適切な処理
- **ファイルサイズ表示** ダウンロード動画のサイズ確認
- **連続ダウンロード** 複数動画の連続処理機能

## 実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/tiktok_downloader.git
cd tiktok_downloader
```

### 2. 仮想環境の作成・アクティベート

**Windows**

```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. プログラムの実行

```bash
python src/video_downloader.py
```

実行後、対話式インターフェースが起動し、TikTokの動画URLを入力するとdownloaded_videosフォルダに動画が保存されます。

## 使用方法

1. プログラムを実行すると対話式モードが開始されます
2. `TikTok動画URL >>>` のプロンプトに動画のURLを入力します
3. 動画のダウンロードが自動で実行されます
4. `exit` と入力するとプログラムが終了します
5. `help` と入力すると使い方が表示されます

## データ形式について

- **入力データ** TikTokの動画URL（https://www.tiktok.com/...）
- **出力データ** MP4形式の動画ファイル
- **保存場所** downloaded_videosフォルダ内

## 注意事項

- このツールは教育目的で作成されています
- ダウンロードする動画の著作権を尊重してください
- 大量のダウンロードはサーバーに負荷をかける可能性があります

## 開発者

YuYu