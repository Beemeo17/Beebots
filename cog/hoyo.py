import discord
from discord import app_commands
from discord.ext import commands
import genshin
import os
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import aiohttp
import datetime
import asyncio
import calendar
import pytz

VN_TIMEZONE = pytz.timezone('Asia/Shanghai')

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

async def main_img(isd):
  async with aiohttp.ClientSession() as session: 
    imgoc = {
      "GENSHIN": "https://media.discordapp.net/attachments/1107978903294853140/1212074878984003634/Khong_Co_Tieu_e166.png?ex=6602f8b2&is=65f083b2&hm=96f904d237652e2de852a90e0f8043d8397b4b39298b3a560ede25c9ed0eb771&a",
      "STARRAIL": "https://media.discordapp.net/attachments/1107978903294853140/1212073816906534954/Khong_Co_Tieu_e166.png?ex=65f082b5&is=65de0db5&hm=cfcadc40e113843b842b12518ee0310d74e119938317a343708ee246bd39d0d3&a",
      "HONKAI": "https://media.discordapp.net/attachments/1107978903294853140/1212074966955204698/Khong_Co_Tieu_e166.png?ex=65f083c7&is=65de0ec7&hm=cc1c4f3867745fe6e3a0544313c59171ca669ccc5298913501ac86b9f346010b&a",
    }
    icus = await fetch_image(session, imgoc[isd])
    return icus

outputs = {"gane": None, "channel": None}

async def upjs(self, Interaction, bu) -> None:
  if bu == 0:
    self.children[bu].disabled = True
    self.children[bu].style=discord.ButtonStyle.green
  else:
    user_id = str(Interaction.user.id)
    data = load_data()
    if data[user_id]["daily_auto"]:
     self.auto_claim.label = "Disabled"
     self.auto_claim.style=discord.ButtonStyle.red
    else:
      self.auto_claim.label = "Enabled"
      self.auto_claim.style=discord.ButtonStyle.green
  await Interaction.edit_original_response(view=self.Button())

class button(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Select())
  @discord.ui.button(label="Claim Daily Reward", style=discord.ButtonStyle.gray)
  async def claim_dailys(self, Interaction, button: discord.ui.Button,):
    user_id = str(Interaction.user.id)
    data = load_data()
    if user_id in data:
      if "cookies" in data[user_id]:
        cookie = data[user_id]["cookies"]
        cookies = await genshin.complete_cookies(cookie)
        client = genshin.Client(cookies)
        games = outputs.get("gane")
        signed_in, claimed_rewards = await client.get_reward_info(game=games)
        rewards = await client.get_monthly_rewards(game=games)
        embed=discord.Embed()
        try:
            embed=discord.Embed()
            await client.claim_daily_reward(game=games)
            embed.add_field(name=f"{rewards[claimed_rewards].name} | Số lượng:{rewards[claimed_rewards].amount}", value=f"Đã nhận Day: {claimed_rewards}", inline=False)
            embed.set_thumbnail(url=rewards[claimed_rewards].icon)
            await Interaction.response.edit_message(content="", embed=embed)
            await upjs(self, Interaction, 0)
        except genshin.AlreadyClaimed:
            assert signed_in
            return await Interaction.response.edit_message(content="Đã nhận thưởng trước đó")
        except Exception as s:
            await Interaction.response.edit_message(content=s)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")
  
  @discord.ui.button(label="Auto_claim", style=discord.ButtonStyle.gray)
  async def auto_claim(self, Interaction, button: discord.ui.Button,):
    user_id = str(Interaction.user.id)
    data = load_data()
    if user_id in data:
      if "daily_auto" in data[user_id]:
       data[user_id]["daily_auto"] = False if data[user_id]["daily_auto"] else True
      else:
        data[user_id]["daily_auto"] = True
      save_data(data)
      await Interaction.response.edit_message(content="")
      await upjs(self, Interaction, 1)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")

