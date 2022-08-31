import discord
from discord.ext import commands

# use cog for all commands
# maybe use inheritence for different grouping of commands

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'Ping: {round(self.client.latency * 1000)}ms')


async def setup(client):
    await client.add_cog(Commands(client))