import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation.py is ready")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title= "Success!", color=discord.Color.gold())
        conf_embed.add_field(name="Kicked:", value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title= "Success!", color=discord.Color.gold())
        conf_embed.add_field(name="Banned:", value=f"{member.mention} has been Banned from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)


    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title= "Success!", color=discord.Color.gold())
        conf_embed.add_field(name="Unbanned:", value=f"<@{userId}> has been Unbanned from the server by {ctx.author.mention}.", inline=False)

        await ctx.send(embed=conf_embed)

async def setup(client):
    await client.add_cog(Moderation(client))