class button2(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Select())
  @discord.ui.button(label="Claim Daily Reward", style=discord.ButtonStyle.green, disabled=True)
  async def claim_dailys1(self, Interaction, button: discord.ui.Button,):
    pass
    
  @discord.ui.button(label="Auto_claim", style=discord.ButtonStyle.gray)
  async def auto_claim1(self, Interaction, button: discord.ui.Button,):
    user_id = str(Interaction.user.id)
    data = load_data()
    if user_id in data:
      if "daily_auto" in data[user_id]:
       data[user_id]["daily_auto"] = False if data[user_id]["daily_auto"] else True
      else:
        data[user_id]["daily_auto"] = True
      save_data(data)
      await Interaction.response.edit_message(content="")
      await upjs(self, Interaction, 1)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")


async def acdaily(image_app, has, claimed_rewards, x, y, i):
  async with aiohttp.ClientSession() as session: 
      dailyt = await fetch_image(session, "https://media.discordapp.net/attachments/1107978903294853140/1212078877799874580/4C10BA33-37C5-4EA6-A901-1712C841D5C8.png?ex=6602fc6b&is=65f0876b&hm=3cbbe99385fa1fb267759f41f5c9525ca9bd78ab9633886d28cd347a9654bf53&a")
      daily_app = Image.open(BytesIO(dailyt)).resize((114, 151))
      dailyl = Image.open(BytesIO(await fetch_image(session, has.icon))).convert("RGBA").resize((102, 102))
      daily_app.paste(dailyl, (6, 10), mask=dailyl)
      if claimed_rewards > i:
        daily_app = ImageEnhance.Brightness(daily_app).enhance(0.8)
        dailys = await fetch_image(session, "https://cdn.discordapp.com/emojis/1212093003943116920.png")
        dailyo = Image.open(BytesIO(dailys)).convert("RGBA").resize((102, 102))
        daily_app.paste(dailyo, (6, 10), mask=dailyo)
      draw_daily = ImageDraw.Draw(daily_app)
      draw_daily.text((25, 122), f"Day {i+1}", font=ImageFont.truetype("zh-cn.ttf", 18), fill=(0, 0, 0))
      draw_daily.text((1, 94), f"x{has.amount}", font=ImageFont.truetype("zh-cn.ttf", 21), fill=(155, 49, 30))
      image_app.paste(daily_app, (x, y))

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="GENSHIN", emoji="<:genshin:1091034774203813908>"),
            discord.SelectOption(label="STARRAIL", emoji="<:Honkaistarrail:1099536405492924416>"),
            discord.SelectOption(label="HONKAI", emoji="<:HonkaiImpact3:1100277662523604992>")
        ]
        super().__init__(placeholder="Các Cộng Cụ", options=options)
    
    async def callback(self, Interaction: discord.Interaction,):
      async with aiohttp.ClientSession() as session: 
        user_id = str(Interaction.user.id)
        game_map = {
            "GENSHIN": genshin.types.Game.GENSHIN,
            "STARRAIL": genshin.types.Game.STARRAIL,
            "HONKAI": genshin.types.Game.HONKAI
        }
        game = game_map.get(self.values[0])
        if game:
            outputs["gane"] = game
            data = load_data()
            if user_id in data and "cookies" in data[user_id]:
                embed_loading = discord.Embed(title="<a:aloading:1152869299942338591> **Đang tạo thông tin..__Hãy kiên nhẫn__** <a:ganyurollst:1118761352064946258>", color=discord.Color.yellow())
                await Interaction.response.edit_message(content=None, embed=embed_loading)
                cookie = data[user_id]["cookies"]
                cookies = await genshin.complete_cookies(cookie)
                client = genshin.Client(cookies)
                rews = await client.get_hoyolab_user()
                signed_ins, claimed_rewards = await client.get_reward_info(game=game)

                rewards = await client.get_monthly_rewards(game=game)
                now = datetime.datetime.now(VN_TIMEZONE)
                assert len(rewards) == calendar.monthrange(now.year, now.month)[1]
              
                image_app = Image.open(BytesIO(await main_img(self.values[0]))).resize((1490, 1275))
                draw = ImageDraw.Draw(image_app)
                draw.text((383, 342), f"{claimed_rewards}", font=ImageFont.truetype("zh-cn.ttf", 37), fill=(155, 49, 30))
                draw.text((1200, 218), f"Tháng {now.month}", font=ImageFont.truetype("zh-cn.ttf", 32), fill=(255, 255, 255))
                i = 0
                x, y = 104, 468
                task = []
                for has in rewards:
                  task.append(acdaily(image_app, has, claimed_rewards, x, y, i))
                  i += 1
                  x += 129
                  if i % 10 == 0:
                    y += 165
                    x = 104
                await asyncio.gather(*task)
                buffer = BytesIO()
                image_app.save(buffer, format='png')
                buffer.seek(0)
                file = discord.File(buffer, filename="showcase.png")
                channel = outputs.get("channel")
                messaget = await channel.send(file=file)
                file_url = messaget.attachments[0]
                embed = discord.Embed(title=f"{self.values[0]} | Điểm danh hàng ngày Hoyolab", description="Nhận thưởng hàng ngày. hãy chọn 1 lựa chọn bên dưới để bắt đầu nhận thưởng!", colour=0x00f5a3, timestamp=datetime.datetime.now())
                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/W2pNzBQRgu8KOxYEOkp-Wx5GYDzpGVNzEHySUPAGzN4/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1111140087770664960/533d867015c8f7437cf8ae9c76d98b30.png")
                embed.add_field(name=f"✅ {rews.nickname}", value="", inline=False)
                embed.set_image(url=file_url)
                embed.add_field(name="daily_auto_claim: ✅" if "daily_auto" in data[user_id] and data[user_id]["daily_auto"] else "daily_auto_claim: ❌", value="", inline=False)
                
                if signed_ins:
                  await Interaction.message.edit(embed=embed, view=button2())
                else:
                  await Interaction.message.edit(embed=embed, view=button())
            else:
                await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sử dụng ``/login`` để tiếp tục")

