import discord
from discord.ext import commands

# use cog for all commands
# maybe use inheritence for different grouping of commands

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'Ping: {round(self.bot.latency * 1000)}ms')


async def setup(bot):
    await bot.add_cog(Commands(bot))