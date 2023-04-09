from discord.ext import commands
from discord.ext.commands.context import Context

from Bot.utils import LOG


def help_message(prefix, guild_name):
    msg = f"""
    ```
    Guild: {guild_name}
    Command Prefix: {prefix}
    
    These are some common Bot commands used in various situations:
    
        Command                 Descriptions
        -----------             ----------------
        Group Commands:
        config, cfg             Add or modify server/bot configuration
        
        Standalone Commands:
        help, h                 Shows this message     
        
        Group Commands have some sub-commands. Run them to know more.
    ```    
    """

    return msg


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
    @commands.command()
    async def help(self, ctx: Context):
        try:
            guild_nane = ctx.guild.name
            prefix = ctx.prefix

            msg = help_message(prefix, guild_nane)

            await ctx.send(f"{msg}")
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(Help(client))
