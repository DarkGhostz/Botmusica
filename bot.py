import discord
import youtube_dl
import asyncio
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

token = os.getenv('token')



# Crie um objeto bot do discord


bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())
youtube = build('youtube', 'v3', developerKey='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')



# Quando o bot estiver pronto, imprima uma mensagem no console
@bot.event
async def on_ready():
    print('Bot de música pronto')

# Comando para fazer o bot entrar em um canal de voz
@bot.command()
async def oi(ctx):
    await ctx.reply(f"Salve, aqui é o bot de musica, prazer {ctx.author}")

# Comando para fazer o bot sair de um canal de voz
@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

# Comando para reproduzir uma música
@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    # conecta ao canal de voz do usuário que executou o comando
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    # busca o vídeo no YouTube usando a biblioteca youtube-dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if 'Music' not in info.get('categories', []):
            await ctx.send('Este vídeo não é um videoclipe.')
            await voice_client.disconnect()
            return
        ydl.download([url])
        video_url = ydl.prepare_filename(info)

    # reproduz o áudio do vídeo usando o FFmpeg
    player = voice_client.play(discord.FFmpegPCMAudio(video_url))
    await asyncio.sleep(0.5) # tempo para reproduzir o vídeo
    await voice_client.disconnect()
    async def play(ctx, url: str, query):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
        return

    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()

    # Para a reprodução atual, se houver
    if voice_client.is_playing():
        voice_client.player()

    player = await voice_client.create_ytdl_player(url)
    player.start()
    # Outro código para pesquisar e reproduzir a música usando o YouTube API
    # ...


# Rode o bot
bot.run(token)