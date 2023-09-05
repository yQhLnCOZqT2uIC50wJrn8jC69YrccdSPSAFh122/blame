import discord, motor.motor_asyncio, time, math, asyncio, typing
from discord.ext import commands
from discord.utils import get
import Core.utils as utils

class backend_tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        zzz = self.bot.get_channel(1040447935688736828)
        #for c in guild.text_channels:
            #if c.permissions_for(guild.me).create_instant_invite:
                #invite = await c.create_invite()
        embed = discord.Embed(title="Blame was added!", description=f'**{guild.name}** - ``{guild.id}`` with **{len(guild.members):,} members**', colour=discord.Color.blurple())
        embed.set_author(name=f"{len(self.bot.guilds)} guilds now!", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="The Blame Team")
        await zzz.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        zzz = self.bot.get_channel(1040449541406728193)
        embed = discord.Embed(title="Blame was removed!", description=f'**{guild.name}** - ``{guild.id}`` with **{len(guild.members):,} members**', colour=0xffcc4d)
        embed.set_author(name=f"{len(self.bot.guilds)} guilds now", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=guild.icon.url)
        await zzz.send(embed=embed)




async def setup(bot):
    await bot.add_cog(backend_tracking(bot))