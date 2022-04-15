import os
import discord
from discord.ext import commands
from discord.utils import get
from asyncio import sleep

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


@client.command(pass_context=True)
async def pressao(ctx):
    voice_client = await ctx.message.author.voice.channel.connect()
    source = discord.FFmpegPCMAudio("pressao.mp3", options="-loglevel panic")
    await play_audio(source, voice_client)


@client.command(pass_context=True)
async def leave(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()


@client.event
async def on_voice_state_update(member, before, after):
    if not member.bot and (
            (before.self_deaf is True and after.self_deaf is False) or (before.channel != after.channel)):

        audio_set = {
            "default": "audio.mp3",
            559498710766321705: "saveiro.mp3",
            458703706137952285: "mutley.mp3",
            254393768067727360: "isolados.mp3",
            575432193795424257: "bolsonara.mp3",
            348484028367896586: "depressao.mp3"
        }

        if before.self_deaf is True and after.self_deaf is False:
            audio = audio_set.get("default")
        else:
            audio = audio_set.get(member.id, "default")

        channel = member.voice.channel
        source = discord.FFmpegPCMAudio(audio, options="-loglevel panic")

        voice_client = await channel.connect()
        await sleep(1)
        await play_audio(source, voice_client)


async def play_audio(source, voice_client):
    voice_client.play(source)

    while voice_client.is_playing():
        await sleep(1)
    await voice_client.disconnect()


token = os.environ.get('TOKEN', None)

client.run(token)
