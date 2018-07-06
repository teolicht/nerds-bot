#!/usr/bin/env python3

from discord.ext import commands
import discord

import asyncio
import random


class Utilities():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete', aliases=['Delete', 'delete'.upper(), 'remove', 'clear', 'clean'])
    async def _delete(self, ctx, amount: int):
        if amount > 100:
            return await ctx.send(":x: I can delete max 100 messages.")
        elif amount <= 0:
            return await ctx.send(":x: How am I supposed to delete `{}` messages?**".format(amount))

        try:
            await ctx.message.delete()
            to_delete = []
            async for msg in ctx.channel.history(limit=amount):
                to_delete.append(msg)
            await ctx.channel.delete_messages(to_delete)

            if len(to_delete) != 1:
                delete_msg = ":recycle: `{}` messages deleted.".format(len(to_delete))
            else:
                delete_msg = ":recycle: `1` message deleted."
            await ctx.send(delete_msg, delete_after=4.0)

        except discord.errors.Forbidden:
            em = discord.Embed(
                title=':x: I can\'t delete messages in this channel...',
                description='''
Possible reasons:
⊳ I need the **Manage Messages** permission.
⊳ I need the **Read Message History** permission.''',
                color=discord.Colour.red())
            await ctx.send(embed=em)

    @commands.command(name='timer', aliases=['Timer', 'TIMER', 'clock'])
    async def _timer(self, ctx, secs: int):
        clocks = '🕛 🕐 🕑 🕒 🕓 🕔 🕕 🕖 🕗 🕘 🕙 🕚'.split()
        clock_index = 0
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        msg = await ctx.send("%02d:%02d:%02d 🕛" % (h, m, s))

        while secs != 0:
            secs -= 1
            clock_index += 1
            if clock_index == 12:
                clock_index = 0
            if secs == 0:
                await msg.edit(content="00:00:00 :white_check_mark:")
            else:
                m, s = divmod(secs, 60)
                h, m = divmod(m, 60)
                await msg.edit(content='%02d:%02d:%02d %s' % (h, m, s, clocks[clock_index]))
                await asyncio.sleep(1)

    @commands.command(name='calc', aliases=['Calc', 'CALC'])
    async def _calc(self, ctx, *, expr):
        expr = ''.join(expr)
        try:
            result = eval(expr)
            await ctx.send("`{}`".format(result))
        except:
            await ctx.send(":x: I couldn't calculate that, I'm sure it's your fault.")

    @commands.command(name='flip', aliases=['Flip', 'FLIP', 'coin'])
    async def _flip(self, ctx):
        side = random.choice(['heads', 'tails'])
        await ctx.send("I flipped a coin and it landed on **{}**.".format(side))

    @commands.command(name='randnum', aliases=['Randnum', 'RANDNUM', 'randum', 'random'])
    async def _randnum(self, ctx, min: int, max: int):
        try:
            number = random.randint(min, max)
        except ValueError:
            return await ctx.send(":warning: An error occurred. Make sure your first number is less than your second number.")
        await ctx.send("`{}`".format(min, max, number))

    @commands.command(name='choose', aliases=['Choose', 'CHOOSE', 'choice', 'chose'])
    async def _choose(self, ctx, *, choices):
        choices = choices.split()
        choice = random.choice(choices)
        return await ctx.send(choice)


def setup(bot):
    bot.add_cog(Utilities(bot))
