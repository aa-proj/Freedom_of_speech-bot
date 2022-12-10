# discord ライブラリをインポート
import discord
from discord.app_commands import Choice

# requestライブラリをインポート
import requests
import typing
import enum

# インテント(discordに何の情報が欲しいのかログインの時に伝える変数)
intents = discord.Intents.default()
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


@client.event
async def on_message_delete(message):
    print('メッセージの削除を確認しました')
    embedVar = discord.Embed(title='メッセージが削除されました。', color=0xE74C3C)
    embedVar.add_field(name=None, value=f'\n{str(message.author.display_name)}' + 'によって送信されたメッセージが削除されました。')
    #原文を表示させる embedVar.add_field(name='aa', value=f'\n{str(message.author)}' + 'によって送信されたメッセージ: 『' + str(message.content) + '』が削除されました。')
    await message.channel.send(embed=embedVar)


# DiscordにTokenでログインする
client.run('TOKEN')
