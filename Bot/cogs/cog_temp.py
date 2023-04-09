from discord.ext import commands
from discord.ext.commands.context import Context

# from discord import ...

from Bot.utils import LOG


class ClassName(commands.Cog):  # <- Change ->
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
    async def DemoCommand(self, ctx: Context):
        await ctx.send("Hii, From Demo Command")


async def setup(client):
    await client.add_cog(ClassName(client))  # <- Change ->

