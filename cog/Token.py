import discord
from discord import app_commands
from discord.ext import commands
import os

class Button(discord.ui.View):
  def __init__(self):
    super().__init__()

  @discord.ui.button(label="TICKET", style= discord.ButtonStyle.green)
  async def click(self, Interaction: discord.Interaction, button: discord.ui.Button,):
        category = discord.utils.get(Interaction.guild.categories, name="TICKET")
        overwrites = {
            Interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        if category is None:
            category = await Interaction.guild.create_category("TICKET", overwrites=overwrites)
        channel = await category.create_text_channel(name=f"{Interaction.user.name}-Tickets", overwrites=overwrites)
        await channel.send(f"Chào mừng bạn, {Interaction.user.mention}! Hãy tham gia cuộc trò chuyện riêng của bạn.")
        await Interaction.response.send_message(f"Tạo ticket thành công! \n Hãy bắt đầu cuộc trò chuyện với kênh: {channel.mention}", ephemeral=True)
    

class token(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    super().__init__()

  @app_commands.command(name="ticket", description="Tạo Ticket")
  async def token(self, Interaction):
    embed = discord.Embed(colour=0x3a160e)
    embed.set_author(name="Tạo Ticket", icon_url="https://discord.com/assets/7d3e3949b8fafe2ebed318974f1ece8b.svg")
    embed.set_image(url="https://media.discordapp.net/attachments/1114095095210311680/1156102323957940285/AZlgvgi.png")
    await Interaction.response.send_message(embed=embed, view=Button())

  
  @commands.command()
  async def ticket(self, ctx):
    embed = discord.Embed(colour=0x3a160e)
    embed.set_author(name="Tạo Ticket", icon_url="https://discord.com/assets/7d3e3949b8fafe2ebed318974f1ece8b.svg")
    embed.set_image(url="https://media.discordapp.net/attachments/1114095095210311680/1156102323957940285/AZlgvgi.png")
    await ctx.send(embed=embed, view=Button())




async def setup(bot):
  await bot.add_cog(token(bot))
