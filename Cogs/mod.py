import discord
from discord.ext import commands


class Mod(commands.Cog):
    """Commands for moderators in a guild."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """Kick a member from the guild"""
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'Done. {user.name} was kicked.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """Ban a member from the guild"""
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'Done. {user.name} was banned.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, name_or_id, *, reason=None):
        """Unban a member from the guild"""
        ban = await ctx.get_ban(name_or_id)
        if not ban:
            return await ctx.send('No user found.')
        await ctx.guild.unban(ban.user, reason=reason)
        await ctx.send(f'Unbanned *{ban.user}* from the server.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a members and deletes their messages."""
        await member.ban(reason=f'Softban - {reason}')
        await member.unban(reason='Softban unban.')
        await ctx.send(f'Done. {member.name} was softbanned.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        """Warn a member via DMs"""
        warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}** for {reason}'
        if not reason:
            warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}**'
        try:
            await user.send(warning)
        except discord.Forbidden:
            return await ctx.send('The user has disabled DMs for this guild or blocked the bot.')
        await ctx.send(f'**{user}** has been **warned**')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        """Delete messages a certain number of messages from a channel."""
        if messages > 99:
            messages = 99
        await ctx.channel.purge(limit=messages + 1)
        await ctx.send(f'{messages} messages deleted.', delete_after=3)


def setup(bot):
    bot.add_cog(Mod(bot))
