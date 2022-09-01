import asyncio
import os

import discord
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents) # prefix for running commands


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Cog")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Cog")

async def load_cog():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded {filename[:-3]}")
                # prints out on terminal cog file has been loaded
            except Exception as e:
                print(f"Failed to load {filename[:-3]}") 
                # prints out on terminal that the cog file has not been loaded correctly


BOT_KEY = "MTAxMjg5NTM5MDA0NTA0NDczNg.G43tZe.xdaI4oXHkbakEalS1rq2gmwmd66UB6Yrt0hwss" 

if __name__ == '__main__':
    asyncio.run(load_cog())
    client.run(BOT_KEY)