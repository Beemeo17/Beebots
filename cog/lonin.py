import discord
from discord import app_commands
from discord.ext import commands
import genshin
import json
import os
import asyncio

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
        Clientt = genshin.Client(cookie)
        rews = await Clientt.get_hoyolab_user()

        embed=discord.Embed(title=f'✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``', color=discord.Color.yellow())
        await Interaction.message.edit(embed=embed)
        await Interaction.response.send_message("Lưu dữ liệu thành công!", ephemeral=True)
    except Exception as e:
        await Interaction.response.send_message(f"Lỗi: {e}", ephemeral=True)


class tklogin(discord.ui.Modal, title="nhập dữ liệu thẳng bằng tài khoản"):
  tk = discord.ui.TextInput(label="Nhập tài khoảng", style=discord.TextStyle.paragraph)
  mk = discord.ui.TextInput(label="Nhập mật khẩu", style=discord.TextStyle.paragraph)
  async def on_submit(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()

    try:
        cookie = await Client.login_with_password(self.tk.value, self.mk.value, port=0)

        data[user_id] = cookie
        save_data(data)
        Clientt = genshin.Client(cookie)
        rews = await Clientt.get_hoyolab_user()

        embed=discord.Embed(title=f'✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``', color=discord.Color.yellow())
        await Interaction.message.edit(embed=embed)
        await Interaction.response.send_message("Lưu dữ liệu thành công!", ephemeral=True)
    except Exception as e:
     await Interaction.response.send_message(f"Lỗi: {e}", ephemeral=True)


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

  @discord.ui.button(label="change data", style= discord.ButtonStyle.gray, emoji="🔁")
  async def channges(self, Interaction, button: discord.ui.Button,):
   data = load_data()
   user_id = str(Interaction.user.id)
   del data[user_id]
   embed=discord.Embed()
   embed.add_field(name="__Hãy chọn phương thức lấy dữ liệu từ tài khoản của bạn!__", value="", inline=False)
   await Interaction.message.edit(embed=embed, view=Button1())
   await Interaction.response.send_message('.', ephemeral=True)

class Button3(discord.ui.View):
  def __init__(self):
    super().__init__()
  @discord.ui.button(label="TIMEOUT", style= discord.ButtonStyle.green, emoji="✖️", disabled=True)
  async def timeoutst(self, Interaction, button: discord.ui.Button,):
    await Interaction.channel.send('...')

class lonin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @app_commands.command(name="login", description="nhập thông tin liên kết data")
  async def login(self, Interaction:discord.Interaction):
    data = load_data()
    user_id = str(Interaction.user.id)
    timeout = 10
    message3 = await Interaction.response.send_message('•', ephemeral=True)
    embeds= discord.Embed(title='Timeout!', description='Timeout bạn có thể sửa dụng lại ``/login`` để tiếp tục login hoặc đổi data',color=discord.Color.red())
    embed = discord.Embed(title="Liên kết data",color=discord.Color.yellow())
    embed.add_field(name="**Thông tin đã kết nối**", value="", inline=False)
    try:
            cookie = data[user_id]
            Clientt = genshin.Client(cookie)
            rews = await Clientt.get_hoyolab_user()
            embed.add_field(name=f"✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``", value="", inline=False)
            message = await Interaction.channel.send(embed=embed, view=Button2())
    except Exception as e:
        embed.add_field(name="__Hãy chọn phương thức lấy dữ liệu từ tài khoản của bạn!__", value="", inline=False)
        embed.add_field(name="❌ Chưa nhập thông tin tài khoản!", value="", inline=False)
        message = await Interaction.channel.send(embed=embed, view=Button1())

    await asyncio.sleep(timeout)
    await message.edit(embed=embeds, view=Button3())




async def setup(bot):
  await bot.add_cog(lonin(bot))