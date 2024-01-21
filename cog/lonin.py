import discord
from discord import app_commands
from discord.ext import commands
import genshin
import json
import os

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
Client = genshin.Client()

class cklogin(discord.ui.Modal, title="nhập dữ liệu cookie"):
  ctk2 = discord.ui.TextInput(label="cookie_token_v2", style=discord.TextStyle.paragraph)
  accmid2 = discord.ui.TextInput(label="account_mid_v2", style=discord.TextStyle.paragraph)
  accid2 = discord.ui.TextInput(label="account_id_v2", style=discord.TextStyle.paragraph)
  ltk2 = discord.ui.TextInput(label="ltoken_v2", style=discord.TextStyle.paragraph)
  async def on_submit(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()
    cookie = f"'cookie_token_v2': '{self.ctk2.value}', 'account_mid_v2': '{self.accmid2.value}', 'account_id_v2': '{self.accid2.value}', 'ltoken_v2': '{self.ltk2.value}', 'ltmid_v2': '{self.accmid2.value}', 'ltmid_v2': '{self.accid2.value}'"

    try:

        data[user_id] = cookie
        save_data(data)

        await Interaction.response.send_message("Lưu dữ liệu thành công!")
    except Exception as e:
        await Interaction.response.send_message(f"Lỗi: {e}")


class tklogin(discord.ui.Modal, title="nhập dữ liệu thẳng bằng tài khoản"):
  tk = discord.ui.TextInput(label="Nhập tài khoảng", style=discord.TextStyle.paragraph)
  mk = discord.ui.TextInput(label="Nhập mật khẩu", style=discord.TextStyle.paragraph)
  async def on_submit(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()

    try:
        cookie = await Client.login_with_password(self.tk.value, self.mk.value, port=8080)

        data[user_id] = cookie
        save_data(data)

        await Interaction.response.send_message("Lưu dữ liệu thành công!")
    except Exception as e:
        await Interaction.response.send_message(f"Lỗi: {e}")


class Button1(discord.ui.View):
  def __init__(self):
    super().__init__()

  @discord.ui.button(label="cookie", style= discord.ButtonStyle.green, emoji="🍪")
  async def cookiel(self, Interaction, button: discord.ui.Button,):
    await Interaction.response.send_modal(cklogin())

  @discord.ui.button(label="Đăng nhập", style= discord.ButtonStyle.green, emoji="🔒")
  async def tklogin(self, Interaction, button: discord.ui.Button,):
    await Interaction.response.send_modal(tklogin())

class Button2(discord.ui.View):
  def __init__(self):
    super().__init__()

  @discord.ui.button(label="Đã liên kết", style= discord.ButtonStyle.green, emoji="✅", disabled=True)
  async def cookiel(self, Interaction, button: discord.ui.Button,):
    await Interaction.response.send_message("ss")


class lonin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.data = load_data()


  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @app_commands.command(name="login", description="nhập thông tin liên kết data")
  async def login(self, Interaction:discord.Interaction):
    user_id = str(Interaction.user.id)
    embed = discord.Embed(title="Liên kết data",color=discord.Color.yellow())
    embed.add_field(name="**Thông tin đã kết nối**", value="", inline=False)
    try:
      cookie = self.data[user_id]
      Clientt = genshin.Client(cookie)
      rews = await Clientt.get_hoyolab_user()
      embed.add_field(name=f"✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``", value="", inline=False)
      await Interaction.response.send_message(embed=embed, view=Button2())
    except Exception as e:
      embed.add_field(name="__hãy chọn phương thức lấy data từ tk của bạn!__", value="", inline=False)
      embed.add_field(name="❌ Chưa nhập thông tin tài khoản!", value="", inline=False)
      await Interaction.response.send_message(embed=embed, view=Button1())




async def setup(bot):
  await bot.add_cog(lonin(bot))
