import discord, motor.motor_asyncio, asyncio, httpx, re
from discord.ext import commands
import Core.utils as utils
import Core.exceptions as exceptions

from libraries import emoji_literals

connection = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://verify:8FM0953pS0onhvB7@sorrow.hn7kg.mongodb.net/axis?retryWrites=true&w=majority')
db = connection.get_database("blameDatabase").get_collection("starboard")

class starboardUtil:
    def setup(server_id):
        db.insert_one({
            "guild_id": server_id,
            "channel": None,
            "amount": None,
            "threshold": None,
            "starboard": "off",
            "emoji": None,
            "color": None,
            "blacklist": [],
            'message_id': None
        })


class stbcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://verify:8FM0953pS0onhvB7@sorrow.hn7kg.mongodb.net/axis?retryWrites=true&w=majority')
        self.db = self.connection.get_database("blameDatabase").get_collection("starboard")
        self.urgecolor = 0xF3DD6C
        self.errorcol = 0xA90F25 # error color
        self.success = discord.Colour.blurple() #theme
        self.checkmoji = "<:blurple_check:921544108252741723>" # success emoji
        self.xmoji = "<:yy_yno:921559254677200957>" # unsuccessful emoji
        self.urgentmoji = "<:n_:921559211366838282>" # exclamation emoji

    @commands.group(
        aliases = ['sb', 'stb', 'star'],
        usage = "Manage_channels",
        description = "Tired of only being able to pin 50 messages? Pin as many as you want, how you want them, and their requirements",
        brief = "subcommand",
        help = "```Syntax: starboard [subcommand] <arg>\nExample: starboard channel #pins```"
    )
    async def starboard(self, ctx):
        if ctx.invoked_subcommand is None:
            await utils.send_command_help(ctx)

    @starboard.command(
        aliases = ['channel', 'set'],
        usage = "Manage_channels",
        description = "Set the channel thats Starboard messaged will be poted in",
        brief = "channel",
        help = "```Syntax: starboard set [channel]\nExample: starboard channel #pins```"
    )
    @commands.has_permissions(manage_channels=True)
    async def setup(self, ctx, channel: discord.TextChannel):
        async with ctx.typing():
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if not check:
                server_ = self.bot.get_guild(ctx.guild.id)
                starboardUtil.setup(server_.id)
                msg = discord.Embed(description="<:check:921544057312915498> **Initiating** starboard setup", timestamp=ctx.message.created_at, color= 0x43B581)
                msg2 = discord.Embed(description="<a:whiteloading:1006977730912464936> **Finishing up**")
                message = await ctx.send(embed=msg)
                await asyncio.sleep(1.5)
                await message.edit(embed=msg2)
                await asyncio.sleep(3)
                await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"channel": channel.id}})
                ms3 = discord.Embed(description=f"<:check:921544057312915498> Starboard is now **active** and set to the channel: <#{channel.id}>", timestamp=ctx.message.created_at, color= 0x43B581)
                await message.edit(embed=ms3)
            else:
                await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"channel": channel.id}})
                ms3 = discord.Embed(description=f"<:check:921544057312915498> The starboard **channel** has been updated to <#{channel.id}>", timestamp=ctx.message.created_at, color= 0x43B581)
                await ctx.send(embed=ms3)
    
    @starboard.command(
        aliases = ['threshold'],
        usage = "Manage_channels",
        description = "Set the starboards reaction limit",
        brief = "int",
        help = "```Syntax: starboard limit [int]\nExample: starboard limit 5```"
    )
    @commands.has_permissions(manage_channels=True)
    async def limit(self, ctx, amount : int):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"amount": amount}})
            ms3 = discord.Embed(description=f"<:check:921544057312915498> **Updated:** Messages will now need **{amount}** **reactions** to get into the starboard", color= 0x43B581)
            await ctx.send(embed=ms3)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color=self.errorcol)
            return await ctx.send(embed=ms1)

    @starboard.command(
        usage = "Manage_channels",
        description = "Toggle the starboard from posting in the channel",
        brief = "None",
        help = "Example: starboard toggle```"
    )
    @commands.has_permissions(manage_channels=True)
    async def toggle(self, ctx):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            data = check['starboard']
            if "off" in data:
                await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"starboard": "on"}})
                ms3 = discord.Embed(description=f"<:check:921544057312915498> The starboard has now been toggled **on**", color= 0x43B581)
                await ctx.send(embed=ms3)
            else:
                await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"starboard": "off"}})
                ms2 = discord.Embed(description=f"<:check:921544057312915498> The starboard has now been toggled **off**", color= 0x43B581)
                await ctx.send(embed=ms2)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1)


    @starboard.command(
        aliases = ['reaction', 'emote'],
        usage = "Manage_channels",
        description = "Change the emoji that will be used for the starboard",
        brief = "emoji",
        help = "```Syntax: starboard emoji <emoji>\nExample: starboard emoji :star:```"
    )
    @commands.has_permissions(manage_channels=True)
    async def emoji(self, ctx, emoji):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            if emoji[0] == "<":
                emoji_obj = await utils.get_emoji(ctx, emoji)
                if emoji_obj is None:
                    raise exceptions.CommandWarning("I have no clue what this emoji is.")
                #emoji = discord.Emoji
                #print(emoji.id, emoji_obj)
                a= emoji.split(">")[0].split(":")[2]
                await self.db.update_one({ "guild": ctx.guild.id }, { "$set": { "emoji": int(a) }})
                ms2 = discord.Embed(description=f"<:check:921544057312915498> The starboard **emoji** has now been set to {emoji}", color= 0x43B581)
                await ctx.send(embed=ms2)
            else:
                emoji_name = emoji_literals.UNICODE_TO_NAME.get(emoji)
                if emoji_name is None:
                    raise exceptions.CommandWarning("I have no clue what this emoji is.")
                await self.db.update_one({ "guild_id": ctx.guild.id}, { "$set": {"emoji": emoji}})
                ms3 = discord.Embed(description=f"<:check:921544057312915498> The starboard **emoji** has now been set to {emoji}", color= 0x43B581)
                await ctx.send(embed=ms3)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1)    

    @starboard.command(
        aliases = ['block'],
        usage = "Manage_channels",
        description = "Blacklsit a channel from being put on the starboard",
        brief = "channel",
        help = "```Syntax: starboard blacklist [channel]\nExample: starboard blacklist #general```"
    )
    @commands.has_permissions(manage_channels=True)
    async def blacklist(self, ctx, channel: discord.TextChannel):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            await self.db.update_one({ "guild_id": ctx.guild.id}, { "$push": {"blacklist": channel.id}})
            ms3 = discord.Embed(description=f"<:check:921544057312915498> The starboard will **no longer count** reactions in {channel.mention}", color= 0x43B581)
            await ctx.send(embed=ms3)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1)         

    @starboard.command(
        aliases = ['unblock'],
        usage = "Manage_channels",
        description = "Unblacklist a channel from the blacklisted starboard channels",
        brief = "channel",
        help = "```Syntax: starboard blacklist [channel]\nExample: starboard blacklist #general```"
    )
    @commands.has_permissions(manage_channels=True)
    async def unblacklist(self, ctx, channel: discord.TextChannel):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            await self.db.update_one({ "guild_id": ctx.guild.id}, { "$pull": {"blacklist": channel.id}})
            ms3 = discord.Embed(description=f"<:check:921544057312915498> {channel.mention} has now been **unblacklisted** and can be put on the starboard", color= 0x43B581)
            await ctx.send(embed=ms3)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1)    




    @starboard.command(
        aliases = ['settings', 'status'],
        usage = "Manage_channels",
        description = "View the current starboard settings",
        brief = "None",
        help = "```Example: starboard settings```"
    )
    @commands.has_permissions(manage_channels=True)
    async def config(self, ctx):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            #guildID = check['guild_id']
            channel = check['channel']
            amount = check['amount']
            starboard = check['starboard']
            if "on" in starboard:
                starboard = "**enabled**"
            else:
                starboard = "**not enabled**"
            emoji = check['emoji']
            color = check['color']
            blacklist = check['blacklist']
            if blacklist:
                for i in blacklist:
                    blacklist = " "
                    blacklist += f"<#{i}>, "
            else:
                blacklist = "**None**"
            embed = discord.Embed(title=f":star: {ctx.guild.name}'s starboard settings", description=f"The starboard is {starboard} in this server and has a threshold of **{amount}**", color=discord.Color.blurple())
            embed.add_field(name="Current", value=f"**Channel:** <#{channel}>\n**Threshold:** {amount}\n**Emoji:** {emoji}\n**Color:** **{color}**\n**Blacklisted:** {blacklist}")
            await ctx.send(embed=embed)
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1) 

    @starboard.command(
        usage = "Manage_channels",
        description = "Changes the starboards message's color (hex)",
        brief = "None",
        help = "```Syntax: starboard color [color]\nExample: starboard color #000000```"
    )
    @commands.has_permissions(manage_channels=True)
    async def color(self, ctx, color=None):
        check = await self.db.find_one({ "guild_id": ctx.guild.id})
        if check:
            if color:
                if "#" in color:
                    match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', color)
                    if match:
                        await self.db.update_one({ "guild_id": ctx.guild.id }, { "$set": { "color": color}})
                    else:
                        return await ctx.send("That color code type doesn't seem to be supported")
                else:
                    ms1 = discord.Embed(description=f"{self.urgentmoji} {ctx.author.mention} **color** must be a **hex** (Must start with #)", color= self.urgecolor)
                    return await ctx.send(embed=ms1)  


            else:
                ms1 = discord.Embed(description=f"{self.urgentmoji} {ctx.author.mention} **color** must be a **hex**", color= self.urgecolor)
                return await ctx.send(embed=ms1)  
        else:
            ms1 = discord.Embed(description=f"{self.xmoji} The starboard has not been setup yet.", color= self.errorcol)
            return await ctx.send(embed=ms1)               

    def embedGenerator(self, msg):
        embed = discord.Embed(color=discord.Color.yellow(), timestamp=msg.created_at)
        embed.set_author(name=f"{msg.author}", icon_url=msg.author.display_avatar.url)
        embed.add_field(name="Source", value=f"[Jump]({msg.jump_url})")
        embed.set_footer(text=f"ID: {msg.id}")

        if msg.content:
            embed.description = msg.content

        attach = msg.attachments[0] if msg.attachments else None
        if attach:
            if attach.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                embed.set_image(url=attach.url)
            else:
                embed.add_field(name='Attachment', value=f'[**{attach.filename}**]({attach.url})', inline=False)
        if msg.embeds:
            image = msg.embeds[0].image.url
            if image:
                embed.set_image(url=image)
        return embed

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        check = await self.db.find_one({ "guild_id": payload.member.guild.id})
        if check:
            try:
                star_channel = self.bot.get_channel(check['channel'])
                channel = self.bot.get_channel(payload.channel_id)
                emoji = check['emoji']
                print("hi")
                if payload.emoji.id == emoji or payload.emoji.name == emoji:
                    print("a")
                    msg = await channel.fetch_message(payload.message_id)
                    reacts = list(filter(lambda r: str(r.emoji) == emoji, msg.reactions))
                    if reacts:
                        react = [user async for user in msg.reactions[0].users()]
                    if len(react) >= check['limit']:
                        starmsg = await star_channel.send(f"{emoji} **{len(react)} |** {channel.mention}", embed=self.embedGenerator(msg))
            except Exception as e:
                print(e)



async def setup(bot):
    await bot.add_cog(stbcmds(bot))
    