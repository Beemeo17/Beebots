import discord
from discord import app_commands
from discord.ext import commands
import genshin
import json
import os
import asyncio
import enka

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
  ctk2 = discord.ui.TextInput(label="cookie_token_v2",
                              style=discord.TextStyle.paragraph)
  accmid2 = discord.ui.TextInput(label="account_mid_v2",
                                 style=discord.TextStyle.paragraph)
  accid2 = discord.ui.TextInput(label="account_id_v2",
                                style=discord.TextStyle.paragraph)
  ltk2 = discord.ui.TextInput(label="ltoken_v2",
                              style=discord.TextStyle.paragraph)

  async def on_submit(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()
    cookie = {'cookie_token_v2': f'{self.ctk2.value}',
              'account_mid_v2': f'{self.accmid2.value}',
              'account_id_v2': f'{self.accid2.value}',
              'ltoken_v2': f'{self.ltk2.value}',
              'ltmid_v2': f'{self.accmid2.value}',
              'ltmid_v2': f'{self.accid2.value}'}
    try:
      if user_id in data:
        data[user_id]["cookies"] = cookie
      else:
        data[user_id] = {"cookies": cookie}
      save_data(data)
      Clientt = genshin.Client(cookie)
      rews = await Clientt.get_hoyolab_user()

      embed = discord.Embed(
          title=
          f'✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``',
          color=discord.Color.yellow())
      await Interaction.message.edit(embed=embed)
      await Interaction.response.edit_message(content="Lưu dữ liệu thành công!")
    except Exception as e:
      await Interaction.response.edit_message(content=f"Lỗi: {e}")


class tklogin(discord.ui.Modal, title="nhập dữ liệu thẳng bằng tài khoản"):
  tk = discord.ui.TextInput(label="Nhập tài khoảng", style=discord.TextStyle.paragraph)
  mk = discord.ui.TextInput(label="Nhập mật khẩu",
                            style=discord.TextStyle.paragraph)

  async def on_submit(self, Interaction):
    user_id = str(Interaction.user.id)
    data = load_data()

    try:
      cookie = await Client.login_with_password(self.tk.value,
                                                self.mk.value,
                                                port=0)
      if user_id in data:
        data[user_id]["cookies"] = cookie
      else:
        data[user_id] = {"cookies": cookie}
      save_data(data)
      Clientt = genshin.Client(cookie)
      rews = await Clientt.get_hoyolab_user()

      embed = discord.Embed(
          title=
          f'✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``',
          color=discord.Color.yellow())
      await Interaction.message.edit(embed=embed)
      await Interaction.response.edit_message(content="Lưu dữ liệu thành công!")
    except Exception as e:
      await Interaction.response.edit_message(content=f"Lỗi: {e}")


class uids(discord.ui.Modal, title="Lưu UID"):
  uid = discord.ui.TextInput(label="Nhập UID",
                             style=discord.TextStyle.paragraph)

  async def on_submit(self, interaction: discord.Interaction):
    async with enka.EnkaAPI() as api:
      user_id = str(interaction.user.id)
      data = load_data()
      try:
        await api.fetch_showcase(self.uid.value)
        if user_id in data:
          data[user_id]["uid"] = self.uid.value
        else:
          data[user_id] = {"uid": self.uid.value}
        save_data(data)
        await interaction.response.edit_message(content=f"Lưu UID:{self.uid.value} thành công!")
      except Exception as e:
        await interaction.response.edit_message(content=f"Lỗi: {e} Vui lòng Kiểm tra lại UID!")


class Button1(discord.ui.View):

  def __init__(self):
    super().__init__()

  @discord.ui.button(label="cookie",
                     style=discord.ButtonStyle.green,
                     emoji="🍪")
  async def cookiel(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    await Interaction.response.send_modal(cklogin())

  @discord.ui.button(label="Đăng nhập",
                     style=discord.ButtonStyle.green,
                     emoji="🔒")
  async def tklogin(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    await Interaction.response.send_modal(tklogin())

  @discord.ui.button(label="UID", style=discord.ButtonStyle.green)
  async def uid(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    await Interaction.response.send_modal(uids())


class Button2(discord.ui.View):

  def __init__(self):
    super().__init__()

  @discord.ui.button(label="Đã liên kết",
                     style=discord.ButtonStyle.green,
                     emoji="✅",
                     disabled=True)
  async def cookiel(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    await Interaction.response.send_message("ss")

  @discord.ui.button(label="change data",
                     style=discord.ButtonStyle.gray,
                     emoji="🔁")
  async def channges(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    data = load_data()
    user_id = str(Interaction.user.id)
    del data[user_id]
    embed = discord.Embed()
    embed.add_field(
        name="__Hãy chọn phương thức lấy dữ liệu từ tài khoản của bạn!__",
        value="",
        inline=False)
    await Interaction.response.edit_message(embed=embed, view=Button1())

  @discord.ui.button(label="UID", style=discord.ButtonStyle.green)
  async def uid(
      self,
      Interaction,
      button: discord.ui.Button,
  ):
    await Interaction.response.send_modal(uids())

class lonin(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(
        f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ"
    )
    print('=' * 50)

  @app_commands.command(name="login",
                        description="nhập thông tin liên kết data")
  async def login(self, Interaction: discord.Interaction):
    data = load_data()
    user_id = str(Interaction.user.id)
    
    embed = discord.Embed(title="Liên kết data", color=discord.Color.yellow())
    embed.add_field(name="**Thông tin đã kết nối**", value="", inline=False)
    if user_id in data:
      if "uid" in data[user_id]:
        uid = data[user_id]["uid"]
        embed.add_field(name=f"UID {uid}", value="", inline=False)
    try:
      cookie = data[user_id]["cookies"]
      Clientt = genshin.Client(cookie)
      rews = await Clientt.get_hoyolab_user()
      embed.add_field(
          name=
          f"✅ Đã kết nối thành công với tài khoản! \nName: ``{rews.nickname}``",
          value="",
          inline=False)
      await Interaction.response.send_message(embed=embed, view=Button2())
    except Exception as e:
      embed.add_field(
          name="__Hãy chọn phương thức lấy dữ liệu từ tài khoản của bạn!__",
          value="",
          inline=False)
      embed.add_field(name="❌ Chưa nhập thông tin tài khoản!", value="", inline=False)
      await Interaction.response.send_message(embed=embed, view=Button1())



async def setup(bot):
  await bot.add_cog(lonin(bot))