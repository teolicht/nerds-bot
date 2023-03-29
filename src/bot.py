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
import json


DESCRIPTION = "A personal Discord bot for friends."
PREFIX = ("n!", "N!")
INTENTS = discord.Intents().all()
CONFIG = json.load(
    open(os.path.join(os.path.dirname(__file__), "cogs/text/config.json"), "r")
)

bot = commands.Bot(description=DESCRIPTION, command_prefix=PREFIX, intents=INTENTS)
bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    global NERDS, GENERAL, ZAP, NRD_ROLE, ZAP_ROLE, NRD_LIST
    NERDS = bot.get_guild(300762607164325893)
    GENERAL = discord.utils.get(NERDS.channels, name="general")
    ZAP = discord.utils.get(NERDS.channels, name="zap")
    NRD_ROLE = discord.utils.get(NERDS.roles, name="NRD")
    ZAP_ROLE = discord.utils.get(NERDS.roles, name="ZAP")
    NRD_LIST = CONFIG["nrd_members"]


@bot.event
async def on_message(message):
    if message.guild is None:
        return

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    if member.guild == NERDS and member.bot is False:
        nrd_list = CONFIG["nrd_members"]
        if member.id in NRD_LIST:
            await member.add_roles(NRD_ROLE)
            await GENERAL.send(
                ":clown: **{0.mention} has joined the server** :white_check_mark:".format(
                    member
                )
            )
        else:
            await member.add_roles(ZAP_ROLE)
            await ZAP.send(
                ":clown: **{0.mention} has joined the server** :white_check_mark:".format(
                    member
                )
            )


@bot.event
async def on_member_remove(member):
    if member.guild == NERDS and member.bot is False:
        if member.id in NRD_LIST:
            await GENERAL.send(
                ":clown: **{0.mention} has left the server** :x:".format(member)
            )
        else:
            await ZAP.send(
                ":clown: **{0.mention} has left the server** :x:".format(member)
            )





@bot.command()
async def ping(ctx):
    def color(r, g, b):
        return discord.Colour.from_rgb(r, g, b)

    t_1 = time.perf_counter()
    await ctx.channel.typing()
    t_2 = time.perf_counter()
    ping = round((t_2 - t_1) * 1000)
    if ping <= 100:
        color = color(0, 211, 14)
    elif ping <= 150:
        color = color(106, 255, 0)
    elif ping <= 200:
        color = color(195, 255, 0)
    elif ping <= 250:
        color = color(255, 255, 0)
    elif ping <= 350:
        color = color(255, 212, 0)
    elif ping <= 400:
        color = color(255, 174, 0)
    elif ping <= 500:
        color = color(255, 127, 0)
    elif ping <= 750:
        color = color(255, 72, 0)
    elif ping <= 900:
        color = color(255, 0, 0)
    else:
        color = color(211, 0, 0)

    em = discord.Embed(title="🏓 Pong!", description="*{}ms*".format(ping), color=color)
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
    if os.name == "posix":
        cmd = cmd.format(r"\`%h\`")
    else:
        cmd = cmd.format(r"`%h`")

    try:
        revision = os.popen(cmd).read().strip().split("\n")
    except OSError:
        revision = "Could not fetch due to memory error."
    for commit in revision:
        if "Merge branch" in commit:
            revision.remove(commit)
    em = discord.Embed(
        description="**Latest changes:**\n" + "\n".join(revision) + "\n⠀",
        color=0xFF2B29,
    )
    em.set_author(
        name="GitHub",
        icon_url="https://cdn.discordapp.com/attachments/477239188203503628/839336908210962442/unknown.png",
        url="https://github.com/teolicht/nerds-bot",
    )
    em.add_field(name="Language", value=f"Python {major}.{minor}.{micro}")
    em.add_field(name="API", value="discord.py {}".format(discord.__version__))
    em.add_field(
        name="Process", value=f"Memory: {memory_usage:.2f} MiB\nCPU: {cpu_usage}%"
    )
    em.set_footer(text=f"✅ Uptime: {d}d {h}h {m}m {s}s")
    await ctx.send(embed=em)


