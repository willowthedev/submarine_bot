import discord
import requests 
import time 

from discord.ext import commands
from requests.exceptions import HTTPError
from tokens import DEEPL_TOKEN

class Translate(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, target_lang :str, *args): 
        start_time = time.time()

        try: 
            parameters = {
                "text": ' '.join(args), 
                "target_lang": target_lang, 
                "auth_key": DEEPL_TOKEN                
            }

            response = requests.get("https://api-free.deepl.com/v2/translate", params = parameters).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception: 
            await ctx.send(f"Error Occurred: {Exception}")
            return
        
        embed = discord.Embed(color = 0xFFFFFF)
        embed.add_field(name = f"{response['translations'][0]['detected_source_language']} -> {target_lang}: {' '.join(args)}", value =f"{response['translations'][0]['text']}")
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: DeepL Translator.")
        await ctx.send(embed = embed)

    @commands.command()
    async def translate_languages(self, ctx): 
        embed = discord.Embed(color = 0xFFFFFF)
        embed.set_footer(text = "BG - Bulgarian\nCS - Czech\nDA - Danish\nDE - German\nEL - Greek\nEN-GB - English (British)\nEN-US - English (American)\nES - Spanish\nET - Estonian\nFI - Finnish\nFR - French\nHU - Hungarian\nIT - Italian\nJA - Japanese\nLT - Lithuanian\nLV - Latvian\nNL - Dutch\nPL - Polish\nPT-PT - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)\nPT-BR - Portuguese (Brazilian)\nRO - Romanain\nRU - Russian\nSK - Slovak\nSL - Slovenian\nSV - Swedish\nZH - Chinese")
        await ctx.send(embed = embed)

def setup(bot): 
    bot.add_cog(Translate(bot))