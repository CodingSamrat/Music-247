from discord.ext import commands
from discord.ext.commands.context import Context

from discord import Guild

from Bot.utils import LOG
from Bot.database import Database, Collections
from Bot.cogs.messages import config_help_message


class ServerConfig(commands.Cog):  # <- Change ->
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    #: write commands here
    #:
    @commands.group(name="config", aliases=["cfg"], invoke_without_command=True)
    async def config(self, ctx: Context):
        try:
            guild_nane = ctx.guild.name
            prefix = ctx.prefix

            msg = config_help_message(prefix, guild_nane, "config")

            await ctx.send(f"{msg}")
        except Exception as e:
            print(e)

    @config.command()
    async def prefix(self, ctx: Context, _prefix):

        try:
            guild_id = str(ctx.guild.id)
            config_data = Database.find(Collections.GUILD, guild_id)["config"]

            prefix = config_data["prefix"]
            config_data["prefix"] = _prefix

            Database.update(Collections.GUILD, {"config": config_data}, guild_id)
            await ctx.send(f"`Command Prefix Updated to {_prefix}`")
        except Exception as e:
            print(e)


async def setup(client):
    await client.add_cog(ServerConfig(client))
