import discord, db.database as database, random, typing
import discord, os, asyncio
from discord.ext import commands

class roleinfO(commands.Cog):
    def __init__(self, client):
        self.bot = client  



    @commands.command(
        aliases=['ri', 'inforole', 'roleinformation', 'rinfo'],
        usage = 'Manage roles',
        description = 'View certain information upon the given role',
        brief = 'role',
        help = '```Syntax: roleinfo [role]\nExample: roleinfo @Owner```'
        )
    async def roleinfo(self, ctx, *, role: discord.Role = None):
        if role is None:
            role = ctx.author.top_role
        guild = ctx.guild
        since_created = (ctx.message.created_at - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{} ({} days ago)".format(role_created, since_created)
        users = len([x for x in guild.members if role in x.roles])
        if str(role.colour) == "#000000":
            colour = "#000000"
            colour = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = str(role.colour).upper()
            color = role.colour
        embed = discord.Embed()
        embed.add_field(name='**Role Name:**', value=f"{role.name}", inline=False)
        embed.add_field(name='**Role ID:**', value=f"{role.id}", inline=False)
        embed.add_field(name="**Users In Role:**", value=f"{users}", inline=False)
        embed.add_field(name="**Mentionable:**", value=f"{role.mentionable}", inline=True)
        embed.add_field(name="**Hoisted:**", value=f"{role.hoist}", inline=True)
        embed.add_field(name="**Position:**", value=f"{role.position}", inline=False)
        embed.add_field(name="**Managed:**", value=f"{role.managed}", inline=True)
        embed.add_field(name="**Colour:**", value=f"{colour}", inline=True)
        embed.add_field(name='**Creation Date:**', value=f"{created_on}", inline=False)
        embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
        embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        await ctx.send(embed=embed)




async def setup(client): 
   await client.add_cog(roleinfO(client))