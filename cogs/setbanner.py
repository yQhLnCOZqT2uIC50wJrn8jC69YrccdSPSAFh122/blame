import discord, db.database as database, random, typing, aiohttp, os, asyncio
from discord.ext import commands

class setbanneR(commands.Cog):
    def __init__(self, client):
        self.bot = client 

    @commands.command(
        aliases = ['bannerset', 'changebanner', 'newbanner', 'setserverbanner'],
        usage = 'Manage guild',
        description = "Change the servers banner to the given one",
        brief = 'image_url, image',
        help = "```Syntax: setbanner [image_url]\nExample: setbanner https://blame.gg/avatars/blameicon.png?size=960```"
    )
    @commands.has_permissions(manage_guild=True)
    async def setbanner(self, ctx, image_url=None):
        vaild_urls = ['https', 'http']
        attachments = ctx.message.attachments
        #if image_url == None:
            #return await ctx.send("Please provide an image or image_url")
        if str(image_url).lower().startswith(tuple(vaild_urls)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as r:
                        read = await r.read()
                await ctx.guild.edit(banner=read, reason=f"Requested by {ctx.author}")
                return await ctx.send("success")
            except Exception as e:
                return await ctx.send("Improper url")
        if attachments:
            async with aiohttp.ClientSession() as session:
                async with session.get(attachments[0].url) as r:
                    scan = await r.read()
            await ctx.guild.edit(banner=scan, reason=f"Requested by {ctx.author}")
            return await ctx.send("success")
        else:
            return await ctx.send("Please provide a supported image or image_url")


async def setup(client): 
   await client.add_cog(setbanneR(client))