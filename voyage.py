import discord
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
voyage = commands.Bot(command_prefix = '.', intents=intents) # prefix for running commands


@voyage.event
async def on_ready():
    print("Voyage is Online.")


@voyage.command()
async def ping(ctx):
    await ctx.send(f'Ping: {round(voyage.latency * 1000)}ms')


@voyage.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


@voyage.command()
async def load(ctx, extension):
    voyage.load_extension(f'cogs.{extension}')


voyage.run("BOT_KEY")