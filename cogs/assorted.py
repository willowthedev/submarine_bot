import discord
import requests
import time

from discord.ext import commands
from requests.exceptions import HTTPError

class Assorted(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(aliases = ['advise'])
    async def advice(self, ctx): 
        start_time = time.time()

        try: 
            response = requests.get("https://api.adviceslip.com/advice").json()
        except HTTPError as e: 
            await ctx.send(e)
            return
        except Exception as e:
            await ctx.send(e)
            return

        embed = discord.Embed(description = response['slip']['advice'], color = 0xFFFFFF)
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: Advice Slip JSON API")
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ['affirm'])
    async def affirmation(self, ctx): 
        start_time = time.time()

        try: 
            response = requests.get("https://www.affirmations.dev/").json()
        except HTTPError as e: 
            await ctx.send(e)
            return
        except Exception as e:
            await ctx.send(e)
            return

        embed = discord.Embed(description = response['affirmation'] + ".", color = 0xFFFFFF)
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: affirmations.dev")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['nyaa', 'meow'])
    async def cat(self, ctx): 
        start_time = time.time()

        try: 
            response = requests.get("https://aws.random.cat/meow").json()
        except HTTPError as e: 
            await ctx.send(e)
            return
        except Exception as e:
            await ctx.send(e)
            return
        
        embed = discord.Embed(color = 0xFFFFFF)
        embed.set_image(url = response['file'])
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: random.cat")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['woof'])
    async def dog(self, ctx): 
        start_time = time.time()
        
        try: 
            response = requests.get("https://dog.ceo/api/breeds/image/random").json()
        except HTTPError as e: 
            await ctx.send(e)
            return
        except Exception as e:
            await ctx.send(e)
            return
        
        embed = discord.Embed(color = 0xFFFFFF)
        embed.set_image(url = response['message'])
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: DogAPI")
        await ctx.send(embed = embed)

def setup(bot): 
    bot.add_cog(Assorted(bot))       