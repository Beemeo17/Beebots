import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
import asyncio
import os
import sqlite3
import genshin
import json
from io import BytesIO
import random
import psutil

ts = 0
tm = 0
th = 0
td = 0

files = "test.json"
def load_data():
  try:
      with open(files, 'r') as file:
          data = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
      data = {}
  return data


class COG_HZ1(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.spam_records = {}
      self.conns = sqlite3.connect('templates/users.db')
      self.cursor = self.conns.cursor()
      # Create table
      self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, name TEXT, exp INTEGER, level INTEGER, explevel INTEGER)'''
                )
      self.cursor.execute('''CREATE TABLE IF NOT EXISTS voice_channels
                            (channel_id INTEGER PRIMARY KEY, owner_id INTEGER, parent_id INTEGER)''')
      self.conns.commit()
      self.tz = pytz.timezone('Asia/Ho_Chi_Minh')
      self.update_data.start()
      self.send_greetings.start()
      self.up_cour.start()
  def cog_unload(self):
      self.update_presence.cancel()
  
  @commands.Cog.listener() #message
  async def on_message(self, message):
    if message.author.bot:
            return
    if message.content.startswith('b!'):
      return
      
    elif message.guild and message.guild.id == 550601755709407233:
        if message.channel.id != 1102490528613937212:
            await self.process_leveling(message)

  @update_presence.before_loop #stats
  async def before_update_presence(self):
      await self.bot.wait_until_ready()

  @tasks.loop(seconds=20)
  async def up_cour(self):
    global ts, tm, th, td
    ts += 20
    if ts == 60:
      ts = 0
      tm += 1
      if tm == 60:
        tm = 0
        th += 1
        if th == 24:
          th = 0
          td += 1

  @up_cour.before_loop
  async def before_uptime(self):
    await self.bot.wait_until_ready()
    
  @tasks.loop(seconds=60) #on time
  async def send_greetings(self):
      current_time = datetime.now(self.tz).time()
      channel = self.bot.get_channel(1241472122275106897)
      if  current_time.hour == 22 and current_time.minute == 0:
          await channel.send("chúc mọi người ngủ ngon 💤**Good Night**💤")

  @tasks.loop(seconds=10) #top info
  async def update_data(self):
      try:
          tz = pytz.timezone('Asia/Ho_Chi_Minh')
          guild = self.bot.get_guild(1241472121826181221)
          channel = self.bot.get_channel(1241763204905042020)
          boosts = guild.premium_subscription_count
          online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
          total_members = guild.member_count
          bot_count = sum(1 for member in guild.members if member.bot)
          embed = discord.Embed(title="**Thông tin server**", color=discord.Color.blue())
          embed.add_field(name=f"> Số Người Đang Online: {online_members}", value="", inline=False)
          embed.add_field(name=f"> Tổng Thành Viên: {total_members}", value="", inline=False)
          embed.add_field(name=f"> Thành Viên: {total_members - bot_count}", value="", inline=False)
          embed.add_field(name=f"> Số Lượng Bot: {bot_count}", value="", inline=False)
          embed.add_field(name=f"> Boost: {boosts}", value="", inline=False)
          current_time = datetime.now(tz).strftime('%H:%M:%S - %d/%m/%Y')
          embed.set_footer(text=f"UPDATE: {current_time}")
          message = await channel.fetch_message(1242764555713777724)
          await message.edit(content=None, embed=embed)
      except Exception as e:
          print(e)
  
  @commands.Cog.listener() #voie
  async def on_voice_state_update(self, member, before, after):
      if before.channel != after.channel:
          if after.channel and after.channel.id == 1242761063309643796:
              guild = member.guild
              category = after.channel.category

              new_channel = await guild.create_voice_channel(name=f"┕🍀{member.name}🍀┛", category=category)

              self.cursor.execute('INSERT INTO voice_channels (channel_id, owner_id, parent_id) VALUES (?, ?, ?)', (new_channel.id, member.id, category.id))
              self.conns.commit()

              await member.move_to(new_channel)

      if before.channel:
          root_channel = before.channel.category
          self.cursor.execute('SELECT * FROM voice_channels WHERE parent_id = ?', (root_channel.id,))
          rows = self.cursor.fetchall()
          if rows:
              for row in rows:
                  child_channel_id = row[0]
                  child_channel = self.bot.get_channel(child_channel_id)
                  if child_channel and len(child_channel.members) == 0:
                      await child_channel.delete()

                      self.cursor.execute('DELETE FROM voice_channels WHERE channel_id = ?', (child_channel_id,))
                      self.conns.commit()

  @commands.Cog.listener() #loi chao
  async def on_member_join(self, user):
    if user.guild.id == 550601755709407233:
      embed = discord.Embed()
      luat_channel = self.bot.get_channel(1241793843674747053)
      thongbao_channel = self.bot.get_channel(1241761574499123301)
      phongtra_channel = self.bot.get_channel(1241472122275106897)
      role_channel = self.bot.get_channel(1241759230768451715)
      embed = discord.Embed(color=0xc8ed0c)
      embed.add_field(name="", value='> chào mừng bạn đến với server')
      embed.set_thumbnail(url=user.avatar)
      embed.add_field(
        name=f"🍁 {luat_channel.mention} Room luật hãy bỏ chút thời gian đọc nó",
        value="",
        inline=False)
      embed.add_field(name=f"🍁 {thongbao_channel.mention} thông báo của server",
                      value="",
                      inline=False)
      embed.add_field(
        name=f"🍁 {phongtra_channel.mention} Room chat sinh hoạt chung",
        value="",
        inline=False)
      embed.add_field(
        name=f"🍁 {role_channel.mention} Room pick role",
        value="",
        inline=False)
      embed.set_image(url="https://images.alphacoders.com/113/1131281.jpg")
      embed.add_field(name="> chúc bạn sẽ có những giây phút tuyệt vời với server",
                      value="",
                      inline=False)
      channel_welcome = self.bot.get_channel(1241758812717715546)
      await channel_welcome.send(f"xin chào {user.mention}", embed=embed)

  """
  @commands.Cog.listener() #tam biet
  async def on_member_remove(self, user):
    if user.guild.id == 550601755709407233:
      embed = discord.Embed()
      embed = discord.Embed(color=0xc8ed0c)
      embed.add_field(name="", value="> cảm ơn vì đã đồng hành cùng server")
      embed.set_thumbnail(url=user.avatar)
      embed.set_image(
        url=
        "https://images2.thanhnien.vn/Uploaded/nthanhluan/2021_12_11/picture10-9485.png"
      )
      embed.add_field(name="> giờ thì tạm biệt ", value="", inline=False)
    
      join_date = user.joined_at.replace(tzinfo=None)
      current_date = datetime.utcnow().replace(tzinfo=None)
      duration = current_date - join_date
      server_duration = duration.days
      embed.set_footer(text=f"Thời gian gắn bó: {server_duration} ngày")
    
      channel = self.bot.get_channel(1092462625994055820)
      await channel.send(f"tạm biệt {user.mention}", embed=embed)"""

  
async def setup(bot):
   await bot.add_cog(COG_HZ1(bot))
