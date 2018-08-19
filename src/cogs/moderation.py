#!/usr/bin/env python3

from discord.ext import commands
import discord
import asyncio
import datetime


muted_members = []
kick_cooldown_members = {}
ban_cooldown_members = {}
mute_cooldown_members = {}
chatmute_cooldown_members = {}
COMMAND_AGAIN = ":x: You can use this command again in `%dh%02dm%02ds`."

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author in kick_cooldown_members:
            m, s = divmod(kick_cooldown_members[ctx.author], 60)
            h, m = divmod(m, 60)
            return await ctx.send(COMMAND_AGAIN % (h, m, s))

        if member.id == 300761654411526154:
            return
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

            i = 18000
            while i != 0:
                kick_cooldown_members[ctx.author] = i
                await asyncio.sleep(1)
                i -= 1
            del kick_cooldown_members[ctx.author]

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
    async def ban(self, ctx, user: discord.User, *, reason=None):
        if ctx.author in ban_cooldown_members:
                m, s = divmod(ban_cooldown_members[ctx.author], 60)
                h, m = divmod(m, 60)
                return await ctx.send(COMMAND_AGAIN % (h, m, s))

        if user.id == 300761654411526154:
            return
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

            i = 43200
            while i != 0:
                ban_cooldown_members[ctx.author] = i
                await asyncio.sleep(1)
                i -= 1
            del ban_cooldown_members[ctx.author]

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
                return await ctx.send(":x: There are no banned users " +
                    "in this server.")

            user = await self.bot.get_user_info(userid)
            banned_users = []
            banned_users = [banned_users.append(ban.user) for ban in bans]

            if user not in banned_users:
                return await ctx.send(":x: `{}` isn't banned from ".format(
                    user) + "this server.")

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
            await ctx.send(embed=":x: I need the **Ban Members** permission")

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
                info = "**ID:** `{0.user.id}`\n**Reason:** {0.reason}".format(
                    ban)
                em.add_field(
                    name='{0}. `{1.user}`'.format(banned_amount, ban),
                    value='{}'.format(info),
                    inline=inline)
                banned_amount += 1
            await ctx.send(embed=em)

        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Ban Members** permission to " +
                "view the list of banned users.")

    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: int = None):
        if ctx.author in mute_cooldown_members:
                m, s = divmod(mute_cooldown_members[ctx.author], 60)
                h, m = divmod(m, 60)
                return await ctx.send(COMMAND_AGAIN % (h, m, s))

        try:
            if member.voice.mute:
                return await ctx.send(":x: That member is already muted.")
            # If member is or is not currently in a voice chat
            if member.voice or not member.voice:
                if duration is None:
                    await member.edit(mute=True)
                    await ctx.send(":white_check_mark: Muted `{0.name}`".format(
                        member))
                else:
                    if duration > 600:
                        return await ctx.send(":x: Max is 600 seconds (10 minutes).")
                    await member.edit(mute=True)
                    await ctx.send(":white_check_mark: Muted `{0.name}`".format(
                        member) + " for `{} sec(s)`".format(duration))
                    await asyncio.sleep(duration)
                    if member.voice.mute:
                        await member.edit(mute=False)
                        await ctx.send(":white_check_mark: " +
                            "Unmuted `{0.name}`".format(member))

            i = 3600
            while i != 0:
                mute_cooldown_members[ctx.author] = i
                await asyncio.sleep(1)
                i -= 1
            del mute_cooldown_members[ctx.author]

        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Mute Members** permission.".format(
                member))
        except AttributeError:
            await ctx.send(":x: That member isn't in a voice chat.")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if member.voice is None or member.voice.mute is False:
            return await ctx.send(":x: That member isn't even muted.")
        if member == ctx.author:
            return await ctx.send(":x: Sorry, you can't unmute yourself.")

        try:
            await member.edit(mute=False)
            await ctx.send(":white_check_mark: Unmuted `{0.name}`".format(
                member))

        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Mute Members** permission " +
                "to unmute {}.".format(mname(member)))

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def chatmute(self, ctx, member: discord.Member, duration: int = None):
        async def cooldown():
            i = 7200
            while i != 0:
                chatmute_cooldown_members[ctx.author] = i
                await asyncio.sleep(1)
                i -= 1
            del chatmute_cooldown_members[ctx.author]

        if member.id == 300761654411526154:
            return
        if ctx.author in chatmute_cooldown_members:
            m, s = divmod(chatmute_cooldown_members[ctx.author], 60)
            h, m = divmod(m, 60)
            return await ctx.send(COMMAND_AGAIN % (h, m, s))
        if member in muted_members:
            return await ctx.send(":x: That member is already chat-muted.")
        muted_members.append(member)
        if duration is None:
            await ctx.send(":white_check_mark: Chat-muted {0.name}".format(
                member))
            if not ctx.author.id == 300761654411526154:
                await cooldown()
        else:
            await ctx.send(":white_check_mark: Chat-muted " +
                "{0.name} for `{1}` minute(s).".format(member, duration))
            await cooldown()
            await asyncio.sleep(duration * 60)
            if member in muted_members:
                muted_members.remove(member)
                await ctx.send(":white_check_mark: {0.mention} is no ".format(
                    member) + "longer chat-muted.")

    @commands.command()
    async def unchatmute(self, ctx, member: discord.Member):
        if member not in muted_members:
            return await ctx.send(":x: That member isn't even chat-muted.")
        muted_members.remove(member)
        await ctx.send(":white_check_mark: {0.name} is no longer ".format(
            member) + "chat-muted.")


def setup(bot):
    bot.add_cog(Moderation(bot))
