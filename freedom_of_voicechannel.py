
import discord
from discord.app_commands import Choice
import requests
import datetime

Discord_Bot_Token="ODMxNzMwNzk1OTU2OTI4NTEz.GV82Tt.r0KfQIh6c8zhSiLWU80LgPYAFzAr6UszVZtI68"

# Discordクライアントを初期化します
intents = discord.Intents.default()
client = discord.Client(intents=intents)

##ああ銀行PY
async def sendMoneyById(ctx,user) -> bool:
    print("請求開始")
    fromId = user.id #固有のユニークID
    toId = "885834421771567125" # ああ国営銀行
    amount = 1

    sendBody = {"fromId": str(fromId), "toId": str(toId), "amount": amount, "memo": "他者を別チャンネルに移動した容疑"}

    username = f"{user.name}#{user.discriminator}"

    # print(sendBody)
    response = requests.post("https://bank.ahoaho.jp/", json=sendBody)
    data = response.json()
    if not data["success"]:
        raise Exception(data["message"])
    elif data["success"]:
        print("success")
        await ctx.guild.system_channel.send(f"チンパン監査官は特別な権力を用いて{username}から{amount}ポイント徴収します。")
    return True



async def audit(ctx, member):
    print("調査開始。")
    server = ctx.guild
    latest_entry = None
    async for entry in server.audit_logs(limit=20):
        if entry.action == discord.AuditLogAction.member_move:
            if not latest_entry or entry.created_at > latest_entry.created_at:
                latest_entry = entry
    if latest_entry:
        print("最新の監査ログを断定。")
        # 最新の監査ログのcreated_atと現在の日時（チャンネル移動が起きた時間）を比較して、差が3秒以内であれば一致と判定する。
        now = datetime.datetime.now(datetime.timezone.utc)
        if abs(now - latest_entry.created_at) < datetime.timedelta(seconds=3):
            user = latest_entry.user
            username = f"{user.name}#{user.discriminator}"
            await ctx.guild.system_channel.send(f"チンパン監査官は{username}がチャンネルを移動させた犯人だと推理しました。")
            print(f"チンパン監査官は{username}がチャンネルを移動させた犯人だと推理しました。")
            await sendMoneyById(ctx,user)
    else:
        print("調査終了。異常なし。")
    return 

#監査ログのアップデートを読んでたけど、移動させた人数が積み重なる時に更新されないらしい。ので却下。
# @client.event
# async def on_audit_log_entry_create(entry):
#     if entry.action == discord.AuditLogAction.member_move:
#         user = entry.user
#         if user:
#             username = f"{user.name}#{user.discriminator}"
#             #await entry.guild.system_channel.send(f"{username}がチャンネルを移動させた犯人です。")
#             print(f"{username}がチャンネルを移動させた犯人です。")
#         else:
#             print("Unknown user moved a channel.")
#     else:
#         print("ボイスチャンネル移動ではない監査ログでした。")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if before.channel is not None:
            print(f"{member.name}が{before.channel.name}から退出しました。")
            await audit(before.channel.guild.system_channel, member)

                    

# Discordに接続します
client.run(Discord_Bot_Token)