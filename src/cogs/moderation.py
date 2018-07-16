#!/usr/bin/env python3

from discord.ext import commands
import discord

import asyncio
import datetime


class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('👑', '👑👑', '👑👑👑')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason:
                reason = ''.join(reason)
                await ctx.guild.kick(member, reason=reason)
            else:
                reason = 'None'
                await ctx.guild.kick(member)

            em = discord.Embed(
                title=':warning: Member kicked:',
                description=member.mention,
                color=discord.Colour.green())
            em.set_thumbnail(url=member.avatar_url)
            em.set_footer(text='Reason: ' + reason)
            await ctx.send(embed=em)

        except discord.errors.Forbidden:
            em = discord.Embed(
                title=':x: I can\'t kick `{}`'.format(member),
                description='''
Here are the possible reasons:
⊳ I can't kick anyone with the same or higher role as me.
⊳ I can't kick the server owner.
⊳ I need the **Kick Members** permission.''',
                color=discord.Colour.red())
            await ctx.send(embed=em)

    @commands.command()
    @commands.has_any_role('👑👑', '👑👑👑')
    async def ban(self, ctx, user: discord.User, *, reason=None):
        try:
            bans = await ctx.guild.bans()
            for ban in bans:
                if ban.user == user:
                    return await ctx.send(":x: `{}` is already banned.".format(
                        user))

            if reason:
                reason = ''.join(reason)
                await ctx.guild.ban(
                    user=user,
                    reason=reason,
                    delete_message_days=0)
            else:
                reason = 'None'
                await ctx.guild.ban(
                    user=user,
                    delete_message_days=0)

            em = discord.Embed(
                title=':warning: User banned:',
                description=user.mention,
                color=discord.Colour.green())
            em.set_thumbnail(url=user.avatar_url)
            em.set_footer(text='Reason: ' + reason)
            await ctx.send(embed=em)

        except discord.errors.Forbidden:
            em = discord.Embed(
                title=':x: I can\'t ban `{}`'.format(user),
                description='''
Possible reasons:
⊳ I can't ban anyone with a higher or same role as me.
⊳ I can't ban the server owner.
⊳ I need the **Ban Members** permission.''',
                color=discord.Colour.red())
            await ctx.send(embed=em)

    @commands.command()
    async def unban(self, ctx, userid: int, *, reason=None):
        try:
            bans = await ctx.guild.bans()
            if not bans:
                return await ctx.send(":x: **There are no banned users " +
                    "in this server.")

            user = await self.bot.get_user_info(userid)
            banned_users = []
            for ban in bans:
                banned_users.append(ban.user)
            if user not in banned_users:
                return await ctx.send(":x: `{}` isn't banned from this server.")

            if reason is None:
                reason = 'None'
                await ctx.guild.unban(user)

            else:
                reason = ''.join(reason)
                await ctx.guild.unban(user, reason=reason)

            em = discord.Embed(
                title=':white_check_mark: User unbanned:',
                description=user.mention,
                color=discord.Colour.green())
            em.set_thumbnail(url=user.avatar_url)
            em.set_footer(text='Reason: ' + reason)
            await ctx.send(embed=em)

        except discord.errors.Forbidden:
            em = discord.Embed(
                title='I can\'t unban `{}`'.format(user),
                description='''
Possible reason:
⊳ I need the **Ban Members** permission.
''',
                color=discord.Colour.red())
            await ctx.send(embed=em)

    @commands.command()
    async def bans(self, ctx):
        try:
            bans = await ctx.guild.bans()
            if not bans:
                return await ctx.send(":x: There are no banned users in " +
                    "this server.")

            banned_amount = 1
            if banned_amount % 2 != 0:
                inline = False
            else:
                inline = True

            em = discord.Embed(title='Banned users')
            em.set_author(name=ctx.guild.name)
            em.set_thumbnail(url=ctx.guild.icon_url)
            for ban in bans:
                id_reason = "**ID:** `{0.user.id}`\n" +
                    "**Reason:** {0.reason}".format(ban)
                em.add_field(
                    name='{0}. `{1.user}`'.format(banned_amount, ban),
                    value='{}\n{}'.format(id_reason, '━' * 12),
                    inline=inline)
                banned_amount += 1
            await ctx.send(embed=em)

        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Ban Members** permission to " +
                "view the list of banned users.")

    @commands.command()
    @commands.has_any_role('⭐⭐⭐', '👑', '👑👑', '👑👑👑')
    async def mute(self, ctx, member: discord.Member, duration: int = None):
        if member.voice.mute is True:
            return await ctx.send(":x: That member is already muted.")

        try:
            if duration is None:
                await member.edit(mute=True)
                await ctx.send(":white_check_mark: Muted `{0.name}`")
            else:
                await member.edit(mute=True)
                await ctx.send(":white_check_mark: Muted `{0.name}` for " +
                    "`{1} sec(s)`".format(member, duration))
                await asyncio.sleep(duration)
                if member.voice.mute:
                    await member.edit(mute=False)
                    await ctx.send(":white_check_mark: " +
                        "Unmuted `{0.name}`".format(member))
        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Mute Members** permission.".format(
                member))

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if member.voice.mute is False:
            return await ctx.send(":x: That member isn't even muted.")
        if member == ctx.author:
            return await ctx.send(":x: Sorry, you can't unmute yourself.")

        try:
            await member.edit(mute=False)
            await ctx.send(":white_check_mark: Unmuted `{0.name}`".format(
                member))

        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Mute Members** permission " +
                "to unmute {0.name}.".format(member))


def setup(bot):
    bot.add_cog(Moderation(bot))
