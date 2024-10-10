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

async def daily_on(self, channel, channel2):
        cookie_message = await channel.fetch_message(1293633954942812253)
        cookie_data = json.loads(cookie_message.content.strip())
        client = genshin.Client()
        client.set_cookies({
            "cookie_token_v2": cookie_data["cookie_token_v2"],
            "account_mid_v2": cookie_data["account_mid_v2"],
            "account_id_v2": cookie_data["account_id_v2"],
            "ltoken_v2": cookie_data["ltoken_v2"],
            "ltmid_v2": cookie_data["ltmid_v2"],
            "ltuid_v2": cookie_data["ltuid_v2"],
        })
        gamep = [
            genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL,
            genshin.types.Game.HONKAI,]
        embed = discord.Embed()
        for games in gamep[:3]:
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
            await channel2.send(embed=embed)


async def get_cookie(channel):
    data = load_data()
    for key, value in data.items():
        if value.get("daily_auto"):
          gamep = [
            genshin.types.Game.GENSHIN, genshin.types.Game.STARRAIL,
            genshin.types.Game.HONKAI,]
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

class Cog_main(commands.Cog):
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
      self.update_presence.start()
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
            await self.check_invite_and_add_role(message)
            await self.process_spam_detection(message)
  
  async def process_leveling(self, message):
      if message.author.bot == self.bot.user:
          return
      self.cursor.execute("SELECT exp, level FROM users WHERE id=?", (message.author.id, ))
      result = self.cursor.fetchone()
  
      if result is None:
          self.cursor.execute("INSERT INTO users (id, name, exp, level) VALUES (?, ?, ?, ?)",
                    (message.author.id, message.author.name, 1, 1))
          self.conns.commit()
      else:
          exp, level = result
          explevel = result
          exp += 1
          new_level = int(exp // ((level * 2) + level)) + 1
          nextlevel = (int(exp // (((level + 1) * 2) + (new_level))) + 1)
          explevel = int(((level + 1) * 2) + (level + 1)) * (nextlevel + 1)
          if new_level > level:
              exp = exp - exp
              self.cursor.execute("UPDATE users SET level=?, exp=?, explevel=? WHERE id=?",
                        (new_level, exp, explevel, message.author.id))
              self.conns.commit()
  
              channel = self.bot.get_channel(int(1092392066417430538))
              await message.channel.send(
                  f"> chúc mừng {message.author.mention} đã lên level {new_level}! hãy tiếp tục tương tác để lên nhưng cấp cao hơn nào:3"
              )
              # Change user nickname
          self.cursor.execute("UPDATE users SET exp=? WHERE id=?", (exp, message.author.id))
          self.conns.commit()
  
      # add role từ level
      try:
          level = result[1]
          guild = message.guild
          if level >= 5:
              role = discord.utils.get(guild.roles, id=1091749838749696095)
              await message.author.add_roles(role)
          if level >= 10:
              role = discord.utils.get(guild.roles, id=1091752849635016724)
              await message.author.add_roles(role)
          if level >= 20:
              role = discord.utils.get(guild.roles, id=1091752767510548692)
              await message.author.add_roles(role)
          if level >= 30:
              role = discord.utils.get(guild.roles, id=1091753182583083188)
              await message.author.add_roles(role)
          if level >= 40:
              role = discord.utils.get(guild.roles, id=1091752917905719316)
              await message.author.add_roles(role)
          if level >= 50:
              role = discord.utils.get(guild.roles, id=1091752954970775613)
              await message.author.add_roles(role)
          if level >= 60:
              role = discord.utils.get(guild.roles, id=1091753084016939080)
              await message.author.add_roles(role)
          if level >= 70:
              role = discord.utils.get(guild.roles, id=1091753014567641238)
              await message.author.add_roles(role)
      except Exception as a:
          return a
  
  async def process_spam_detection(self, message):
      if message.guild and message.guild.id == 550601755709407233:
          guild = self.bot.get_guild(550601755709407233)
          member = guild.get_member(message.author.id)
          if message.channel.id == 1102490528613937212 or message.channel.id == 1116014367058706493:
              return
          if message.author.bot:
              return
  
          author_id = message.author.id
          self.spam_records.setdefault(author_id, {"count1": 0, "spam_role_mentioned": False})
          spam_info = self.spam_records[author_id]
          # 1
          if len(message.content) <= 6:
              spam_info["count1"] += 1
  
              if spam_info["count1"] >= 13 and not spam_info["spam_role_mentioned"]:
                  try:
                      role = discord.utils.get(message.guild.roles, id=1091731148025110609)
                      await message.author.add_roles(role)
                      await message.channel.send(f"{message.author.mention} đang spam, bạn đã bị mute")
                      spam_info["spam_role_mentioned"] = True
  
                      await asyncio.sleep(180)
                      await message.author.remove_roles(role)
                      await message.channel.send(f"{message.author.mention} đã được mở hạn chế!")
                      self.spam_records.pop(author_id)
                  except Exception as sp1:
                      print("id spam", sp1)
                      return sp1
          # 2
          spam_info.setdefault("count2", 0)
          spam_info.setdefault("spam_mentioned", False)
  
          async for m in message.channel.history(limit=13, before=message):
              if m.author == message.author and m.content == message.content:
                  spam_info["count2"] += 1
  
          if spam_info["count2"] >= 13 and not spam_info["spam_mentioned"]:
              try:
                  role = discord.utils.get(message.guild.roles, id=1091731148025110609)
                  await message.author.add_roles(role)
                  await message.channel.send(f"{message.author.mention} đang spam, bạn đã bị mute")
                  spam_info["spam_mentioned"] = True
  
                  await asyncio.sleep(180)
                  await message.author.remove_roles(role)
                  await message.channel.send(f"{message.author.mention} đã được mở hạn chế!")
                  self.spam_records.pop(author_id)
              except Exception as sp2:
                  print("id spam", sp2)
                  return sp2
  
          await asyncio.sleep(30)
          if author_id in self.spam_records:
              self.spam_records.pop(author_id)
  
  async def check_invite_and_add_role(self, message):
      invite_link = await self.check_invite_link(message.content)
      if invite_link:
          if message.author.guild_permissions.manage_guild or message.author.id == message.guild.owner_id:
              return
          await message.delete()
          channel_inv = self.bot.get_channel(1108049138685329448)
          await message.channel.send(f"{message.author.mention} đã gửi một liên kết mời máy chủ tại {message.channel.mention} và đã bị xóa.")
          await self.add_role_to_user(message.author)
  
  async def check_invite_link(self, content):
      if "discord.gg" in content:
          return True
      return False
  
  async def add_role_to_user(self, user):
    guild = user.guild
    MuteRole = discord.utils.get(guild.roles, name='Muted')
    if not MuteRole:
        MuteRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(MuteRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
    reason = "Gửi link **__invite__** \n Chúng tôi sẽ xem xét và xử lý bạn!"
    await user.add_roles(MuteRole, reason=reason)
    await user.send(f"Bạn đã bị muted trong server **{guild.name}** | Reason: **{reason}**")

  @tasks.loop(seconds=60) #view gem
  async def update_presence(self):
      global start_time
      start_time = datetime.now()
      game = discord.Game(name="❄️HIVE Teyvat❄️")
      await self.bot.change_presence(activity=game)

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

  @commands.command(help="stats bot")
  async def stats(self, ctx):
    global ts, tm, th, td
    embed = discord.Embed(title="bot stats")
    embed.add_field(name=f"<a:blobdj:1153569751201759232> {td}d:{th}h:{tm}m:{ts}s", value="", inline=False)
    embed.add_field(name=f"<:emoji_45:1217819246978138153> CPU: {psutil.cpu_percent()}%", value="", inline=True)
    embed.add_field(name=f"<:emoji_44:1217819116325568692> RAM: {psutil.virtual_memory()[2]}%", value="", inline=True)
    await ctx.send(embed=embed)
    
  @tasks.loop(seconds=60) #on time
  async def send_greetings(self):
      current_time = datetime.now(self.tz).time()
      channel = self.bot.get_channel(699305290289381477)
      if current_time.hour == 7 and current_time.minute == 0:
          await channel.send("chúc mọi người một ngày mới vui vẻ 🧩**Good Morning**🧩")
      elif  current_time.hour == 22 and current_time.minute == 0:
          await channel.send("chúc mọi người ngủ ngon 💤**Good Night**💤")
      elif current_time.hour == 23 and current_time.minute == 7:
            channels = self.bot.get_channel(1156104339291635758)
            await get_cookie(channels)
            channelr = self.bot.get_channel(1100282433963831366)
            await daily_on(self, channelr, channels)

  @tasks.loop(seconds=10) #top info
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
          self.cursor.execute("SELECT name, level, exp FROM users ORDER BY level DESC, exp DESC LIMIT 3")
          results = self.cursor.fetchall()
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
  
  @commands.Cog.listener() #voie
  async def on_voice_state_update(self, member, before, after):
    if before.channel != after.channel:
        if after.channel and after.channel.id == 1107965775219789854:
            guild = member.guild
            category = after.channel.category

            new_channel = await guild.create_voice_channel(name=f"┕🍀{member.name}🍀┛", category=category, user_limit=10)

            self.cursor.execute('INSERT INTO voice_channels (channel_id, owner_id, parent_id) VALUES (?, ?, ?)', (new_channel.id, member.id, category.id))
            self.conns.commit()

            await member.move_to(new_channel)


            embed = discord.Embed(
                title="Quản lý channel Voice",
                description=f"Voice channel của {member.mention} đã được tạo.",
                color=discord.Color.blue()
            )
            
            # Tạo các button
            class mobdul(discord.ui.Modal, title="Sửa giới hạn người có thể tham gia"):
                member = discord.ui.TextInput(label="limit_member")
                async def on_submit(self, interaction):
                    try:
                        new_limit = int(self.member.value)
                        await interaction.channel.edit(user_limit=new_limit)
                        await interaction.response.send_message(f"Giới hạn người dùng được chỉnh thành {new_limit}.")
                    except (ValueError, TimeoutError):
                        await interaction.response.send_message("lỗi đầu vào hoặc timeout.")

            class VoiceChannelView(discord.ui.View):
                def __init__(self, bot, channel, owner_id, timeout=None):
                    super().__init__(timeout=timeout)
                    self.bot = bot
                    self.channel = channel
                    self.owner_id = owner_id

                @discord.ui.button(label="User limit", style=discord.ButtonStyle.primary)
                async def adjust_user_limit(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id != self.owner_id:
                        await interaction.response.send_message("Bạn không phải chủ voice.", ephemeral=True)
                        return

                    await interaction.response.send_modal(mobdul())


                @discord.ui.button(label="quyền kênh", style=discord.ButtonStyle.secondary)
                async def adjust_privacy(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id != self.owner_id:
                        await interaction.response.send_message("Bạn không phải chủ voice.", ephemeral=True)
                        return

                    overwrites = self.channel.overwrites
                    if member.guild.default_role in overwrites and overwrites[member.guild.default_role].connect is False:
                        overwrites[member.guild.default_role] = discord.PermissionOverwrite(connect=True)
                        await self.channel.edit(overwrites=overwrites)
                        await interaction.response.send_message("Channel is now public.")
                    else:
                        overwrites[member.guild.default_role] = discord.PermissionOverwrite(connect=False)
                        await self.channel.edit(overwrites=overwrites)
                        await interaction.response.send_message("Channel is now private.")


                @discord.ui.button(label="", emoji="🛗", style=discord.ButtonStyle.success)
                async def allow_user(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id != self.owner_id:
                        await interaction.response.send_message("Bạn không phải chủ voice.", ephemeral=True)
                        return

                    await interaction.response.send_message("Vui lòng mention người dùng bạn muốn cấp quyền truy cập voice!")

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', check=check, timeout=30)
                        allowed_user = msg.mentions[0]
                        overwrites = self.channel.overwrites
                        overwrites[allowed_user] = discord.PermissionOverwrite(connect=True)
                        await self.channel.edit(overwrites=overwrites)
                        await interaction.followup.send(f"{allowed_user.mention} đã có thể tuy cập voice này.")
                    except (IndexError, TimeoutError):
                        await interaction.followup.send("Lỗi hoặc timeout.")

                @discord.ui.button(label="", emoji="🚷", style=discord.ButtonStyle.danger)
                async def disconnect_user(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if interaction.user.id != self.owner_id:
                        await interaction.response.send_message("Bạn không phải chủ voice.", ephemeral=True)
                        return

                    await interaction.response.send_message("Vui lòng mention người dùng bạn muốn đuổi khỏi voice!")

                    def check(m):
                        return m.author == interaction.user and m.channel == interaction.channel

                    try:
                        msg = await self.bot.wait_for('message', check=check, timeout=30)
                        user_to_disconnect = msg.mentions[0]
                        member = interaction.guild.get_member(user_to_disconnect.id)
                        if member and member.voice and member.voice.channel == self.channel:
                            await member.move_to(None)
                            await interaction.followup.send(f"{user_to_disconnect.mention} đã bị đuổi khỏi voice này.")
                        else:
                            await interaction.followup.send("Người dùng mention không có trong voice này!")
                    except (IndexError, TimeoutError):
                        await interaction.followup.send("Lỗi hoặc timeout.")

            view = VoiceChannelView(self.bot, new_channel, member.id)
            await new_channel.send(embed=embed, view=view)

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

  @commands.Cog.listener() #add role emoji
  async def on_raw_reaction_add(self, payload):
      message_id = payload.message_id
      if message_id == 1102870362443743242:
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
          if payload.emoji.name == 'coop_beebot':
              role = guild.get_role(1102868806348574730)
              member = guild.get_member(payload.user_id)
              await member.add_roles(role)

  @commands.Cog.listener() #xoa role emoji
  async def on_raw_reaction_remove(self, payload):
      message_id = payload.message_id
      if message_id == 1102870362443743242:
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
          if payload.emoji.name == 'coop_beebot':
              role = guild.get_role(1102868806348574730)
              member = guild.get_member(payload.user_id)
              await member.remove_roles(role)

  @commands.Cog.listener() #loi chao
  async def on_member_join(self, user):
    if user.guild.id == 550601755709407233:
      embed = discord.Embed()
      luat_channel = self.bot.get_channel(898419988396920852)
      thongbao_channel = self.bot.get_channel(1091019454894325760)
      phongtra_channel = self.bot.get_channel(699305290289381477)
      role_channel = self.bot.get_channel(1091755587462758530)
      tongquan_channel = self.bot.get_channel(1089797118178377768)
      embed = discord.Embed(color=0xc8ed0c)
      embed.add_field(name="", value='> chào mừng bạn đến với server')
      embed.set_thumbnail(url=user.avatar)
      embed.add_field(
        name=f"🍁 {luat_channel.mention} hãy bỏ chút thời gian đọc nó",
        value="",
        inline=False)
      embed.add_field(name=f"🍁 {tongquan_channel.mention} Room diễn đàn",value="",inline=False)
      embed.add_field(name=f"🍁 {thongbao_channel.mention} thông báo của server",
                      value="",
                      inline=False)
      embed.add_field(
        name=f"🍁 {phongtra_channel.mention} Room chat sinh hoạt chung",
        value="",
        inline=False)
      embed.add_field(
        name=f"🍁 {role_channel.mention} Room chi tiết về các role trong server",
        value="",
        inline=False)
      embed.set_image(url="https://images.alphacoders.com/113/1131281.jpg")
      embed.add_field(name="> chúc bạn sẽ có những giây phút tuyệt vời với server",
                      value="",
                      inline=False)
      channel_welcome = self.bot.get_channel(869833896030793828)
      channel_pcha = self.bot.get_channel(699305290289381477)
      await channel_welcome.send(f"xin chào {user.mention}", embed=embed)
      await channel_pcha.send(f"hello {user.mention}, hãy cùng trò chuyện với mọi người ở đây nào")

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
      await channel.send(f"tạm biệt {user.mention}", embed=embed)

  
async def setup(bot):
   await bot.add_cog(Cog_main(bot))
