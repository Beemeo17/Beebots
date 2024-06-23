import time
import discord
from discord.ext import commands
import os

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        if (not ctx.author.guild_permissions.manage_guild):
            await ctx.send("Bạn không có quyền sửa dụng lệnh này")
            return
        guild = ctx.guild
        MuteRole = discord.utils.get(guild.roles, name='Muted')

        if not MuteRole:
            MuteRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(MuteRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
        await member.add_roles(MuteRole, reason=reason)
        await ctx.send(f"đã muted {member.mention}")
        await member.send(f"Bạn đã bị muted trong server **{guild.name}** | Reason: **{reason}**")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if (not ctx.author.guild_permissions.manage_guild):
            await ctx.send("Bạn không có quyền sửa dụng lệnh này")
            return
        guild = ctx.guild
        MuteRole = discord.utils.get(member.roles, name='Muted')

        if not MuteRole:
            await ctx.send(f"{member.nickname} hiện không bị muted!")
        await member.remove_roles(MuteRole)
        await ctx.send(f"đã gỡ muted {member.mention}")
        await member.send(f"Bạn đã được gỡ muted trong server **{guild.name}**")

    @commands.command(help="ping lệnh bot") #id tree commands
    async def IDs(self, ctx, name):
        commands = await self.bot.tree.fetch_commands()
        for cmd in commands:
            if cmd.name == name:
                await ctx.send(f"</{name}:{cmd.id}> --> `{cmd.description}`")


async def setup(bot):
  await bot.add_cog(Commands(bot))
