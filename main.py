import os
import discord
from discord.ext import commands
from discord.utils import get
from asyncio import sleep

from app import keep_alive

intents = discord.Intents.default()
intents.members = True

prefix = '>'

audio_files = os.listdir("resources/audio")
gif_files = os.listdir("resources/gif")
commands_audio = list(filter(lambda file: file.endswith(".mp3"), audio_files))

client = commands.Bot(command_prefix=prefix, intents=intents)

audio_set = {
    "default": "audio.mp3",
    559498710766321705: "saveiro.mp3",
    458703706137952285: "mutley.mp3",
    254393768067727360: "isolados.mp3",
    575432193795424257: "bolsonara.mp3",
    348484028367896586: "depressao.mp3",
    359083993989120000: "surprise.mp3"
}


@client.command(pass_context=True)
async def on_ready(ctx):
    print('Logged on as {0}!'.format(ctx.user))


@client.command(pass_context=True)
async def oi(ctx):
    await ctx.message.author.send("oi!")


@client.command(pass_context=True)
async def on_member_join(ctx):
    guild = ctx.guild
    if guild.system_channel is not None:
        mensagem = f'{ctx.mention} acabou de entrar no {guild.name}'
        await guild.system_channel.send(mensagem)


@client.command(pass_context=True)
async def carro(ctx):
    await ctx.message.channel.send("meu carro tá fazendo um barulho estranho ãããããããããããaãããããââââââââAÂÂÂÂÂ "
                                   "ééééééééééééèèèèèèèèè ôôôôôôôôôôôôâââââAÂÂââââããããã cadê o mecânico", tts=True)


@client.event
async def on_message(msg):
    if check_command(msg):
        command = msg.content[1:].lower() + ".mp3"
        if check_command_exists_at_resources(command):
            if member_is_not_at_voice_channel(msg):
                await msg.channel.send(f'<@{msg.author.id}>, você deve se conectar a um canal de voz para executar '
                                       f'esse comando.')
                return

            voice_client = await msg.author.voice.channel.connect()
            source = discord.FFmpegPCMAudio("resources/audio/" + command, options="-loglevel panic")
            await publish_message_gif(msg)
            await play_audio(source, voice_client)
        else:
            await client.process_commands(msg)


@client.command(pass_context=True)
async def commands(ctx):
    full_message = ""
    list_commands = list(map(lambda command: command[:-4], commands_audio)) + ["carro", "leave", "oi"]
    count = 0

    for command_formatted in list_commands:
        if count == 5:
            full_message = "\n" + full_message
            count = 0

        full_message = prefix + command_formatted + "\t" + full_message
        count += 1

    await ctx.message.channel.send(full_message)


@client.command(pass_context=True)
async def leave(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()


@client.event
async def on_voice_state_update(member, before, after):
    if valid_voice_update_event(member, before, after):

        channel = member.voice.channel

        if member_is_not_self_deaf_anymore(before, after):
            audio = audio_set.get("default")
        else:
            audio = audio_set.get(member.id, "audio.mp3")

        source = discord.FFmpegPCMAudio("resources/audio/" + audio, options="-loglevel panic")

        voice_client = await channel.connect()
        await sleep(0.5)
        await play_audio(source, voice_client)


def member_is_not_self_deaf_anymore(before, after):
    return before.self_deaf is True and after.self_deaf is False


def valid_voice_update_event(member, before, after):
    return not member.bot and after.channel is not None and (
            (before.self_deaf is True and after.self_deaf is False) or
            (before.channel != after.channel and after.channel != after.channel.guild.afk_channel))


async def publish_message_gif(msg):
    gif = msg.content[1:].lower() + ".gif"
    if gif in gif_files:
        await msg.channel.send(file=discord.File("resources/gif/" + gif))


async def play_audio(source, voice_client):
    voice_client.play(source)

    while voice_client.is_playing():
        await sleep(0.2)
    await voice_client.disconnect()


def check_command(msg):
    return msg.content and len(msg.content) > 0 and prefix == msg.content[0]


def check_command_exists_at_resources(command):
    return command in commands_audio


def member_is_not_at_voice_channel(msg):
    return msg.author.voice is None


token = os.environ.get('TOKEN', None)

keep_alive()
client.run(token)
