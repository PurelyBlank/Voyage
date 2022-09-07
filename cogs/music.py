import discord
from discord.ext import commands
import wavelink


class CustomPlayer(wavelink.Player):

    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.connect_nodes())


    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='127.0.0.1',
            port=2333,
            password='youshallnotpass'
        )
    
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')


    @commands.Cog.listener()
    async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason=None):
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)


    @commands.command(name='connect')
    async def connect(self, ctx):
        vc = ctx.voice_client # represents a discord voice connection
        
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("Please join a voice channel to connect.")

        if not vc:
            await ctx.author.voice.channel.connect(cls=CustomPlayer())
        else:
            await ctx.send("The bot is already connected to a voice channel")


    @commands.command(name='disconnect')
    async def disconnect(self, ctx):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command(name='play')
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        '''
        Fix play method, sends error saying not in vc when in vc
        Fix discord.Embed, not displaying embedded message in chat
        '''
        vc = ctx.voice_client
        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

        if vc.is_playing():

            vc.queue.put(item=search)

            await ctx.send(embed=discord.Embed(
                title=search.title,
                url=search.uri,
                author=ctx.author,
                description=f"Queued {search.title} in {vc.channel}"
            ))


        else:
            await vc.play(search)

            await ctx.send(embed=discord.Embed(
                title=vc.source.title,
                url=vc.source.uri,
                author=ctx.author,
                description=f"Playing {vc.source.title} in {vc.channel}"
            ))

    ### Test rest of commands out
    @commands.command(name='skip')
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("Nothing is playing.")
            if vc.queue.is_empty:
                return await vc.stop()

            await vc.seek(vc.track.length * 1000)
            if vc.is_paused():
                await vc.resume()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command(name='pause')
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
            else:
                await ctx.send("Nothing is playing.")
        else:
            await ctx.send("The bot is not connected to a voice channel")


    @commands.command(name='resume')
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
            else:
                await ctx.send("Nothing is paused.")
        else:
            await ctx.send("Voyage is not connected to a voice channel")


    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Could not find a track.")
        else:
            await ctx.send("Please join a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))