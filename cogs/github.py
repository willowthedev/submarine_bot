import discord 
import requests

from discord.ext import commands

class Github(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot
        
    @commands.group(brief = "All Github related commands.")
    async def github(self, ctx): 
        pass

    @github.command(brief = "Retrieves a response from a random selection of Github's design philosophies.")
    async def zen(self, ctx): 
        request = requests.get("https://api.github.com/zen")

        if request.status_code == 200: 
            zen = str(request.content)
            await ctx.send(zen[2:-1])
        else: 
            await ctx.send("I'm having troubing acessing the Github API, please try again later.")

def setup(bot): 
    bot.add_cog(Github(bot))