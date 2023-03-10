import os
import discord
from discord.ext import commands
from discord.utils import get
from asyncio import sleep

intents = discord.Intents.default()
intents.members = True

prefix = '>'
client = commands.Bot(command_prefix=prefix, intents=intents)

audio_files = os.listdir("resources/audio")
gif_files = os.listdir("resources/gif")
soundtrack_files = os.listdir("resources/soundtracks")

@client.command(pass_context=True)
async def carro(ctx):
    await ctx.message.channel.send("meu carro tá fazendo um barulho estranho ãããããããããããaãããããââââââââAÂÂÂÂÂ "
                                   "ééééééééééééèèèèèèèèè ôôôôôôôôôôôôâââââAÂÂââââããããã cadê o mecânico", tts=True)


@client.event
async def on_message(msg):
    if check_valid_command(msg):
        command = msg.content[1:].lower()

        if member_is_not_at_voice_channel(msg):
            await msg.channel.send(f'<@{msg.author.id}>, você deve se conectar a um canal de voz para executar '
                                   f'esse comando.')
            return

        await publish_message_gif(msg)
        await play_audio(f"audio/{command}.mp3", msg.author.voice.channel)

        if check_command_exists_at_resources(f"{command}.mp3", audio_files) is False \
                and check_command_exists_at_resources(f"{command}.gif", gif_files) is False:
            await client.process_commands(msg)


@client.event
async def on_voice_state_update(member, before, after):
    if valid_voice_update_event(member, before, after):

        channel = member.voice.channel

        if member_is_not_self_deaf_anymore(before, after):
            audio = "soundtracks/default.mp3"
        else:
            audio = get_soundtrack_by_user(member.id)

        await sleep(0.5)
        await play_audio(audio, channel)


@client.command(pass_context=True)
async def commands(ctx):
    full_message = ""
    list_commands = list(map(lambda command: command[:-4], audio_files)) + ["carro", "leave", "oi"]
    commands_per_line = 0

    for command_formatted in list_commands:
        if commands_per_line == 5:
            full_message = "\n" + full_message
            commands_per_line = 0

        full_message = prefix + command_formatted + "\t" + full_message
        commands_per_line += 1

    await ctx.message.channel.send(full_message)


@client.command(pass_context=True)
async def leave(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()


async def play_audio(audio, channel):
    if check_command_exists_at_resources(audio):
        source = discord.FFmpegPCMAudio(f"resources/{audio}", options="-loglevel panic")
        voice_client = await channel.connect()
        voice_client.play(source)

        while voice_client.is_playing():
            await sleep(0.2)
        await voice_client.disconnect()


async def publish_message_gif(msg):
    gif = msg.content[1:].lower() + ".gif"
    if gif in gif_files:
        await msg.channel.send(file=discord.File("resources/gif/" + gif))


def member_is_not_self_deaf_anymore(before, after):
    return before.self_deaf is True and after.self_deaf is False


def valid_voice_update_event(member, before, after):
    return not member.bot and after.channel is not None and (
            (before.self_deaf is True and after.self_deaf is False) or
            (before.channel != after.channel and after.channel != after.channel.guild.afk_channel))


def check_valid_command(msg):
    return msg.content and len(msg.content) > 0 and prefix == msg.content[0] and not msg.author.bot


def check_command_exists_at_resources(command):
    command_split = command.split("/")
    name_file = command_split[-1]
    return (name_file in audio_files) or (name_file in soundtrack_files)


def get_soundtrack_by_user(id):
    name = f"{id}.mp3"

    if (name in soundtrack_files):
        return f"soundtracks/{name}"

    return "soundtracks/default.mp3"


def member_is_not_at_voice_channel(msg):
    return msg.author.voice is None
