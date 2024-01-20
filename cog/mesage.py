import discord
from discord.ext import commands
import os
import sqlite3
import asyncio

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_records = {}
      
        self.conns = sqlite3.connect('templates/users.db')
        self.cursor = self.conns.cursor()
        
        # Create table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, name TEXT, exp INTEGER, level INTEGER, explevel INTEGER)'''
                  )
        self.conns.commit()

  
    @commands.Cog.listener()
    async def on_ready(self):
      filename = os.path.basename(__file__)
      print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
      print('='* 50)

  
    @commands.Cog.listener()
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
                await channel.send(
                    f"> chúc mừng {message.author.mention} đã lên level {new_level}! hãy tiếp tục tương tác và tận hưởng niềm vui trong guild thôi nào"
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
            if any(role.id == 1087675803170525254 for role in message.author.roles):
                return
            await message.delete()
            channel_inv = self.bot.get_channel(1108049138685329448)
            await channel_inv.send(f"{message.author.mention} đã gửi một liên kết mời máy chủ tại {message.channel.mention} và đã bị xóa.")
            await self.add_role_to_user(message.author)
    
    async def check_invite_link(self, content):
        if "discord.gg" in content:
            return True
        return False
    
    async def add_role_to_user(self, user):
        guild = user.guild
        role = discord.utils.get(guild.roles, id=1091731148025110609)
        await user.add_roles(role)


async def setup(bot):
  await bot.add_cog(Message(bot))