import discord
from discord.ext import commands
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from datetime import datetime, timedelta, time
import aiohttp
import datetime
import asyncio
import json

isput = {"x" :None, "y" :None, "channel" :None}
async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def cre(xp, yp):
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://media.discordapp.net/attachments/1107978903294853140/1209149933635117137/3AF1A67D-FA57-4D1B-AD8E-63B68CF53894.png?ex=65e5dfa1&is=65d36aa1&hm=845659fb12f4d8d3e864d0bfa23d58ff846bc1c6c92b8d9a190c779701b15457&a",
            "https://media.discordapp.net/attachments/1107978903294853140/1209147724398727208/image0.jpg?ex=65e5dd92&is=65d36892&hm=f69226f3f85370ae12af6bd8479aec9cf3a70d7d40d16fc5fb902421e5bb2769&a",
            "https://media.discordapp.net/attachments/1107978903294853140/1209147827662487593/image0.jpg?ex=65e5ddaa&is=65d368aa&hm=ba84af0c3e747128d33725edd250c30a3b961f6b2988c4a770641cfb2a992503&a"
        ]
        images = await asyncio.gather(*[fetch_image(session, url) for url in urls])
        imgapp = Image.open(BytesIO(images[0])).convert("RGBA").resize((100, 100))
        draw = ImageDraw.Draw(imgapp)
        for image, pos in zip(images[1:], [(42, 42), (xp, yp)]):
            nvop = Image.open(BytesIO(image)).convert("RGBA").resize((17, 17))
            imgapp.paste(nvop, pos, mask=nvop)
        buffer = BytesIO()
        imgapp.save(buffer, format='png')
        buffer.seek(0)
        file = discord.File(buffer, filename="output.png")      
        channel = isput.get("channel")
        message = await channel.send(file=file)
        file_url = message.attachments[0]
        embed = discord.Embed()
        embed.set_image(url=file_url)
        return embed
        
class Button(discord.ui.View):
  def __init__ (self, *, timeout=300):
    super().__init__(timeout=timeout) 
    self.x = isput.get("x")
    self.y = isput.get("y")
    self.xg = 62
    self.yg = 82
  @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji="◀️")
  async def bt1(self, I: discord.Interaction, button: discord.ui.button):
   self.x -= 1.25 if self.x == -1.25 else self.x == 5
   self.xg -= 20
   embed = await cre(self.xg, self.yg)
   await I.response.edit_message(content=None, embed=embed)

  @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji="▶️")
  async def bt2(self, I: discord.Interaction, button: discord.ui.button):
   self.x += 1.25 if self.x <= 5 else self.x == 0
   self.xg += 20
   embed = await cre(self.xg, self.yg)
   await I.response.edit_message(content=None, embed=embed)

  @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji="🔽")
  async def bt3(self, I: discord.Interaction, button: discord.ui.button):
   self.y -= 1.25 if self.y >= 0 else self.y == 5
   self.yg += 20
   embed = await cre(self.xg, self.yg)
   await I.response.edit_message(content=None, embed=embed)

  @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji="🔼")
  async def bt4(self, I: discord.Interaction, button: discord.ui.button):
   self.y += 1.25 if self.y <= 5 else self.y == 0
   self.yg -= 20
   embed = await cre(self.xg, self.yg)
   await I.response.edit_message(content=None, embed=embed)


class gem(commands.Cog):
 def __init__ (self, bot):
   self.bot = bot

 @commands.command()
 async def te(self, ctx):
  x = 2.5
  y = 2.5
  channel = self.bot.get_channel(1118977913392476210)
  isput["x"] = x
  isput["y"] = y
  isput["channel"] = channel
  embed = await cre(62, 82)
  await ctx.send(embed=embed, view=Button())

async def setup(bot):
  await bot.add_cog(gem(bot))
    
  
