import discord
from discord.ext import commands
from discord import app_commands
import genshin
from bs4 import BeautifulSoup
import asyncio
import re

counts = 11
cougoc = 11

async def event(I, input):
     lclient = genshin.Client()
     te = await lclient.get_genshin_announcements(lang="vi-vn")
     if input > (len(te)-1):
         input = len(te) - 1
     elif input < 11:
         input = 11
     embed = discord.Embed(title=te[input].title)
     embed.set_image(url=te[input].banner)
     soup = BeautifulSoup(te[input].content, 'html.parser')
     printed_items = []
     for item in soup.find_all('span')[:25]:
      if item.text not in printed_items:
        cleaned_text = re.sub(r'<t class="t_lc">|</t>', '', item.text)
        embed.add_field(name="", value=cleaned_text, inline=False)
        printed_items.append(item.text)
     await I.response.edit_message(embed=embed)

class skip(discord.ui.Modal, title="page skip"):
    page = discord.ui.TextInput(label="Trang skip tới", style=discord.TextStyle.paragraph)

    async def on_submit(self, I: discord.Interaction):
        if self.page.value.isdigit():
            await event(I, int(self.page.value) + 10)
            await pages().up_button(I, int(self.page.value))
        elif isinstance(self.page.value, str):
            await I.response.send_message("❌Vui lòng nhập đúng Trang muốn chuyển tới!❌", ephemeral=True)

class pages(discord.ui.View):
  def __init__(self, timeout=300):
    super().__init__(timeout=timeout)
    global counts, cougoc
    self.counts = 11
    self.cougoc = 12

  async def Tout(self, I):
      self.min_next.disabled = True
      self.next_trai.disabled = True
      self.skips.disabled = True
      self.next_phai.disabled = True
      self.max_next.disabled = True
      await I.edit_original_response(view=self)
    
  async def up_bu(self, I, bu):
    lclient = genshin.Client()
    te = await lclient.get_genshin_announcements(lang="vi-vn")
    self.skips.label = f"{bu}/{len(te) - (self.cougoc-1)}"
    await I.edit_original_response(view=self)
    
  async def up_button(self, I, bu):
    lclient = genshin.Client()
    te = await lclient.get_genshin_announcements(lang="vi-vn")
    if bu > len(te) - (self.cougoc):
        bu = len(te) - (self.cougoc-1)
        self.max_next.disabled = True
        self.next_phai.disabled = True
        self.min_next.disabled = False
        self.next_trai.disabled = False
    elif bu < 1:
        bu = 1
        self.min_next.disabled = True
        self.next_trai.disabled = True
        self.max_next.disabled = False
        self.next_phai.disabled = False
    else:
        self.max_next.disabled = False
        self.next_phai.disabled = False
        self.min_next.disabled = False
        self.next_trai.disabled = False
    self.counts = bu + 10
    self.skips.label = f"{bu}/{len(te) - (self.cougoc-1)}"
    await I.edit_original_response(view=self)

  @discord.ui.button(label="<<", style=discord.ButtonStyle.green, disabled=True)
  async def min_next(self, I: discord.Interaction, button: discord.ui.Button,):
    lclient = genshin.Client()
    te = await lclient.get_genshin_announcements(lang="vi-vn")
    self.counts = self.cougoc - 1
    await event(I, self.counts)
    button.disabled = True
    self.next_trai.disabled = True
    self.max_next.disabled = False
    self.next_phai.disabled = False
    self.skips.label = f"{self.counts-10}/{len(te) - (self.cougoc-1)}"
    await I.edit_original_response(view=self)
    
  @discord.ui.button(label="<", style=discord.ButtonStyle.gray, disabled=True)
  async def next_trai(self, I: discord.Interaction, button: discord.ui.Button,):
      lclient = genshin.Client()
      te = await lclient.get_genshin_announcements(lang="vi-vn")
      self.counts -= 1
      await event(I, self.counts)
      if self.counts <= self.cougoc:
          button.disabled = True
          self.min_next.disabled = True
      self.max_next.disabled = False
      self.next_phai.disabled = False
      self.skips.label = f"{self.counts-10}/{len(te) - (self.cougoc-1)}"
      await I.edit_original_response(view=self)
    
  @discord.ui.button(label="1/1", style=discord.ButtonStyle.gray)
  async def skips(self, I: discord.Interaction, button: discord.ui.Button,):
    await I.response.send_modal(skip())

  @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
  async def next_phai(self, I: discord.Interaction, button: discord.ui.Button,):
      lclient = genshin.Client()
      te = await lclient.get_genshin_announcements(lang="vi-vn")
      self.counts += 1
      await event(I, self.counts)
      if self.counts == (len(te) - 1):
          button.disabled = True
          self.max_next.disabled = True
      self.min_next.disabled = False
      self.next_trai.disabled = False
      self.skips.label = f"{self.counts-10}/{len(te) - (self.cougoc-1)}"
      await I.edit_original_response(view=self)

  @discord.ui.button(label=">>", style=discord.ButtonStyle.green)
  async def max_next(self, I: discord.Interaction, button: discord.ui.Button,):
    lclient = genshin.Client()
    te = await lclient.get_genshin_announcements(lang="vi-vn")
    self.counts = len(te) - 1
    await event(I, self.counts)
    button.disabled = True
    self.next_phai.disabled = True
    self.min_next.disabled = False
    self.next_trai.disabled = False
    self.skips.label = f"{self.counts-10}/{len(te) - (self.cougoc-1)}"
    await I.edit_original_response(view=self)
  
class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lclient = genshin.Client()

    @app_commands.command(name="event", description="Tổng hợp sự kiện genshin")
    async def evt(self, Interaction):
        cougoc = 11
        lclient = genshin.Client()
        te = await lclient.get_genshin_announcements(lang="vi-vn")
        embed = discord.Embed(title=te[cougoc].title)
        embed.set_image(url=te[cougoc].banner)
        soup = BeautifulSoup(te[cougoc].content, 'html.parser')
        printed_items = []
        for item in soup.find_all('span')[:25]:
         if item.text not in printed_items:
          cleaned_text = re.sub(r'<t class="t_lc">|</t>', '', item.text)
          embed.add_field(name="", value=cleaned_text, inline=False)
          printed_items.append(item.text)
        await Interaction.response.send_message(embed=embed, view=pages())
        await pages().up_bu(Interaction, 1)
        await asyncio.sleep(300)
        await pages().Tout(Interaction)


async def setup(bot):
  await bot.add_cog(events(bot))
