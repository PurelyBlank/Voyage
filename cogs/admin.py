import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(color=discord.Colour.dark_orange(), title="", description="")
            embed.add_field(name="Kicked:", 
                
                value=f"""
                **{member}** has been kicked.
                Reason: **{reason}** 
                """, inline=True)
            
            await ctx.reply(embed=embed)

        except discord.Forbidden:
            await ctx.send(f'You do not have the proper permissions to kick.')
        except discord.HTTPException:
            await ctx.send(f'Kicking failed.')


    @commands.command(name="ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(color=discord.Colour.dark_red(), title="", description="")
            embed.add_field(name="Banned:", 
                
                value=f"""
                **{member}** has been **banned** from the server.
                Reason: **{reason}** 
                """, inline=True)
            
            await ctx.reply(embed=embed)

        except discord.Forbidden:
            await ctx.send(f'You do not have the proper permissions to ban.')
        except discord.NotFound:
            await ctx.send(f'{member} not found!')
        except discord.HTTPException:
            await ctx.send('Banning Failed.')


    @commands.command(name="unban")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member: discord.User, reason=None):
        try:
            await ctx.guild.unban(member)
            embed = discord.Embed(color=discord.Colour.dark_red(), title="", description="")
            embed.add_field(name="Unbanned:", 
                
                value=f"""
                **{member}** has been **unbanned** from the server.
                Reason: **{reason}** 
                """, inline=True)
            
            await ctx.reply(embed=embed)

        except discord.NotFound:
            await ctx.send(f'{member} not found!')
        except discord.Forbidden:
            await ctx.send(f'Do not have proper permission to unban!')
        except discord.HTTPException:
            await ctx.send(f'Unbanning failed.')


    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        if amount > 100:
            user = ctx.author.name
            await ctx.send(f"{user}, you cannot clear that amount!")
        else:
            await ctx.channel.purge(limit=amount + 1)


async def setup(bot):
    await bot.add_cog(Admin(bot))