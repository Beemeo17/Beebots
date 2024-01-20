import discord 
from discord.ext import commands
import os

class addemojirole(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
      message_id = payload.message_id
      if message_id == 1102870362443743242:
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
          if payload.emoji.name == 'coop_beebot':
              role = guild.get_role(1102868806348574730)
              member = guild.get_member(payload.user_id)
              await member.add_roles(role)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
      message_id = payload.message_id
      if message_id == 1102870362443743242:
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
          if payload.emoji.name == 'coop_beebot':
              role = guild.get_role(1102868806348574730)
              member = guild.get_member(payload.user_id)
              await member.remove_roles(role)


async def setup(bot):
  await bot.add_cog(addemojirole(bot))