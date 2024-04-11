import discord
from discord.ext import commands
from discord import app_commands
import json
import genshin
import asyncio
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import aiohttp
import operator

files = "test.json"
def load_data():
  try:
      with open(files, 'r') as file:
          data = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
      data = {}
  return data

def save_data(data):
  with open(files, 'w') as file:
      json.dump(data, file, indent=4)

async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def download_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def char_nt(nts):
    async with aiohttp.ClientSession() as session: 
        nt = {
            "Anemo": "https://cdn.discordapp.com/emojis/1104082571635204218.webp",
            "Geo": "https://cdn.discordapp.com/emojis/1104082872958197760.webp",
            "Electro": "https://cdn.discordapp.com/emojis/1104082811578761327.webp",
            "Dendro": "https://cdn.discordapp.com/emojis/1104082739759677602.webp",
            "Hydro": "https://cdn.discordapp.com/emojis/1104082936065691678.webp",
            "Pyro": "https://cdn.discordapp.com/emojis/1104082999802351707.webp",
            "Cryo": "https://cdn.discordapp.com/emojis/1104082671631601725.webp",
            "5★": "https://cdn.discordapp.com/emojis/1118426449238568980.webp",
            "4★": "https://cdn.discordapp.com/emojis/1118426412731342920.webp"
        }
        ints = await fetch_image(session, nt[nts])
        return ints

async def char_rate(rate):
    async with aiohttp.ClientSession() as session:
        if rate == 5:
            ratety = "https://cdn.discordapp.com/attachments/1107978903294853140/1227303277092278424/Day_12_2.png?ex=6627ea3f&is=6615753f&hm=3210e9f2d610a0eee1f7630886fb6f51a1e66f484e7358d6f511e9ebd4519287&"
        if rate == 4:
            ratety = "https://media.discordapp.net/attachments/1107978903294853140/1227303276865650789/Day_12_1.png?ex=6627ea3f&is=6615753f&hm=f23a88a92f1244307525f82345ea6975e1ab544b0514b118fafdeba33be44f81&=&format=webp&quality=lossless&width=102&height=135"
        return ratety

