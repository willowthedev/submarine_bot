import asyncio
import discord
import random
import requests
import os 
import time 

from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from requests.exceptions import HTTPError

class Open_Vision(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot

    def validate_image(self, image):
        try:
            with Image.open(image) as img:
                return f"image/{img.format.lower()}"
        except Exception as e:
            print(f"Error: {e.args[0]}")

    def get_prediction_mask(self, image, bounding_boxe, score, label, color, text_offset=10, opacity=96):
        x1, y1, x2, y2 = bounding_boxe

        mask = Image.new("RGBA", image.size, color + (0,))
        draw = ImageDraw.Draw(mask)

        font = ImageFont.truetype("fonts/Montserrat-Regular.ttf", 20)
        text_x, text_y = font.getsize(label)
        draw.rectangle(((x1, y1), (x1 + text_x, y1 - text_y)), fill=color + (opacity,))
        draw.text((x1, y1 - text_y), text=label, fill="white", font=font)

        draw.rectangle(((x1, y1), (x2, y2)), fill=color + (opacity,))

        return mask

    def apply_masks(self, image, masks):
        for mask in masks:
            image = Image.alpha_composite(image, mask)
        image = image.convert("RGB")
        return image

    def visualize_image_predictions(self, image, predictions):
        img = Image.open(image)
        img = img.convert("RGBA")

        labels = set([prediction["label"] for prediction in predictions])
        colors = {
            label: (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
            for label in labels
        }

        masks = []

        for prediction in predictions:
            bounding_boxe = (
                prediction["bbox"]["x1"],
                prediction["bbox"]["y1"],
                prediction["bbox"]["x2"],
                prediction["bbox"]["y2"],
            )
            score = prediction["score"]
            label = prediction["label"]
            color = colors[label]

            mask = self.get_prediction_mask(
                image=img, bounding_boxe=bounding_boxe, score=score, label=label, color=color
            )
            masks.append(mask)

        img = self.apply_masks(img, masks)

        return img
  
    @commands.command()
    async def what_is(self, ctx): 
        start_time = time.time()
        
        async with ctx.typing():
            try: 
                attachment = ctx.message.attachments[0]
                url = attachment.url
                name = attachment.filename

                response = requests.get(url)
                with open(f"./images/open-vision/{name}", "wb") as image: 
                    image.write(response.content)
            except HTTPError as e: 
                await ctx.send(f"HTTP Error Occurred: {e}")
                return
            except Exception as e: 
                await ctx.send(f"Error Occurred: {e}")
                return
            
            try: 
                image = f"./images/open-vision/{name}"
                mimetype = self.validate_image(image)
                files = {"image": (image, open(image, "rb"), mimetype)}
                body = {"model": "yolov4"}

                url = 'https://api.openvisionapi.com/api/v1/detection'
                response = requests.post(url, files=files, data=body)
            except HTTPError as e: 
                await ctx.send(f"HTTP Error Occurred: {e}")
                return
            except Exception as e: 
                await ctx.send(f"Error Occurred: {e}")
                return
            
            embed = discord.Embed(color = 0xFFFFFF)
            
            try:            
                predictions = response.json()["predictions"]
                
                if len(predictions) == 0: 
                    embed.description = f"I found objects, but I have no idea what they are!"
                else: 
                    image = self.visualize_image_predictions(image, predictions)
                    image.save(f"./images/open-vision/{name}")
                
                score = response.json()['predictions'][0]['score']
                label = response.json()['predictions'][0]['label']

                embed.description = f"I am {float(score) * 100}% sure that the highlighted object is a {label}."
            except IndexError as e: 
                pass
            except KeyError as e: 
                embed.description = f"Sorry, I didn't detect any objects!"
            except Exception as e: 
                await ctx.send(e)
            
            embed.set_image(url = f"attachment://{name}")
            embed.set_footer(text = f"Completed in {time.time()-start_time} seconds.\nPowered by: Open Vision API.")
            file = discord.File(f"./images/open-vision/{name}", filename = name)
            await ctx.send(file = file, embed = embed)

            os.remove(f"./images/open-vision/{name}")
    
def setup(bot): 
    bot.add_cog(Open_Vision(bot))