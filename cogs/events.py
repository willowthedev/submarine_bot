import discord 

from discord.ext import commands

class Events(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): 
        print(f"-----")
        print(f"{self.bot.user} has connected to Discord!")
        print(f"{self.bot.user}'s id is: {self.bot.user.id}")
        print(f"-----")
        await self.bot.change_presence(activity = discord.Game(f".help"))

def setup(bot): 
    bot.add_cog(Events(bot))