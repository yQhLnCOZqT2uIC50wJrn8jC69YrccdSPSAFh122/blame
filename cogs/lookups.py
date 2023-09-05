import motor.motor_asyncio, datetime, asyncio, aiohttp, requests, difflib, typing
import discord,io,os,sys,json,datetime,functools
from discord.ext import commands
from Core import utils as util
from PIL import Image
import http
from urllib.request import urlopen
from io import BytesIO
import base64
def num(number):
	return ("{:,}".format(number))

class LookupS(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = self.bot.db["guildAuth"]
		self.errorcol = 0xA90F25 # error color
		self.urgecolor = 0xF3DD6C # exclamation color
		self.error=discord.Colour.blurple()
		self.success = discord.Colour.blurple() #theme
		self.session=aiohttp.ClientSession()
		self.checkmoji = "<:blurple_check:921544108252741723>" # success emoji
		self.xmoji = "<:yy_yno:921559254677200957>" # unsuccessful emoji
		self.urgentmoji = "<:n_:921559211366838282>" # exclamation emoji

	@commands.command(name='xbox', description="show a xbox account", brief='username', usage='Send Messages', help="```Example: ;xbox cop```")
	async def xbox(self, ctx, *, username=None):
		async with ctx.typing():
			try:
				try:
					username=username.replace(" ", "%20")
				except:
					pass
				async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
					async with client.get(f"https://playerdb.co/api/player/xbox/{username}") as r:
						data = await r.json()
						try:
							embed=discord.Embed(title=data['data']['player']['username'], color=int("0f7c0f", 16), url=f"https://xboxgamertag.com/search/{username}").add_field(name='Gamerscore', value=data['data']['player']['meta']['gamerscore'], inline=True).add_field(name='Tenure', value=data['data']['player']['meta']['tenureLevel'], inline=True).add_field(name='Tier', value=data['data']['player']['meta']['accountTier'], inline=True).add_field(name='Rep', value=data['data']['player']['meta']['xboxOneRep'].strip("Player"), inline=True).set_author(name=ctx.author, icon_url=ctx.author.display_avatar).set_footer(text="Xbox", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Xbox_one_logo.svg/1024px-Xbox_one_logo.svg.png").add_field(name='Color', value=f"#{requests.get(data['data']['player']['meta']['preferredColor']).json()['primaryColor']}", inline=True)
							embed.set_thumbnail(url=data['data']['player']['avatar']).add_field(name="ID", value=data['data']['player']['id'], inline=True)
							if data['data']['player']['meta']['bio']:
								embed.description=data['data']['player']['meta']['bio']
							await ctx.reply(embed=embed)
						except:
							embed=discord.Embed(title=data['data']['player']['username'], color=int("0f7c0f", 16), url=f"https://xboxgamertag.com/search/{username}").add_field(name='Gamerscore', value=data['data']['player']['meta']['gamerscore'], inline=True).add_field(name='Tenure', value=data['data']['player']['meta']['tenureLevel'], inline=True).add_field(name='Tier', value=data['data']['player']['meta']['accountTier'], inline=True).add_field(name='Rep', value=data['data']['player']['meta']['xboxOneRep'].strip("Player"), inline=True).set_author(name=ctx.author, icon_url=ctx.author.display_avatar).set_footer(text="Xbox", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Xbox_one_logo.svg/1024px-Xbox_one_logo.svg.png").add_field(name='Color', value=f"#{requests.get(data['data']['player']['meta']['preferredColor']).json()['primaryColor']}", inline=True).add_field(name="ID", value=data['data']['player']['id'], inline=True)
							if data['data']['player']['meta']['bio']:
								embed.description=data['data']['player']['meta']['bio']
							await ctx.reply(embed=embed)
			except:
				return await ctx.send(embed=discord.Embed(description=f"{self.urgentmoji} {ctx.author.mention}: **Gamertag `{username}` not found**", color=int("faa61a", 16)))

	def crop_skin(self, raw_img):
		img = Image.open(raw_img)
		# coords of the face in the skin
		cropped = img.crop((8, 8, 16, 16))
		resized = cropped.resize((500, 500), resample=Image.NEAREST)

		output = io.BytesIO()
		resized.save(output, format="png")
		output.seek(0)

		return output
		
	@commands.command(name="minecraft", description="Shows information about a Minecraft user", brief="username", aliases=["namemc"], usage='Send Messages',help="```Example: ;namemc cop```")
	async def minecraft(self, ctx, *, user):
		async with self.session.get(f"https://api.mojang.com/users/profiles/minecraft/{user}") as resp:
			if resp.status != 200:
				return await ctx.send("Could not find user. Sorry")
			data = await resp.json()
		name = data["name"]
		uuid = data["id"]
		url=f"https://namemc.com/{name}?q={uuid}"
		# async with self.session.get(f"https://api.mojang.com/user/profiles/{uuid}/names") as resp:
		# 	if resp.status != 200:
		# 		return await ctx.send("An error occurred while fetching name history from Mojang. Sorry.")
		# 	name_history = await resp.json()
		# previous_names = []
		# for name_data in reversed(name_history):
		# 	p_name = name_data["name"]
		# 	timestamp = name_data.get("changedToAt")
		# 	if not timestamp:
		# 		previous_names.append(f"{p_name} - N/A")
		# 		continue
		# 	seconds = timestamp / 1000
		# 	date = datetime.datetime.fromtimestamp(seconds + (timestamp % 1000.0) / 1000.0)
		# 	date_str = discord.utils.format_dt(date, style="R")
		# 	human_friendly = f"{p_name} - {date_str}"
		# 	previous_names.append(discord.utils.escape_markdown(human_friendly))
		async with self.session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}") as resp:
			if resp.status != 200:
				return await ctx.send("An error occurred while fetching profile data from Mojang. Sorry.")
			profile_data = await resp.json()
		raw_texture_data = profile_data["properties"][0]["value"]
		texture_data = json.loads(base64.b64decode(raw_texture_data))
		async with self.session.get(texture_data["textures"]["SKIN"]["url"]) as resp:
			if resp.status != 200:
				return await ctx.send("An error occurred while fetching skin data from Mojang. Sorry.")
			bytes = await resp.read()
			img = io.BytesIO(bytes)

		# Crop out only the face of the skin
		partial = functools.partial(self.crop_skin, img)
		face = await self.bot.loop.run_in_executor(None, partial)

		em = discord.Embed(
			title=name,url=url,
			color=0x70B237,
		)
		em.set_thumbnail(url="attachment://face.png")
		em.set_footer(text=f"UUID: {uuid}")

		em.add_field(name="Previous Names", value="N/A")

		file = discord.File(face, filename="face.png")
		await ctx.send(embed=em, file=file)

	@commands.command(name='twitter', aliases=['twit'], help="```Example: ;twitter cop```", usage='Send Messages',description="twitter account lookup", brief="username")
	@commands.guild_only()
	async def twitter(self, ctx, *, username:str=None):
		"""Usage:
			!twitter <username>"""
		logo=self.bot.get_emoji(989747227524210708)
		if username == None:
			embed=discord.Embed(description=f"{self.warn} {ctx.author.mention}: you must include a twitter handle in the command.",color=self.error)
			embed.set_author(name=ctx.author.name, icon=ctx.author.display_avatar)
			await ctx.reply(embed=embed)
		else:
			userRequest = requests.get('https://twitter.com/i/api/graphql/mCbpQvZAw6zu_4PvuAUVVQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22' + username + '%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D', headers={"Cookie": "guest_id=v1%3A163519131615142822; kdt=dGB7SfUPKd3OrrnASFrmXzaoRVOEwodvrPetTKqS; twid=u%3D247051251; auth_token=12a8e074d3f45bec8e665f3bfd3e6a0f7ff52a0d; ct0=4d22e1f52cd8f01c9acfd59114a937ec533d46a1c9efe08ff394bdf00bad17234b97a57e5d6db9d5244a1ae65fb3fba394fa871f415b88b4267f05dea26b45ef12a51e09db284df1bed6ff324c975a60; lang=en","Sec-Ch-Ua": """-Not.A/Brand"";v=""8"", ""Chromium"";v=""102""","X-Twitter-Client-Language": "en","X-Csrf-Token": "4d22e1f52cd8f01c9acfd59114a937ec533d46a1c9efe08ff394bdf00bad17234b97a57e5d6db9d5244a1ae65fb3fba394fa871f415b88b4267f05dea26b45ef12a51e09db284df1bed6ff324c975a60","Sec-Ch-Ua-Mobile": "?0","Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA","Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36","X-Twitter-Auth-Type": "OAuth2Session","X-Twitter-Active-User": "yes","Sec-Ch-Ua-Platform": """macOS""","Accept": "*/*","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://twitter.com/markus","Accept-Encoding": "gzip, deflate","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",})
		if userRequest.text == r'{"data":{}}':
			return await ctx.reply(embed=discord.Embed(description=f"{self.warn} {ctx.author.mention}: [**@{username}**](https://twitter.com/{username}) doesn't exist", color=self.error))
		elif '"reason":"Suspended"' in userRequest.text:
			await ctx.reply(embed=discord.Embed(description=f'{self.warn} {ctx.author.mention}: [**@{username}**](https://twitter.com/{username}) is suspended', color=self.error))
			results = self.bot.api.get_user(screen_name=username)
			if not results:
				embed=discord.Embed(description=f"{self.warn} {ctx.author.mention}: **@{username}** doesn't exist",color=self.error)
				embed.set_author(name=ctx.author.name, icon=ctx.author.display_avatar)
				await ctx.reply(embed=embed)
			else:
				result = results
				imgurl=f"https://twitter.com/{username}/photo"
				if str(result.protected) == True:
					pv='🔒'
				else:
					pv=''
				if str(result.verified) == True:
					vf="<a:b_verifyblue:926931019339284561>"
				else:
					vf=""
				twtav=await http.get(imgurl, res_method="read")
				embed=discord.Embed(title=f"{result.name} (@{username}) {pv} {vf}",description=f"{result.description}", url="https://twitter.com/" + result.screen_name,color=0x1da1f2)
				embed.add_field(name="Tweets",value=num(result.statuses_count),inline=True)
				embed.add_field(name="Following",value=num(result.friends_count),inline=True)
				embed.add_field(name="Followers",value=num(result.followers_count),inline=True)
				embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
				embed.set_footer(text="Joined at "+result.created_at.strftime("%b, %Y"), icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png")
				try:
					embed.set_thumbnail(url=result.profile_image_url)
				except:
					pass
				link=f"https://twitter.com/{result.screen_name}"
				view = discord.ui.View()
				view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, emoji=logo, url=link))
				await ctx.reply(embed=embed, view=view)

	@commands.command(name='github', description='show github account information', usage='Send Messages', help="```Example: ;github antinuke0day```", brief='username')
	async def github(self, ctx, user):
		try:
			def user_data():
				url = f"https://api.github.com/users/{user}"
				
				response = urlopen(url)
				data = json.loads(response.read())

				with open(f"db/{ctx.message.guild.id}.json", "w") as f:
					json.dump(data, f, indent=4)

			user_data()

			with open(f"db/{ctx.message.guild.id}.json", "r") as f:
				data = json.load(f)

				bio = data["bio"]
				avatar = data["avatar_url"]
				followers = str(data["followers"])
				following = str(data["following"])
				twitter = data["twitter_username"]
				email = data["email"]
				company = data["company"]
				if data["blog"] == "":
					blog = "None"
				else:
					blog = data["blog"]
			
			repos = data["repos_url"]
			response = urlopen(repos)
			data = json.loads(response.read())
			url = f"https://github.com/{user}"
			git = self.bot.get_emoji(921613260720074773)
			bi = self.bot.get_emoji(921796465544822784)
			mut = self.bot.get_emoji(921796523182919780)
			folmut = self.bot.get_emoji(921796458510946374)
			twit = self.bot.get_emoji(921807071970729984)
			mail = self.bot.get_emoji(921838079118028800)
			blow = self.bot.get_emoji(921574528163938325)
			glo = self.bot.get_emoji(921613254168547388)
			tab = self.bot.get_emoji(921753792641392690)
			url2 = f"https://github.com/{user}?tab=following"
			url3 = f"https://github.com/{user}?tab=followers"
			url4 = f"https://github.com/{user}?tab=repositories"
			url5 = f"https://twitter.com/{twitter}"

			embed = discord.Embed(title=f"GitHub Search {git}", description=f"[{user}]({url})", colour=discord.Color.blurple())
			embed.set_thumbnail(url=avatar)
			embed.add_field(name=f"{bi} __Bio__", value=f'{bio}')
			embed.add_field(name=f"{mut} __Followers__", value=f'[{followers}]({url3})')
			embed.add_field(name=f"{folmut} __Following__", value=f'[{following}]({url2})')
			embed.add_field(name="__Socials__", value=f"{twit} **Twitter:** [{twitter}]({url5})\n{mail} **Email:** {email}\n{blow} **Blog:** {blog}\n{glo} **Company** {company}\n{tab} **Repositories:** [{(len(data))}]({url4})")

			#repos = data["repos_url"]
		#  response = urlopen(repos)
		# data = json.loads(response.read())
		# for i in range(len(data)):
			#    embed.add_field(name=(len(data)), value=(len(data)))

			await ctx.send(embed=embed)
		except Exception as e:
			print(e)

	@commands.command(name='wanted', description="wanted poster of a member's avatar", usage='Send Messages', help="```Example: ;wanted @cop#0001```", brief="member")
	async def wanted(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		wanted = Image.open("assets/wanted.jpg")
		print("jje")

		asset = user.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)

		pfp = pfp.resize((177,177))

		wanted.paste(pfp, (120,212))

		wanted.save("assets/profile.jpg")

		await ctx.send(file = discord.File("assets/profile.jpg"))

	@commands.command(name='rip', description="rips a member's avatar", usage="Send Messages", help="```Example: ;rip @cop#0001```", brief="member")
	async def rip(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		rip = Image.open("assets/rip.png")

		asset = user.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)

		pfp = pfp.resize((177,177))

		rip.paste(pfp, (120,250))

		rip.save("assets/profile2.png")

		await ctx.send(file = discord.File("assets/profile2.png"))

	@commands.command(name='burn', description="burn a member's avatar", usage='Send Messages', help="```Example: ;burn @cop#0001```", brief="member")
	async def burn(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		burn = Image.open("assets/burn.gif")

		asset = user.display_avatar.with_size(128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)


		pfp = pfp.resize((140,140))

		burn.paste(pfp, (130,130))

		burn.save("assets/burn2.gif", save_all=True)

		await ctx.send(file = discord.File("assets/burn2.gif"))

	@commands.command(name='triggered', description="shows a member's avatar as triggered", help="```Example: ;triggered @cop#0001```", brief="member", usage='Send Messages')
	async def triggered(self, ctx, member: discord.Member=None):
		if not member: # if no member is mentioned
			member = ctx.author # the user who ran the command will be the member
			
		async with aiohttp.ClientSession() as trigSession:
			async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.display_avatar.with_size(1024)}') as trigImg: # get users avatar as png with 1024 size
				imageData = BytesIO(await trigImg.read()) # read the image/bytes
				
				await trigSession.close() # closing the session and;
				
				await ctx.reply(file=discord.File(imageData, 'triggered.gif'))


	@commands.command(name='blame', description="blameify a member's avatar", brief='member', usage='Send Messages', help="```Example: ;blame @cop#0001```",aliases = ['blameify'])
	async def blame(self, ctx, member: discord.Member = None):
		member = member or ctx.author
		async with ctx.typing():
			async with aiohttp.ClientSession() as session:
				async with session.get(
				f'https://some-random-api.ml/canvas/blurple?avatar={member.display_avatar.replace(static_format="png")}'
			) as af:
					if 300 > af.status >= 200:
						fp = BytesIO(await af.read())
						file = discord.File(fp, "blurple.png")
						em = discord.Embed(
							color=discord.Color.blurple(),
						)
						em.set_image(url="attachment://blurple.png")
						await ctx.send(embed=em, file=file)
					else:
						await ctx.send('I failed... Sorry')
					await session.close()

	@commands.command(name='lgbtq', description="lgbtqify a member's avatar", usage='Send Messages', brief='member', help="```Example: ;lgbtq @sorrow#1984```")
	async def lgbtq(self, ctx, member: discord.Member = None):
		'''Horny license just for u'''
		member = member or ctx.author
		async with ctx.typing():
			async with aiohttp.ClientSession() as session:
				async with session.get(
				f'https://some-random-api.ml/canvas/gay?avatar={member.display_avatar.with_size(128).with_static_format("png")}'
			) as af:
					if 300 > af.status >= 200:
						fp = BytesIO(await af.read())
						file = discord.File(fp, "gay.png")
						em = discord.Embed(
							color=discord.Color.blurple(),
						)
						em.set_image(url="attachment://gay.png")
						await ctx.send(embed=em, file=file)
					else:
						await ctx.send('No horny :(')
					await session.close()


async def setup(bot):
	await bot.add_cog(LookupS(bot))