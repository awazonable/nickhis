import discord
import json
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Botの設定
TOKEN = os.getenv('DISCORD_TOKEN_NICKHIS')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN_NICKHISが設定されていません。.envファイルを確認してください。")

CONFIG_FILE = "config.json"

# Botの初期化
intents = discord.Intents.default()
intents.members = True  # ニックネーム変更検知のため
bot = commands.Bot(command_prefix="!", intents=intents)

# 設定データを保存する関数
def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# 設定データを読み込む関数
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

db = load_config()  # 起動時に設定をロード

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()  # 全サーバーでアプリケーションコマンドを同期
    print("Slash commands synced.")

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.nick != after.nick:
        guild_id = str(after.guild.id)
        if guild_id in db:
            log_channel = bot.get_channel(int(db[guild_id]))
            if log_channel:
                await log_channel.send(f"{before.name} のニックネームが `{before.nick}` → `{after.nick}` に変更されました。")

class NicknameLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_nickname_log", description="ニックネーム変更ログを投稿するチャンネルを設定")
    @app_commands.describe(channel="ログを投稿するチャンネル")
    async def set_nickname_log(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        db[guild_id] = channel.id
        save_config(db)  # 設定を保存
        await interaction.response.send_message(f"ニックネーム変更ログを {channel.mention} に設定しました。", ephemeral=True)

    @app_commands.command(name="show_nickname_log", description="設定済みのニックネーム変更ログのチャンネルを表示")
    async def show_nickname_log(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id in db:
            channel = bot.get_channel(int(db[guild_id]))
            if channel:
                await interaction.response.send_message(f"現在、ニックネーム変更ログは {channel.mention} に設定されています。", ephemeral=True)
            else:
                await interaction.response.send_message("設定されたチャンネルが見つかりません。再設定してください。", ephemeral=True)
        else:
            await interaction.response.send_message("ニックネーム変更ログのチャンネルは設定されていません。", ephemeral=True)

# コグをBotに登録
bot.tree.add_command(NicknameLogger(bot).set_nickname_log)
bot.tree.add_command(NicknameLogger(bot).show_nickname_log)

bot.run(TOKEN)
