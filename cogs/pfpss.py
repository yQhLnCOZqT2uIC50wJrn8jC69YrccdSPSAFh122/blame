import discord, random, motor
import random
from Core import utils
from discord.ext import commands, tasks
from colorama import Fore as f

class pfpSSS(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.pfps = self.bot.db["pfps"]
        self.errorcol = 0xA90F25 # error color
        self.urgecolor = 0xF3DD6C # exclamation color
        self.success = discord.Colour.blurple() #theme
        self.checkmoji = "<:blurple_check:921544108252741723>" # success emoji
        self.xmoji = "<:yy_yno:921559254677200957>" # unsuccessful emoji
        self.urgentmoji = "<:n_:921559211366838282>" # exclamation emoji




    @commands.hybrid_group()
    async def pfp(self, ctx): 
        try:
            if ctx.invoked_subcommand is None:
                embed = discord.Embed(title="Command: pfp", description="Get random profile pictures from 4 different genres **(boyicon, boygif, girlicon, girlgif)**\n```Example: pfp boyicon```", color = discord.Color.blurple())
                embed.set_author(name="Pfp help", icon_url=ctx.me.avatar.url)
                embed.set_footer(text=f"Page 1/{len([sc for sc in self.bot.get_command('pfp').walk_commands()])} ・ Pfp")
                return await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @pfp.command(aliases=["bi", 'boyicon'],
    usage = "send_messages",
    description = "Generate a male icon profile picture",
    brief= "None",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def boyicons(self, ctx):
            channel = ctx.message.channel
            lines = open('boyimages.txt').read().splitlines()
            myline =random.choice(lines)
            try:
                color=int(await utils.color_from_image_url(url=myline), 16)
                embed = discord.Embed(color=color, timestamp=ctx.message.created_at)
            except:
                embed = discord.Embed(color=discord.Color.blurple(), timestamp=ctx.message.created_at)
            embed.set_image(url=myline)
            embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
            embed.set_footer(text="https://blame.gg/discord")
            msg = await ctx.send(embed=embed)
            try:
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
            except:
                pass


    @pfp.command(aliases=["bgif", 'bg', 'boygif'],
    usage = "send_messages",
    description = "Generate a male gif profile picture",
    brief= "None",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def boygifs(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('boygifs.txt').read().splitlines()
        myline =random.choice(lines)
        embed.set_image(url=myline)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass


    @pfp.command(aliases=["gi", "gicon", 'girlicon'],
    usage = "send_messages",
    description = "Generate a female icon profile picture",
    brief= "None",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def girlicons(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('girlimages.txt').read().splitlines()
        myline =random.choice(lines)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_image(url=myline)
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass

    @pfp.command(aliases=["ggif", 'girlgif'],
    usage = "send_messages",
    description = "Generate a female gif profile picture",
    brief= "None",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def girlgifs(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('girlgifs.txt').read().splitlines()
        myline =random.choice(lines)
        embed.set_image(url=myline)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass

    @commands.hybrid_command(aliases=["bi"],
    usage = "send_messages",
    description = "Generate a male icon profile picture",
    brief= "None")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def boyicon(self, ctx):
            channel = ctx.message.channel
            lines = open('boyimages.txt').read().splitlines()
            myline =random.choice(lines)
            embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
            embed.set_image(url=myline)
            embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
            embed.set_footer(text="https://blame.gg/discord")
            msg = await ctx.send(embed=embed)
            try:
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
            except:
                pass


    @commands.hybrid_command(aliases=["bgif", 'bg'],
    usage = "send_messages",
    description = "Generate a male gif profile picture",
    brief= "None",)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def boygif(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('boygifs.txt').read().splitlines()
        myline =random.choice(lines)
        embed.set_image(url=myline)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass


    @commands.hybrid_command(aliases=["gi", "gicon"],
    usage = "send_messages",
    description = "Generate a female icon profile picture",
    brief= "None"
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def girlicon(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('girlimages.txt').read().splitlines()
        myline =random.choice(lines)

        embed.set_image(url=myline)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass

    @commands.hybrid_command(aliases=["ggif"],
    usage = "send_messages",
    description = "Generate a female gif profile picture",
    brief= "None")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def girlgif(self, ctx):
        channel = ctx.message.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x36393e)
        lines = open('girlgifs.txt').read().splitlines()
        myline =random.choice(lines)
        embed.set_image(url=myline)
        embed.set_author(name='Follow us on pinterest', icon_url="https://cdn.discordapp.com/attachments/843129964957794354/1025532590221971496/unknown.png", url="https://pinterest.com/blamepfps")
        embed.set_footer(text="https://blame.gg/discord")
        msg = await ctx.send(embed=embed)
        try:
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        except:
            pass

    @commands.hybrid_group(
        aliases = ['autopfps'],
        usage = 'manage_channels',
        description ="Chose a genre, have the bot send pfps of it every 40 sec"
        )
    async def autopfp(self, ctx):
        try:
            if ctx.invoked_subcommand is None:
                embed = discord.Embed(title="Command: autopfp", description=":star: **[Premium](http://discord.gg/blame)** A module that allows you to autopost pfps from different genres.\n```Syntax: autopfp [subcommand] <argument>\nExample: autopfp add #pfps girlicons```", color = discord.Color.blurple())
                embed.set_author(name="autopfp help", icon_url=ctx.me.avatar.url)
                embed.set_footer(text=f"Page 1/{len([sc for sc in self.bot.get_command('autopfp').walk_commands()])} ・ autopfp")
                return await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @autopfp.command(
        aliases = ['set'],
        usage = "Manage_channels",
        description = ":star: **[Premium](http://discord.gg/blame)** Autpost specific genre every 40 sec",
        brief = 'genre',
        help = "```Syntax: autopfp add [channel] <genre>\nExample: autopfp add #pfps girlicons```"
    )
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx):
        return await ctx.send(embed=discord.Embed(description=f":star: This command is only for **[premium users](http://discord.gg/blame)**", color=0x43B581))

    @autopfp.command(
        aliases = ['gen', 'types', 'genre'],
        usage = "Manage_channels",
        description = "View the pfp genres",
        brief = 'genre',
        help = "```Syntax: autopfp add [channel] <genre>\nExample: autopfp add #pfps girlicons```"
    )
    @commands.has_permissions(manage_channels=True)
    async def genres(self, ctx):
        genres = ['girlicons', 'girlgifs', 'boygifs', 'boyicons', 'animeicons', 'animegifs', 'banners']
        generess="\n".join(genre for genre in genres)
        return await ctx.send(embed=discord.Embed(title=f"{self.urgentmoji} Genres", description=f"```girlicons\n{generess}```", color=self.urgecolor))


    @autopfp.command(
        aliases = ['del'],
        usage = "Manage_channels",
        description = ":star: **[Premium](http://discord.gg/blame)** Remove an autopfp channel",
        brief = 'channel',
        help = "```Syntax: autopfp remove [channel]\nExample: autopfp remove #pfps```"
    )
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        return await ctx.send(embed=discord.Embed(description=f":star: This command is only for **[premium users](http://discord.gg/blame)**", color=0x43B581))


    @pfp.command(
        aliases = ['set'],
        usage = "Manage_channels",
        description = ":star: **[Premium](http://discord.gg/blame)** Set a channel that blame will autopost pfps to",
        brief = 'genre',
        help = "```Syntax: autopfp add [channel] <genre>\nExample: autopfp add #pfps girlicons```"
    )
    @commands.has_permissions(manage_channels=True)
    async def autopfpadd(self, ctx):
        return await ctx.send(embed=discord.Embed(description=f":star: This command is only for **[premium users](http://discord.gg/blame)**", color=0x43B581))




    
async def setup(bot):
    await bot.add_cog(pfpSSS(bot))