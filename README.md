# Nickname Logger Bot

Discordサーバー内のニックネーム変更を監視し、ログを記録するDiscord Botです。

## 機能

- サーバー内のメンバーのニックネーム変更を自動検知
- 指定したチャンネルにニックネーム変更のログを投稿
- スラッシュコマンドによる簡単な設定管理

## コマンド

- `/set_nickname_log` - ニックネーム変更ログを投稿するチャンネルを設定
- `/show_nickname_log` - 現在設定されているログチャンネルを表示

## セットアップ方法

1. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

2. 環境変数の設定:
   - プロジェクトのルートディレクトリに`.env`ファイルを作成
   - 以下の内容を記述:
   ```
   DISCORD_TOKEN_NICKHIS=your_discord_bot_token_here
   ```
   - `your_discord_bot_token_here`をDiscord Developer Portalで取得したBotトークンに置き換え

3. Botを起動:
```bash
python main.py
```

## 注意事項

- Botには「メンバーを表示」の権限が必要です
- ログを投稿するチャンネルに対して、Botに「メッセージを送信」の権限が必要です
- `.env`ファイルはGitにコミットしないでください（セキュリティのため）

## 技術スタック

- Python 3.x
- discord.py 2.5.2
- python-dotenv 1.0.1
- JSON（設定データの保存）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
