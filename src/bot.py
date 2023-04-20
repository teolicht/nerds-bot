import random
import asyncio
import logging
import pickle
import discord
from discord.ext import commands
from cogs import settings


description = "A private Discord bot for friends."
command_prefix = ("n!", "N!")
intents = discord.Intents().all()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
discord.utils.setup_logging(handler=handler)

initial_extensions = [
    "cogs.fun",
    "cogs.handler",
    "cogs.help",
    "cogs.information",
    "cogs.moderation",
    "cogs.pictures",
    "cogs.reddit",
    "cogs.utilities"
]


class NerdsBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            help_command=None,
            intents=intents
        )

    async def setup_hook(self) -> None:
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="/help")
        )

        try:
            print("-" * 50)
            print("Logged in as")
            print("> " + self.user.name)
            print("> ID: " + str(self.user.id))
            print("-" * 50)
        except Exception as e:
            print(e)

        bot_launch_time = discord.utils.utcnow()
        with open("bot_launch_time.pkl", "wb") as file:
            pickle.dump(bot_launch_time, file, pickle.HIGHEST_PROTOCOL)
            file.close()

        global NERDS_GUILD, GENERAL_CHANNEL, ZAP_CHANNEL
        NERDS_GUILD = self.get_guild(settings.NERDS["GUILD"])
        GENERAL_CHANNEL = discord.utils.get(
            NERDS_GUILD.channels, id=settings.NERDS["GENERAL"]
        )
        ZAP_CHANNEL = discord.utils.get(NERDS_GUILD.channels, id=settings.NERDS["ZAP"])

    async def on_message(self, message):
        if message.guild is not None:
            await self.process_commands(message)

    async def on_member_join(self, member):
        NRD_ROLE = discord.utils.get(NERDS_GUILD.roles, name="NRD")
        ZAP_ROLE = discord.utils.get(NERDS_GUILD.roles, name="ZAP")
        if member.bot is True:
            return
        if member.guild != NERDS_GUILD:
            return
        if member.id in settings.NERDS_MEMBERS:
            await member.add_roles(NRD_ROLE)
        else:
            await member.add_roles(ZAP_ROLE)
        await GENERAL_CHANNEL.send(
            f":clown: **{member.mention} has joined the server** :white_check_mark:"
        )
        await ZAP_CHANNEL.send(
            f":clown: **{member.mention} has joined the server** :white_check_mark:"
        )

    async def on_member_remove(self, member: discord.Member):
        if member.guild == NERDS_GUILD and member.bot is False:
            await GENERAL_CHANNEL.send(f"**{member.mention} has left the server** :x:")
            await ZAP_CHANNEL.send(f"**{member.mention} has left the server** :x:")

    async def start(self) -> None:
        await super().start(settings.TOKEN, reconnect=True)


# NerdsBot instance
bot = NerdsBot()

@bot.command()
async def sync(ctx):
    if ctx.author.id != settings.NERDS_MEMBERS[0]:
        return ctx.send(":x: You cannot use this command.")
    synced = await ctx.bot.tree.sync()
    await ctx.send(f":white_check_mark: Synced `{len(synced)}` commands")

# This command shall be rewritten and moved to utilities cog
@bot.command()
async def poll(
    # fmt: off
    ctx, question, duration: int, option1, option2,
    option3=None, option4=None, option5=None, option6=None,
    option7=None, option8=None, option9=None, option10=None,
):
    # fmt: on
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
    em.set_author(name=f"{ctx.author.name}'s poll",
                    icon_url=ctx.author.display_avatar)
    react_msg = await ctx.send(embed=em)

    for reaction in reactions[: len(options)]:
        await react_msg.add_reaction(reaction)

    while duration > 0:
        if duration > 1:
            second = "seconds"
        else:
            second = "second"
        em.set_footer(
            text="This poll will end in {} {}.".format(duration, second))
        await react_msg.edit(embed=em)

        await asyncio.sleep(1)
        duration -= 1

    await react_msg.edit(embed=em)

    onesV, twosV, threesV, foursV, fivesV = [], [], [], [], []
    sixsV, sevensV, eightsV, ninesV, tensV = [], [], [], [], []
    numbers = [ones, twos, threes, fours, fives,
                sixs, sevens, eights, nines, tens]
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
            description="__Result__{}\n:star: {}".format(
                "".join(total), winner_option),
        )
    else:
        em = discord.Embed(
            title=question, description="__Result__{}".format(
                "".join(total))
        )
    em.set_author(name=f"{ctx.author.name}'s poll",
                    icon_url=ctx.author.display_avatar)
    if winner_option:
        em.set_footer(text="❌ This poll has ended.")
        await react_msg.edit(embed=em)
    else:
        em.set_footer(text="It's a tie! Picking a random winner...")
        await asyncio.sleep(3)
        await react_msg.edit(embed=em)

        em = discord.Embed(
            title=question,
            description="__Result__{}\n:star: {}".format(
                "".join(total), tie_winner),
        )
        em.set_author(
            name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar
        )
        em.set_footer(text="❌ This poll has ended.")
        await react_msg.edit(embed=em)


# Maybe move this to a launcher file at some point?
asyncio.run(bot.start())


