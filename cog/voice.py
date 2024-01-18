import sqlite3
import discord
from discord.ext import commands
import os 

class VoiceChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conns = sqlite3.connect('templates/voice_channels.db')
        self.cursor = self.conns.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS voice_channels
                              (channel_id INTEGER PRIMARY KEY, owner_id INTEGER, parent_id INTEGER)''')
        self.conns.commit()

    @commands.Cog.listener()
    async def on_ready(self):
      filename = os.path.basename(__file__)
      print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
      print('='* 50)

  
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if after.channel and after.channel.id == 1107965775219789854:
                guild = member.guild
                category = after.channel.category

                new_channel = await guild.create_voice_channel(name=f"┕🍀{member.name}🍀┛", category=category)

                self.cursor.execute('INSERT INTO voice_channels (channel_id, owner_id, parent_id) VALUES (?, ?, ?)', (new_channel.id, member.id, category.id))
                self.conns.commit()

                await member.move_to(new_channel)

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

async def setup(bot):
   await bot.add_cog(VoiceChannelCog(bot))
