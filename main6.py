import discord, uvloop, aiohttp, os,time, socket, os,logging,asyncio, motor.motor_asyncio, Core.help as _init, db.database as connections
from discord.ext import commands
from discord import Status
from datetime import datetime as dt
from colorama import Fore as f
from cogs.voicemaster import PersistentView
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from typing import Dict
from blame_redis import RivalRedis
import Core.confirm as cop_is_gae
from dotenv import load_dotenv
load_dotenv(verbose=True)

os.environ["JISHAKU_NO_UNDERSCORE"] = "true"

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class blame(commands.AutoShardedBot):
	def __init__(self):
		self.global_cd = commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.member)
		self.start_time = time.time()
		self.cluster = 6
		super().__init__(shard_count=30, shard_ids=[25,26,27,28,29], owner_ids=[236522835089031170, 493545772718096386, 714703136270581841,1082429362420326421],command_prefix=connections.getprefix,help_command = _init.MyHelp(),case_insensitive = True,intents=discord.Intents().all(),activity = discord.Activity(name="discord.gg/blame", type=5),)

	async def setup_hook(self):
		self.redis = await RivalRedis.from_url()
		self.sesh = ClientSession(connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET))
		self.connection = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://verify:8FM0953pS0onhvB7@sorrow.hn7kg.mongodb.net/axis?retryWrites=true&w=majority')
		self.db = self.connection.get_database("blameDatabase")
		self.add_view(PersistentView(bot=self))
		self.http_session = self.sesh

bot = blame()

@bot.event
async def on_message_edit(before, after):
	if before.content != after.content:
		await bot.process_commands(after)

@bot.event
async def on_ready():
	try:
		await load_extensions()
	except:
		pass

@bot.check
async def cooldown_check(ctx):
	if str(ctx.invoked_with).lower() == "help":
		return True
	bucket = bot.global_cd.get_bucket(ctx.message)
	retry_after = bucket.update_rate_limit()
	if retry_after:
		raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.member)
	return True

@bot.check
async def command_status(ctx):
	db = bot.db['commandStatus']
	fetchGuild = await db.find_one({'guild_id': ctx.guild.id})
	if fetchGuild:
		status = fetchGuild['disabled']
		if str(ctx.command) in status:
			await ctx.send(embed=discord.Embed(description=f"<:SystemMessageWarn:1039319472026177676> {ctx.author.mention}: This command is **disabled** in this **server**", color=0xfaa61b), delete_after=8)
			return False
		else:
			return True
	else:
		return True

async def load_extensions():
	folders = []
	for i in os.listdir("cogs"):
		if i == "__pycache__": pass
		elif i in folders: 
			for x in os.listdir(f"cogs/{i}"):
				if x == "__pycache__": pass
				elif x == "oldanti" or x == "oldwelc": pass
				else:
					cog = f"cogs.{i}.{x[:-3]}"
					try:
						await bot.load_extension(cog)
						logging.basicConfig(
								level=logging.INFO,
								format=f"{f.LIGHTRED_EX}[{f.RESET}{f.BLUE}%(asctime)s{f.RESET}{f.LIGHTRED_EX}]{f.RESET} {f.GREEN}->{f.RESET} {f.LIGHTCYAN_EX}%(message)s{f.RESET}",
								datefmt="%H:%M:%S",
						)
						print(f"{f.LIGHTRED_EX}[{f.RESET}{f.BLUE}(Successfully Initiated){f.RESET}{f.LIGHTRED_EX}]{f.RESET} {f.GREEN}->{f.RESET} {f.LIGHTGREEN_EX}{cog}{f.RESET}")
					except Exception as e:
						print(f"{f.YELLOW}->{f.RESET} {f.LIGHTRED_EX}Failed to load{f.RESET} {f.BLUE}->{f.RESET} {f.YELLOW}{cog}{f.RESET} Error: {f.RED}{e}{f.RESET}")
		else:
			cog = f"cogs.{i[:-3]}"
			try:
				await bot.load_extension(cog)
				print(f"{f.LIGHTRED_EX}[{f.RESET}{f.BLUE}(Successfully Initiated){f.RESET}{f.LIGHTRED_EX}]{f.RESET} {f.GREEN}->{f.RESET} {f.LIGHTGREEN_EX}{cog}{f.RESET}")
			except Exception as e:
				print(f"{f.YELLOW}->{f.RESET} {f.LIGHTRED_EX}Failed to load{f.RESET} {f.BLUE}->{f.RESET} {f.YELLOW}{cog}{f.RESET} Error: {f.RED}{e}{f.RESET}")
	await bot.load_extension('jishaku') 

if __name__ == "__main__":
	bot.run(os.environ['token'])

