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

from emojis import Emoji
from cogs.nerds import nerds


description = "A Discord bot written by Lanit#3333."
prefix = ('n!', 'N!')

initial_extensions = [
    'cogs.handler',
    'cogs.invites',
    'cogs.information',
    'cogs.pictures',
    'cogs.fun',
    'cogs.moderation',
    'cogs.utilities']

bot = commands.Bot(
    description=description,
    command_prefix=prefix)
bot.remove_command('help')

async def change_status():
    await bot.wait_until_ready()

    statuses = ['oof', 'blyat', 'cyka', 'cyunt', 'sussu', 'gey', 'ur mom gey', 'jeff',
                'GRRRRRRRRRRRRRRRRRRRRR', 'ecksdee', 'heck', 'm\'lady', 'hipócritas',
                'What the fuck did you just fucking say about me, you little bitch?',
                'it is {} my dudes AAAAAAAAAAAAAAAAA'.format(datetime.datetime.now().strftime('%A').lower()),
                '2+2=4-1=3 quick maths', 'bazinga']
    status_option = random.choice(statuses)

    while True:
        status_text = 'n!help • ' + status_option
        status = discord.Game(status_text)
        await bot.change_presence(activity=status)
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    print("ONLINE")

    nerds_guild = bot.get_guild(300762607164325893)
    music_channel = bot.get_channel(452157904066183169)
    has_role = False

    for role in nerds_guild.roles:
        if role == 425688731190820864:
            has_role = True

    if has_role is False:
        lorenzo_role = nerds(nerds_guild, 'lorenzo_role')
        await nerds(nerds_guild, 'lorenzo').add_roles(lorenzo_role)

executed = 0
@bot.event
async def on_command(ctx):
    global executed
    executed += 1
    print("{0} : n!{1.command.name} • {1.message.author}".format(executed, ctx))

@bot.event
async def on_member_join(member):
    def edit_member(member_name):
        member = nerds(option=member_name)
        if member_name == 'lorenzo':
            member.add_roles(nerds(option='lorenzo_role'))
            pass
        if member == nerds(option='lorenzo'):
            member.add_roles(nerds(option='lorenzo_role'))
            member.edit(nick='')
    if member.guild.id == 300762607164325893:
        channel = nerds.get_channel(451854600064991242)

        await channel.send("{0.awesome} Welcome back to hell, {1.mention}!".format(Emoji, member))

        if member == nerds(option='lorenzo'):
            edit_member(nerds(option='lorenzo'))

        elif member == nerds(option='clachip'):
            edit_member(nerds(option='clachip'))

        elif member == nerds(option='jeff'):
            edit_member(nerds(option='jeff'))

        elif member == nerds(option='leo'):
            edit_member(nerds(option='leo'))

        elif member == nerds(option='mesh'):
            edit_member(nerds(option='mesh'))

        elif member == nerds(option='ogdroid'):
            edit_member(nerds(option='ogdroid'))

        elif member == nerds(option='pedron'):
            edit_member(nerds(option='pedron'))

@bot.event
async def on_message(message):
    if message.channel.id == 459775059192447005:
            DJBot_cmds = """
.play .disconnect .np .aliases .ping .skip .seek .soundcloud .remove .loopqueue
.search .stats .loop .donate .shard .join .lyrics .info .resume .settings .move
.forward .skipto .clear .replay .clean .pause .removedupes .volume .rewind
.playtop .playskip .invite .shuffle .queue .leavecleanup
""".split()
            if not message.content.startswith(('n!mute', 'n!unmute')):
                if not message.content.startswith(tuple(DJBot_cmds)) and not message.author.id == 235088799074484224:
                    await message.delete()

    if message.guild is None:
        print("PM : \"{2.content}\" - {2.author}".format(message))
    else:
        await bot.process_commands(message)

@bot.command(name='ping', aliases=['Ping', 'PING', 'latency'])
async def _ping(ctx):
    t_1 = time.perf_counter()
    await ctx.trigger_typing()
    t_2 = time.perf_counter()
    time_delta = round((t_2 - t_1) * 1000)

    em = discord.Embed(
        title="🏓 Pong!{0.online}".format(Emoji),
        description='*{}ms*'.format(time_delta))
    await ctx.send(embed=em)

@bot.command(name='poll')
async def _poll(ctx, question, duration: int, option1, option2, option3=None, option4=None, option5=None,
                option6=None, option7=None, option8=None, option9=None, option10=None):
    await ctx.message.delete()

    initial_options = [option1, option2, option3, option4, option5, option6, option7, option8, option9, option10]
    options = []
    for option in initial_options:
        if option is not None:
            options.append(option)

    ones, twos, threes, fours, fives, sixs, sevens, eights, nines, tens = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

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
        em.set_footer(text="This poll will be closed in {} {}.".format(duration, second))
        await react_msg.edit(embed=em)

        await asyncio.sleep(1)
        duration -= 1

    await react_msg.edit(embed=em)

    ones_voters, twos_voters, threes_voters, fours_voters, fives_voters = [], [], [], [], []
    sixs_voters, sevens_voters, eights_voters, nines_voters, tens_voters  = [], [], [], [], []
    numbers = [ones, twos, threes, fours, fives, sixs, sevens, eights, nines, tens]
    voters = [ones_voters, twos_voters, threes_voters, fours_voters, fives_voters,
              sixs_voters, sevens_voters, eights_voters, nines_voters, tens_voters]

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

    format1 = '**{}**\n └ {}' # Format to be used if the option has at least one voter
    format2 = '**{}**' # Format to be used if the option has no voters
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
        em = discord.Embed(title=question, description="__Result__{}\n:star: {}".format(''.join(total), winner_option))
    else:
        em = discord.Embed(title=question, description="__Result__{}".format(''.join(total)))
    em.set_author(name='Poll', icon_url=ctx.author.avatar_url)
    if winner_option:
        em.set_footer(text='❌ This poll has been closed.')
        await react_msg.edit(embed=em)
    else:
        em.set_footer(text="It's a tie! Picking a random winner...")
        await asyncio.sleep(3)
        await react_msg.edit(embed=em)

        em = discord.Embed(title=question, description="__Result__{}\n:star: {}".format(''.join(total), tie_winner))
        em.set_author(name='Poll', icon_url=ctx.author.avatar_url)
        em.set_footer(text='❌ This poll has been closed.')
        await react_msg.edit(embed=em)


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)

        except Exception as e:
            print("Failed to load extension {}:{}".format(extension, file=sys.stderr)
            traceback.print_exc()

    bot.loop.create_task(change_status())
    bot.run("Mzg2NTY4ODg4MTQzNTc3MTA2.DYsYJQ.qkGjjtkyYndxPravxyKZPWCEO-Q")
