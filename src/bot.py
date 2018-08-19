#!/usr/bin/env python3

from discord.ext import commands
import discord
import time
import traceback
import sys
import random
import asyncio
import datetime
import logging
import psutil
import os
from cogs.config import botoken
from cogs.emojis import Emoji
from cogs.nerds import nerds
from cogs.moderation import muted_members

description = "A Discord bot written by Lanit#3333."
prefix = ('n!', 'N!')

initial_extensions = [
    'cogs.handler',
    'cogs.invites',
    'cogs.information',
    'cogs.pictures',
    'cogs.fun',
    'cogs.moderation',
    'cogs.utilities',
    'cogs.reddit']

bot = commands.Bot(
    description=description,
    command_prefix=prefix)
bot.remove_command('help')
bot.launch_time = datetime.datetime.utcnow()

# async def change_status():
#     await bot.wait_until_ready()
#
#     statuses = ['oof', 'blyat', 'cyka', 'cyunt', 'sussu', 'gey', 'ur mom gey',
#                 'jeff', 'GRRRRRRRRRRRRRRRRRRRRR', 'ecksdee', 'heck',
#                 'm\'lady', 'it is {} my dudes AAAAAAAAAAAAAAAAA'.format(
#                     datetime.datetime.now().strftime('%A').lower()),
#                 'hipócritas', '2+2=4-1=3 quick maths', 'bazinga', 'hella gay']
#     status_option = random.choice(statuses)
#
#     while True:
#         status_text = 'n!help • ' + status_option
#         status = discord.Game(status_text)
#         await bot.change_presence(activity=status)
#         await asyncio.sleep(30)-

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await bot.change_presence(activity=discord.Game('n!help'))

@bot.event
async def on_message(message):
    if message.guild is not None:
        if message.author in muted_members:
            return await message.delete()
        if message.channel.name == 'music':
            DJ_cmds = ['play', 'disconnect', 'np', 'aliases', 'ping', 'skip',
             'seek', 'soundcloud', 'remove', 'loopqueue', 'search', 'stats',
             'loop', 'donate', 'shard', 'join', 'lyrics', 'info', 'resume',
             'settings', 'move', 'forward', 'skipto', 'clear', 'replay',
             'clean', 'pause', 'removedupes', 'volume', 'rewind', 'playtop',
             'playskip', 'invite', 'shuffle', 'queue', 'leavecleanup']
            if message.content[1:] not in DJ_cmds:
                if message.author.id not in [235088799074484224,
                                             252128902418268161]:
                    await message.delete()
        await bot.process_commands(message)
    else:
        return

@bot.command(name='ping', aliases=['Ping', 'PING', 'latency'])
async def _ping(ctx):
    def color(r, g, b):
        return discord.Colour.from_rgb(r, g, b)

    t_1 = time.perf_counter()
    await ctx.trigger_typing()
    t_2 = time.perf_counter()

    ping = round((t_2 - t_1) * 1000)
    if ping <= 100:
        color = color(0, 211, 14)
    elif ping <= 170:
        color = color(106, 255, 0)
    elif ping <= 230:
        color = color(195, 255, 0)
    elif ping <= 270:
        color = color(255, 255, 0)
    elif ping <= 340:
        color = color(255, 212, 0)
    elif ping <= 400:
        color = color(255, 174, 0)
    elif ping <= 500:
        color = color(255, 127, 0)
    elif ping <= 650:
        color = color(255, 72, 0)
    elif ping <= 850:
        color = color(255, 0, 0)
    else:
        color = color(211, 0, 0)

    em = discord.Embed(
        title='🏓 Pong!',
        description='*{}ms*'.format(ping),
        color=color)
    await ctx.send(embed=em)

