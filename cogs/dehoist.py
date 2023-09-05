import discord, db.database as database, typing, Core.utils as util, time
import discord, os, asyncio
from discord.ext import commands

class deshoisT(commands.Cog):
    def __init__(self, client):
        self.bot = client 


    @commands.command(
        aliases = ['dhoist', 'dehoist'],
        usage = 'Manage nicknames, Manage server',
        description = "Dehoist all hoisted nicknames within a role such as, nicknames that begin with !, ?, and special characters",
        brief = 'role',
        help = "```Syntax: dehoistnames [role]\nExample: dehoistnames @Members\nNote -> This only dehoists member's nicknames within the role.```"
    )
    @commands.has_permissions(manage_nicknames=True, manage_guild=True)
    async def dehoistnames(self, ctx, role: discord.Role=None):
        try:
            if role==None:
                return await ctx.send("Please be sure to provide a role.")
            else:
                count = 0
                for member in role.members:
                    count = count + 1
                    time_take = count / 20
                    break
                await ctx.send(f"```Analyzing {len(role.members)} members within role: {role.name}\nWill take approximatley: {time_take} minutes```")
                await ctx.message.add_reaction("✅")

                for member in role.members:
                    hoisted = ['!', '?']
                    if str(member.nick).startswith(tuple(hoisted)):
                        await member.edit(nick=member.nick.replace("!" or '?', ''), reason=f"Dehoisting nicknames within role: [ {role.name} ]. Author - {ctx.message.author}")
                        await asyncio.sleep(3)
        except:
            pass


                    



async def setup(client): 
   await client.add_cog(deshoisT(client))