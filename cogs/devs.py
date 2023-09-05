import discord, motor.motor_asyncio, time, math, asyncio, typing
from discord.ext import commands
from discord.utils import get
import Core.utils as utils

devs = [236522835089031170, 386192601268748289, 352190010998390796, 753277825372389402, 493545772718096386]

class developers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db['blacklists']
        self.staff = self.bot.db['blameStaff']
        self.data = self.bot.db['data']
        self.accepted = self.bot.db['consented']

    async def cog_check(self, ctx):
        if ctx.author.id in devs:
            return True
        else:
            return False

    @commands.group(invoke_without_command=True, aliases = ["bl"], hidden=True)
    async def blacklist(self, ctx):
            embed = discord.Embed(description="**__Blacklisting loaded__**\n\n blacklist user\nblacklist guild", color=0xF2A0FD)
            await ctx.send(embed=embed)

    @blacklist.command(aliases = ['member'], hidden=True)
    async def user(self, ctx, user: discord.User = None, *, arg=None):
        if ctx.author.id in devs:
            try:
                check = await self.db.count_documents({ "user": user.id })
                if user == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!blacklist user **[userID] [reason]**")
                if arg == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!blacklist user **[userID] [reason]**")

                if check:
                    return await ctx.send(f"{user.mention} ``{user.id}`` is already blacklisted.")
                else:
                    await self.db.insert_one({
                    "user": user.id,
                    "reason": arg,
                })
                    await ctx.send(f"**{user.id}** is now blacklisted for ```{arg}```")

            except Exception as e:
                print(e)
        else:
            return

    @blacklist.command(aliases = ['server', 'serv'], hidden=True)
    async def guild(self, ctx, guild_id: int=None, *, arg=None):
        if ctx.author.id in devs:
            try:
                guild = self.bot.get_guild(guild_id)
                check = await self.db.count_documents({ "guild_id": guild_id })
                if not guild:
                    return await ctx.send("guild not found")
                if guild_id == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!blacklist guild **[guildID] [reason]**")
                if arg == None:
                    return await ctx.send("Incorrect.\n**__Correct format:__** !!blacklist guild **[guildID] [reason]**")

                if check:
                    return await ctx.send(f"``{guild_id}`` is already blacklisted")

                else:
                        await self.db.insert_one({
                        "guild": guild_id,
                        "reason": arg,
                    })
                        await ctx.send(f"**{guild.name}** (``{guild.id}``) is now blacklisted")
                        try:
                            await guild.leave()
                        except:
                            pass
            except Exception as e:
                print(e)
        else:
            return

    @commands.command(hidden=True, aliases=["mutual", 'mutuals'])
    async def mutual_servers(self, ctx, user: typing.Optional[discord.User]):
        user = ctx.author if not await self.bot.is_owner(ctx.author) else (user or ctx.author)
        guilds = sorted(user.mutual_guilds, key=lambda g: g.member_count, reverse=True)[0:30]

        embed = discord.Embed(
            title=f"I have {len(guilds)} servers in common with {user}:",
            description="\n".join([f"[`{guild.member_count}`] **{guild.name}** " for guild in guilds]),
        )

        await ctx.send("Here are the mutual servers:", embed=embed)


    @commands.command(hidden=True)
    async def scraper(self, ctx, chan=None):
        if ctx.message.author.id in devs: 
            try:
                if chan == None:
                    await ctx.send("give a channel ID next time")
                else:

                    channel = await self.bot.fetch_channel(chan)
                    messages = [message async for message in channel.history(limit=5000)]
                    dodo = ["boygifs", "boyimages", "girlgifs", "girlimages", "animeicons", "animegifs", 'banners']
                    await ctx.send(f"now scraping <#{channel.id}>\nWhat ``database`` do I add these too? **(**``boygifs, boyimages, girlgifs, girlimages, animeicons, animegifs, banners``**)**?")
                    msgz = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=20)

                    if msgz.content.lower() == "boygifs":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("boygifs.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("boygifs.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``boygifs`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "boyimages":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("boyimages.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("boyimages.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``boyimages`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "girlgifs":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("girlgifs.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("girlgifs.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``girlgifs`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "girlimages":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("girlimages.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("girlimages.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``girlimages`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "animeicons":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("animeicons.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("animeicons.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``animeicons`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "animegifs":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("animegifs.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("animegifs.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``animegifs`` now has ``{Counter}`` images")

                    if msgz.content.lower() == "banners":
                        await msgz.add_reaction('👍')
                        for x in messages:
                            if x.attachments:
                                attachment = x.attachments[0] 
                                f = open("banners.txt", "a")
                                f.write(attachment.url + '\n')
                                f.close()
                            file = open("banners.txt","r")
                            Counter = 0
                            Content = file.read()
                            CoList = Content.split("\n")
                            for i in CoList:
                                if i:
                                    Counter += 1
                        await ctx.send(f"``DONE!`` -  Our database ``bannners`` now has ``{Counter}`` images")
                    
                    if not msgz.content.lower() in dodo:
                        await ctx.send("That is not in our database.")
                        pass
            except:
                pass
        else:
            return

    @commands.command(aliases = ['apicheck', 'apicount'])
    async def pfpcount(self, ctx):
        async with ctx.typing():
            file = open("boygifs.txt","r")
            Counter = 0
            Content = file.read()
            CoList = Content.split("\n")
            for i in CoList:
                if i:
                    Counter += 1
            file2 = open("boyimages.txt","r")
            Counter2 = 0
            Content2 = file2.read()
            CoList2 = Content2.split("\n")
            for i in CoList2:
                if i:
                    Counter2 += 1
            file3 = open("girlgifs.txt","r")
            Counter3 = 0
            Content3 = file3.read()
            CoList3 = Content3.split("\n")
            for i in CoList3:
                if i:
                    Counter3 += 1
            file4 = open("girlimages.txt","r")
            Counter4 = 0
            Content4 = file4.read()
            CoList4 = Content4.split("\n")
            for i in CoList4:
                if i:
                    Counter4 += 1
            file5 = open("animeicons.txt","r")
            Counter5 = 0
            Content5 = file5.read()
            CoList5 = Content5.split("\n")
            for i in CoList5:
                if i:
                    Counter5 += 1
            file6 = open("animegifs.txt","r")
            Counter6 = 0
            Content6 = file6.read()
            CoList6 = Content6.split("\n")
            for i in CoList6:
                if i:
                    Counter6 += 1
            file7 = open("banners.txt","r")
            Counter7 = 0
            Content7 = file7.read()
            CoList7 = Content7.split("\n")
            for i in CoList7:
                if i:
                    Counter7 += 1
        embed = discord.Embed(title="__Pfp Count__", description=f"boygif row: ``{Counter} gifs``\nboyimages row: ``{Counter2} images``\ngirlgifs row: ``{Counter3} gifs``\ngirlimages row: ``{Counter4} images``\nanimeicons row: ``{Counter5}`` images\nanimegifs row: ``{Counter6}`` gifs\nbanner row: ``{Counter7}`` images & gifs")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def serverinv(self, ctx, *, guild_name):
        if ctx.message.author.id in devs:
            try:
                    guild = discord.utils.get(self.bot.guilds, name=guild_name) # Get the guild by name
                    if guild is None:
                        await ctx.send("No guild with that name found.") # No guild found
                        return
                    for c in guild.text_channels:
                        if c.permissions_for(guild.me).create_instant_invite:
                            invite = await c.create_invite() # Guild found
                            await ctx.send(f"{invite}")
                            break
            except:
                await ctx.send("I dont have permissions in that server")
                pass
        else:
            return

    @commands.command(hidden=True)
    async def addstaff(self, ctx, member: discord.Member=None):
        if ctx.message.author.id in devs:
            await self.staff.insert_one({"user_id": member.id})
            return await ctx.send(embed=discord.Embed(description=f"<@{member.id}> is **now a staff** and has been granted permissions", color=discord.Colour.blurple()))
        else:
            return await ctx.message.add_reaction("❌")

    @commands.command(hidden=True)
    async def delstaff(self, ctx, member: discord.Member=None):
        if ctx.message.author.id in devs:
            await self.staff.delete_one({"user_id": member.id})
            return await ctx.send(embed=discord.Embed(description=f"<@{member.id}> is **no longer** a staff, **permissions revoked**", color=discord.Colour.blurple()))
        else:
            return await ctx.message.add_reaction("❌")

    @commands.command(aliases=['revoke'], hidden=True)
    async def reset(self, ctx, member: discord.Member=None):
        find = await self.staff.find_one({"user_id": ctx.author.id})
        if find or ctx.message.author.id in devs:
            if member == None:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}: I need a **member**", color = discord.Color.blurple()))
            check = await self.data.find_one({"user_id": member.id})
            if check:
                await self.data.delete_one({ "user_id": member.id})
                return await ctx.message.add_reaction("<:check:921544057312915498>")
            else:
                return await ctx.send(embed=discord.Embed(description=f"<@{member.id}> **has no records...***", color=discord.Color.blurple()))
        else:
            return await ctx.message.add_reaction("❌")

    @commands.command(aliases=['accept'], hidden=True)
    async def add(self, ctx, member: discord.Member=None):
        find = await self.staff.find_one({"user_id": ctx.author.id})
        if find or ctx.message.author.id in devs:
            if member == None:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}: I need a **member**", color = discord.Color.blurple()))
            check = await self.accepted.find_one({"user_id": member.id})
            if check:
                return await ctx.send(embed=discord.Embed(description=f"@<{member.id} has **already** given **consent**", color=discord.Color.blurple()))
            else:
                await self.accepted.insert_one({"user_id": member.id})
                return await ctx.message.add_reaction("<:check:921544057312915498>")
        else:
            return await ctx.message.add_reaction("❌")
    
    @commands.command(aliases = ['mycmds'], hidden=True)
    async def mycommands(self, ctx):
        find = await self.staff.find_one({"user_id": ctx.author.id})
        if find or ctx.message.author.id in devs:
            embed = discord.Embed(description=f"**{ctx.author.name}**: {ctx.author.mention}・ <:z_staff:921559260989636668> (**Blame Staff**)\n\n・**accept** - auto consents a user incase of error\n・**revoke** - revokes a user from the non-consented, so they can use commands.", color=discord.Color.blurple())
            embed.set_author(name=f"{ctx.author} {ctx.author.id}", icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            return await ctx.send(embed=embed)
        else:
            return await ctx.message.add_reaction("❌")
    

    @commands.command(hidden=True, aliases=['servers'])
    @commands.bot_has_permissions(read_message_history=True, add_reactions=True, embed_links=True)
    async def topservers(self, ctx: commands.Context) -> None:
        if ctx.message.author.id in devs:
            async with ctx.typing():
                guilds = sorted(list(self.bot.guilds), key=lambda s: s.member_count, reverse=True)
                rows = []
                content = discord.Embed(title=f"{len(self.bot.guilds)} servers", description="", color=discord.Color.blurple())
                for i, server in enumerate(guilds, start=1):
                    try:
                        rows.append(f"``{i}.`` **{server.name}** - *{server.member_count:,} members*")
                        #if await server.vanity_invite():
                            #rows.append(f"``{i}.`` **[{server.name}]({await server.vanity_invite()})** - *{server.member_count} members*")
                    except:
                        pass
                        rows.append(f"``{i}.`` **{server.name}** - *{server.member_count} members*")
                await utils.send_as_pages(ctx, content, rows)
        else:
            return

    @commands.command(hidden=True, aliases=['neservers', 'ns'])
    @commands.bot_has_permissions(read_message_history=True, add_reactions=True, embed_links=True)
    async def newservers(self, ctx: commands.Context) -> None:
        if ctx.message.author.id in devs:
            async with ctx.typing():
                guilds = sorted(list(self.bot.guilds), key=lambda s: s.me.joined_at)
                rows = []
                content = discord.Embed(title=f"latest joined servers", description="", color=discord.Color.blurple())
                for i, server in enumerate(guilds, start=1):
                    try:
                        rows.append(f"``{i}.`` **{server.name}** - *{server.member_count:,} members*")
                        #if await server.vanity_invite():
                            #rows.append(f"``{i}.`` **[{server.name}]({await server.vanity_invite()})** - *{server.member_count} members*")
                    except:
                        pass
                        rows.append(f"``{i}.`` **{server.name}** - *{server.member_count} members*")
                await utils.send_as_pages(ctx, content, rows)
        else:
            return

async def setup(bot):
    await bot.add_cog(developers(bot))