@bot.command()
async def poll(
    ctx,
    question,
    duration: int,
    option1,
    option2,
    option3=None,
    option4=None,
    option5=None,
    option6=None,
    option7=None,
    option8=None,
    option9=None,
    option10=None,
):
    await ctx.message.delete()
    initial_options = [
        option1,
        option2,
        option3,
        option4,
        option5,
        option6,
        option7,
        option8,
        option9,
        option10,
    ]
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

    reactions = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]

    description = []
    for x, option in enumerate(options):
        description += "\n{} {}\n\u200b".format(reactions[x], option)
    em = discord.Embed(title=question, description="".join(description))
    em.set_author(name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar)
    react_msg = await ctx.send(embed=em)

    for reaction in reactions[: len(options)]:
        await react_msg.add_reaction(reaction)

    while duration > 0:
        if duration > 1:
            second = "seconds"
        else:
            second = "second"
        em.set_footer(text="This poll will end in {} {}.".format(duration, second))
        await react_msg.edit(embed=em)

        await asyncio.sleep(1)
        duration -= 1

    await react_msg.edit(embed=em)

    onesV, twosV, threesV, foursV, fivesV = [], [], [], [], []
    sixsV, sevensV, eightsV, ninesV, tensV = [], [], [], [], []
    numbers = [ones, twos, threes, fours, fives, sixs, sevens, eights, nines, tens]
    voters = [
        onesV,
        twosV,
        threesV,
        foursV,
        fivesV,
        sixsV,
        sevensV,
        eightsV,
        ninesV,
        tensV,
    ]

    cache_msg = await react_msg.channel.fetch_message(react_msg.id)
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
        try:
            for x, num in enumerate(numbers):
                if num == highest_nums[0]:
                    tie_options.append(options[x])
        except IndexError:
            em.set_footer(text="❌ No one voted.")
            await react_msg.edit(embed=em)
            for reaction in cache_msg.reactions:
                async for user in reaction.users():
                    await cache_msg.remove_reaction(reaction, user)
            return

        tie_winner = random.choice(tie_options)
        em.set_footer(text="It's a tie! Picking a random winner...")
        await react_msg.edit(embed=em)

    else:
        for x, num in enumerate(numbers):
            if num == highest_nums[0]:
                winner_option = options[x]
        em.set_footer(text="❌ This poll has ended.")
        await react_msg.edit(embed=em)

    for reaction in cache_msg.reactions:
        async for user in reaction.users():
            await cache_msg.remove_reaction(reaction, user)

    format1 = "**{}**\n └ {}"  # To be used the option has at least one voter
    format2 = "**{}**"  # To be used if the option has no voters
    results = []
    for x, voter in enumerate(voters):
        voters[x] = ", ".join(voters[x])
        if numbers[x] > 0:
            results.append(format1.format(numbers[x], voters[x]))
        else:
            results.append(format2.format(numbers[x]))

    total = []
    for x, option in enumerate(options):
        total += "\n`{}`: {}\n".format(option, results[x])

    if winner_option:
        em = discord.Embed(
            title=question,
            description="__Result__{}\n:star: {}".format("".join(total), winner_option),
        )
    else:
        em = discord.Embed(
            title=question, description="__Result__{}".format("".join(total))
        )
    em.set_author(name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar)
    if winner_option:
        em.set_footer(text="❌ This poll has ended.")
        await react_msg.edit(embed=em)
    else:
        em.set_footer(text="It's a tie! Picking a random winner...")
        await asyncio.sleep(3)
        await react_msg.edit(embed=em)

        em = discord.Embed(
            title=question,
            description="__Result__{}\n:star: {}".format("".join(total), tie_winner),
        )
        em.set_author(
            name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar
        )
        em.set_footer(text="❌ This poll has ended.")
        await react_msg.edit(embed=em)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print("Failed to load extension {}:".format(filename, file=sys.stderr))
                traceback.print_exc()


async def main():
    await load()
    await bot.start(CONFIG["token"])


asyncio.run(main())
