import os, string, random, io,orjson
import re
import aiohttp, textwrap
import discord
import datetime
import re,aiohttp,orjson,discord,io
from humanize import intword
from typing import Optional
import binascii
import os
from re import findall
from io import BytesIO
from PIL import Image
from httpx import AsyncClient
from pytube import YouTube
import pytube
import binascii, asyncio, time
import button_paginator as pg
#from shazamio import Shazam
#from pydub import AudioSegment
from discord.ext import tasks, commands
from ast import Bytes
def find_hashtags(text):
    r=re.findall("(#+[a-zA-Z0-9(_)]{1,})",text)
    return r

spotify_token = ""
spotify_token_expiry = 0.0
async def get_spotify_token() -> str:
    global spotify_token, spotify_token_expiry
    if spotify_token_expiry - 300 > time.time():
        print(f"using spotify token: {spotify_token[:41]}")
        return spotify_token
    async with aiohttp.ClientSession() as session:
        async with session.post("https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=aiohttp.BasicAuth('c8eaa24eae5449e2a376a4ea831ec87b', 'ea7dde97dbb74132bfbd65589c9a816b'),
        ) as r:
            spot = await r.json()
            spotify_token = spot["access_token"]
            spotify_token_expiry = time.time() + 3600
            print(f"updated spotify token: {spotify_token[:41]}")
            return spotify_token

