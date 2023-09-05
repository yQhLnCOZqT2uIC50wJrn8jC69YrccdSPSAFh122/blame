import aioredis, asyncio
from discord.ext import commands, tasks
from os import environ


class redis(commands.Cog):
    """For redis."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pool = None
#        self._connect_task = self.bot.loop.create_task(self.connect())
        self.cache_values.start()

    async def connect(self):
        self.pool = await aioredis.create_redis_pool(f"redis://127.0.0.1:6379", encoding='utf-8')
        self.bot.redis=self.pool
        print(f"Connected to Pool")

    #async def close(self):
   #     self.pool.close()
  #      await self.pool.wait_closed()

    async def wait_until_ready(self):
        await self._connect_task

 #   def cog_unload(self):
 #       self.bot.loop.create_task(self.close())

    async def cache(self):
        await self.bot.redis.set(f'g{self.bot.cluster}',len(self.bot.guilds))
        await self.bot.redis.set(f'm{self.bot.cluster}',sum(self.bot.get_all_members()))

    @tasks.loop(minutes=10)
    async def cache_values(self):
        try:
            await self.bot.redis.set(f'g{self.bot.cluster}',len(self.bot.guilds))
            await self.bot.redis.set(f'm{self.bot.cluster}',sum(self.bot.get_all_members()))
            print("Successful Statistic Cache")
        except Exception as e:
            print(f"Redis Loop Exception: {e}")
            pass
        



async def setup(bot: commands.Bot):
    await bot.add_cog(redis(bot))
