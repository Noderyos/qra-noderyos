import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from config_loader import config
import utils


class Radio(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("Radio cog loaded")

    @app_commands.command(name="callsign", description="Lookup a radio callsign")
    async def callsign(self, interaction: discord.Interaction, callsign: str):
        country = utils.find_callsign(callsign)
        await interaction.response.send_message(
            f"`{callsign}` comes from `{country}`" if country
            else f"`{callsign}` origin is unknown :("
        )


async def setup(bot: commands.Bot):
    cog = Radio(bot)
    await bot.add_cog(cog)