async def get_video_binary(download_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as video:
                binary=await video.read()
        return binary
    except Exception as e:
        print(e)

def formatt(text):
    if " thousand" in text:
        text=text.replace(" thousand", "k")
    if " million" in text:
        text=text.replace(" million", "m")
    return text

async def make_embed(ctx, data):
    desc=data['desc']

    if data['is_video']==True:
        stats=data['stats']
        digg_count=stats['digg_count']
        play_count=stats['play_count']
        comment_count=stats['comment_count']
        author_name=data['username']
        author_icon=data['avatar']
        hashtags=find_hashtags(desc)
        des=desc.split(" ")
        for d in des:
            if d.startswith("#"):
                des.remove(d)
        text=f"\n❤️  {formatt(intword(digg_count))}   👀  {formatt(intword(play_count))}   💬  {formatt(intword(comment_count))} "
        description=re.sub("#(\w+)",""," ".join(d for d in des))
        embed=discord.Embed(description=f"[{' '.join(d for d in des)}]({data['url']})",color=0x000000).set_author(name=author_name,icon_url=author_icon)
        embed.set_footer(text=f"{text} ∙ {str(ctx.author)}", icon_url='https://cdn.discordapp.com/attachments/851633587915587615/1041917050152554536/TikTok.png')
        async with aiohttp.ClientSession() as session:
            async with session.get(data['items']) as j:
                file=discord.File(fp=io.BytesIO(await j.read()),filename='blame_tiktok.mp4')
        return await ctx.send(embed=embed,file=file)
    else:
        stats=data['stats']
        digg_count=stats['digg_count']
        play_count=stats['play_count']
        comment_count=stats['comment_count']
        author_name=data['username']
        author_icon=data['avatar']
        hashtags=find_hashtags(desc)
        des=desc.split(" ")
        for d in des:
            if d.startswith("#"):
                des.remove(d)
        embeds=[]
        d=0
        for i in data['items']:
            d+=1
            text=f"\n❤️  {formatt(intword(digg_count))}   👀  {formatt(intword(play_count))}   💬  {formatt(intword(comment_count))} | Page {d}/{len(data['items'])}"
            description=re.sub("#(\w+)",""," ".join(d for d in des))
            embed=discord.Embed(description=f"[TikTok]({data['url']}) Requested by {str(ctx.author)}\n"+" ".join(d for d in des),color=5793266).set_author(name=author_name,icon_url=author_icon)
            embed.set_footer(text=text)
            embed.set_image(url=i)
            embeds.append(embed)
        paginator = pg.Paginator(ctx.bot, embeds, ctx, invoker=ctx.author.id)
        if len(embeds) > 1:
            paginator.add_button('prev', emoji='<:left:934237439772483604>', style=discord.ButtonStyle.blurple)
            paginator.add_button('next', emoji='<:right:934237462660788304>', style=discord.ButtonStyle.blurple)
            paginator.add_button('goto', label=None, emoji="<:filter:1000215652591734874>", style=discord.ButtonStyle.blurple)
            paginator.add_button('delete', emoji='<:stop:958054042637054013>', label=None, style=discord.ButtonStyle.blurple)
        await paginator.start()
        await paginator.start()#AudioSegment.converter = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffprobe ="C:\\ffmpeg\\ffmpeg\\bin\\ffprobe.exe"

#AudioSegment.converter = "/usr/bin/ffmpeg"
#AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
#AudioSegment.ffprobe ="/usr/bin/ffprobe"
#tiktok = TikTokApi()



class Tiktok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session=aiohttp.ClientSession()
#binascii.hexlify(os.urandom(8))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        if msg.content.startswith('blame '):
            ctx=await self.bot.get_context(msg)
            link = msg.content.strip('blame ')
            spotify = "https?://open.spotify.com/(?P<type>album|playlist|track)/(?P<id>[a-zA-Z0-9]+)"
            get = re.search(spotify, link)
            is_true = "((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            true = re.search(is_true, link)
            if "tiktok" in msg.content.lower():
                async with ctx.typing():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://api.rival.rocks/tiktok?url={link}",headers={'api-key':"64bc1eab-4f0a-4feb-a18e-7c6c82e73654"}) as f:
                            if f.status == 200:
                                c=await f.json()
                    return await make_embed(ctx=ctx,data=c)
            if get:
                async with ctx.typing():
                    try:
                        link1 = msg.content.strip("blame https://open.spotify.com/track/")
                        full_link = msg.content.strip("blame ")
                        headers = {"Authorization": f"Bearer {await get_spotify_token()}"}
                        base = f"https://api.spotify.com/v1/tracks/"
                        async with aiohttp.ClientSession() as session:
                            async with session.get(str(base+link1), headers=headers) as scrape:
                                results = await scrape.json()
                                artist = results['album']['artists'][0]['name']
                                name = results['name']
                                image = results['album']['images'][0]['url']
                                query = {}
                                query = str(artist+name)
                                params = {'search_query': query}
                                async with aiohttp.ClientSession() as s:
                                    async with s.get('http://www.youtube.com/results?', params=params) as html_content:
                                        a = await html_content.text()
                                        search_results = re.findall(r'\/watch\?v=([a-zA-Z0-9_-]{11})', a)
                                        link = f'https://youtube.com/watch?v={search_results[0]}'
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

                                            stream = video.streams.filter(only_audio=True).first()
                                            if stream != "720p":
                                                stream = video.streams.filter(only_audio=True).first()
                                                if stream is None:
                                                    if resolution != "360p":
                                                        stream = video.streams.filter(only_audio=True).first()
                                                    if stream is None:
                                                        if resolution != "144p":
                                                            stream = video.streams.filter(only_audio=True).first()
                                                        else:
                                                            stream = None
                                            stream.stream_to_buffer(buffer)
                                            buffer.seek(0)
                                            file_ = discord.File(buffer, filename=f"blameSpotify.mp3")
                                            return file_
                                        def get_vid():
                                            video = pytube.YouTube(str(link))
                                            return video
                                        async def get(ctx):
                                            file = await self.bot.loop.run_in_executor(None, download)
                                            if file:
                                                video = await self.bot.loop.run_in_executor(None, get_vid)
                                                return await msg.channel.send(file=file, embed=discord.Embed(description=f"**[{artist} - {name}]({full_link})**", color=0x1ed55f).set_footer(text=f" 🎶 {video.views:,} play's ∙ {msg.author}", icon_url='https://cdn.discordapp.com/attachments/851633587915587615/1041433951727788174/spotify.gif').set_author(name=artist, icon_url=image))
                                            else:
                                                return await ctx.send("Something went wrong")
                                        return await get(link)
                    except Exception as e:
                        pass; print(e); return await msg.channel.send("URL unavailable at this time. Try again later..")
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
                            #descrip = textwrap.shorten(f'{video.description}', width=100, placeholder='...')
                            mins, secs = divmod(video.length, 60)
                            return await msg.channel.send(file=file, embed=discord.Embed(description=f"**[{video.author} - {video.title}]({video.channel_url})**", color=0xff0404).set_footer(text=f"⏰ {mins}:{secs} 💻 720p 👀 {video.views:,} ∙ {msg.author}", icon_url="https://cdn.discordapp.com/attachments/851633587915587615/1041441974596665364/youtube.gif").set_author(name=video.author, icon_url=video.thumbnail_url))
                        else:
                            return await msg.channel.send('Something went wrong..')
                    return await get(msg)


            #else:
              #  if link.startswith('https') or link.startswith('http'):
                   # async with msg.channel.typing():
                      #  newLink = f"https://api.trace.moe/search?url={link}"
                    #    async with aiohttp.ClientSession() as ses:
                         #   async with ses.get(newLink) as resp:
                              #  b = await resp.json()
                             #   link2 = b['result'][0]['video']
                               # async with ses.get(link2) as p:
                                 #   with io.BytesIO(await p.read()) as file:
                                        #anime = b['result'][0]['filename'].split('-', 1)
                                      #  ep = b['result'][0]['episode']
                                        #return await msg.reply(embed=discord.Embed(description=f"**{anime[0]} Episode {ep}**", color=0x000000).set_footer(text=f"⏪ {b['result'][0]['from']}  ⏩ {b['result'][0]['to']} ❤️ {b['result'][0]['anilist']}"), file = discord.File(file, 'blame_anime.mp4'))
                #else:
                   # return


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
