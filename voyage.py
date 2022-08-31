import os
import discord
from discord.ext import commands
import asyncio


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents) # prefix for running commands


@client.event
async def on_ready():
    print("Voyage is Online.")


# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Ping: {round(voyage.latency * 1000)}ms')

# @client.command()
# async def clear(ctx, amount=1):
#     await ctx.channel.purge(limit=amount + 1)


# @client.command()
# async def kick(ctx, member : discord.Member, *, reason=None):
#     await member.kick(reason=reason)


# @client.command()
# async def ban(ctx, member : discord.Member, *, reason=None):
#     await member.ban(reason=reason)
#     await ctx.send(f'Banned {member.mention}')


# @client.command()
# async def unban(ctx, *, member):
#     banned_users = await ctx.guild.bans()
#     member_name, member_discriminator = member.split('#')

#     for entries in banned_users:
#         user = entries.user
#         if (user.name and user.discriminator) == (member_name, member_discriminator):
#             await ctx.guild.unban(user)
#             await ctx.send(f'Unbanned {user.mention}')
#             return


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
            except Exception as e:
                print("Failed")

BOT_KEY = "" 

if __name__ == '__main__':
    asyncio.run(load_cog())
    client.run(BOT_KEY)