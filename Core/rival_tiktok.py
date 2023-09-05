from datetime import datetime
import re,aiohttp,orjson

class Video:
    def __init__(self, api):
        self.api = api
        
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
            
    async def get_data(self, url, raw=False) -> dict:
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

    def highest_soundquality_download_url(self, data):
        bit_rates = data["bit_rate"]
        bit_rates.sort(key=lambda key: key["bit_rate"], reverse=True)
        return bit_rates[0]["play_addr"]["url_list"][2]