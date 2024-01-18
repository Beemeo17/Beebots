import discord
from discord.ext import commands
import os
import asyncio
import genshin

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)


# bot on
@bot.event
async def on_ready():
  print("DISCORD ON BOT!")
  await run_data()
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
    elif current_time.hour == 12 and current_time.minute == 15 :
      await dailys()
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
      
async def dailys(*cookies_data):
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


#===================================

async def run_data():
  client1 = genshin.Client(
    {
      "ltuid_v2": 139734936,
      "ltoken_v2":
      'v2_CAISDGM5b3FhcTNzM2d1OBokYWRmZDE3ZTMtMDc1Ny00ZTI2LTgxY2ItZDhhY2Y2MTYxNGY3IMfa96cGKL_NlzEwmN_QQg==',
      "ltmid_v2": '1kvjdm9qmp_hy',
      "cookie_token_v2":
      'v2_CAQSDGM5b3FhcTNzM2d1OBokYWRmZDE3ZTMtMDc1Ny00ZTI2LTgxY2ItZDhhY2Y2MTYxNGY3IMfa96cGKJbYt-EFMJjf0EI=',
      "account_mid_v2": '1kvjdm9qmp_hy',
      "account_id_v2": 139734936
    },
    lang="vi-vn")

  data1 = await client1.get_hoyolab_user()
  

  signed_ins1, claimed_rewardss1 = await client1.get_reward_info(game=genshin.types.Game.STARRAIL)

  signed_in1, claimed_rewards1 = await client1.get_reward_info(
    game=genshin.types.Game.GENSHIN)

  dailys1 = f'{data1.nickname}-GI<{signed_in1}•{claimed_rewards1}>+HSR<{signed_ins1}•{claimed_rewards1}>'

  client2 = genshin.Client(
    {
      "ltuid": 89595259,
      "ltoken": 'W26k5CAFSzoR5UHCXMNXBoLdgWahoe2VNIKEIsjb'
    },
    lang="vi-vn")

  data2 = await client2.get_hoyolab_user()
  
  signed_in2, claimed_rewards2 = await client2.get_reward_info(
    game=genshin.types.Game.GENSHIN)
 
  signed_ins2, claimed_rewardss2 = await client2.get_reward_info(
  game=genshin.types.Game.STARRAIL)

  dailys2 = f'{data2.nickname}-GI<{signed_in2}•{claimed_rewards2}>+HSR<{signed_ins2}•{claimed_rewards2}>'

  
  global start_time
  start_time = datetime.now()
  game = discord.Game(name=f"DAILY\n {dailys1} \n {dailys2}")
  await bot.change_presence(activity=game)
#===================================


import pytz
from datetime import datetime, time
current_time = datetime.now()
tz = pytz.timezone('Asia/Ho_Chi_Minh')


async def main():
  await bot.start(os.getenv ("TOKEN"))


asyncio.run(main())
