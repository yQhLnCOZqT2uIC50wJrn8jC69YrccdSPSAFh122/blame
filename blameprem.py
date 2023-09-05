

import discord,asyncio,os
from discord.ext import commands


class blameInitiator(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=',', case_insensitive = True, intents=discord.Intents.all(),activity = discord.Activity(name="development", type=5))

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await load_extensions()
        print('------')


bot = blameInitiator()
bot.owner_ids = [236522835089031170, 714703136270581841, 386192601268748289, 753277825372389402]

@bot.event
async def on_guild_join(guild):
    await guild.leave()

async def load_extensions():
    os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
    await bot.load_extension('jishaku')

async def main():
    await bot.start('Nzc1ODc1MTE0OTM5NTgwNDM2.GYYxbW.9QayWSZf-Xw0B4HCa7LGs5Yu5kNX0wBv1lxswA')
asyncio.run(main())

