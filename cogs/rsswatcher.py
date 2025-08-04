import discord
from discord.ext import commands, tasks
from config_loader import config
import utils
from rss import RSS


class RSSWatcher(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("RSSWatcher cog loaded")
        self.watcher.start()

    @tasks.loop(hours=1)
    async def watcher(self):
        for rss_url, channel_id in config.RSS_FEEDS:
            print("Watching", rss_url, channel_id)
            channel = self.bot.get_channel(channel_id)
            rss = RSS(rss_url, cache_file="cache/rss.json")
            embeds = rss.get_news()
            for embed_json in embeds:
                embed = discord.Embed().from_dict(embed_json)
                if channel:
                    await channel.send(embed=embed)

    @watcher.before_loop
    async def before_watcher(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    cog = RSSWatcher(bot)
    await bot.add_cog(cog)
