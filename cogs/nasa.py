import discord
import requests 
import time 

from discord.ext import commands
from requests.exceptions import HTTPError
from tokens import NASA_TOKEN

class NASA(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    async def apod(self, ctx): 
        start_time = time.time()
        
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_TOKEN}"

        try: 
            response = requests.get(url).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

        try: 
            embed=discord.Embed(title=response['title'], description=response['explanation'], color=0xFFFFFF)
            
            if response['media_type'] == 'video':
                embed.url = response['url']
            else:
                embed.set_image(url=response['url'])
                
            try: 
                embed.set_author(name=response['copyright'])
            except KeyError as e: 
                pass
            
            embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: NASA's Astronomy Picture of the Day.")
            await ctx.send(embed=embed)
        except Exception as e: 
            await ctx.send(e)

def setup(bot): 
    bot.add_cog(NASA(bot))