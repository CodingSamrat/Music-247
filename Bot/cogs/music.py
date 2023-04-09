from discord.ext import commands
from discord.ext.commands.context import Context

# from discord import ...

from Bot.utils import LOG


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    @commands.group(name="music")
    async def music(self, ctx: Context):
        await ctx.send("Hii, From Music Command")

    @music.group(name="music")
    async def play(self, ctx: Context):
        await ctx.send("`Playing`")


async def setup(client):
    await client.add_cog(Music(client))

