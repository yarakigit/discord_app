# インストールした discord.py を読み込む
import discord
import datetime
from discord.ext import tasks

# タイトル
title = "締切まであと"
#ここで日付けを指定
dead_time = datetime.datetime(year=2022, month=2, day=10, hour=17)

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'hogepiyo'
# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/timer」と発言したら「残り時間」が返る処理
    if message.content == '/timer':
        #発言したチャンネルのIDを取得
        channel_id = message.channel.id
        send_message = await message.channel.send("timer start")
        #発現したメッセージのIDを取得
        message_id= send_message.id
        send_message_every.start(channel_id,message_id) #定期実行するメソッドの後ろに.start()をつける

# 1秒間間隔で実行        
@tasks.loop(seconds=1)
async def send_message_every(channel_id,message_id):
    # 上位関数で取得したチャンネルのIDを使う
    channel = client.get_channel(channel_id)
    # 時間の処理 開始
    dt_now = datetime.datetime.now()#現在時刻取得
    diff_time = dead_time - dt_now#現在時刻との差分
    days = diff_time.days
    seconds= diff_time.seconds
    hours= seconds//3600
    minutes= (seconds//60) % 60
    seconds= seconds - hours*3600 -minutes*60
    out_str = '残り '+str(days)+'日 '+str(hours)+'時間 '+str(minutes)+'分 ' + str(seconds)+'秒'
    #時間の処理 終了
    #await channel.send(out_str)
    # 上位関数で取得したメッセージのIDを使う
    msg= await channel.fetch_message(message_id)
    #Embedメソッドを使う
    embed = discord.Embed(title=title,description=out_str,color=discord.Colour.orange())
    #await msg.edit(content=out_str)
    await msg.edit(embed=embed)
    
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

