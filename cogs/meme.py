import discord, random, aiohttp, httpx, Core.utils as util
from discord.ext import commands
from typing import List
import discord.ui
from serpapi import GoogleSearch
import re, async_cse

keys = ["be619ba84ffa6cad1294ecc4ad778f8b684a768d397f8c1e5a9b467e3b29d074",
'b369359c90046731740e621aa4fe9e7b2523791721f35f12536dc015ac89e6de',
'3098eb06c653176209dca7e9a7b0ed34ff243e2a123849fc17cbacfd89fd36e6',
'72ddbbf23ca292e03a5b9663e5ba58b6b9d502e2177d8c26eaad400c4f2de0be',
'1194a3f1adc432d9dd1404d31218e2a75401de781c1f5a321707eeefd5f6c129',
'2d13391a269db6a664e61d5185a957bda3e576f536f69e9b7eb8ed63e56ac1c7']

async def search(query):
	try:
		params = {"api_key": str(random.choice(keys)),"engine": "google","q": query, "google_domain": "google.com", "gl": "us","hl": "en","num": "100","tbm": "isch", "safe": "active"}
		search = GoogleSearch(params)
		results = search.get_dict()['images_results']

		if "https://serpapi.com/search" not in results and results and results != "No searches for your query found.":
			return results
	except:
		retry = next(iter(keys)); print(retry)


class Paginator(discord.ui.View):
	def __init__(self, embeds: List[discord.Embed]):
		super().__init__(timeout=60)
		self.embeds = embeds
		self.current_page = 0

	@discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple, disabled=True)
	async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
		if self.current_page == 1:
			self.previous_page.disabled = True
		self.next_page.disabled = False
		self.current_page -= 1
		embed = self.embeds[self.current_page]

		await interaction.response.edit_message(embed=embed, view=self)

	@discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple, disabled=False)
	async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
		self.current_page += 1
		print(self.current_page)
		if self.current_page == len(self.embeds) - 1:
			self.next_page.disabled = True
		self.previous_page.disabled = False
		embed = self.embeds[self.current_page]

		await interaction.response.edit_message(embed=embed, view=self)


