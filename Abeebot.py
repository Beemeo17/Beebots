import discord
from discord.ext import commands, tasks
import os
import sqlite3
import asyncio
import genshin
import calendar
import requests

conn = sqlite3.connect('templates/users.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, name TEXT, exp INTEGER, level INTEGER, explevel INTEGER)'''
          )

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)


# bot on
@bot.event
async def on_ready():
  update_data.start()
  print("█▄▄ █▀█ ▀█▀   ▄▀█   █▀ ▄▀█ █▄░█   █▀ ▄▀█ █▄░█ █▀▀")
  print("█▄█ █▄█ ░█░   █▀█   ▄█ █▀█ █░▀█   ▄█ █▀█ █░▀█ █▄█")
  await update_presence()
  try:
    synced = await bot.tree.sync()
    print(
      f"[OK] {bot.user.name}#{bot.user.discriminator} - Connect {len(synced)} SLASH COMMANDS"
    )
    print('=' * 50)
  except Exception as e:
    print(e)
  while True:
    current_time = datetime.now(tz).time()
    channel = bot.get_channel(699305290289381477)
    if current_time.hour == 22 and current_time.minute == 0:
      await channel.send("chúc mọi người ngủ ngon 💤**Good Night**💤")
    elif current_time.hour == 7 and current_time.minute == 0:
      await channel.send(
        "chúc mọi người một ngày mới vui vẻ 🧩**Good Morning**🧩")
    elif current_time.hour == 23 and current_time.minute == 5 :
      await mainss()
    await asyncio.sleep(60)


async def daily_reward(client):
  games = [
    genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL,
    genshin.types.Game.HONKAI
  ]
  channel = bot.get_channel(1118977913392476210)
  for gamess in games:
    datasss = await client.get_hoyolab_user()
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
      
async def mainss(*cookies_data):
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
  for data in cookies_data:
    client = genshin.Client(lang="vi-vn")
    client.set_cookies(data)
    clients.append(client)
  tasks = [daily_reward(client) for client in clients]
  await asyncio.gather(*tasks)


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return

  raise error


async def update_presence():
  global start_time

  start_time = datetime.now()
  game = discord.Game(name="❄️HIVE Teyvat❄️")
  await bot.change_presence(activity=game)



import pytz
from datetime import datetime, time

tz = pytz.timezone('Asia/Ho_Chi_Minh')


@tasks.loop(seconds=10)
async def update_data():
  try:
    guild = bot.get_guild(550601755709407233)
    channel = guild.get_channel(1105730219110825984)

    boosts = guild.premium_subscription_count
    current_time = datetime.now(tz).strftime('%H:%M:%S - %d/%m/%Y')
    online_members = sum(1 for member in guild.members
                         if member.status != discord.Status.offline)
    total_members = guild.member_count
    bot_count = sum(1 for member in guild.members if member.bot)

    embed = discord.Embed(title="**Thông tin server**",
                          color=discord.Color.blue())
    embed.add_field(name=f"> Số Người Đang Online: {str(online_members)}",
                    value="",
                    inline=False)
    embed.add_field(name=f"> Tổng Thành Viên: {str(total_members)}",
                    value="",
                    inline=False)
    embed.add_field(
      name=f"> Thành Viên: {str(((total_members)) - ((bot_count)))}",
      value="",
      inline=False)
    embed.add_field(name=f"> Số Lượng Bot: {str(bot_count)}",
                    value="",
                    inline=False)
    embed.add_field(name=f"> Boost: {str(boosts)}", value="", inline=False)

    c.execute(
      "SELECT name, level, exp FROM users ORDER BY level DESC, exp DESC LIMIT 3"
    )
    results = c.fetchall()

    embed.add_field(name="**Bảng Xếp Hạng**", value="", inline=False)
    embed.set_thumbnail(url="https://example.com/leaderboard_icon.png")

    for index, result in enumerate(results):
      name, level, exp = result
      message_count = exp - 1
      embed.add_field(name=f"> #{index+1} - {name}",
                      value=f"> Level: **{level}**   EXP: **{message_count}**",
                      inline=False)
      embed.set_footer(text=f"UPDATE: {current_time}")

    message = await channel.fetch_message(1111143360707711016)
    await message.edit(content=None, embed=embed)

  except Exception as e:
    return e


#setlevel
@bot.tree.command(name="uplevel", description="setlevel")
async def uplevel(Interaction, member: discord.Member, level: int):
  if not discord.utils.get(Interaction.user.roles, id=594761273200082955):
    await Interaction.channel.send("Bạn không có quyền sử dụng lệnh này.")
    return

  mentioned_user = member
  exp = 0
  c.execute("UPDATE users SET level=?, exp=? WHERE id=?",
            (level, exp, mentioned_user.id))
  conn.commit()

  await Interaction.response.send_message(
    f"Đã cập nhật level của {mentioned_user.mention} thành {level}.")
  new_nickname = f"[TT{level}] {mentioned_user.name}"
  try:
    await mentioned_user.edit(nick=new_nickname)
  except discord.Forbidden:
    return


current_time = datetime.now()
vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')


import keep_alive
keep_alive.keep_alive()


async def load():
  for filename in os.listdir('./cog'):
    if filename.endswith(".py"):
      await bot.load_extension(f'cog.{filename[:-3]}')


async def main():
  await load()
  await bot.start(os.environ['TOKEN'])


asyncio.run(main())
