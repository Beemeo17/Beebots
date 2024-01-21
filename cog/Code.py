import discord
from discord import app_commands
from discord.ext import commands
import genshin
import requests
import os
from datetime import datetime, time

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

class Redeem(discord.ui.Modal, title="Redeem code Genshin Impact"):
  code_Gi = discord.ui.TextInput(label="Hãy điền code Genshin vào bên dưới", style=discord.TextStyle.paragraph, required=False)
  code_Hsr = discord.ui.TextInput(label="Hãy điền code Star Rail vào bên dưới", style=discord.TextStyle.paragraph, required=False)
  async def on_submit(self, Interaction):
     
      user_id = str(Interaction.user.id)
      data = load_data()
      if user_id in data:
        cookie = data[user_id]
       
        cookies = await genshin.complete_cookies(cookie)
        client = genshin.Client(cookies)
        if self.code_Gi.value != "":
          try:
              try:
                await Interaction.response.edit_message(content=f"**...**")
              except discord.errors.InteractionResponded:
                pass
            
              await client.redeem_code(self.code_Gi.value, game=genshin.types.Game.GENSHIN)
              embed=discord.Embed(title=f"giftcode nhập thành công [GENSHIN] ```{self.code_Gi.value}```", colour=0x00f576)  
              await Interaction.message.edit(embed=embed)
          except genshin.RedemptionException as e:
              embed=discord.Embed(title="**GENSHIN** \ngiftcode không tồn tại hoặc đã được sửa dụng", description=f"```{e}```", colour=0xf5003d)
              await Interaction.message.edit(embed=embed)
          except genshin.AccountNotFound:
              embed=discord.Embed(title="Không có tài khoản.", colour=0xf5003d)
              await Interaction.message.edit(embed=embed)
            
        elif self.code_Hsr.value != "":
            try:
                try:
                  await Interaction.response.edit_message(content=f"**...**")
                except discord.errors.InteractionResponded:
                  pass
  
                await client.redeem_code(self.code_Hsr.value, game=genshin.types.Game.STARRAIL)
                embed=discord.Embed(title=f"giftcode nhập thành công [STARRAIL] ```{self.code_Hsr.value}```", colour=0x00f576)  
                await Interaction.message.edit(embed=embed)
            except genshin.RedemptionException as e:
              embed=discord.Embed(title="**STARRAIL** \ngiftcode không tồn tại hoặc đã được sửa dụng", description=f"```{e}```", colour=0xf5003d)
              await Interaction.message.edit(embed=embed)
            except genshin.AccountNotFound:
              embed=discord.Embed(title="Không có tài khoản.", colour=0xf5003d)
              await Interaction.message.edit(embed=embed)
      else:
         await Interaction.response.send_message('bạn chưa có data hãy dùng ``/login`` để nhập data!')
      
      

class Select(discord.ui.Select):
  def __init__ (self):
    options = []
    options.append(discord.SelectOption(label="Daily", value="Daily_all", emoji="<a:Cat_Daiza:1065889446697914368>"))
    super().__init__(placeholder="Các Cộng Cụ", options=options)
  async def callback(self, Interaction):
   user_id = str(Interaction.user.id)
   data = load_data()
   if user_id in data:
    cookie = data[user_id]
    
    cookies = await genshin.complete_cookies(cookie)
    client = genshin.Client(cookies)
    
    if self.values[0] == "Daily_all":
      games= [genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL, genshin.types.Game.HONKAI]
      embed= discord.Embed()
      for gamess in games:
        parts = gamess.split('.')
        result = parts[-1]
        try:
            signed_in, claimed_rewards = await client.get_reward_info(game=gamess)
            reward = await client.claim_daily_reward(game=gamess)
    
            if isinstance(reward, genshin.GeetestTriggered):
                embed.add_field(name=f"**__{result}__** hoàn tất điểm danh.", value="", inline=False)
            elif isinstance(reward, genshin.AlreadyClaimed):
                assert signed_in
            elif isinstance(reward, genshin.GenshinException) and reward.retcode == -10002:
                embed.add_field(name="không tìm thấy tài khoản.", value="", inline=False)
            else:
                assert not signed_in
    
            rewards = await client.get_monthly_rewards(game=gamess)
            assert rewards[claimed_rewards].name == reward.name
        except Exception as e:
            embed.add_field(name=f"lỗi điểm danh **__{result}__**: {e}", value="", inline=False)
      await Interaction.channel.send(embed=embed)
   else:
         await Interaction.response.send_message('bạn chưa có data hãy dùng ``/login`` để nhập data!')
      

class SelectView(discord.ui.View):
  def __init__ (self, timeout=300):
    super().__init__(timeout=timeout)
    self.add_item(Select())
    
  @discord.ui.button(label="Redeem", style= discord.ButtonStyle.danger, emoji="<:nthach:1150124385345220780>")
  async def click1(self, Interaction: discord.Interaction, Button: discord.ui.Button,):
    await Interaction.response.send_modal(Redeem())



class Codes(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @commands.command(name="code", description="Redeem code game")
  async def code(self, ctx):
    embed = discord.Embed(title="Redeem code", description="Chức năng đang trong quá trình phát triển", colour=0x00f5a3, timestamp=datetime.now())
    await ctx.send(embed=embed, view=SelectView())


async def setup(bot):
  await bot.add_cog(Codes(bot))
