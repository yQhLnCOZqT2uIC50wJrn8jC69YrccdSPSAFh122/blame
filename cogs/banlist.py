from pydoc import describe
import discord, db.database as database, Core.utils as util
import discord, os, asyncio
from discord.ext import commands

class banLisT(commands.Cog):
    def __init__(self, client):
        self.bot = client  


    @commands.command(
        aliases = ['bans', 'serverbans'],
        usage = 'Ban members',
        description = "View the servers ban list (limit=100)",
        brief = 'None',
        help = "```Example: banlist"
    )
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        bans = [entry.user.name async for entry in ctx.guild.bans(limit=100)]
        totalbans = [entry.user.name async for entry in ctx.guild.bans(limit=10000)]
        ban_reasons = [entry.reason async for entry in ctx.guild.bans(limit=100)]
        here = [f"**{bans}**: ``{ban_reasons}``" for bans, ban_reasons in zip(bans, ban_reasons)]
        content = discord.Embed(description="")
        content.set_author(name=f"{ctx.guild.name}'s ban list", icon_url=ctx.guild.icon.url)
        content.set_footer(text=f'({len(here)} viewable bans, reasons) ∙ ({len(totalbans) - len(here)} unviewable bans) ∙ ({len(totalbans)} total bans)')
        content.set_thumbnail(url=ctx.guild.icon.url)
        content.color = discord.Color.blurple()
        rows = []

        for count, i in enumerate(here, start=1):
            rows.append(f"``{count})`` {i}")
        await util.send_as_pages(ctx, content, rows)

async def setup(client): 
   await client.add_cog(banLisT(client))