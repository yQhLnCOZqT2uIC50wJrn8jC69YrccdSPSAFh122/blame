import discord, uvloop, aiohttp, os,time, socket, os,logging,asyncio, motor.motor_asyncio, Core.help as _init, db.database as connections
from discord.ext import commands
from discord import Status
from datetime import datetime as dt
from colorama import Fore as f
from cogs.voicemaster import PersistentView
from aiohttp import AsyncResolver, ClientSession, TCPConnector
#from discord.ext.ipc.server import Server
#from discord.ext.ipc.objects import ClientPayload
from typing import Dict
from blame_redis import RivalRedis
import Core.confirm as cop_is_gae

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
class blameInitiator(commands.AutoShardedBot):
	def __init__(self):
		self.global_cd = commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.member)
		self.start_time = time.time()
		self.cluster = 1
                self.connection = motor.motor_asyncio.AsyncIOMotorClient
		self.redis = None
		super().__init__(shard_count=28, shard_ids=[0, 1, 2, 3, 4], command_prefix=connections.getprefix,help_command = _init.MyHelp(),case_insensitive = True,intents=discord.Intents().all(),activity = discord.Activity(name="discord.gg/blame", type=5),)
		#self.ipc = ipc.Server(self, secret_key="EpG7JJSv_X7zU6cgNBxn-y_WS_1A0InC")
	#@Server.route()
	#async def get_user_data(self, data: ClientPayload) -> Dict:
		#user = self.get_user(data.user_id)
		#return user._to_minimal_user_json()

def internal(self):
	settings = {
			"token":"Nzc2MTI4NDEwNTQ3MTI2MzIy.Ge-ip8.m02H5WHfSaY1540ePwRmqzDUEaLtxdCPCdqlBE",
			"client.owner_ids": [236522835089031170, 493545772718096386, 714703136270581841]}
	return settings["token"]
client = blameInitiator()
client.owner_ids = [236522835089031170, 714703136270581841, 386192601268748289, 352190010998390796]
os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
class MyBot(commands.Bot):
		async def is_owner(self, user: discord.User):
				if user.id in client.owner_ids:  # Implement your own conditions here
						return True
				return await super().is_owner(user)

@client.event
async def on_message_edit(before, after):
	await client.process_commands(after)

@client.event
async def on_ready():
	try:
		await load_extensions()
	except:
		pass

@client.check
async def cooldown_check(ctx):
	if str(ctx.invoked_with).lower() == "help":
		return True
	bucket = client.global_cd.get_bucket(ctx.message)
	retry_after = bucket.update_rate_limit()
	if retry_after:
		raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.member)
	return True

@client.check
async def command_status(ctx):
	db = client.db['commandStatus']
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
						await client.load_extension(cog)
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
				await client.load_extension(cog)
				print(f"{f.LIGHTRED_EX}[{f.RESET}{f.BLUE}(Successfully Initiated){f.RESET}{f.LIGHTRED_EX}]{f.RESET} {f.GREEN}->{f.RESET} {f.LIGHTGREEN_EX}{cog}{f.RESET}")
			except Exception as e:
				print(f"{f.YELLOW}->{f.RESET} {f.LIGHTRED_EX}Failed to load{f.RESET} {f.BLUE}->{f.RESET} {f.YELLOW}{cog}{f.RESET} Error: {f.RED}{e}{f.RESET}")
	await client.load_extension('jishaku') 





async def main():
	async with ClientSession(connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET)) as http_session:
		async with client:
			client.connection = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://verify:8FM0953pS0onhvB7@sorrow.hn7kg.mongodb.net/axis?retryWrites=true&w=majority')
			client.db = client.connection.get_database("blameDatabase")
			client.add_view(PersistentView(bot=client))
			client.http_session = http_session
			token_fetch = internal(self=client)
			logging.basicConfig(
					level=logging.INFO,
					format=f"{f.LIGHTRED_EX}[{f.RESET}{f.BLUE}%(asctime)s{f.RESET}{f.LIGHTRED_EX}]{f.RESET} {f.GREEN}->{f.RESET} {f.LIGHTCYAN_EX}%(message)s{f.RESET}",
					datefmt="%H:%M:%S",
			)
			#await client.ipc.start()
			#discord.utils.setup_logging()
			await client.start(token_fetch)
asyncio.run(main()) 
