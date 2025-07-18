import sys

import discord
from discord.ext import commands
from config_loader import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='..', intents=intents)

@bot.event
async def on_ready():
    print(f'[INFO] Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"[INFO] Synchronised {len(synced)} slash command(s)")
    except Exception as e:
        print(f"[ERROR] Slash commands sync failed : {e}", file=sys.stderr)

@bot.tree.command(name="ping", description="ping pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

bot.run(config.BOT_TOKEN)