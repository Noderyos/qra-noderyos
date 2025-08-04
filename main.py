import sys
import asyncio
import discord
from discord.ext import commands
from config_loader import config
import utils
import random

import logging

logging.basicConfig(level=logging.INFO)

logger = utils.Logger()
logger.set_logger_name("Master")

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='..',
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=random.choice(config.ACTIVITY_MESSAGES)
    )
)


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
    await bot.load_extension("cogs.logger")
    await bot.load_extension("cogs.radio")
    await bot.load_extension("cogs.rsswatcher")
    await bot.start(config.BOT_TOKEN)

asyncio.run(main())
