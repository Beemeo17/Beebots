import discord
from discord.ext import commands, tasks
import os
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

# bot on
@bot.event
async def on_ready():
  try:
    synced = await bot.tree.sync()
    print(f"[OK] {bot.user.name}#{bot.user.discriminator} - Connect {len(synced)} SLASH COMMANDS")
    print('=' * 50)
  except Exception as e:
    print(e)

import keep_alive
keep_alive.keep_alive()
async def load():
  for filename in os.listdir('./cog'):
    if filename.endswith(".py"):
      await bot.load_extension(f'cog.{filename[:-3]}')
async def main():
  await load()
  await bot.start(os.environ['TOKEN'])
  
asyncio.run(main())
