import os
import asyncio
from dotenv import load_dotenv

from discord.ext import commands
from discord import Intents
from discord import Guild

# from Bot import __version__
from Bot.utils import LOG
from Bot.config import DEFAULT_CONFIG, COGS
from Bot.database import Database
from Bot.database import Collections

__all__ = ("boot", "__version__")
__version__ = "1.0.0"


def get_server_prefix(bot, message) -> str:
    guild_id = str(message.guild.id)
    guild_name = message.guild.name

    #: Getting Server data
    server_data = Database.find(Collections.GUILD, guild_id)

    if server_data:
        #: Fetching Prefix
        prefix = server_data["config"]["prefix"]

        return prefix

    else:
        server_data = {
            "_id": guild_id,
            "guild_name": guild_name,
            "in_guild": True,
            "config": DEFAULT_CONFIG
        }

        # col_guild.insert(server_data)
        Database.insert(Collections.GUILD, server_data)
        return DEFAULT_CONFIG["prefix"]


#: Configuring Intents
intents = Intents.default()
intents.message_content = True
intents.members = True
intents.auto_moderation = True


#: Initiating Bot
bot = commands.Bot(command_prefix=get_server_prefix, intents=intents)
bot.remove_command('help')


#:  Events Start Here
@bot.event
async def on_ready():
    LOG.success(TEXT="Bot is Up & Running...")
    print(f"Bot: {bot.user.name}")
    print(f"version: {__version__}")
    print(f"No. of Guilds: {len(bot.guilds)}")
    print("* * *\n")


@bot.event
async def on_guild_join(guild: Guild):

    #: Collect Guild info
    guild_id = str(guild.id)
    guild_name = guild.name
    in_guild = True
    config = DEFAULT_CONFIG

    #: Get server data from database
    server_data = Database.find(Collections.GUILD, guild_id)

    #: Check if data server data already exist
    if server_data:

        #: Update Server data
        Database.update(Collections.GUILD, {"in_guild": in_guild}, guild_id)

    else:
        #: Insert Data into database
        server_data = {
            "_id": guild_id,
            "guild_name": guild_name,
            "in_guild": in_guild,
            "config": config
        }

        #: writing to database
        Database.insert(Collections.GUILD, server_data)



@bot.event
async def on_guild_remove(guild: Guild):
    #: Collect Guild info
    guild_id = str(guild.id)
    in_guild = False

    #: Updating database
    Database.update(Collections.GUILD, {"in_guild": in_guild}, guild_id)


#: Loading Extensions(cogs) & Starting Bot
async def start_bot(token):

    async with bot:
        LOG.debug(TEXT="Loading Extensions")

        #: Load all cogs
        for cog in COGS:
            try:
                await bot.load_extension(f"Bot.cogs.{cog}")
                LOG.debug(TEXT=f"Loading - Bot.cogs.{cog}")

            except Exception as e:
                LOG.error(TEXT=f"{e}")

        print("")
        LOG.debug(TEXT="Initiating Bot...")
        await bot.start(token)


#: Entrypoint of the Bot
def boot():
    #: Loading Bot Token
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    #: Initiating Bot
    asyncio.run(start_bot(TOKEN))


if __name__ == "__main__":
    pass
