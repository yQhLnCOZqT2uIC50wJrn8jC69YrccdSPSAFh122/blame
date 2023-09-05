import discord, db.database as database, typing, Core.utils as util, time
import discord, os, asyncio
from discord.ext import commands

class iNrolE(commands.Cog):
    def __init__(self, client):
        self.bot = client 


    @commands.command(
        aliases = ['inr', 'ir', 'inrol'],
        usage = 'Manage roles',
        description = 'View the members and amount within the given role',
        brief = 'role',
        help = "```Syntax: inrole [role]\nExample: inrole @Users```"
    )
    @commands.has_permissions(manage_roles=True)
    async def inrole(self, ctx, *, r: typing.Union[ discord.Role, str ]=None):
        if r == None:
            await util.send_command_help(ctx)
        if isinstance(r, discord.Role):
            role=r
            content = discord.Embed(title=f"Members in role: {role.name}")
            content.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            rows = []
            for member in role.members:
                rows.append(f"{member.mention}")
            content.description=rows
            content.set_footer(text=f"{len(role.members)} member(s) ∙ {ctx.guild.name}")
            content.color = discord.Color.blurple()
            await util.send_as_pages(ctx, content, rows)
        if isinstance(r, str):
            lis=[]
            for rr in ctx.guild.roles:
                if r in str(rr.name) or r.lower() in str(rr.name).lower():
                    role=rr
                    content = discord.Embed(title=f"Members in role: {role.name}")
                    content.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                    rows = []
                    for member in role.members:
                        if len(role.members) > 200:
                            return await ctx.send("Too large")
                        else:
                            pass
                        rows.append(f"{member.mention}")
                    content.color = discord.Color.blurple()
                    content.set_footer(text=f"{len(role.members)} member(s) ∙ {ctx.guild.name}")
                    await util.send_as_pages(ctx, content, rows)


async def setup(client): 
   await client.add_cog(iNrolE(client))