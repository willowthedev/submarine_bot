import discord

from discord.ext import commands

class Admin(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def load (self, ctx, extension): 
        try: 
            self.bot.load_extension(f"cogs.{extension}")
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Loaded Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  
        except discord.DiscordException:
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Failed to Load Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unload (self, ctx, extension): 
        try: 
            self.bot.unload_extension(f"cogs.{extension}")
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Unloaded Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  
        except discord.DiscordException:
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Failed to Unload Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def reload (self, ctx, extension): 
        try: 
            self.bot.reload_extension(f"cogs.{extension}")
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Reloaded Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  
        except discord.DiscordException:
            embed = discord.Embed(color = 0xFFFFFF)
            embed.add_field(name = f"Admin", value =f"Failed to Reload Extension: *{extension}.py*", inline = False)
            await ctx.send(embed = embed)  

def setup(bot): 
    bot.add_cog(Admin(bot))