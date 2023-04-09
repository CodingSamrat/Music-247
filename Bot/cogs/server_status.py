from discord.ext import commands
from discord.ext.commands.context import Context

from discord import Guild

from Bot.utils import LOG


class ServerStatus(commands.Cog):  # <- Change ->
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    @commands.command()
    async def ping(self, ctx: Context):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Bot latency: `{latency} ms`")


async def setup(client):
    await client.add_cog(ServerStatus(client))
