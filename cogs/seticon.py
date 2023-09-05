import discord, db.database as database, random, typing, aiohttp
import discord, os, asyncio
from discord.ext import commands

class setIcoN(commands.Cog):
    def __init__(self, client):
        self.bot = client  

    @commands.command(
        aliases = ['setguildicon', 'setserverpfp', 'setservericon'],
        usage = "Manage guild",
        description = "Change the servers icon to the given one",
        brief = 'image_url, image',
        help = f"```Syntax: seticon [image_url]\nExample: seticon https://blame.gg/avatars/blameicon.png?size=1024```"
    )
    @commands.has_permissions(manage_guild=True)
    @commands.has_permissions(manage_guild=True)
    async def seticon(self, ctx, image_url=None):
        vaild_urls = ['https', 'http']
        attachments = ctx.message.attachments
        #if image_url == None:
            #return await ctx.send("Please provide an image or image_url")
        if str(image_url).lower().startswith(tuple(vaild_urls)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as r:
                        read = await r.read()
                await ctx.guild.edit(icon=read, reason=f"Requested by {ctx.author}")
                return await ctx.send("success")
            except Exception as e:
                return await ctx.send("Improper url")
        if attachments:
            async with aiohttp.ClientSession() as session:
                async with session.get(attachments[0].url) as r:
                    scan = await r.read()
            await ctx.guild.edit(icon=scan, reason=f"Requested by {ctx.author}")
            return await ctx.send("success")
        else:
            return await ctx.send("Please provide a supported image or image_url")






async def setup(client): 
   await client.add_cog(setIcoN(client))