class SelectView(discord.ui.View):
  def __init__ (self, timeout=300):
    super().__init__(timeout=timeout)
    self.add_item(Select())
  async def on_timeout(self, I: discord.Interaction):
    await I.message.delete()


class Codes(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @app_commands.command(name="daily", description="Nhận thưởng điểm danh hàng ngày")
  async def code(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()
    if user_id in data:
      channel = self.bot.get_channel(1118977913392476210)
      outputs["channel"] = channel
      embed = discord.Embed(title=f"{self.bot.user.name} | Điểm danh hàng ngày Hoyolab", description="Nhận thưởng hàng ngày. hãy chọn 1 lựa chọn bên dưới để bắt đầu nhận thưởng!", colour=0x00f5a3, timestamp=datetime.datetime.now())
      embed.set_thumbnail(url=self.bot.user.avatar)
      await Interaction.response.send_message(embed=embed, view=SelectView())
    else:
        await Interaction.response.send_message(content="Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")

  @app_commands.command(name="redeem", description="redeem code")
  @app_commands.describe(games="Chọn nơi nhập code") 
  @app_commands.choices(games=[
    discord.app_commands.Choice(name="GENSHIN", value=genshin.types.Game.GENSHIN),
    discord.app_commands.Choice(name="STARRAIL", value=genshin.types.Game.STARRAIL),
  ])
  async def redeems(self, I: discord.Interaction, code: str, games: discord.app_commands.Choice[str], user: discord.Member = None):
    user_id = str(I.user.id) if user is None else str(user.id)
    data = load_data()
    if user_id in data:
      if "cookies" in data[user_id]:
        cookie = data[user_id]["cookies"]
        cookies = await genshin.complete_cookies(cookie)
        client = genshin.Client(cookies)
        try:
            await client.redeem_code(code, game=games.value)
            await I.response.send_message(f"giftcode nhập thành công [{games.name}] ```{code}```")  
        except genshin.RedemptionException as e:
            await I.response.send_message(f"**{games.name}**```{e}```\ngiftcode không tồn tại hoặc đã được sửa dụng")
        except genshin.AccountNotFound:
            await I.response.send_message("Không có tài khoản.")
      else:
        await I.response.send_message("Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")

async def setup(bot):
  await bot.add_cog(Codes(bot))
