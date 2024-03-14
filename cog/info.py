import time
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import datetime
import sqlite3
import os 

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
        self.conn = sqlite3.connect('templates/users.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY, name TEXT, exp INTEGER, level INTEGER, explevel INTEGER)'''
                      )

    @app_commands.command(name="info", description="avatar và thông tin")
    async def stats(self, Interaction, member: discord.Member):
            mentioned_user = member
       
            embed = discord.Embed(color=discord.Color.dark_theme())
            author_name = f"{mentioned_user.name}#{Interaction.user.discriminator} \n{mentioned_user.display_name}"

            self.c.execute("SELECT exp, level, explevel FROM users WHERE id=?", (mentioned_user.id,))
            result = self.c.fetchone()
            if result is not None:
              exp, level, explevel = result
              if result is None:
                  embed.add_field(name="**bạn ko có level**", value="")
              else:
                  self.c.execute("SELECT COUNT(*) FROM users WHERE level > ?", (level,))
                  ranking = self.c.fetchone()[0] + 1
                  embed.add_field(name=f"**Bạn đang ở level:** {level} | **Ranking:** #{ranking}", value=f"**Exp:** {exp}/{explevel}")
            if mentioned_user.avatar is not None:
                avatar_user = f"{mentioned_user.avatar}"
                embed.set_author(name=author_name, icon_url=mentioned_user.avatar)
                embed.set_image(url=avatar_user)
            else:
              embed.set_author(name=author_name)
            start_time = time.monotonic()
            await Interaction.response.send_message("Pinging...", ephemeral=True)
            end_time = time.monotonic()
            user_ping = round((end_time - start_time) * 1000)

            member = Interaction.guild.get_member(mentioned_user.id)
            join_date = member.joined_at.replace(tzinfo=None)
            current_date = datetime.datetime.utcnow().replace(tzinfo=None)
            duration = current_date - join_date
            server_duration = duration.days

            now = datetime.datetime.now()
            new_time = now - datetime.timedelta(seconds=(duration.days + 1) * 24 * 60 * 60)
      
            embed.add_field(name=f"ping: {user_ping}ms \nĐã tham gia: <t:{int(new_time.timestamp())}:R> ``{server_duration} ngày``", value="", inline=False)

            await Interaction.channel.send(embed=embed)
   
async def setup(bot):
   await bot.add_cog(InfoCog(bot))
