from statcord import StatcordClient
from discord.ext import commands
import os, asyncio, aiohttp


class MyStatcordCog(commands.Cog): #website is statcord.com sometimes it will go down and log in the console the errors but its okay just ignore em it will log all the missing logs when the site is back up
    def __init__(self, bot):
        self.bot = bot
        



async def setup(bot):
    await bot.add_cog(MyStatcordCog(bot))
