import discord
import requests 
import time

from datetime import datetime
from discord.ext import commands
from requests.exceptions import HTTPError
from tokens import OPENWEATHER_TOKEN

class Weather(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot
    
    @commands.command(brief = "Current Weather!")
    async def weather(self, ctx, *args):
        start_time = time.time()

        arg = ','.join(args)
        location = f"http://api.openweathermap.org/geo/1.0/direct?q={arg}&limit=1&appid={OPENWEATHER_TOKEN}"

        try: 
            location = requests.get(location).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception: 
            await ctx.send(f"Error Occurred: {Exception}")
            return

        try:
            latitude = location[0]['lat']
            longitude = location[0]['lon']
        except IndexError: 
            await ctx.send(f"No location found for {args}!")
            return

        weather = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={OPENWEATHER_TOKEN}"
        print(weather)

        try: 
            weather = requests.get(weather).json()
        except HTTPError as e: 
            await ctx.send(f"HTTP Error Occurred: {e}")
            return
        except Exception as e: 
            await ctx.send(f"Error Occurred: {e}")
            return

        current_temp = weather['current']['temp']
        current_temp_c = round(current_temp - 273.15, 2)
        current_temp_f = round((current_temp - 273.15) * (9/5) + 32, 2)

        feels_like = weather['current']['feels_like']
        feels_like_c = round(feels_like - 273.15, 2)
        feels_like_f = round((feels_like - 273.15) * (9/5) + 32, 2)

        humidity = weather['current']['humidity']
        wind_speed = weather['current']['wind_speed']
        visibility = weather['current']['visibility']

        sunrise = weather['daily'][0]['sunrise']
        sunrise = datetime.utcfromtimestamp(sunrise).strftime('%H:%M')

        sunset = weather['daily'][0]['sunset']
        sunset = datetime.utcfromtimestamp(sunset).strftime('%H:%M')

        thumbnail_url = f"http://openweathermap.org/img/wn/{weather['current']['weather'][0]['icon']}.png"

        embed = discord.Embed(description = f"Current Weather for {location[0]['name']}, {location[0]['country']}", color = 0xFFFFFF)
        embed.add_field(name = "Conidition:", value = weather['current']['weather'][0]['description'], inline = True)
        embed.add_field(name = "Temperature:", value = f"{current_temp_c}°C / {current_temp_f}°F", inline = True)
        embed.add_field(name = "Feels Like:", value = f"{feels_like_c}°C / {feels_like_f}°F", inline = True)
        embed.add_field(name = "Humidity:", value = f"{humidity}%", inline = True)
        embed.add_field(name = "Wind Speed:", value = f"{wind_speed}m/s", inline = True)
        embed.add_field(name = "Visibility:", value = f"{visibility}m", inline = True)
        embed.add_field(name = "Sunrise:", value = f"{sunrise} UTC", inline = True)
        embed.add_field(name = "Sunset:", value = f"{sunset} UTC", inline = True)
        embed.set_thumbnail(url = thumbnail_url)
        embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: OpenWeatherMap.")
        await ctx.send(embed = embed)

        try:
            for count, _ in enumerate(weather['alerts']):
                await ctx.send(f"**{weather['alerts'][count]['sender_name']}**:\n{weather['alerts'][count]['description']}\n")
        except Exception as e: 
            pass

def setup(bot): 
    bot.add_cog(Weather(bot))