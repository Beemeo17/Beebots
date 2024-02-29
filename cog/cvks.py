import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
import asyncio
import os
import sqlite3
import genshin
import json

files = "test.json"
def load_data():
  try:
      with open(files, 'r') as file:
          data = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
      data = {}
  return data

async def get_cookie(channel):
    data = load_data()
    for key, value in data.items():
        if value.get("daily_auto"):
          gamep = [
            genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL,
            genshin.types.Game.HONKAI]
          embed = discord.Embed()
          for games in gamep[:3]:
            client = genshin.Client(value.get("cookies"))
            signed_in, claimed_rewards = await client.get_reward_info(game=games)
            rews = await client.get_hoyolab_user()
            try:
              await client.claim_daily_reward(game=games)
              embed.add_field(name=f"{games[19:]} | Hoàn thành điểm danh | {rews.nickname}", value="", inline=False)
            except genshin.AlreadyClaimed:
                assert signed_in
                embed.add_field(name=f"{games[19:]} | Đã nhận thưởng trước đó | {rews.nickname}", value="", inline=False)
            except Exception as s:
                embed.add_field(name=f"{games[19:]} | {s} | {rews.nickname}", value="", inline=False)
          await channel.send(embed=embed)


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('templates/users.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, name TEXT, exp INTEGER, level INTEGER, explevel INTEGER)''')
        self.tz = pytz.timezone('Asia/Ho_Chi_Minh')
        self.update_data.start()
        self.send_greetings.start()
        self.update_presence.start()
    def cog_unload(self):
        self.update_presence.cancel()

    @tasks.loop(seconds=60)
    async def update_presence(self):
        global start_time
        start_time = datetime.now()
        game = discord.Game(name="❄️HIVE Teyvat❄️")
        await self.bot.change_presence(activity=game)

    @update_presence.before_loop
    async def before_update_presence(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=60)
    async def send_greetings(self):
        current_time = datetime.now(self.tz).time()
        channel = self.bot.get_channel(699305290289381477)
        if current_time.hour == 7 and current_time.minute == 0:
            await channel.send("chúc mọi người một ngày mới vui vẻ 🧩**Good Morning**🧩")
        elif  current_time.hour == 22 and current_time.minute == 0:
            await channel.send("chúc mọi người ngủ ngon 💤**Good Night**💤")
        elif current_time.hour == 23 and current_time.minute == 4:
            channels = self.bot.get_channel(1156104339291635758)
            await get_cookie(channels)

    @commands.Cog.listener()
    async def on_ready(self):
      filename = os.path.basename(__file__)
      print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
      print('='* 50)
  
    @tasks.loop(seconds=10)
    async def update_data(self):
        try:
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            guild = self.bot.get_guild(550601755709407233)
            channel = self.bot.get_channel(1105730219110825984)
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
            self.c.execute("SELECT name, level, exp FROM users ORDER BY level DESC, exp DESC LIMIT 3")
            results = self.c.fetchall()
            embed.add_field(name="**Bảng Xếp Hạng**", value="", inline=False)
            embed.set_thumbnail(url="https://example.com/leaderboard_icon.png")
            for index, (name, level, exp) in enumerate(results):
                message_count = exp - 1
                embed.add_field(name=f"> #{index+1} - {name}", value=f"> Level: **{level}**   EXP: **{message_count}**", inline=False)
            current_time = datetime.now(tz).strftime('%H:%M:%S - %d/%m/%Y')
            embed.set_footer(text=f"UPDATE: {current_time}")
            message = await channel.fetch_message(1111143360707711016)
            await message.edit(content=None, embed=embed)
        except Exception as e:
            print(e)
          
async def setup(bot):
   await bot.add_cog(ServerInfo(bot))