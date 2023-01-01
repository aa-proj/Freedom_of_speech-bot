# discord ライブラリをインポート
import discord
from discord.app_commands import Choice

# requestライブラリをインポート
import requests
import typing
import enum

# インテント(discordに何の情報が欲しいのかログインの時に伝える変数)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

# Discordクライアントを準備 インテントを引数に渡してる
client = discord.Client(intents=intents)

# コマンドツリーをログイン後に取得してる
tree = discord.app_commands.CommandTree(client)

# ギルド変数(鯖IDを変数に入れておく)
guild_target = discord.Object(id=606109479003750440)

# ライブラリにイベントを登録 "on_ready"
# readyの時にDiscord側から実行される
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # コマンドツリーをシンク(同期する)
    await tree.sync(guild=guild_target)

#メッセージの削除を確認したら通知
@client.event
async def on_message_delete(message):
    print('メッセージの削除を確認しました')
    print(message.author)
    if message.author.bot:
        return
    await message.channel.send(f'{str(message.author.display_name)}さんのメッセージが削除されました。\n必要であれば</genron>で監査ログをチェックできます。')
        #原文を表示させる embedVar.add_field(name='aa', value=f'\n{str(message.author)}' + 'が送信したメッセージ: 『' + str(message.content) + '』が削除されました。')


#コマンドで監査ログをチェックして最新のメッセージデリートを表示
@tree.command(name='genron', description='言論の自由を守れ!', guild=guild_target) 
async def genron(interaction: discord.Integration):
    async for entry in interaction.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
        print(entry.user)
        print(entry.target)
        print(type(entry.target))
        if entry.user.bot:
            return
        if entry.user == entry.target:
            return
        embedVar = discord.Embed(title='メッセージが削除されました。', color=0xE74C3C)
        embedVar.add_field(name=f'\n犯人 {str(entry.user.display_name)}', value=f'\n{str(entry.target.display_name)}が送信したメッセージが削除されました。'
        )
        await interaction.response.send_message(embed=embedVar)

# DiscordにTokenでログインする
client.run('TOKEN')