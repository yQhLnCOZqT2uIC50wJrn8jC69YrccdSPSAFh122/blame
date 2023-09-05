import discord, Core.utils as util
import discord, os, asyncio
from discord.ext import commands

class BotLisT(commands.Cog):
    def __init__(self, client):
        self.bot = client  


    @commands.command(
        aliases = ['bots', 'serverbots'],
        usage = "Send messages",
        description = "View all the bots in the server",
        brief = 'None',
        help = "```Example: bots```"
    )
    async def botlist(self, ctx):
        rows = []
        content = discord.Embed(description="", timestamp=ctx.message.created_at)
        content.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar)
        content.set_thumbnail(url=ctx.guild.icon.url)
        content.color = discord.Color.blurple()
        for m in ctx.guild.members:
            if m.bot:
                rows.append(f" {m.mention} - ``{m.id}``")
                content.set_footer(text=f"({len([m for m in ctx.guild.members if m.bot])} Total bots) • ({len([m for m in ctx.guild.members if m.bot and m.public_flags.verified_bot])} Verified) • ({len([m for m in ctx.guild.members if m.bot and not m.public_flags.verified_bot])} Unverified)")
        await util.send_as_pages(ctx, content, rows)








async def setup(client): 
   await client.add_cog(BotLisT(client))