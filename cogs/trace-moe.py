import discord 
import requests
import urllib.parse
import time

from discord.ext import commands
from requests.exceptions import HTTPError

class Trace_Moe(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    async def what_anime(self, ctx): 
        start_time = time.time()
        
        async with ctx.typing():
            try: 
                attachment = ctx.message.attachments[0]
                attachment_url = attachment.url
                url = f"https://api.trace.moe/search?url={urllib.parse.quote_plus(attachment_url)}"

                trace_moe_response = requests.get(url).json()

            except HTTPError as e: 
                await ctx.send(f"HTTP Error Occurred: {e}")
                return
            except Exception as e: 
                await ctx.send(f"Error Occurred: {e}")
                return

            try: 
                # Here we define our query as a multi-line string
                query = '''
                query ($id: Int) { # Define which variables will be used in the query (id)
                Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                    id
                    title {
                    romaji
                    english
                    native
                    }
                }
                }
                '''

                # Define our query variables and values that will be used in the query request
                variables = {
                    'id': trace_moe_response['result'][0]['anilist']
                }

                url = "https://graphql.anilist.co"

                anilist_response = requests.post(url, json={'query': query, 'variables': variables}).json()
            except HTTPError as e: 
                await ctx.send(f"HTTP Error Occurred: {e}")
                return
            except Exception as e: 
                await ctx.send(f"Error Occurred: {e}")
                return

        confidence = trace_moe_response['result'][0]['similarity']
        enlish = anilist_response['data']['Media']['title']['english']
        romaji = anilist_response['data']['Media']['title']['romaji']
        native = anilist_response['data']['Media']['title']['native']
        episode = trace_moe_response['result'][0]['episode']
        
        embed = discord.Embed(description = f"I am **{round(confidence * 100, 2)}%** sure that this image is from:\n**English:** {enlish}\n**Romaji:** {romaji}\n**Native:** {native}\n**Episode:** {episode}",color = 0xFFFFFF)
        embed.set_image(url=attachment_url)
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: trace.moe and AniList.")
        await ctx.send(embed = embed)
def setup(bot): 
    bot.add_cog(Trace_Moe(bot))