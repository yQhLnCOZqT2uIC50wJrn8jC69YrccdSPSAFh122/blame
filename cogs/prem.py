import discord, motor, aiohttp, re, asyncio, httpx, importlib
from datetime import date
from discord.ext import commands, tasks
from PIL import Image
import Core.utils
from Core.utils import get_theme

errorcol = 0xA90F25
urgecolor = 0xF3DD6C
success = discord.Colour.blurple()
checkmoji = "<:blurple_check:921544108252741723>"
xmoji = "<:yy_yno:921559254677200957>"
urgentmoji = "<:n_:921559211366838282>"

class donors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error=discord.Colour.blurple()
        self.db = self.bot.db['boosterrole']
        self.userdb = self.bot.db['userboostroles']
        self.theme = self.bot.db['theme']
        self.vanity = self.bot.db['vanityroles']
        self.cacheThemes.start()
        self.themes = {}
        #self.color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)

    @tasks.loop(minutes=100)
    async def cacheThemes(self):
        getThemes = self.theme.find({})
        guild_ids = []
        themes = []
        for i in await getThemes.to_list(length=999):
            get_guilds =i['guild_id']
            get_color = i['color']
            guild_ids.append(get_guilds)
            themes.append(get_color)
        Core.utils.themes = {guild_ids: {'color': themes} for(guild_ids, themes) in zip(guild_ids, themes)}
        print('cached themes')

    @cacheThemes.before_loop
    async def before_cacheThemes(self):
        await self.bot.wait_until_ready()


    @commands.group(
        aliases = ['br', 'boostr', 'boosterole'],
        usage = 'manage_guild',
        description = 'Allow your server boosters to manage and create their own role',
        brief = 'None',
        help = "```Syntax: boosterrole [subcommand] <args>\nExample: boosterrole setup```"
    )
    async def boosterrole(self, ctx):
        try:
            if ctx.invoked_subcommand is None:
                embed = discord.Embed(title="Command: boosterrole", description="Allow your server boosters to manage and create their own role\n```Syntax: boosterrole [subcommand] <args>\nExample: boosterrole setup```", color = discord.Color.blurple())
                embed.set_author(name="boosterrole help", icon_url=ctx.me.avatar.url)
                embed.set_footer(text=f"Page 1/{len([sc for sc in self.bot.get_command('boosterrole').walk_commands()])} ・ boosterrole")
                return await ctx.send(embed=embed)
        except Exception as e:
            print(e)   

    @boosterrole.command(
        usage = 'manage_guild',
        description = 'Setup the boosterrole module so you can get started',
        brief = 'None',
        help = "```Example: boosterrole setup```"
    )  
    async def setup(self, ctx):
        async with ctx.typing():
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if check:
                return await ctx.send(embed=discord.Embed(description=f"{xmoji} The boosterrole module is **already setup.** If you'd like to **restart** it, please use the ``boosterrole forcerestart`` command.", color =errorcol))
            if not check:
                await self.db.insert_one({
                    "guild_id": ctx.guild.id,
                    "user_id": ctx.author.id,
                    "role": None
                })
                return await ctx.send(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} The **boosterrole** module has now been **enabled**. Your **boosters** can begin creating their **own roles** with ``boosterrole create``", color=0x43B581))

    @boosterrole.command(
        aliases = ['new', 'add'],
        usage = 'booster',
        description = 'Create your own role if you boost the server',
        brief = "role name",
        help = "```Syntax: boosterrole create [rolename]\nExample: boosterrole create blame is the best bot```"
    )
    async def create(self, ctx, *, role_name:str):
        async with ctx.typing():
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if check:
                if ctx.author.premium_since:
                    existing = await self.userdb.find_one({"user_id": ctx.author.id})
                    if existing:
                        return await ctx.send(embed=discord.Embed(description=f"{urgentmoji} {ctx.author.mention} You already have an existing **booster role**: <@&{existing['role']}>", color=urgecolor))
                    else:
                        if len(role_name) > 30:
                            return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} Your **role name** cannot be over **30 characters** long.", color=urgecolor))
                        else:
                            create = await ctx.guild.create_role(name=role_name)
                            today = date.today()
                            d2 = today.strftime("%B %d, %Y")
                            await self.userdb.insert_one({
                                "guild_id": ctx.guild.id,
                                "user_id": ctx.author.id,
                                "role": create.id,
                                "date": str(d2)
                            })
                            await asyncio.sleep(1)
                            check = await self.userdb.find_one({"user_id": ctx.author.id})
                            roles = ctx.guild.get_role(check['role'])
                            await ctx.author.add_roles(roles, reason="Booster role created")
                            return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've successfully created your **booster role** with the name: **{role_name}**", color=0x43B581))
                else:
                    return await ctx.reply(embed=discord.Embed(description=f"{xmoji} **You are not a booster**", color=errorcol))
            else:
                return await ctx.reply(embed=discord.Embed(description=f"{urgentmoji} {ctx.author.mention} The **boosterrole module** has not been enabled in this server. Ask a **server mod** to set it up using the ``boosterrole setup`` command.", color=urgecolor))

    @boosterrole.command(
        aliases = ['pic', 'picture', 'emoji'],
        usage = 'booster',
        description = "Edit your booster role icon",
        brief = 'url',
        help = "```Syntax: boosterrole icon [image or url]\nExample: boosterrole icon https://blame.gg/assets/1.png```"
    )
    async def icon(self, ctx, img):
        async with ctx.typing():
            vaild_urls = ['https://cdn.discordapp', 'https://media.discordapp.net']
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if check:
                if not ctx.guild.premium_tier == 3:
                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} This guild is not **level 3**. To use this **command** the server must have **15 boosts**", color=errorcol))
                else:
                    if ctx.author.premium_since:
                        existing = await self.userdb.find_one({"user_id": ctx.author.id})
                        if existing:
                            if img.lower().startswith(tuple(vaild_urls)):                                           
                                user_role = await self.userdb.find_one({"user_id": ctx.author.id})
                                role = ctx.guild.get_role(user_role['role'])
                                try:
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(img) as r:
                                            new = await r.read()
                                    await role.edit(display_icon=new)
                                    return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've **successfully** set your **booster role icon**", color=0x43B581))
                                except:
                                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} Oops, looks like that **image type** is not **supported**", color=errorcol))

                            elif ctx.message.attachments:
                                user_role2 = await self.userdb.find_one({"user_id": ctx.author.id})
                                role2 = ctx.guild.get_role(user_role2['role'])
                                try:
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(ctx.message.attachments[0].url) as r:
                                            scan = await r.read()
                                    await role2.edit(display_icon=scan)
                                    return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've **successfully** set your **booster role icon**", color=0x43B581))
                                except:
                                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} Oops, looks like that **image type** is not **supported**", color=errorcol))
                        else:
                            return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} You don't have your own boosterrole **yet!** Use ``boosterrole create`` to make one.", color=errorcol))
                    else:
                        return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} **You are not a booster of this server**", color=errorcol))
            else:
                return await ctx.reply(embed=discord.Embed(description=f"{urgentmoji} {ctx.author.mention} The **boosterrole module** has not been enabled in this server. Ask a **server mod** to set it up using the ``boosterrole setup`` command.", color=urgecolor))


    @boosterrole.command(
        aliases = ['clr', 'hex'],
        usage = 'booster',
        description = 'Change the color of your boosterrole',
        brief = "hex",
        help = "```Syntax: boosterrole color [hex]\nExample: boosterrole color #a33e3e```"
    )
    async def color(self, ctx, hex):
        async with ctx.typing():
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if check:
                if not ctx.guild.premium_tier == 3:
                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} This guild is not **level 3**. To use this **command** the server must have **15 boosts**", color=errorcol))
                else:
                    if ctx.author.premium_since:
                        existing = await self.userdb.find_one({"user_id": ctx.author.id})
                        if existing:
                            if hex.startswith('#'):
                                role = ctx.guild.get_role(existing['role'])
                                match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', hex)
                                if match:
                                    hex = hex.strip('#')
                                    newhex = int("0x" + hex, 16)
                                    await role.edit(color=newhex)
                                    return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've **successfully** set your boosterrole color to **{hex}**", color=0x43B581))
                                else:
                                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} No results found for this color code", color=errorcol))
                            else:
                                async with httpx.AsyncClient() as client:
                                    r = await client.get(f"https://www.thecolorapi.com/id?hex={hex}&format=json")
                                if r.status_code == 200:
                                    res = r.json()
                                    value = res['hex']['value']
                                    print(value)
                                    if "#000000" in value:
                                        return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} No results found for that color code", color=errorcol))
                                    else:
                                        value = value.strip('#')
                                        role = ctx.guild.get_role(existing['role'])
                                        new = int("0x" + value, 16)
                                        await role.edit(color=new)
                                        return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've **successfully** set your boosterrole color to **{hex}**", color=0x43B581))
                        else:
                            return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} You don't have your own boosterrole **yet!** Use ``boosterrole create`` to make one.", color=errorcol))
                    else:
                        return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} **You are not a booster of this server**", color=errorcol))
            else:
                return await ctx.reply(embed=discord.Embed(description=f"{urgentmoji} {ctx.author.mention} The **boosterrole module** has not been enabled in this server. Ask a **server mod** to set it up using the ``boosterrole setup`` command.", color=urgecolor))

    @boosterrole.command(
        aliases = ['n', 'edit'],
        usage = 'booster',
        description = 'Change the name of your boosterrole',
        brief = "name",
        help = "```Syntax: boosterrole name [name]\nExample: boosterrole name i love blame```"
    )
    async def name(self, ctx, *, name):
        async with ctx.typing():
            check = await self.db.find_one({ "guild_id": ctx.guild.id})
            if check:
                if not ctx.guild.premium_tier == 3:
                    return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} This guild is not **level 3**. To use this **command** the server must have **15 boosts**", color=errorcol))
                else:
                    if ctx.author.premium_since:
                        existing = await self.userdb.find_one({"user_id": ctx.author.id})
                        if existing:
                            role = ctx.guild.get_role(existing['role'])
                            await role.edit(name=name)
                            return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've **successfully** changed you boosterrole name to: **{name}**", color=0x43B581))
                        else:
                            return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} You don't have your own boosterrole **yet!** Use ``boosterrole create`` to make one.", color=errorcol))
                    else:
                        return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} **You are not a booster of this server**", color=errorcol))
            else:
                return await ctx.reply(embed=discord.Embed(description=f"{urgentmoji} {ctx.author.mention} The **boosterrole module** has not been enabled in this server. Ask a **server mod** to set it up using the ``boosterrole setup`` command.", color=urgecolor))
    
    @boosterrole.command(
        aliases = ['forceremove', 'remove', 'delete', 'del'],
        usage = 'administrator, booster',
        description = 'force reset yours boosterrole',
        brief = "name",
        help = "```Example: boosterrole forcereset @jacob```"
    )
    async def forcereset(self, ctx):
        existing = await self.userdb.find_one({"user_id": ctx.author.id})
        if existing:
            role = ctx.guild.get_role(existing['role'])
            await role.delete(reason=f"Booster role removed by {ctx.author}")
            await self.userdb.delete_one({"user_id": ctx.author.id})
            return await ctx.reply(embed=discord.Embed(description=f"<:check:921544057312915498> {ctx.author.mention} You've successfully removed your boosterrole", color=0x43B581))
        else:
            return await ctx.send(embed=discord.Embed(description=f"{xmoji} {ctx.author.mention} You don't have your own boosterrole **yet!** Use ``boosterrole create`` to make one.", color=errorcol))

    @commands.command(
        aliases = ['theme', 'settheme', 'themeset'],
        usage = 'administrator',
        description = "Change the bots color theme in your server!",
        brief = "hex",
        help = "```Syntax: themeset [hex]\nExample: themeset #fefbfa```")
    @commands.has_permissions(administrator=True)
    async def set_theme(self, ctx, color):
        async with ctx.typing():
            check = await self.theme.find_one({"guild_id": ctx.guild.id})
            if check and '#' in color:
                match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', color)
                if match:
                    color = color.strip('#')
                    await self.theme.update_one({"guild_id": ctx.guild.id }, {"$set":{"color": color}})
                    await asyncio.sleep(1)
                    self.cacheThemes.restart()
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} <:check:921544057312915498> **Updated theme** to **{color}**", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
                else:
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} {xmoji} **{color}** is not a **supported** color", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
            if check and not '#' in color:
                color = color.replace(color, f'#{color}')
                match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', color)
                if match:
                    color = color.strip('#')
                    await self.theme.update_one({"guild_id": ctx.guild.id }, {"$set":{"color": color}})
                    await asyncio.sleep(1)
                    self.cacheThemes.restart()
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} <:check:921544057312915498> **Updated theme** to **{color}**", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
                else:
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} {xmoji} **{color}** is not a **supported** color", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
            if not check and '#' in color:
                match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', color)
                if match:
                    color = color.strip('#')
                    try:
                        await self.theme.insert_one({ "guild_id": ctx.guild.id, "color": str(color)})
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(1)
                    self.cacheThemes.restart()
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} <:check:921544057312915498> Set **theme** to **{color}**", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
                else:
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} {xmoji} **{color}** is not a **supported** color", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
            if not check and not '#' in color:
                color = color.replace(color, f'#{color}')
                match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', color)
                if match:
                    color = color.strip('#')
                    try:
                        await self.theme.insert_one({ "guild_id": ctx.guild.id, "color": str(color)})
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(1)
                    self.cacheThemes.restart()
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} <:check:921544057312915498> Set **theme** to **{color}**", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
                else:
                    return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} {xmoji} **{color}** is not a **supported** color", color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16)))
    
    @commands.command()
    async def tta(self, ctx):
        embed = discord.Embed(description='yo!', color=int(await get_theme(self, bot=self.bot, guild=ctx.guild.id), 16))
        await ctx.send(embed=embed)


    @commands.group(
        aliases = ['vanityrole', 'van'],
        usages = 'manage_guild',
        description = 'Give your members custom roles depending on their status (specified by you)',
        brief = 'subcommand',
        help = "```Syntax: vanity <subcommand>\nExample: vanity set /blame````"
    )
    @commands.has_permissions(manage_guild=True)
    async def vanity(self, ctx):
        if ctx.invoked_subcommand is None:
            await Core.utils.command_group_help(ctx)


async def setup(bot):
    await bot.add_cog(donors(bot)) 
