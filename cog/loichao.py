import discord 
from discord.ext import commands
from datetime import datetime, time
import os

class loichao(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  
  @commands.Cog.listener()
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

  @commands.Cog.listener()
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
   await bot.add_cog(loichao(bot))