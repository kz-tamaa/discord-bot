import discord
from discord.ext import commands
from glob import glob
from pathlib import Path
import os


bot = commands.Bot(command_prefix='!')
client = discord.Client()
voice = None
player = None

MUSIC_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/music'


# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('hello everyone !!')
    print('Let\'s enjoy music !!')


@client.event
async def on_message(message):
    global voice, player
    if message.author.bot:
        # 発言者がBotの場合
        return
    if message.content.startswith('!list'):
        # ローカルに存在する音楽ファイルの一覧を表示
        music_list = glob(MUSIC_FOLDER + '/*.mp3')
        embed = discord.Embed(title="Music List", description="以下、音楽リストです。", color=0xeee657)
        for i, music in enumerate(music_list):
            embed.add_field(name=str(i) + '\t:\t' + Path(music).stem, value=Path(music).stem, inline=False)
        await client.send_message(message.channel, embed=embed)
    if message.content.startswith('!play') and len(message.content.split()) == 2:
        if is_not_joined_voice_channel(message):
            await client.send_message(message.channel, 'ボイスチャンネルに参加した上で実行してください！！')
            return
        if voice is None:
            voice = await client.join_voice_channel(message.author.voice_channel)
        elif voice.is_connected():
            if player is not None and player.is_playing():
                player.stop()
        music_list = glob(MUSIC_FOLDER + '/*.mp3')
        try:
            music_path = music_list[int(message.content.split()[1])]
            player = voice.create_ffmpeg_player(music_path)
            player.start()
            embed = discord.Embed(title='Now Playing!', description=Path(music_path).stem)
            await client.send_message(message.channel, embed=embed)
        except IndexError:
            await client.send_message(message.channel, '曲が存在しません！')
    if message.content.startswith('!stop') and player is not None and player.is_playing():
        if is_not_joined_voice_channel(message):
            await client.send_message(message.channel, 'ボイスチャンネルに参加した上で実行してください！！')
            return
        player.stop()


def is_not_joined_voice_channel(message) -> bool:
    return message.author.voice_channel is None


# @bot.command()
# async def add():
#     print('aa')
#
#
# @bot.event()
# async def on_message(message):
#     await bot.process_commands(message)
#     await client.send_message(message.channel, 'うぇい')


client.run('NTI0NTU5ODQ2MjQ3MjM1NTk0.Dvp2Dg.zNPhkoF3AfVkvmmWuh1AuT4zJu8')
# bot.run('NTI0NTU5ODQ2MjQ3MjM1NTk0.Dvp2Dg.zNPhkoF3AfVkvmmWuh1AuT4zJu8')
