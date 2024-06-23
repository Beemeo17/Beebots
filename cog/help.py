import discord
from discord.ext import commands
from discord import app_commands
    
class help(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @app_commands.command(name="help", description="Lệnh hỗ trợ")
  async def help(self, I: discord.Interaction):
    await I.response.send_message(embed=await slash_command(self, self.bot), view=Button(self.bot))

async def commands(self, bot):
    embed = discord.Embed(title="Các lệnh hiện có")
    embed.set_thumbnail(url=bot.user.avatar)
    for command in bot.commands:
      embed.add_field(name=f"``{command.name}``", value="", inline=False)
    embed.set_footer(text="prefix: ``+``")
    return embed

async def slash_command(self, bot):
  embed = discord.Embed(title="Các lệnh hiện có")
  embed.set_thumbnail(url=bot.user.avatar)
  command = await bot.tree.fetch_commands()
  for cmd in command:
    embed.add_field(name=f"</{cmd.name}:{cmd.id}> des: ``{cmd.description}``", value="", inline=False)
  embed.set_footer(text=f"prefix: ``+``")
  return embed

conut = True
class Button(discord.ui.View):
    def __init__ (self, bot):
      super().__init__()
      self.bot = bot
    
    @discord.ui.button(label="", emoji="🔁")
    async def button(self, I: discord.Interaction, button: discord.ui.Button,):
      global conut
      conut = not conut
      if conut:
        await I.response.edit_message(embed=await slash_command(self, self.bot))
      else:
        await I.response.edit_message(embed=await commands(self, self.bot))

async def setup(bot):
  await bot.add_cog(help(bot))
