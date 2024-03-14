import discord
from discord.ext import commands
from discord import app_commands
    
class help(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @app_commands.command(name="help", description="Lệnh hỗ trợ")
  async def help(self, I: discord.Interaction):
    embed = discord.Embed(title="Các lệnh hiện có")
    embed.set_thumbnail(url=self.bot.user.avatar)
    command = await self.bot.tree.fetch_commands()
    for cmd in command:
      embed.add_field(name=f"</{cmd.name}:{cmd.id}> des: ``{cmd.description}``", value="", inline=False)
    embed.set_footer(text="prefix: ``+``")
    await I.response.send_message(embed=embed)

async def setup(bot):
  await bot.add_cog(help(bot))
