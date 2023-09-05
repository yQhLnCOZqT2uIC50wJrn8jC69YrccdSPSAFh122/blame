import discord, os, asyncio
from discord.ext import commands

class StatuS(commands.Cog):
    def __init__(self, client):
        self.bot = client  

    @commands.command(
        usage = "Send Messages",
        description = "View yours or another member's status",
        brief = 'member',
        help = "```Syntax: status [member]\nExample: status @jacob```"
    )
    async def status(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        for s in member.activities:
            if isinstance(s, discord.CustomActivity):
                return await ctx.send(f"{member.name} status is **{s}** ")
            else:
                return await ctx.send(f"{member.name} has no custom status")




async def setup(client): 
   await client.add_cog(StatuS(client))


