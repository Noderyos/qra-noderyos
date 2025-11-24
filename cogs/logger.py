from discord.ext import commands
from config_loader import config
import utils
import discord

class Logger(commands.Cog, utils.Logger):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.info("Logger cog loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_message(
            config.LOG_MEMBERS_CHANNEL_ID,
            f":door: **{member.name}** has joined."
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.send_message(
            config.LOG_MEMBERS_CHANNEL_ID,
            f":wave: **{member.name}** has left."
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        author = message.author
        content = message.content or "[Empty or non-textual message]"

        await self.send_message(
            config.LOG_MESSAGES_CHANNEL_ID,
            f":wastebasket: **{author}** deleted a message in **{message.channel}**:\n"
            f"```\n{content}\n```"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return

        await self.send_message(
            config.LOG_MESSAGES_CHANNEL_ID,
            f":pencil2: **{before.author}** edited a message in **{before.channel}**:\n"
            f"**Before:**\n```\n{before.content}\n```"
            f"**After:**\n```\n{after.content}\n```"
        )
    
    async def send_message(self, channel_or_thread_id, content):
        channel = await self.bot.fetch_channel(channel_or_thread_id)

        if isinstance(channel, (discord.Thread,)):
            if channel.archived:
                await channel.edit(archived=False)
            return await channel.send(content)
        elif isinstance(channel, discord.TextChannel):
            return await channel.send(content)
        else:
            self.error(f"Channel type {type(channel)} not supported")

async def setup(bot: commands.Bot):
    cog = Logger(bot)
    await bot.add_cog(cog)