@bot.command()
async def info(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    h, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    m, s = divmod(remainder, 60)
    d, h = divmod(h, 24)
    major, minor, micro = sys.version_info[:3]

    memory_usage = psutil.Process().memory_full_info().uss / 1024**2
    cpu_usage = psutil.cpu_percent()

    cmd = r'git show -s HEAD~3..HEAD --format="[{}](https://github.com/teolicht/nerds-bot/commit/%H) %s (%cr)"'
    if os.name == 'posix':
        cmd = cmd.format(r'\`%h\`')
    else:
        cmd = cmd.format(r'`%h`')

    try:
        revision = os.popen(cmd).read().strip()
    except OSError:
        revision = "Could not fetch due to memory error."
    print(cmd); print('-----------------'); print(revision)
    em = discord.Embed(description='Latest changes:\n' + revision,
                       color=0xffc700)
    em.set_author(
        name='Nerds Bot',
        icon_url=bot.user.avatar_url)
    em.add_field(
        name='Language',
        value=f'Python {major}.{minor}.{micro}')
    em.add_field(
        name='API',
        value='discord.py {}'.format(discord.__version__))
    em.add_field(
        name='Process',
        value=f'Memory: {memory_usage:.2f} MiB\nCPU: {cpu_usage}%')
    em.add_field(
        name='Uptime',
        value=f'{d}d {h}h {m}m {s}s')
    await ctx.send(embed=em)

@bot.command(name='poll')
async def _poll(ctx, question, duration: int, option1, option2, option3=None,
                option4=None, option5=None, option6=None, option7=None,
                option8=None, option9=None, option10=None):
    await ctx.message.delete()

    initial_options = [option1, option2, option3, option4, option5, option6,
                       option7, option8, option9, option10]
    options = []
    for option in initial_options:
        if option is not None:
            options.append(option)

    ones, twos, threes, fours, fives = 0, 0, 0, 0, 0
    sixs, sevens, eights, nines, tens = 0, 0, 0, 0, 0

    if len(options) < 2:
        return await ctx.send(":x: At least 2 options needed.")
    elif len(options) > 10:
        return await ctx.send(":x: Max 10 options allowed.")

    reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

    description = []
    for x, option in enumerate(options):
        description += '\n{} {}'.format(reactions[x], option)
    em = discord.Embed(title=question, description=''.join(description))
    em.set_author(name='Poll', icon_url=ctx.author.avatar_url)
    react_msg = await ctx.send(embed=em)

    for reaction in reactions[:len(options)]:
        await react_msg.add_reaction(reaction)

    while duration > 0:
        if duration > 1:
            second = "seconds"
        else:
            second = "second"
        em.set_footer(text="This poll will be closed in {} {}.".format(
            duration, second))
        await react_msg.edit(embed=em)

        await asyncio.sleep(1)
        duration -= 1

    await react_msg.edit(embed=em)

    onesV, twosV, threesV, foursV, fivesV = [], [], [], [], []
    sixsV, sevensV, eightsV, ninesV, tensV  = [], [], [], [], []
    numbers = [ones, twos, threes, fours, fives,
               sixs, sevens, eights, nines, tens]
    voters = [onesV, twosV, threesV, foursV,
              fivesV, sixsV, sevensV, eightsV,
              ninesV, tensV]

    cache_msg = await react_msg.channel.get_message(react_msg.id)
    for reaction in cache_msg.reactions:
        async for user in reaction.users():
            if user != bot.user:
                for x, voter in enumerate(voters):
                    if reaction.emoji == reactions[x]:
                        numbers[x] += 1
                        voter.append(user.mention)

    highest_num = max(numbers)
    highest_nums = []

    for num in numbers:
        if num == highest_num:
            highest_nums.append(num)
    if len(highest_nums) > 1:
        winner_option = False
        tie_options = []
        for x, num in enumerate(numbers):
            if num == highest_nums[0]:
                tie_options.append(options[x])
        tie_winner = random.choice(tie_options)
        em.set_footer(text='It\'s a tie! Picking a random winner...')
        await react_msg.edit(embed=em)

    else:
        for x, num in enumerate(numbers):
            if num == highest_nums[0]:
                winner_option = options[x]
        em.set_footer(text='❌ This poll has been closed.')
        await react_msg.edit(embed=em)

    for reaction in cache_msg.reactions:
        async for user in reaction.users():
            await cache_msg.remove_reaction(reaction, user)

    format1 = '**{}**\n └ {}' # To be used the option has at least one voter
    format2 = '**{}**' # To be used if the option has no voters
    results = []
    for x, voter in enumerate(voters):
        voters[x] = ', '.join(voters[x])
        if numbers[x] > 0:
            results.append(format1.format(numbers[x], voters[x]))
        else:
            results.append(format2.format(numbers[x]))

    total = []
    for x, option in enumerate(options):
        total += '\n{}: {}\n'.format(option, results[x])

    if winner_option:
        em = discord.Embed(
            title=question,
            description="__Result__{}\n:star: {}".format(
                ''.join(total), winner_option))
    else:
        em = discord.Embed(
            title=question,
            description="__Result__{}".format(
                ''.join(total)))
    em.set_author(name='Poll', icon_url=ctx.author.avatar_url)
    if winner_option:
        em.set_footer(text='❌ This poll has been closed.')
        await react_msg.edit(embed=em)
    else:
        em.set_footer(text="It's a tie! Picking a random winner...")
        await asyncio.sleep(3)
        await react_msg.edit(embed=em)

        em = discord.Embed(
            title=question,
            description="__Result__{}\n:star: {}".format(
                ''.join(total), tie_winner))
        em.set_author(name='Poll', icon_url=ctx.author.avatar_url)
        em.set_footer(text='❌ This poll has been closed.')
        await react_msg.edit(embed=em)


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)

        except Exception as e:
            print("Failed to load extension {}:".format(
                extension, file=sys.stderr))
            traceback.print_exc()

    # bot.loop.create_task(change_status())
    bot.run(botoken)
