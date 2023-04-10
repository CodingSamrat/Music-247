from discord.ext import commands
from discord.ext.commands.context import Context

from Bot.utils import LOG
from Bot.cogs.messages import base_help_message


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    @commands.command(aliases=["h"])
    async def help(self, ctx: Context):
        try:
            guild_nane = ctx.guild.name
            prefix = ctx.prefix

            msg = base_help_message(prefix, guild_nane)

            await ctx.send(f"{msg}")
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Help(client))
