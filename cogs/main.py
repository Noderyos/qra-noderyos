import discord
from discord.ext import commands
from discord import app_commands
import utils


class Main(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("Main cog loaded")

    @app_commands.command(name="ping", description="ping pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")


async def setup(bot: commands.Bot):
    cog = Main(bot)
    await bot.add_cog(cog)
