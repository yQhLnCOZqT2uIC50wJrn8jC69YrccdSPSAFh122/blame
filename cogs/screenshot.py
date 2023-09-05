import discord, db.database as database
import discord, os, asyncio, aiohttp
import time
from discord.ext import commands

async def api_req(url):
    token = "T9PZN6A-7A0M90W-GM4WJKF-APCTFJ0"
    query = 'https://shot.screenshotapi.net/screenshot'
    params = f"?token={token}&url={url}"
    obj = query + params
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(obj) as response:
                try:
                    data = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    return None
            if response.status == 200:
                return data


class screenShoT(commands.Cog):
    def __init__(self, client):
        self.bot = client  

    @commands.command(
        aliases = ['screenshot'],
        usage = "Send messages",
        description = "Take a screenshot of the specified URL",
        brief = "query",
        help = "```Syntax: screenshot [url]\nExample: screenshot https://blame.gg```"

    )
    async def ss(self, ctx, query=None):
        try:
            if query == None:
                return await ctx.send("need link pls")
            if query:
                async with ctx.channel.typing():
                    t = time.localtime(time.time())
                    subj = await api_req(url=query)
                    if subj is None:
                        return None
                    else:
                        image = subj['screenshot']
                        #tim = subj.request_time
                        embed = discord.Embed(title="Screenshot results..", description=f"**[{query}](https://blame.gg)**")
                        embed.colour = discord.Colour.blurple()

                        embed.set_image(url=image)
                        embed.set_footer(text=f"Delay: {t.tm_sec}s ∙ is_fresh: {subj['is_fresh']} ∙ Snapped: {subj['created_at']}")
                        return await ctx.send(embed=embed)
            else:
                return await ctx.send("error")
        except Exception as e:
            print(e)



async def setup(client): 
   await client.add_cog(screenShoT(client))