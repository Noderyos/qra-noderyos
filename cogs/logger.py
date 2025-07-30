from discord.ext import commands
from config_loader import config
import utils


class Logger(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("Logger cog loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(config.LOG_MEMBERS_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f":door: **{member.name}** has joined.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.bot.get_channel(config.LOG_MEMBERS_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f":wave: **{member.name}** has left.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(config.LOG_MESSAGES_CHANNEL_ID)
        if log_channel:
            author = message.author
            content = message.content or "[Empty or non-textual message]"
            await log_channel.send(
                f":wastebasket: **{author}** deleted a message in **{message.channel}**:\n" +
                f"```\n{content}\n```"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(config.LOG_MESSAGES_CHANNEL_ID)
        if log_channel and before.content != after.content:
            await log_channel.send(
                f":pencil2: **{before.author}** edited a message in **{before.channel}**:\n" +
                f"**Before:**\n```\n{before.content}\n```\n**After:**\n```\n{after.content}\n```"
            )


async def setup(bot: commands.Bot):
    cog = Logger(bot)
    await bot.add_cog(cog)
