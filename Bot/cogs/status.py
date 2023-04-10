from discord.ext import commands
from discord.ext.commands.context import Context

# from discord import ...

from Bot.utils import LOG


class Status(commands.Cog):  # <- Change ->
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

    @commands.command(name="status", aliases=["stat"])
    async def status(self, ctx: Context):
        await ctx.send("Hii, Status")


async def setup(client):
    await client.add_cog(Status(client))  # <- Change ->

