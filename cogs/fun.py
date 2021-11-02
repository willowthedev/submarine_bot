import discord
import random
import requests
import time

from discord.ext import commands
from requests import HTTPError

class Fun(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        start_time = time.time()
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.",
                    "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                    "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                    "My sources say no.", "Outlook is not so good.", "Very doubtful."]
        embed = discord.Embed(color = 0xFFFFFF)
        embed.add_field(name = f"❓ Question:", value = f"{question}", inline = False)
        embed.add_field(name = f"🎱 8ball:", value = f"{random.choice(responses)}", inline = False)
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.") 
        await ctx.send(embed = embed)

    @commands.command(aliases = ['flip'])
    async def toss(self, ctx):
        directory = "./images/toss"

        faces = ["Heads!", "Tails!"]
        toss = random.choice(faces)

        if toss == "Heads!": 
            image = discord.File(f"{directory}/heads.png", filename = "heads.png")
            await ctx.send(f"**{ctx.author}** you flipped **{toss}**", file = image)
        if toss == "Tails!": 
            image = discord.File(f"{directory}/tails.png", filename = "tails.png")
            await ctx.send(f"**{ctx.author}** you flipped **{toss}**", file = image)

def setup(bot): 
    bot.add_cog(Fun(bot))