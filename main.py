import os
import discord
 
from discord.ext import commands
from tokens import DISCORD_TOKEN

bot = commands.Bot(command_prefix = ".")

for filename in os.listdir('./cogs'): 
    if filename.endswith('.py'): 
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded: {filename}")

bot.run(DISCORD_TOKEN)