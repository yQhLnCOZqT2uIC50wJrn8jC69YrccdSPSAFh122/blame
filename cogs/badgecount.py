import discord, Core.utils as util
import discord, os, asyncio
from discord.ext import commands


#**{len([m for m in ctx.guild.members if m.check(author=for m in ctx.guild.members)])}

class badgecouNT(commands.Cog):
    def __init__(self, client):
        self.bot = client  


    @commands.command(
        aliases = ['badgecount', 'badge'],
        usage = 'Send messages',
        description = "View badge statistics within your server",
        brief = 'None',
        help = "```Example: badges```"
    )
    async def badges(self, ctx):
        first = discord.Embed(title=f"<a:loading:921613350310383666> Analyzing {len(ctx.guild.members)}...", color=discord.Color.blurple())
        firstsend = await ctx.send(embed=first)
        await asyncio.sleep(0.8)
        second = discord.Embed(title=f"{ctx.guild.name} Badge Statistics", description=f"<:staff:921574394084618330> Discord Staff: **{len([m for m in ctx.guild.members if m.public_flags.staff])}**\n<:BadgeBugHunter:925625840488816700> Bug Hunter: **{len([m for m in ctx.guild.members if m.public_flags.bug_hunter])}**\n<:BadgeBugHunterLvl2:925644695479144478> Bug Hunter Level 2: **{len([m for m in ctx.guild.members if m.public_flags.bug_hunter_level_2])}**\n<:Moderator:985597978574200832> Discord Certified Moderator: **{len([m for m in ctx.guild.members if m.public_flags.discord_certified_moderator])}**\n<:badge_earlysupporter:921544103039230032> Early Supporter: **{len([m for m in ctx.guild.members if m.public_flags.early_supporter])}**\n<:VerifiedBotDev:921574550293073962> Early Verified Bot Developer: **{len([m for m in ctx.guild.members if m.public_flags.early_verified_bot_developer])}**\n<:CB_hypesquad:921544078468984843> Hypesquad: **{len([m for m in ctx.guild.members if m.public_flags.hypesquad])}**\n<:badge_balance:921544098773614612> Hypesquad Balance: **{len([m for m in ctx.guild.members if m.public_flags.hypesquad_balance])}**\n<:badge_bravery:921544099981570091> Hypesquad Bravery: **{len([m for m in ctx.guild.members if m.public_flags.hypesquad_bravery])}**\n<:badge_brilliance:921544101726392320> Hypequad Brilliance: **{len([m for m in ctx.guild.members if m.public_flags.hypesquad_brilliance])}**\n<:BadgePartner:925624836993204235> Discord Partner: **{len([m for m in ctx.guild.members if m.public_flags.partner])}**\n<:blurple_bot2:921812004715524157><:blurple_bot1:921812007798337546> Verified Bots: **{len([m for m in ctx.guild.members if m.public_flags.verified_bot])}**\n<:bot:921595812956479499> Bots: **{len([m for m in ctx.guild.members if m.bot and not m.public_flags.verified_bot])}**\n<a:0_boost1:921806963359252480> Boosters: **{len(ctx.guild.premium_subscribers)}**", color=discord.Color.blurple())
        second.set_footer(text=f"Total: {len(ctx.guild.members)}")
    
        await firstsend.edit(embed=second)




async def setup(client): 
   await client.add_cog(badgecouNT(client))