async def sk_chars(sk_char_goc, sk_char_draw, char, xs, ys, t, char_goc):
    async with aiohttp.ClientSession() as session: 
        try:
            sk_char_icon = Image.open(BytesIO(await fetch_image(session, char.icon))).convert("RGBA").resize((102, 102))
            sk_char_goc.paste(sk_char_icon, (6, 10), mask=sk_char_icon)
        except Exception as s:
            pass
        text = char.name
        text_bbox = sk_char_draw.textbbox((0, 0), text, font=ImageFont.truetype("zh-cn.ttf", 14))

        text_position = ((sk_char_goc.width - text_bbox[2]) // 2, 128)
        sk_char_draw.text(((sk_char_goc.width - text_bbox[2]) // 2, 128), text, font=ImageFont.truetype("zh-cn.ttf", 14), fill=(0, 0, 0))

        x, y = 92, 20
        sk_char_draw.rounded_rectangle([2 - 5, 110 - 5, 2 + 110 + 5, 110 + 4 + 5], 8, fill=(255,255,255))
        sk_char_draw.text((2, 107), f"Lv.{char.level}  C.{char.constellation}  BFF.{char.friendship}", font=ImageFont.truetype("zh-cn.ttf", 12), fill=(0, 0, 0))
        
        sk_char_draw.ellipse([x - 23, y - 23, x + 23, y + 23], fill=(190,190,190))
        sk_char_VKicon = Image.open(BytesIO(await fetch_image(session, char.weapon.icon))).convert("RGBA").resize((35, 35))
        sk_char_goc.paste(sk_char_VKicon, (x-16, y-16), mask=sk_char_VKicon)
        
        sk_char_draw.text((78, 27), f"  {char.weapon.refinement}", font=ImageFont.truetype("zh-cn.ttf", 16), fill=(255, 255, 0))

        sk_char_nt = Image.open(BytesIO(await char_nt(char.element))).convert("RGBA").resize((35, 35))
        sk_char_goc.paste(sk_char_nt, (x-89, y-17), mask=sk_char_nt)
        char_goc.paste(sk_char_goc, (xs, ys))

class all_characters(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @app_commands.command(name="characters", description="Hiển thị tất cả characters sửa hữu")
    async def all_characters(self, Interaction, member: discord.Member = None):
        async with aiohttp.ClientSession() as session: 
            try:
                user_id = str(Interaction.user.id) if member is None else str(member.id)
                data = load_data()
                cookie = data[user_id]["cookies"]
            except Exception as s:
                return await Interaction.response.send_message("Bạn chưa đăng kí hãy sửa dụng </login:1198488196087025755> để tiếp tục")
            embeds = discord.Embed()
            embeds.add_field(name="vui lòng đợi thông tin được sử lý", value="", inline=False)
            await Interaction.response.send_message(embed=embeds, ephemeral=True)
            data = load_data()
            cookie = data[user_id]["cookies"]
            client = genshin.Client(cookie)
            uid = await client._get_uid(game=genshin.types.Game.GENSHIN)
            characters = await client.get_genshin_characters(uid)
            char_index = await client.get_genshin_user(uid)
            player = await client.get_genshin_diary(uid)
            char_goc = Image.new('RGBA', (1340, (160 * ((char_index.stats.characters) // 9) + 260)), color = (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_goc)
            char_draw.rounded_rectangle([45 - 5, 12 - 5, 45 + 1296 + 5, 12 + 64 + 5], 8, fill=(170,170,170))

            texts = f"{player.nickname}      {player.uid}      {player.server}"
            text_boxs = char_draw.textbbox((0, 0), texts, font=ImageFont.truetype("zh-cn.ttf", 36))
            char_draw.text((((45 + 1296) - text_boxs[2]) // 2, 22), texts, font=ImageFont.truetype("zh-cn.ttf", 36), fill=(0, 0, 0))
            
            xs, ys, t= 49, 100, 0
            chars = []
            nts = {}
            for char in characters:
                sk_char_load = await fetch_image(session, await char_rate(char.rarity))
                sk_char_goc = Image.open(BytesIO(sk_char_load)).resize((114, 151))
                sk_char_draw = ImageDraw.Draw(sk_char_goc)
                chars.append(sk_chars(sk_char_goc, sk_char_draw, char, xs, ys, t, char_goc))
                xs += 125
                if (t+1) % 10 == 0:
                    ys += 160
                    xs = 49
                t += 1
                nts[char.element] = nts.get(char.element, 0) + 1
                nts[f"{char.rarity}★"] = nts.get(f"{char.rarity}★", 0) + 1

            sorted_counts = dict(sorted(nts.items(), key=operator.itemgetter(1), reverse=True))
            fields = [(element, count) for element, count in sorted_counts.items()]
            xss, t = 98, 0
            yss = (160 * ((char_index.stats.characters) // 9) + 115)
            for field in fields:
                char_draw.rounded_rectangle([(xss -47) - 5, (yss) - 5, (xss -47) + 190 + 5, (yss) + 40 + 5], 8, fill=(100,100,100))
                char_draw.text((xss, yss), f"{field[1]} {field[0]}", font=ImageFont.truetype("zh-cn.ttf", 30), fill=(255, 255, 255))
                all_char_nt = Image.open(BytesIO(await char_nt(field[0]))).convert("RGBA").resize((35, 35))
                char_goc.paste(all_char_nt, (xss- 45, yss+2), mask=all_char_nt)
                xss += 230
                if (t+1) % 5 ==0:
                    xss = 98
                    yss += 80
                t += 1
            await asyncio.gather(*chars)
            buffer = BytesIO()
            char_goc.save(buffer, format='png')
            buffer.seek(0)

            file = discord.File(buffer, filename="showcase.png")
            channel =self.bot.get_channel(1118977913392476210)
            messaget = await channel.send(file=file)
            file_url = messaget.attachments[0]

            embed = discord.Embed(color=discord.Color.brand_green())
            embed.set_author(name=Interaction.user.name, icon_url=Interaction.user.avatar)
            embed.set_image(url=file_url)
            embed.set_footer(text=f"{uid} - {char_index.stats.characters} Characters", icon_url=self.bot.user.avatar)
            await Interaction.channel.send(embed=embed)
            

async def setup(bot):
    await bot.add_cog(all_characters(bot))
