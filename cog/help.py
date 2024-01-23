import discord
from discord import app_commands
from discord.ext import commands
import os 

class helps(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  
  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @app_commands.command(name="help", description="Lệch hỗ trợ")
  async def help(self, Interaction):
    async def button1_callback(interaction):
        await interaction.response.edit_message(embed=embed1)
        
    async def button2_callback(interaction):
        await interaction.response.edit_message(embed=embed2)
    
    async def button3_callback(interaction):
        await interaction.response.edit_message(embed=embed3)
  
  
    button1 = discord.ui.Button(label="", style=discord.ButtonStyle.green, emoji="◀️", custom_id="button1")
    button1.callback = button1_callback
  
    embed1 = discord.Embed(title="các lệnh hỗ trợ",
                        description="`các lệnh của bot`",
                        color=0x21c4b9)
    embed1.add_field(name="**/Ticket**", value="> Tạo Ticket", inline=False)
    embed1.add_field(name="**/info**",
                  value="> xem avatar và thông tin",
                  inline=False)
    embed1.add_field(name="**/ping**",
                  value="> trả về ping của bot ",
                  inline=False)
    embed1.add_field(name='**/login**', value='> lệnh input cookie', inline=False)
    embed1.add_field(name="**/hoyo**", value='> Các Cộng Cụ', inline=False)
    embed1.add_field(
    name="**/scuid**",
    value=
    "> khi sửa dụng lệnh và nhập uid của bạn vào bot, bot sẽ tim kiếm thông tin của uid và trả về kết quả ",
    inline=False)
  
  
    button2 = discord.ui.Button(label="", style=discord.ButtonStyle.green, emoji="▶", custom_id="button2")
    button2.callback = button2_callback
  
    embed2 = discord.Embed(title="các lệnh hỗ trợ" ,description="`các lệnh của bot`" , color=0x21c4b9)
    embed2.add_field(name="command prefix ``+``", value="", inline=False)
  
  
    button3 = discord.ui.Button(label="hướng dẫn", style=discord.ButtonStyle.green, custom_id="button3")
    button3.callback = button3_callback
  
    embed3 = discord.Embed(color=0x21c4b9)
    embed3.set_image(url=
    "https://cdn.discordapp.com/attachments/1107978903294853140/1110924003134165072/Khong_Co_Tieu_e45_20230511160103.png"
  )
  
    button4 = discord.ui.Button(label="support", url="https://discord.gg/NjG3MDUJc4")
  
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
  
    await Interaction.response.send_message(embed=embed1, view=view)

async def setup(bot):
   await bot.add_cog(helps(bot))
