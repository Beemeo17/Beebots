import discord
from discord.ext import commands
from discord import app_commands
import genshin
from discord.ui import Select, View
from bs4 import BeautifulSoup
import datetime
import pytz
import asyncio
import re

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lclient = genshin.Client()

    @app_commands.command(name="event")
    async def te(self, Interaction: discord.Interaction):
        events = await self.lclient.get_genshin_announcements(lang="vi-vn")
        select = Select(placeholder="All event", options = [
            discord.SelectOption(label=event.subtitle, value=f"{i+1}") for i, event in enumerate(events[11:])
        ])
        async def my_callback(Interaction):
         lclient = genshin.Client()
         te = await lclient.get_genshin_announcements(lang="vi-vn")
         a = int(select.values[0]) + 10
         print(a)
         embed = discord.Embed(title=te[a].title)
         embed.set_image(url=te[a].banner)
         soup = BeautifulSoup(te[a].content, 'html.parser')
         printed_items = []
         for item in soup.find_all('span')[:25]:
          if item.text not in printed_items:
            cleaned_text = re.sub(r'<t class="t_lc">|</t>', '', item.text)
            embed.add_field(name="", value=cleaned_text, inline=False)
            printed_items.append(item.text)
         await Interaction.response.edit_message(embed=embed)
        
        view = View()
        select.callback = my_callback
        view.add_item(select)
        a = 11
        embed = discord.Embed(title=events[a].title)
        embed.set_image(url=events[a].banner)
        soup = BeautifulSoup(events[a].content, 'html.parser')
        printed_items = []
        for item in soup.find_all('span')[:25]:
         if item.text not in printed_items:
            cleaned_text = re.sub(r'<t class="t_lc">|</t>', '', item.text)
            embed.add_field(name="", value=cleaned_text, inline=False)
            printed_items.append(item.text)
                
        await Interaction.response.send_message(embed=embed, view=view)
        await asyncio.sleep(180)
        select.disabled = True
        select.placeholder = " timeout!!"
        await Interaction.edit_original_response(view=view)

async def setup(bot):
  await bot.add_cog(events(bot))
