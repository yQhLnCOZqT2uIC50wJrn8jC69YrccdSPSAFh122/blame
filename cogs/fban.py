import discord
from discord.ext import commands
from typing import List
import discord.ui


class fbaN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases = ['fban', 'yeet', 'bann'],
        usage = 'Send messages',
        description = "Fake ban a member from the server",
        brief = "member, reason",
        help = '```Syntax: fban [member] [reason]\nExample: fban @jacob sus concerning jokes```'
    )
    async def fakeban(self, ctx, member: discord.Member=None, *, reason=None):
        if member == None:
            return await ctx.send("Provide a user to fban")
        if reason == None:
            return await ctx.send(f"**{member}** has been banned from {ctx.guild.name} ** -- unable to send dm**")
        else:
            await ctx.send(f"**{member}** has been banned from {ctx.guild.name} - **{reason}**")

        


async def setup(bot):
    await bot.add_cog(fbaN(bot))