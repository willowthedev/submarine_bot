import discord 
import requests
import time

from discord.ext import commands
from requests.exceptions import HTTPError
from tokens import RAPIDAPI_TOKEN

class Words(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command()
    async def define(self, ctx, arg: str): 
        start_time = time.time()
        
        try: 
            url = f"https://wordsapiv1.p.rapidapi.com/words/{arg}"

            headers = {
                'x-rapidapi-key': RAPIDAPI_TOKEN,
                'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
            }

            response = requests.get(url, headers = headers).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

        embed = discord.Embed(description = f"{arg} ({response['pronunciation']['all']})", color = 0xFFFFFF)
        for count, _ in enumerate(response['results']):
            try: 
                example = response['results'][count]['examples'][0]
            except Exception as e: 
                example = "no example available for this definition"

            embed.add_field(name = f"Result {count+1}:", value = f"**Part of Speech:**\n{response['results'][count]['partOfSpeech']}\n**Definition:**\n{response['results'][count]['definition']}\n**Examples:**\n{example}\n----------", inline = False)

        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: WordsAPI.")
        await ctx.send(embed = embed)

    @commands.command()
    async def antonyms(self, ctx, arg: str): 
        start_time = time.time()
        
        try: 
            url = f"https://wordsapiv1.p.rapidapi.com/words/{arg}/antonyms"

            headers = {
                'x-rapidapi-key': "79281f7e6emsh0379b149ee9c6afp11e4edjsn997da8071571",
                'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
            }

            response = requests.get(url, headers = headers).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception: 
            await ctx.send(f"Error Occurred: {Exception}")
            return

        antonyms = ""
        for count, _ in enumerate(response['antonyms']):
            antonyms += "-" + response['antonyms'][count] + "\n"
        
        embed = discord.Embed(color = 0xFFFFFF)

        if len(antonyms) == 0: 
            embed.add_field(name = f"Antonyms for '{arg}':", value = f"no antonyms available for '{arg}'")
        else:
            embed.add_field(name = f"Antonyms for '{arg}':", value = antonyms) 
        
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: WordsAPI.")
        await ctx.send(embed = embed)

    @commands.command()
    async def synonyms(self, ctx, arg: str): 
        start_time = time.time()
        
        try: 
            url = f"https://wordsapiv1.p.rapidapi.com/words/{arg}/synonyms"

            headers = {
                'x-rapidapi-key': RAPIDAPI_TOKEN,
                'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
            }

            response = requests.get(url, headers = headers).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception: 
            await ctx.send(f"Error Occurred: {Exception}")
            return

        synonyms = ""
        for count, _ in enumerate(response['synonyms']):
            synonyms += "-" + response['synonyms'][count] + "\n"
        
        embed = discord.Embed(color = 0xFFFFFF)
        
        if len(synonyms) == 0: 
            embed.add_field(name = f"Synonyms for '{arg}':", value = f"no synonyms available for '{arg}'")
        else:
            embed.add_field(name = f"Synonyms for '{arg}':", value = synonyms) 
        
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: WordsAPI.")
        await ctx.send(embed = embed)

def setup(bot): 
    bot.add_cog(Words(bot))