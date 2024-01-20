import time
import discord
from discord.ext import commands
from discord import app_commands
import os

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      filename = os.path.basename(__file__)
      print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
      print('='* 50)

  
    @app_commands.command(name="ping",description="Trả về thời gian ping của bot",)
    async def ping(self, Interaction: commands.Context, p: str = None):
        if p is None:
            bot_ping = round(self.bot.latency * 1000)
            start_time = time.monotonic()
            await Interaction.response.send_message("Pinging...")
            end_time = time.monotonic()
            user_ping = round((end_time - start_time) * 1000)
            await Interaction.channel.send(f"Ping của bạn: {user_ping}ms | Ping của bot: {bot_ping}ms")
        else:
            role_id = 1087675803170525254
            if role_id in [role.id for role in Interaction.user.roles]:
                channel = Interaction.channel
                await channel.send(p)


async def setup(bot):
  await bot.add_cog(PingCog(bot))
