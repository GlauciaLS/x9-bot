from asyncio import sleep
import os
import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='>', intents=intents)


@client.command(pass_context=True)
async def on_ready(ctx):
    print('Logged on as {0}!'.format(ctx.user))


@client.command(pass_context=True)
async def oi(ctx):
    await ctx.message.author.send("oi!", tts=True)


@client.command(pass_context=True)
async def on_member_join(ctx):
    guild = ctx.guild
    if guild.system_channel is not None:
        mensagem = f'{ctx.mention} acabou de entrar no {guild.name}'
        await guild.system_channel.send(mensagem)


@client.event
async def on_voice_state_update(member, before, after):
    if not member.bot and (
            (before.self_deaf is True and after.self_deaf is False) or (before.channel != after.channel)):

        source = discord.FFmpegPCMAudio("audio.mp3", options="-loglevel panic")

        channel = member.voice.channel
        voice_client = get(client.voice_clients, guild=member.guild)

        if voice_client is None or not voice_client.is_connected():
            voice_client = await channel.connect()

        voice_client.play(source)

        while voice_client.is_playing():
            await sleep(1)
        await voice_client.disconnect()

token = os.environ.get('TOKEN', None)

client.run(token)
