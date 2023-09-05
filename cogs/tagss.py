import discord,orjson,socket
from discord.ext import commands, tasks
import typing, humanize
import datetime,unidecode
import humanfriendly
import tweepy
import random, re, asyncio, aiohttp
from discord import ui, Interaction, app_commands, Object, AppCommandType
from datetime import timedelta
from typing import Union
from datetime import datetime
from io import BytesIO
from collections import deque
from discord.ext.commands import errors
import psutil
import requests, os, ast, inspect
from bs4 import BeautifulSoup
from typing import Union
import time
import logging
logger = logging.getLogger(__name__)

class tagss(commands.Cog, name="tagss"):
	"""Custom server commands"""

	def __init__(self, bot):
		self.bot = bot
		self.icon = "📌"
		self.tags={}
		self.tagloop.start()

	@commands.Cog.listener()
	async def on_user_update(self, before, after):
		if before.name == after.name:
			return
		beforetag=f"{before.name}#{before.discriminator}"
		aftertag=f"{after.name}#{after.discriminator}"
		if beforetag != aftertag:# and not after.id in self.bot.cache.nodata:#await self.bot.db.execute("""SELECT * FROM nodata WHERE user_id = %s""", before.id):
			tag=f"{before.name}#{before.discriminator}"
			if before.name.isalpha() and before.name == unidecode.unidecode(before.name) and len(before.name) < 9:
				if str(before.discriminator) not in self.tags:
					self.tags[str(before.discriminator)]=[]
				self.tags[str(before.discriminator)].append(f"**{discord.utils.escape_markdown(before.name)}#{before.discriminator}** - {discord.utils.format_dt(datetime.now(), style='R')}")
				await self.bot.redis.set(f"tagsblame", orjson.dumps(self.tags))

	@tasks.loop(hours=5)
	async def tagloop(self):
		#self.tags.clear()
		self.tags.clear()
		logger.info("Cleared Tag Table")

	@tagloop.before_loop
	async def before(self):
		await self.bot.wait_until_ready()
		logger.info("Starting Tag Clear Loop")



async def setup(bot):
	await bot.add_cog(tagss(bot))