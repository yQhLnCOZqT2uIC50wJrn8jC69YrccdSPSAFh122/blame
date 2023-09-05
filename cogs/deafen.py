import discord, db.database as database, typing, Core.utils as util
from matplotlib.pyplot import text
import discord, os, asyncio
from discord.ext import commands

class deafeN(commands.Cog):
    def __init__(self, client):
        self.bot = client 



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def deafen(self, ctx, member: discord.Member=None):
        try:
            if member:
                if member.voice:
                    if member.top_role.position > ctx.author.top_role.position:
                        return await ctx.send("You cannot deafen someone higher than you")
                    else:
                        await member.edit(deafen=True)
                        return await ctx.send(f"{member} has been deafened")
                else:
                    return await ctx.send("theyre not connected")
            else:
                return await ctx.send("Please give a member to deafen")
        except Exception as e:
            print(e)






async def setup(client): 
   await client.add_cog(deafeN(client))