class memeS(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.actions = [
				'***blushes***',
				'***whispers to self***',
				'***cries***',
				'***screams***',
				'***sweats***',
				'***twerks***',
				'***runs away***',
				'***screeches***',
				'***walks away***',
				'***sees bulge***',
				'***looks at you***',
				'***notices buldge***',
				'***starts twerking***',
				'***huggles tightly***',
				'***boops your nose***',
				'***wags my tail***',
				'***pounces on you***',
				'***nuzzles your necky wecky***',
				'***unzips your pants***',
				'***licks lips***',
				'***glomps and huggles***',
				'***glomps***',
				'***looks around suspiciously***',
				'***smirks smuggly***'
				]



		self.faces = [
			"(・\`ω\´・)",
			";;w;;",
			"OwO",
			"owo",
			"UwU",
			"\>w\<",
			"^w^",
			"ÚwÚ",
			"^-^",
			":3",
			"x3",
			'Uwu',
			'uwU',
			'(uwu)',
			"(ᵘʷᵘ)",
			"(ᵘﻌᵘ)",
			"(◡ ω ◡)",
			"(◡ ꒳ ◡)",
			"(◡ w ◡)",
			"(◡ ሠ ◡)",
			"(˘ω˘)",
			"(⑅˘꒳˘)",
			"(˘ᵕ˘)",
			"(˘ሠ˘)",
			"(˘³˘)",
			"(˘ε˘)",
			"(˘˘˘)",
			"( ᴜ ω ᴜ )",
			"(„ᵕᴗᵕ„)",
			"(ㅅꈍ ˘ ꈍ)",
			"(⑅˘꒳˘)",
			"( ｡ᵘ ᵕ ᵘ ｡)",
			"( ᵘ ꒳ ᵘ ✼)",
			"( ˘ᴗ˘ )",
			"(ᵕᴗ ᵕ⁎)",
			"*:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*",
			"*˚*(ꈍ ω ꈍ).₊̣̇.",
			"(。U ω U。)",
			"(U ᵕ U❁)",
			"(U ﹏ U)",
			"(◦ᵕ ˘ ᵕ◦)",
			"ღ(U꒳Uღ)",
			"♥(。U ω U。)",
			"– ̗̀ (ᵕ꒳ᵕ) ̖́-",
			"( ͡U ω ͡U )",
			"( ͡o ᵕ ͡o )",
			"( ͡o ꒳ ͡o )",
			"( ˊ.ᴗˋ )",
			"(ᴜ‿ᴜ✿)",
			"~(˘▾˘~)",
			"(｡ᴜ‿‿ᴜ｡)",
			]

	@commands.command(
		usage = "Send_message",
		description = "Finds and returns a random subreddit memes",
		brief = "None",
		help = "```Example: meme```"
	)
	async def meme(self, ctx):
		r = httpx.get("https://meme-api.herokuapp.com/gimme")
		res = r.json()
		title = res["title"]
		ups = res["ups"]
		author = res["author"]
		spoiler = res["spoiler"]
		nsfw = res["nsfw"]
		subreddit = res["subreddit"]
		url = res["url"]
		img = res["url"]
		postlink = res["postLink"]

		em = discord.Embed(title=f"{title}", description=f"Subreddit: **{subreddit}**\n Author: **{author}**", url=postlink)
		em.set_image(url=img)
		em.set_footer(text=f"👍 {ups}| 💬 0 | Spoiler: {spoiler} | NSFW: {nsfw}")
		return await ctx.send(embed=em)

	@commands.command(
		aliases = ["imgg"],
		usage = "Send_messages",
		description = "Google some images from a query of your choice.",
		brief = "query",
		help = "```Syntax: img [query]\nExample: img elon musk```"
	)
	async def imagee(self, ctx, *, query):
		try:
			async with ctx.typing():
				results = await search(query=query)
				
				embeds=[discord.Embed(title=f"Results for {query}", description=f"[{result['title']}]({result['link']})", color=0xa3a3a3).set_image(url=result['original']).set_footer(text=f"Page {result['position']}/100 Google Image Results | safe:active", icon_url="https://images-ext-2.discordapp.net/external/2X-ElcbGoaIJUc8yTuboiHqMF0N9C3dDUyOsT9n14po/https/bleed.bot/img/google.png").set_author(name=ctx.author, icon_url=ctx.author.display_avatar) for result in results]
				await util.imgpage(ctx=ctx, embeds=embeds)
			# footer url taken from bleed credits to jon
		except:
			return await ctx.send("No results found")

	@commands.command(
		aliases = ["img"],
		usage = "Send_messages",
		description = "Google some images from a query of your choice.",
		brief = "query",
		help = "```Syntax: img [query]\nExample: img elon musk```"
	)
	async def image(self, ctx, *, query):
		try:
			async with ctx.typing():
				google = async_cse.Search("AIzaSyAL3vrVdKXNXy-DBSV69FFrA-gaCvfAiog")
				result = await google.search(query, safesearch=True, image_search=True)
				count=[result.image_url for result in result]
				embeds=[discord.Embed(title=f"Results for {query}", description=f"[{result.title}]({result.image_url})", color=0xa3a3a3).set_image(url=result.image_url).set_footer(text=f"{len(count)} Google Image Results Found | safe:active", icon_url="https://images-ext-2.discordapp.net/external/2X-ElcbGoaIJUc8yTuboiHqMF0N9C3dDUyOsT9n14po/https/bleed.bot/img/google.png").set_author(name=ctx.author, icon_url=ctx.author.display_avatar) for result in result]
				await util.imgpage(ctx=ctx, embeds=embeds)
			# footer url taken from bleed credits to jon
		except Exception as e:
			print(e)
			return await ctx.send("No results found")


	@commands.command(hidden=True)
	async def pagination(self, ctx: discord.ext.commands.Context):
		embeds = [
			discord.Embed(
				description="This is page 1"
			),
			discord.Embed(
				description="This is page 2"
			),
			discord.Embed(
				description="This is page 3"
			),
			discord.Embed(
				description="This is page 4"
			),
		]
		await ctx.send(embed=embeds[0], view=Paginator(embeds))





async def setup(bot):
	await bot.add_cog(memeS(bot))