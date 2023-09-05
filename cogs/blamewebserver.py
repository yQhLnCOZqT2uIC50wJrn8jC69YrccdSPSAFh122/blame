import os,json,aiohttp,socket,datetime,discord,asyncio,unidecode
import ssl
from datetime import datetime
import aiohttp_cors
from aiohttp import web
from discord.ext import commands, tasks
from prometheus_async import aio
from Core import log

apikeys=['adminrivalkey1337','adminblamekey1337']

logger = log.get_logger(__name__)

loop=asyncio.new_event_loop()

USE_HTTPS = os.environ.get("WEBSERVER_USE_HTTPS", "no")
HOST = os.environ.get("WEBSERVER_HOSTNAME")
PORT = int(os.environ.get("WEBSERVER_PORT", 0))
SSL_CERT = os.environ.get("WEBSERVER_SSL_CERT")
SSL_KEY = os.environ.get("WEBSERVER_SSL_KEY")


class WebServer(commands.Cog):
    """Internal web server to provice realtime statistics to the website"""

    def __init__(self, bot):
        self.bot = bot
        self.tags = {}
        self.app = web.Application()
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/tags", self.rival_lookup)
        # Configure default CORS settings.
        self.cors = aiohttp_cors.setup(
            self.app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            },
        )

        # Configure CORS on all routes.
        for route in list(self.app.router.routes()):
            self.cors.add(route)

        # https
        if USE_HTTPS == "yes":
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(SSL_CERT, SSL_KEY)
        else:
            self.ssl_context = None

    async def cog_load(self):
        loop.create_task(self.run())

    async def cog_unload(self):
        self.cache_stats.cancel()
        await self.shutdown()

    async def rival_lookup(self,request):
        d={}
        d['status']="Success"
        d['tags']=self.tags
        return web.Response(text=json.dumps(d),status=200)


    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name == after.name:
            return
        beforetag=f"{before.name}#{before.discriminator}"
        aftertag=f"{after.name}#{after.discriminator}"
        if beforetag != aftertag:
            tag=f"{before.name}#{before.discriminator}"
            if before.name.isalpha() and before.name == unidecode.unidecode(before.name) and len(before.name) < 9:
                if str(before.discriminator) not in self.tags:
                    self.tags[str(before.discriminator)]=[]
                self.tags[str(before.discriminator)].append(f"{before.name}#{before.discriminator} • {discord.utils.format_dt(datetime.now(), style='R')}")

    async def shutdown(self):
        await self.app.shutdown()
        await self.app.cleanup()

    async def run(self):
        await self.bot.wait_until_ready()
        if HOST is not None:
            try:
                logger.info(f"Starting webserver on {HOST}:{PORT}")
                await web._run_app(
                    self.app,
                    host="127.0.0.1",
                    port="6969",
                    access_log=logger,
                    print=None,
                    ssl_context=self.ssl_context,
                )
            except OSError as e:
                logger.warning(e)

    @staticmethod
    async def index(request):
        return web.Response(text="Welcome to Blames's IPC API, Powered by Rival")


async def setup(bot):
    await bot.add_cog(WebServer(bot))
