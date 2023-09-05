import os, string, random
import re
import aiohttp
import discord
from shazamio import Shazam
from pydub import AudioSegment
from discord.ext import tasks, commands
from ast import Bytes
from TTApi import TikTokApi
from io import BytesIO
#AudioSegment.converter = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe ="C:\\ffmpeg\\ffmpeg\\bin\\ffprobe.exe"

AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AudioSegment.ffprobe ="/usr/bin/ffprobe"
tiktok = TikTokApi()

class Tiktok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


   # @commands.Cog.listener()
    #async def on_message(self, msg):
      #  if msg.author.bot: return
       # if msg.content.startswith('blame '):
           # async with msg.channel.typing():
              #  async def down():
                    #link = msg.content.strip('blame ')
                    #video_data = tiktok.video.parse_video_data(link)
                   # no_watermark_download = video_data["download_urls"]["no_watermark"]
                   # video_binary = tiktok.video.get_video_binary(no_watermark_download)
                   # bytes_io = BytesIO(video_binary) # discord.py takes this shit for some reason
                    #embed = discord.Embed(color =0x000000)
                    #embed.description = f'**{video_data["description"]}]**'
                    #embed.set_author(name="Tiktok by @"+video_data["author"]["username"], icon_url="https://cdn.discordapp.com/emojis/1010602768660181012.png?size=256", url=video_data["video_url"])
                    #embed.set_footer(text=f"💬 {video_data['stats']['comment_count']} | 👍 {video_data['stats']['likes']} | 🔗 {video_data['stats']['shares']} ({video_data['stats']['views']} views)\n🎵 {video_data['music']['title']} (by {video_data['music']['author']})")
                    #await msg.reply(file=discord.File(fp=bytes_io, filename="tiktok.mp4"), embed=embed)
                #await down()
        #else:
            #return

    @commands.command()
    async def fyp(self, ctx):
        async with ctx.typing():
            #async def down():
                #fyp_videos = tiktok.feed.for_you()
                #random_num = random.randint(1, 10)
               # no_watermark_download = fyp_videos[random_num]["download_urls"]["no_watermark"]
                #video_binary = tiktok.video.get_video_binary(no_watermark_download)
                #bytes_io = BytesIO(video_binary)
                #embed = discord.Embed(color =0x000000)
               # embed.set_author(name=f"{fyp_videos[random_num]['author']['username']}・{fyp_videos[random_num]['author']['user_id']}", icon_url="https://cdn.discordapp.com/emojis/1010602768660181012.png?size=256", url=fyp_videos[random_num]['video_url'])
               # embed.description = f'**{fyp_videos[random_num]["description"]}**'
                #embed.set_author(name="Tiktok by @"+video_data["author"]["username"], icon_url="https://cdn.discordapp.com/emojis/1010602768660181012.png?size=256", url=video_data["video_url"])
                #embed.set_footer(text=f"💬 {fyp_videos[random_num]['stats']['comment_count']} | 👍 {fyp_videos[random_num]['stats']['likes']} | 🔗 {fyp_videos[random_num]['stats']['shares']} ({fyp_videos[random_num]['stats']['views']} views)\n🎵 {fyp_videos[random_num]['music']['title']} (by {fyp_videos[random_num]['music']['author']})")
                #await ctx.reply(file=discord.File(fp=bytes_io, filename="tiktok.mp4"), embed=embed)
            await ctx.send("This command is currently being fixed")

   

async def setup(bot):
    await bot.add_cog(Tiktok(bot))
