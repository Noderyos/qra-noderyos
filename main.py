import sys
import asyncio
import discord
from discord.ext import commands
from config_loader import config
import utils

logger = utils.Logger()
logger.set_logger_name("Master")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='..', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synchronised {len(synced)} slash command(s)")
    except Exception as e:
        logger.error(f"Slash commands sync failed : {e}")

async def main():
    await bot.load_extension("cogs.main")
    await bot.start(config.BOT_TOKEN)

asyncio.run(main())
