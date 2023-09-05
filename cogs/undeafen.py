import discord, db.database as database, typing, Core.utils as util, random
from matplotlib.pyplot import text
import discord, os, asyncio
from discord.ext import commands
from datetime import datetime

class UndeafeN(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def undeafen(self, ctx, member: discord.Member=None):
        try:
            if member:
                if member.voice:
                    if member.top_role.position > ctx.author.top_role.position:
                        return await ctx.send("You cannot undeafen someone higher than you")
                    else:
                        await member.edit(deafen=False)
                        return await ctx.send(f"{member} has been undeafened")
                else:
                    return await ctx.send("not connected")
            else:
                return await ctx.send("Please give a member to undeafen")
        except Exception as e:
            print(e)



async def setup(client): 
   await client.add_cog(UndeafeN(client))