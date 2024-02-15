import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
import asyncio
import os
import sqlite3
import genshin

channelt = {'channelm' :None}
async def daily_reward(client):
      games = [
        genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL,
        genshin.types.Game.HONKAI
      ]
      for s, gamess in enumerate(games):
        datasss = await client.get_hoyolab_user()
        channel = channelt.get('channelm')
        try:
          signed_in, claimed_rewards = await client.get_reward_info(game=gamess)
          reward = await client.claim_daily_reward(game=gamess)
          if isinstance(reward, genshin.GeetestTriggered):
              await channel.send(f"{gamess[:-8]} hoàn tất điểm danh | {datasss.nickname}.")
          elif isinstance(reward, genshin.AlreadyClaimed):
              await channel.send(f"{gamess[:-8]} đã điểm danh | {datasss.nickname}.")
          elif isinstance(reward, genshin.GenshinException) and reward.retcode == -10002:
              await channel.send("Không tìm thấy tài khoản.")
          else:
            assert not signed_in
          rewards = await client.get_monthly_rewards(game=gamess)
          assert rewards[claimed_rewards].name == reward.name
        except Exception as e:
          await channel.send(f"lỗi trong điểm danh {gamess}: {e} | {datasss.nickname}")
async def logins(*cookies_data):
      cookies_data = [
        {
          "ltuid": 139734936,
          "ltoken": '5qs4vLtAHhNAZ2cvH38alyRVHjRs6Uy9XzgHkjcB'
        },#beemin
        {
          "ltuid": 89595259,
          "ltoken": 'W26k5CAFSzoR5UHCXMNXBoLdgWahoe2VNIKEIsjb'
        },#jenn
      ]
      clients = []
      for a, data in enumerate(cookies_data):
        client = genshin.Client(lang="vi-vn")
        client.set_cookies(data)
        clients.append(client)
      tasks = [daily_reward(client) for client in clients]
      await asyncio.gather(*tasks)

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
        elif current_time.hour == 23 and current_time.minute == 18:
            await logins()
  
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise erro

    @commands.Cog.listener()
    async def on_ready(self):
      filename = os.path.basename(__file__)
      print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
      print('='* 50)
  
    @tasks.loop(seconds=10)
    async def update_data(self):
        try:
            channel = self.bot.get_channel(1118977913392476210)
            channelt['channelm'] = channel
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