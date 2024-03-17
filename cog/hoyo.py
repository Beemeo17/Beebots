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
      "GENSHIN": "https://iili.io/JWOq5kQ.png",
      "STARRAIL": "https://iili.io/JWOq7pV.png",
      "HONKAI": "https://iili.io/JWOqaTB.png",
    }
    icus = await fetch_image(session, imgoc[isd])
    return icus

outputs = {"gane": None, "channel": None}

async def acdaily(image_app, has, claimed_rewards, x, y, i):
  async with aiohttp.ClientSession() as session: 
      dailyt = await fetch_image(session, "https://iili.io/JWOqchP.jpg")
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

class button(discord.ui.View):
  def __init__(self, *, timeout=300):
    super().__init__(timeout=timeout)

  async def Tout(self, I):
    self.daily_callback.disabled = True
    self.daily_callback.placeholder = "❌ Timeout!!"
    self.claim_dailys.disabled = True
    self.auto_claim.disabled = True
    await I.edit_original_response(view=self)

  async def on_select(self, I):
    self.claim_dailys.disabled = False
    self.auto_claim.disabled = False
    self.claim_dailys.style = discord.ButtonStyle.gray
    await I.edit_original_response(view=self)
  
  async def up_button(self, I, sin):
    user_id = str(I.user.id)
    data = load_data()
    if sin:
      self.claim_dailys.disabled = True
      self.claim_dailys.style = discord.ButtonStyle.green
    if "daily_auto" in data[user_id]:
      if data[user_id]["daily_auto"]:
       self.auto_claim.label = "Disabled"
       self.auto_claim.style=discord.ButtonStyle.red
      else:
        self.auto_claim.label = "Enabled"
        self.auto_claim.style=discord.ButtonStyle.green
    await I.edit_original_response(view=self)
  
  @discord.ui.button(label="Claim Daily Reward", style=discord.ButtonStyle.gray, disabled=True)
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
            button.disabled = True
            button.style = discord.ButtonStyle.green
            await Interaction.edit_original_response(view=self)
        except genshin.AlreadyClaimed:
            assert signed_in
            return await Interaction.response.edit_message(content="Đã nhận thưởng trước đó")
        except Exception as s:
            await Interaction.response.edit_message(content=s)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng </login:1198488196087025755> để tiếp tục")
  
  @discord.ui.button(label="Auto_claim", style=discord.ButtonStyle.gray, disabled=True)
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
      if data[user_id]["daily_auto"]:
       self.auto_claim.label = "Disabled"
       self.auto_claim.style=discord.ButtonStyle.red
      else:
        self.auto_claim.label = "Enabled"
        self.auto_claim.style=discord.ButtonStyle.green
      await Interaction.edit_original_response(view=self)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng </login:1198488196087025755> để tiếp tục")

  options = [
            discord.SelectOption(label="GENSHIN", emoji="<:genshin:1091034774203813908>"),
            discord.SelectOption(label="STARRAIL", emoji="<:Honkaistarrail:1099536405492924416>"),
            discord.SelectOption(label="HONKAI", emoji="<:HonkaiImpact3:1100277662523604992>")
        ]
  @discord.ui.select(placeholder="All Game", options=options, row=1)
  async def daily_callback(self, Interaction, select: discord.ui.Select,):
    async with aiohttp.ClientSession() as session: 
        user_id = str(Interaction.user.id)
        game_map = {
            "GENSHIN": genshin.types.Game.GENSHIN,
            "STARRAIL": genshin.types.Game.STARRAIL,
            "HONKAI": genshin.types.Game.HONKAI
        }
        game = game_map.get(select.values[0])
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
              
                image_app = Image.open(BytesIO(await main_img(select.values[0]))).resize((1490, 1275))
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
                embed = discord.Embed(title=f"{select.values[0]} | Điểm danh hàng ngày Hoyolab", description="Nhận thưởng hàng ngày. hãy chọn 1 lựa chọn bên dưới để bắt đầu nhận thưởng!", colour=0x00f5a3, timestamp=datetime.datetime.now())
                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/W2pNzBQRgu8KOxYEOkp-Wx5GYDzpGVNzEHySUPAGzN4/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1111140087770664960/533d867015c8f7437cf8ae9c76d98b30.png")
                embed.add_field(name=f"✅ {rews.nickname}", value="", inline=False)
                embed.set_image(url=file_url)
                embed.add_field(name="daily_auto_claim: ✅" if "daily_auto" in data[user_id] and data[user_id]["daily_auto"] else "daily_auto_claim: ❌", value="", inline=False)
                await Interaction.message.edit(embed=embed)
                await self.on_select(Interaction)
                await self.up_button(Interaction, signed_ins)
            else:
                await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sử dụng </login:1198488196087025755> để tiếp tục")

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
      await Interaction.response.send_message(embed=embed, view=button())
      await asyncio.sleep(300)
      await button().Tout(Interaction)
    else:
        await Interaction.response.send_message(content="Bạn chưa đăng kí hãy sửa dụng </login:1198488196087025755> để tiếp tục")

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
        await I.response.send_message("Bạn chưa đăng kí hãy sửa dụng </login:1198488196087025755> để tiếp tục")

async def setup(bot):
  await bot.add_cog(Codes(bot))
