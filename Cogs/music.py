import discord
from discord.ext import commands
import random
import asyncio
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):
    ffmpegopts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    def __init__(self, source, *, data):
        super().__init__(source)

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):

        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source, **cls.ffmpegopts), data=data)

    @classmethod
    async def regather_stream(cls, data, *, loop):

        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'], **cls.ffmpegopts), data=data)


class MyQueue(asyncio.Queue):

    def __len__(self):
        return self.qsize()

    def shuffle(self):
        random.shuffle(self._queue)


class MusicPlayer:
    """
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_cog', 'queue', 'next', 'current', '_channel', 'np')

    def __init__(self, ctx):

        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel

        self._cog = ctx.cog
        self.np = None

        self.queue = MyQueue()
        self.next = asyncio.Event()

        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""

        await self.bot.wait_until_ready()

        while True:
            self.next.clear()
            # Try to get the next song within 2 minutes.
            # If no song will be added to the queue in time,
            try:
                async with timeout(120):  # 2 minutes
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue
            self.current = source
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send('Now Playing: `{}`'.format(source.title))
            await self.next.wait()
            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


async def __local_check(ctx):
    """A local check which applies to all commands in this cog."""
    if not ctx.guild:
        raise commands.NoPrivateMessage
    return True


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):

        self.bot = bot
        self.players = {}
        self.loop = True

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        player = self.players.get(ctx.guild.id)
        if not player:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    def cog_unload(self):
        for player in self.players.values():
            self.bot.loop.create_task(player.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_command_error(self, ctx, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command()
    async def join(self, ctx):
        """Joins a channel"""
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song."""
        self.loop = False
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.join)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)

        await player.queue.put(source)

    @commands.command()
    async def skip(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client
        self.loop = False

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffles the queue."""
        ctx.player_state = self.get_player(ctx)
        if len(ctx.player_state.queue) == 0:
            return await ctx.send('Empty queue.')

        ctx.player_state.queue.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name="leave")
    async def stop(self, ctx):
        """Stop the currently playing song and destroy the player."""
        vc = ctx.voice_client
        self.loop = False

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        await self.cleanup(ctx.guild)

    @commands.command(name='repeat')
    async def _loop(self, ctx, *, search: str):
        """Play a song on repeat"""
        if not self.loop:
            self.loop = True
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.join)

        player = self.get_player(ctx)
        while self.loop and ctx.voice_client.is_connected():
            if not ctx.voice_client.is_playing():
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                await player.queue.put(source)
            else:
                await asyncio.sleep(10)
                continue

    @shuffle.before_invoke
    @_loop.before_invoke
    @skip.before_invoke
    @stop.before_invoke
    @join.before_invoke
    @play.before_invoke
    async def ensure_voice_state(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')


def setup(bot):
    bot.add_cog(Music(bot))
