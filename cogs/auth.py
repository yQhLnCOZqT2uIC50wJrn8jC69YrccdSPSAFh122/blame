import motor.motor_asyncio, datetime, asyncio
import discord
from discord.ext import commands

list = [493545772718096386, 386192601268748289, 236522835089031170]

class guildAuth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.headers = {"Authorization": "Bot #token"}
        self.db = self.bot.db["guildAuth"]#fetching collection 1
        self.errorcol = 0xA90F25 # error color
        self.urgecolor = 0xF3DD6C # exclamation color
        self.success = discord.Colour.blurple() #theme
        self.checkmoji = "<:blurple_check:921544108252741723>" # success emoji
        self.xmoji = "<:yy_yno:921559254677200957>" # unsuccessful emoji
        self.urgentmoji = "<:n_:921559211366838282>" # exclamation emoji

   # @commands.Cog.listener()
    #async def on_guild_join(self, guild):
    #    try:
           # check = await self.db.count_documents({ "guild_id": guild.id })
           # if not check:
              #  for channel in guild.text_channels:
                  #  if channel.permissions_for(guild.me).send_messages:
                      #  await channel.send("This guild has not been authorized. If you'd like to sort something out please contact us here -> https://blame.gg\n\n**Notice:** You will not find my features in the public version of blame as I am customly made.")
                     #   await guild.leave()
                    #    break
           # else:
               # for channel in guild.text_channels:
                   # if channel.permissions_for(guild.me).send_messages:
                     #   await guild.owner.send("Congrats, this guild has been authorized to use me :) For any support directly contact sorrow or kite.")
                     #   break
        #except Exception as e: 
           # print(e)

    @commands.group(invoke_without_command=True, hidden=True)
    async def guild(self, ctx):
        if ctx.message.author.id in list:
            try:
                await ctx.send("__Commands:__\n\nguild auth add\nguild auth remove")

            except Exception as e: 
                print(e)
        else:
            return await ctx.message.add_reaction("❌")

    @guild.group(hidden=True)
    async def auth(self, ctx):
        if ctx.message.author.id in list:
            try:
                if ctx.invoked_subcommand is None:
                    await ctx.send("Improper command. Maybe you meant, **guild auth add** or **guild auth remove**?")
            except Exception as e: 
                print(e)
        else:
            return await ctx.message.add_reaction("❌")

    @auth.command(hidden=True)
    async def add(self, ctx, guild_id: int=None, *, arg=None):
        if ctx.message.author.id in list:
            try:
                if guild_id == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!guild auth add **[guildID] [reason]**")
                if arg == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!guild auth add **[guildID] [reason]**")
                else:
                    self.db.insert_one({
                        "guild_id": guild_id,
                        "reason": f"{str(arg)}"
                    })
                    await ctx.send(f":thumbsup: Guild ID \➡️ ``{guild_id}`` has been authorized with the reason \⬇️\n```{arg} - {ctx.author}```")
            except Exception as e:
                print(e)
        else:
            return await ctx.message.add_reaction("❌")

    @auth.command(aliases = ['delete'], hidden=True)
    async def remove(self, ctx, guild_id: int=None):
        if ctx.message.author.id in list:
            try:
                if guild_id == None:
                    await ctx.send("Incorrect.\n**__Correct format:__** !!guild auth remove **[guildID]")
                if guild_id:
                    self.db.delete_one({
                        "guild_id": guild_id,
                    })
                    await ctx.send(f":thumbsup: Guild ID \➡️ ``{guild_id}`` has been un-authorized**(removed)** by:⬇️\n```- {ctx.author}```")
                    try:
                        find = self.bot.get_guild(guild_id)
                        find.leave()
                        await ctx.send(f"Left **{find.name}** - ``{find.id}``")
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send("Not found!")
            except Exception as e:
                print(e)
        else:
            return await ctx.message.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(guildAuth(bot))