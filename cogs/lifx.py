import discord
import requests 
import time 

from discord.ext import commands
from requests.exceptions import HTTPError
from ids import DESK_LAMP
from tokens import LIFX_TOKEN

class LIFX(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.group()
    async def lifx(self, ctx): 
        pass

    @lifx.group()
    async def lamp(self, ctx): 
        pass

    @lamp.command()
    async def off(self, ctx): 
        try: 
            token = LIFX_TOKEN

            headers = {
                "Authorization": "Bearer %s" % token,
            }

            payload = {
                "power": "off",
            }

            response = requests.put(f'https://api.lifx.com/v1/lights/{DESK_LAMP}/state', data=payload, headers=headers)      
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

    @lamp.command()
    async def on(self, ctx): 
        try: 
            token = LIFX_TOKEN

            headers = {
                "Authorization": "Bearer %s" % token,
            }

            payload = {
                "power": "on",
            }

            response = requests.put(f'https://api.lifx.com/v1/lights/{DESK_LAMP}/state', data=payload, headers=headers)      
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

    @lamp.command()
    async def brightness(self, ctx, arg: float): 
        try: 
            token = LIFX_TOKEN

            headers = {
                "Authorization": "Bearer %s" % token,
            }

            payload = {
                "brightness": arg,
            }

            response = requests.put(f'https://api.lifx.com/v1/lights/{DESK_LAMP}/state', data=payload, headers=headers)      
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

    @lamp.command()
    async def color(self, ctx, arg: str): 
        try: 
            token = LIFX_TOKEN

            headers = {
                "Authorization": "Bearer %s" % token,
            }

            payload = {
                "color": arg,
            }

            response = requests.put(f'https://api.lifx.com/v1/lights/{DESK_LAMP}/state', data=payload, headers=headers)      
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

    @lamp.command()
    async def kelvin(self, ctx, arg: int): 
        try: 
            token = LIFX_TOKEN

            headers = {
                "Authorization": "Bearer %s" % token,
            }

            payload = {
                "kelvin": arg,
            }

            response = requests.post(f'https://api.lifx.com/v1/lights/{DESK_LAMP}/state/delta', data=payload, headers=headers)      
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return
    
    
def setup(bot): 
    bot.add_cog(LIFX(bot))