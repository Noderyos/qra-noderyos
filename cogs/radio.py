import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from config_loader import config
import utils
import asyncio
import pickle


class Radio(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("Radio cog loaded")
        self.check_time.start()

    @app_commands.command(name="callsign", description="Lookup a radio callsign")
    async def callsign(self, interaction: discord.Interaction, callsign: str):
        country = utils.find_callsign(callsign)
        await interaction.response.send_message(
            f"`{callsign}` comes from `{country}`" if country
            else f"`{callsign}` origin is unknown :("
        )

    @tasks.loop(minutes=1)
    async def check_time(self):
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:
            channel = self.bot.get_channel(config.R4UAB_UPDATE_CHANNEL)
            for art in utils.get_new_r4uab_articles():
                art.update(utils.get_r4uab_article(art["post_id"]))

                embed = discord.Embed(title=art["title"], url=art["link"],
                                      description=art["content"], colour=0x5300a3)
                embed.set_author(name="R4UAB",
                                 url="https://r4uab.ru",
                                 icon_url="https://r4uab.ru/content/uploads/2018/01/cropped-favicon-1-32x32.png")
                for cat in art["categories"]:
                    embed.add_field(name="Category", value=cat, inline=True)
                embed.set_image(url=art["image_url"])
                embed.set_footer(text=art["pub_date"])
                if channel:
                    await channel.send(embed=embed)

    @check_time.before_loop
    async def before_check_time(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    cog = Radio(bot)
    await bot.add_cog(cog)
