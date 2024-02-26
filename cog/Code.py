import discord
from discord import app_commands
from discord.ext import commands
import genshin
import requests
import os
from datetime import datetime, time
import json

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

outputs = {"gane": None}
class button1(discord.ui.View):
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
        try:
            await client.claim_daily_reward(game=games)
            await Interaction.response.edit_message(content="Nhận thưởng thành công")
        except genshin.AlreadyClaimed:
            assert signed_in
            return await Interaction.response.edit_message(content="Đã nhận thưởng trước đó")
        except Exception as s:
            await Interaction.response.edit_message(content=s)
    else:
        await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")
    
  @discord.ui.button(label="On", style=discord.ButtonStyle.gray, disabled=True)
  async def auto_claim(self, Interaction, button: discord.ui.Button,):
    print(1)

class button2(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Select())
  @discord.ui.button(label="Claim Daily Reward", style=discord.ButtonStyle.green, disabled=True)
  async def claim_dailys1(self, Interaction, button: discord.ui.Button,):
    print(2)

  @discord.ui.button(label="On", style=discord.ButtonStyle.gray, disabled=True)
  async def auto_claim1(self, Interaction, button: discord.ui.Button,):
    print(1)

class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="GENSHIN", emoji="<:genshin:1091034774203813908>"),
            discord.SelectOption(label="STARRAIL", emoji="<:Honkaistarrail:1099536405492924416>"),
            discord.SelectOption(label="HONKAI", emoji="<:HonkaiImpact3:1100277662523604992>")
        ]
        super().__init__(placeholder="Các Cộng Cụ", options=options)
    
    async def callback(self, Interaction: discord.Interaction):
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
                cookie = data[user_id]["cookies"]
                cookies = await genshin.complete_cookies(cookie)
                client = genshin.Client(cookies)
                embed = discord.Embed(title=f"BeeBot | Điểm danh hàng ngày Hoyolab(daily)", description="Nhận thưởng hàng ngày. hãy chọn 1 lựa chọn bên dưới để bắt đầu nhận thưởng!", colour=0x00f5a3, timestamp=datetime.now())
                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/W2pNzBQRgu8KOxYEOkp-Wx5GYDzpGVNzEHySUPAGzN4/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1111140087770664960/533d867015c8f7437cf8ae9c76d98b30.png")
                signed_ins, claimed_rewards = await client.get_reward_info(game=game)
                embed.add_field(name="daily_auto_claim: ❌", value="", inline=False)
                if signed_ins:
                    await Interaction.response.edit_message(embed=embed, view=button2())
                else:
                    await Interaction.response.edit_message(embed=embed, view=button1())
            else:
                await Interaction.response.edit_message(content="Bạn chưa đăng kí hãy sử dụng ``/login`` để tiếp tục")

    
class SelectView(discord.ui.View):
  def __init__ (self, timeout=300):
    super().__init__(timeout=timeout)
    self.add_item(Select())

class Codes(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @app_commands.command(name="daily", description="Nhận thưởng điểm danh hàng ngày")
  async def code(self, Interaction):
    embed = discord.Embed(title=f"{self.bot.user.name} | Điểm danh hàng ngày Hoyolab(daily)", description="Nhận thưởng hàng ngày. hãy chọn 1 lựa chọn bên dưới để bắt đầu nhận thưởng!", colour=0x00f5a3, timestamp=datetime.now())
    embed.set_thumbnail(url=self.bot.user.avatar)
    await Interaction.response.send_message(embed=embed, view=SelectView())

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
