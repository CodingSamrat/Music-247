from discord.ext import commands
from discord.ext.commands.context import Context

from Bot.cogs.messages import music_help_message
from discord import FFmpegPCMAudio
from discord import utils

from youtubesearchpython import VideosSearch
from youtube_dl import YoutubeDL

from Bot.database import Database
from Bot.database import Collections
from Bot.utils import LOG
from Bot.config import CHANNEL

FFMPEG_OPTIONS = {
    "executable": "vendor/ffmpeg/ffmpeg.exe",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        #: Music staffs
        self.is_playing = False
        self.queue = []

    #: Bot Events
    #:
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.Cog.success(self)

    def _chech_link(self, _query):
        link = ""
        _is_playlist = False

        if _query.startswith("https://www.youtube.com/watch?v="):
            link = _query
            if "list=" in _query:
                _is_playlist = True
        elif _query.startswith("https://youtube.com/watch?v="):
            link = _query
            if "list=" in _query:
                _is_playlist = True
        else:
            videosSearch = VideosSearch(_query)
            link = videosSearch.result()["result"][0]["link"]

        return link, _is_playlist

    def _add_to_queue(self, _stream_url, _title):
        queue_obj = {
            "title": _title,
            "url": _stream_url
        }
        #: Append song to Queue...
        self.queue.append(queue_obj)

    async def _add_music_to_queue(self, _query):
        link, _is_playlist = self._chech_link(_query)

        #: If the given link is a playlist link
        if _is_playlist:
            self.queue = []

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url=link, download=False)

                for video in info["entries"]:
                    title = video["title"].split("|")[0]
                    stream_url = video["formats"][0]["url"]
                    self._add_to_queue(stream_url, title)

        #: If the given link is a song link
        elif not _is_playlist:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                video = ydl.extract_info(url=link, download=False)

                title = video["title"].split("|")[0]
                stream_url = video["formats"][0]["url"]

                self._add_to_queue(stream_url, title)

    def _play_music(self, ctx: Context):
        #: Check if queue is empty
        if len(self.queue) > 0:
            if not self.is_playing:
                #: Get source audio
                url = self.queue[0]["url"]
                title = self.queue[0]["title"]

                source = FFmpegPCMAudio(url, **FFMPEG_OPTIONS)

                #: Play music
                ctx.voice_client.play(source, after=lambda e: self._play_next_music(ctx))
                self.is_playing = True

                return title

            else:
                return "Already playing"

        elif len(self.queue) <= 0:
            self.is_playing = False
            return 0

    def _play_next_music(self, ctx: Context):
        self.is_playing = True
        if len(self.queue) > 0:
            #: remove the first element as you are currently playing it
            self.queue.pop(0)

            #: get the first url
            m_url = self.queue[0]['url']

            try:
                source = FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda e: self._play_next_music(ctx))

            except Exception as ex:
                print(ex)
        else:
            self.is_playing = False

    #: write commands here
    #:
    @commands.group(name="music", aliases=["m"], invoke_without_command=True)
    async def music(self, ctx: Context):
        try:
            guild_nane = ctx.guild.name
            prefix = ctx.prefix

            msg = music_help_message(prefix, guild_nane, "music")

            await ctx.send(f"{msg}")
        except Exception as e:
            print(e)

    @music.command(name="channel")
    async def channel(self, ctx: Context, _channel_id: str = None):
        channel_name = CHANNEL
        channel_id = _channel_id
        channel = None

        #: Create channel
        if channel_id is None:
            await ctx.guild.create_text_channel(CHANNEL)
            channel = utils.get(ctx.guild.channels, name=CHANNEL)
            channel_id = str(channel.id)
        #     pass
        #
        elif channel_id is not None:
            channel = ctx.guild.get_channel(int(channel_id))
            channel_name = ctx.guild.get_channel(int(channel_id)).name

        music_obj = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "queue": []
        }
        Database.update(Collections.GUILD, {"music": music_obj}, str(ctx.guild.id))
        await ctx.send(f"Music channel setup Successful!\n Now visit {channel.mention} ...")

    @music.command(name="play", aliases=["p"])
    async def play(self, ctx: Context):

        if ctx.author.voice is None:
            await ctx.send("`You are not in a voice channel`")
        elif ctx.author.voice is not None:
            await ctx.send(f"`Joining to - {ctx.author.voice.channel}`")

            voice_channel = ctx.author.voice.channel
            try:
                if ctx.voice_client is None:
                    await voice_channel.connect()
                    await ctx.send(f"`Connecting to {voice_channel}`")

                else:
                    await ctx.voice_client.move_to(voice_channel)
                    await ctx.send(f"`Moving to {voice_channel}`")

                r = self._play_music(ctx)
                if r == 0:
                    await ctx.send("`Queue is empty. Add music to queue, then play.`")

            except Exception as e:
                print(e)

    @music.command(name="pause", aliases=["ps"])
    async def pause(self, ctx: Context):
        await ctx.voice_client.pause()
        await ctx.send("`Paused`")

    @music.command(name="resume", aliases=["r"])
    async def resume(self, ctx: Context):
        await ctx.voice_client.resume()
        await ctx.send("`Resume`")

    @music.command(name="stop", aliases=["s"])
    async def stop(self, ctx: Context):
        await ctx.voice_client.stop()
        await ctx.send("`stopped`")

    @music.command(name="next", aliases=["n"])
    async def next(self, ctx: Context):

        ctx.voice_client.stop()

        self._play_next_music(ctx)
        await ctx.send("`Playing next music`")

    @music.command(name="add", aliases=["a"])
    async def add(self, ctx: Context, *, _query):
        await self._add_music_to_queue(_query)
        # await ctx.send("`adding`")

    @music.command(name="queue", aliases=["q"])
    async def queue(self, ctx: Context):
        music_list = [item["title"] for item in self.queue]
        msg = "Music in Queue - \n"
        if len(self.queue) > 0:
            for music in music_list:
                msg += music + "\n"
        else:
            msg += "No music in queue\nAdd music using `=music add [music link]`"
        await ctx.send(f"```{msg}```")


async def setup(client):
    await client.add_cog(Music(client))

