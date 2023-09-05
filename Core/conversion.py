import os, string, random, io,orjson
import re
import aiohttp, textwrap
import discord
from pytube import YouTube
import pytube
import binascii, asyncio, time
#from shazamio import Shazam
#from pydub import AudioSegment
from discord.ext import tasks, commands
from ast import Bytes
#AudioSegment.converter = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe ="C:\\ffmpeg\\ffmpeg\\bin\\ffprobe.exe"

#AudioSegment.converter = "/usr/bin/ffmpeg"
#AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
#AudioSegment.ffprobe ="/usr/bin/ffprobe"
#tiktok = TikTokApi()



class Tiktok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def get_video_binary(self, download_url):
        """
        DOWNLOAD_URL (str):
            Get this from the object that the parse_video_data function returns, it can either be download_video_url or download_video_url_watermark
            
        Returns:
            binary: Raw binary mp4 data        
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as video:
                    binary=await video.read()
            #self.api.debug.success(f"Received binary data ({video.elapsed.total_seconds()}s)")
            return binary
        except Exception as e:
            print(e)
            
    async def get_data(self, url):
        """Grabs the video data from a tiktok video url
        
        URL/VIDEO_ID (str):
            https://vm.tiktok.com/ZMNnX3Q4q 
            7116227445648395526 
            https://www.tiktok.com/@peachyfitness4/video/7116227445648395526
        
        RAW (bool):
            Optional if u want the raw data tiktok provided from the video (this contains way more info)
            
        Returns:
            formatted data from the video in a json object 
            
        """
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://tikwm.com/api?url={url}") as f:
                d=await f.json()
                return d['data']


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        if msg.content.startswith('blame '):
            link = msg.content.strip('blame ')
            is_true = "((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            true = re.search(is_true, link)
            if "tiktok" in msg.content.lower():
                data=await self.get_data(url=link)
                if data:
                    embed=discord.Embed(description=data['title'], color=discord.Color.blurple()).set_author(name=data['author']['nickname'],icon_url=data['author']['avatar'].replace("\\\\", "\\"))
                    async with aiohttp.ClientSession() as session:
                        async with session.get(data['play'].replace("\\\\","\\")) as f:
                            video_binary=await f.read()
                    await msg.channel.send(embed=embed,file=discord.File(fp=video_binary, filename='blametiktok.mp4'))
            if true:
                async with msg.channel.typing():
                    def download(url=link):
                        resolution= "720p"
                        method = "mp4"
                        try:
                            video = pytube.YouTube(str(url))
                        except Exception as exc:
                            raise exc
                        if video.length > 900:
                            raise TypeError("The video cannot be longer than 15 minutes.")
                        buffer = io.BytesIO()

                        stream = video.streams.filter(file_extension="mp4", res=resolution).first()
                        if stream != "720p":
                            stream = video.streams.filter(file_extension="mp4", res="720p").first()
                            if stream is None:
                                if resolution != "360p":
                                    stream = video.streams.filter(file_extension="mp4", res="360p").first()
                                if stream is None:
                                    if resolution != "144p":
                                        stream = video.streams.filter(file_extension="mp4", res="144p").first()
                                    else:
                                        stream = None
                        stream.stream_to_buffer(buffer)
                        buffer.seek(0)
                        file_ = discord.File(buffer, filename=f"blameYoutube.mp4")
                        return file_
                    def get_vid():
                        video = pytube.YouTube(str(link))
                        return video
                    async def get(ctx):
                        file = await self.bot.loop.run_in_executor(None, download)
                        if file:
                            video = await self.bot.loop.run_in_executor(None, get_vid)
                            descrip = textwrap.shorten(f'{video.description}', width=100, placeholder='...')
                            return await ctx.reply(file=file, embed=discord.Embed(description=f"<a:youtube:921863397623087184> **[{video.author} - {video.title}]({video.channel_url})**\n{descrip}", color=0x000000).set_footer(text=f"⏩ {video.length} 💻 720p 👀 {video.views:,}").set_thumbnail(url=video.thumbnail_url))
                        else:
                            return await ctx.send('Something went wrong..')
                    return await get(msg)

            else:
                if link.startswith('https') or link.startswith('http'):
                    async with msg.channel.typing():
                        newLink = f"https://api.trace.moe/search?url={link}"
                        async with aiohttp.ClientSession() as ses:
                            async with ses.get(newLink) as resp:
                                b = await resp.json()
                                link2 = b['result'][0]['video']
                                async with ses.get(link2) as p:
                                    with io.BytesIO(await p.read()) as file:
                                        anime = b['result'][0]['filename'].split('-', 1)
                                        ep = b['result'][0]['episode']
                                        return await msg.reply(embed=discord.Embed(description=f"**{anime[0]} Episode {ep}**", color=0x000000).set_footer(text=f"⏪ {b['result'][0]['from']}  ⏩ {b['result'][0]['to']} ❤️ {b['result'][0]['anilist']}"), file = discord.File(file, 'blame_anime.mp4'))
                else:
                    return


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

    @commands.command()
    async def aaa(self, ctx, aa):
        def download(url=aa):
            resolution= "720p"
            method = "mp4"
            try:
                video = pytube.YouTube(str(url))
            except Exception as exc:
                raise exc
            if video.length > 900:
                raise TypeError("The video cannot be longer than 15 minutes.")
            buffer = io.BytesIO()

            stream = video.streams.filter(file_extension="mp4", res=resolution).first()
            if stream != "720p":
                stream = video.streams.filter(file_extension="mp4", res="720p").first()
                if stream is None:
                    if resolution != "360p":
                        stream = video.streams.filter(file_extension="mp4", res="360p").first()
                    if stream is None:
                        if resolution != "144p":
                            stream = video.streams.filter(file_extension="mp4", res="144p").first()
                        else:
                            stream = None
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            file_ = discord.File(buffer, filename=f"123.mp4")
            return file_
        def get_vid():
            video = pytube.YouTube(str(aa))
            return video
        async def get(ctx):
            file = await self.bot.loop.run_in_executor(None, download)
            if file:
                video = await self.bot.loop.run_in_executor(None, get_vid)
                descrip = textwrap.shorten(f'{video.description}', width=100, placeholder='...')
                return await ctx.reply(file=file, embed=discord.Embed(description=f"<a:youtube:921863397623087184> **[{video.author} - {video.title}]({video.channel_url})**\n{descrip}", color=0x000000).set_footer(text=f"⏩ {video.length} 💻 720p 👀 {video.views:,}").set_thumbnail(url=video.thumbnail_url))
            else:
                return await ctx.send('error')
        return await get(ctx)
            #return await ctx.send(file=discord.File(buffer, filename=f"123.mp4" if method == "mp4" else f"123.mp3"))
        #return self.Video(file_, video.length, stream.resolution, video.watch_url, video.views)


async def setup(bot):
    await bot.add_cog(Tiktok(bot))
