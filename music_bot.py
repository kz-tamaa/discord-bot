import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio


bot = commands.Bot(command_prefix="|")
client = discord.Client()
vc = None

# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('hello everyone !!')
    print('Let\'s enjoy music !!')


@client.event
async def on_message(message):
    channel = client.get_channel(message.author.voice_channel.id)
    if message.content.startswith('/bye'):
        if client.is_voice_connected(channel.server):
            voice = client.voice_client_in(channel.server)
        else:
            voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player('voicetext_02.mp3')
        player.start()
    if message.content.startswith('/inu'):
        vc = await client.join_voice_channel(channel)
        print(vc)
        reply = 'わん'
        await client.send_message(message.channel, reply)


client.run('NTI0NTU5ODQ2MjQ3MjM1NTk0.Dvp2Dg.zNPhkoF3AfVkvmmWuh1AuT4zJu8')
