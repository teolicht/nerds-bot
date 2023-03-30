import asyncio
import random
import datetime
import os
import threading
import discord
from discord import app_commands
from discord.ext import commands


PATH = os.path.dirname(__file__)
annoyed_members = []
cure_members = []
on_cooldown = False


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def mname(self, member: discord.Member):
        """If member.nick exists, return it, otherwise,
        return member.name"""
        if member.nick:
            return member.nick
        else:
            return member.name

    def cooldown_timer(self):
        global on_cooldown
        on_cooldown = False

    # async def nope(self, msg):
    #     await msg.add_reaction("\U0001f1f3")  # N
    #     await msg.add_reaction("\U0001f1f4")  # O
    #     await msg.add_reaction("\U0001f1f5")  # P
    #     await msg.add_reaction("\U0001f1ea")  # E

    @commands.command()
    async def say(self, ctx, *, text):
        try:
            await ctx.message.delete()
            text = "".join(text)
            await ctx.send(text)
        except discord.errors.Forbidden:
            await ctx.send(
                ":x: I need the **Manage Messages** permission "
                + "so I can delete your message."
            )

    @app_commands.command(description="Make the bot send someone a DM.")
    @app_commands.describe(target="A member in this server.")
    @app_commands.describe(message="Message content.")
    async def sayto(
        self, interaction: discord.Interaction, target: discord.Member, message: str
    ):
        em = discord.Embed(
            title=f"Dear {target.name}",
            description=f"*I was sent here by {interaction.user.mention} to tell you this:*\n\n{message}\n\u200b",
            timestamp=discord.utils.utcnow(),
        )
        await target.send(embed=em)
        em = discord.Embed(
            description=f":white_check_mark: Sent message to {target.mention}"
        )
        em.set_author(
            name=self.mname(interaction.user), icon_url=interaction.user.display_avatar
        )
        await interaction.response.send_message(embed=em)

    @commands.command()
    async def big(self, ctx, *, text):
        msg = ""

        def big(letter):
            return f":regional_indicator_{letter}: "

        for char in "".join(text):
            char = char.lower()
            if char == "0":
                msg += ":zero:"
            elif char == "1":
                msg += ":one:"
            elif char == "2":
                msg += ":two:"
            elif char == "3":
                msg += ":three:"
            elif char == "4":
                msg += ":four:"
            elif char == "5":
                msg += ":five:"
            elif char == "6":
                msg += ":six:"
            elif char == "7":
                msg += ":seven:"
            elif char == "8":
                msg += ":eight:"
            elif char == "9":
                msg += ":nine:"
            elif char in ["a", "ã", "á", "à", "â", "å"]:
                msg += big("a")
            elif char == "b":
                msg += big("b")
            elif char == "c":
                msg += big("c")
            elif char == "d":
                msg += big("d")
            elif char in ["e", "é", "è", "ê"]:
                msg += big("e")
            elif char == "f":
                msg += big("f")
            elif char == "g":
                msg += big("g")
            elif char == "h":
                msg += big("h")
            elif char in ["i", "í", "ì", "î"]:
                msg += big("i")
            elif char == "j":
                msg += big("j")
            elif char == "k":
                msg += big("k")
            elif char == "l":
                msg += big("l")
            elif char == "m":
                msg += big("m")
            elif char in ["n", "ñ"]:
                msg += big("n")
            elif char in ["o", "õ", "ó", "ò", "ô", "ø"]:
                msg += big("o")
            elif char == "p":
                msg += big("p")
            elif char == "q":
                msg += big("q")
            elif char == "r":
                msg += big("r")
            elif char == "s":
                msg += big("s")
            elif char == "t":
                msg += big("t")
            elif char in ["u", "ú", "ù", "û"]:
                msg += big("u")
            elif char == "v":
                msg += big("v")
            elif char == "w":
                msg += big("w")
            elif char == "x":
                msg += big("x")
            elif char == "y":
                msg += big("y")
            elif char == "z":
                msg += big("z")
            elif char == " ":
                msg += "    "
            else:
                msg += char

        try:
            await ctx.message.delete()
            await ctx.send(msg)
        except discord.errors.Forbidden:
            await ctx.send(
                ":x: I need the **Manage Messages** permission so I can delete your message first."
            )

    @app_commands.command(description="Roast someone in the server.")
    @app_commands.describe(target="A member in this server.")
    async def roast(self, interaction: discord.Interaction, target: discord.Member):
        if target == self.bot.user:
            return await interaction.response.send_message(
                ":regional_indicator_n::regional_indicator_o::regional_indicator_p::regional_indicator_e:"
                ":exclamation: I shall not roast myself!"
            )

        with open(os.path.join(PATH, "text/roasts.txt")) as file:
            roasts = [line.rstrip("\n") for line in file]
        roast = random.choice(roasts)

        em = discord.Embed(
            description=f"{target.mention},\n{roast}",
            color=discord.Colour.red(),
        )
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Kill yourself.")
    async def suicide(self, interaction: discord.Interaction):
        author = interaction.user
        nick = self.mname(author)
        if "💀" in nick:
            return await interaction.response.send_message(":x: You're already dead.")
        em = discord.Embed(
            description=f":skull: {interaction.user.mention} has suicided!",
            color=discord.Colour.red(),
        )
        # If the nick is longer than 31 characters (limit is 32), the skull cannot be added
        if len(nick) > 30:
            return await interaction.response.send_message(embed=em)
        try:
            await author.edit(nick="💀{}".format(nick))
        except discord.errors.Forbidden:
            pass
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Kill a member in this server.")
    @app_commands.describe(target="A member in this server.")
    async def kill(self, interaction: discord.Interaction, target: discord.Member):
        target_nick = self.mname(target)
        author_nick = self.mname(interaction.user)
        if target == self.bot.user:
            return await interaction.response.send_message(
                ":regional_indicator_n::regional_indicator_o::regional_indicator_p::regional_indicator_e::exclamation: I shall not kill myself!"
            )
        if target == interaction.user:
            return await interaction.response.send_message(
                ":x: If you want to kill yourself, you should use `/suicide`"
            )
        if "💀" in target_nick:
            return await interaction.response.send_message(
                ":x: That member is already dead."
            )
        if "💀" in author_nick:
            return await interaction.response.send_message(
                ":x: How are you going to kill someone if YOU are dead?"
            )
        em = discord.Embed(
            description=f":skull: {target.mention} has been killed by {interaction.user.mention}! :skull_crossbones:",
            color=discord.Colour.red(),
        )
        amongus_gifs = [
            "https://media.tenor.com/F__GSvFsf20AAAAC/among-us-kill.gif",
            "https://media.tenor.com/Zi1l60KaBGMAAAAC/among-us-kill.gif",
            "https://media.tenor.com/0l5kHLfHhhgAAAAC/among-us.gif",
        ]
        gif = random.choice(amongus_gifs)
        em.set_image(url=gif)
        # If the nick is longer than 31 characters (limit is 32), the skull cannot be added, send just the message instead
        if len(target_nick) > 31:
            return await interaction.response.send_message(embed=em)
        try:
            await target.edit(nick=f"💀{target_nick}")
        except discord.errors.Forbidden:
            pass
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Respawn a dead member.")
    @app_commands.describe(target="A member in this server.")
    async def respawn(self, interaction: discord.Interaction, target: discord.Member):
        nick = self.mname(target)
        if target == interaction.user:
            return await interaction.response.send_message(
                ":x: You can't respawn yourself, that's not how it works..."
            )
        if "💀" in nick:
            new_name = nick.replace("💀", "")
            await target.edit(nick=new_name)
            await interaction.response.send_message(
                f":innocent: Welcome back, {target.mention}. You have been respawned!"
            )
        else:
            await interaction.response.send_message(
                f":x: {target.mention} is not even dead, mate."
            )

    @app_commands.command(
        description="Respawn all dead members. Three people needed for this command."
    )
    async def cure(self, interaction: discord.Interaction):
        global cure_members
        # if len is 2, then only one more member is required to cure, so there are 3 members already
        if len(cure_members) == 2:
            members = interaction.guild.members
            for member in members:
                nick = self.mname(member)
                if "💀" in nick:
                    new_name = nick.replace("💀", "")
                    await member.edit(nick=new_name)
            cure_members = []
            return await interaction.response.send_message(
                ":angel: Everyone has respawned!"
            )
        if interaction.user in cure_members:
            await interaction.response.send_message(
                ":x: You've already used the cure command. Someone else needed!"
            )
        else:
            cure_members.append(interaction.user)
            members_needed = 3 - len(cure_members)
            await interaction.response.send_message(
                f":innocent: {interaction.user.mention} is trying to cure everyone! :sparkles:  "
                f"{members_needed} more member(s) required."
            )

    @commands.command()
    async def rps(self, ctx, choice):
        def comparison(userC, botC):
            if userC == botC:
                return "Tie"
            elif userC == "Rock" and botC == "Scissors":
                return "Win"
            elif userC == "Paper" and botC == "Rock":
                return "Win"
            elif userC == "Scissors" and botC == "Paper":
                return "Win"
            else:
                return "Lose"

        def endgame(member, userC, botC):
            em = discord.Embed()
            if comparison(userC, botC) == "Tie":
                em = discord.Embed(description=member + ", it's a tie!")
            elif comparison(userC, botC) == "Win":
                em = discord.Embed(
                    description=member + ", you won!", color=discord.Colour.green()
                )
            else:
                em = discord.Embed(
                    description=member + ", you lost!", color=discord.Colour.red()
                )
            return em

        choices = ["Rock", "Paper", "Scissors"]
        botC = random.choice(choices)
        if choice.lower() not in ["r", "rock", "p", "paper", "s", "scissors"]:
            await ctx.send("`{}` is not a valid choice.".format(choice))
        else:
            await asyncio.sleep(1)
            await ctx.send("I choose **{}**".format(botC))
            await asyncio.sleep(1)

            if choice.lower() in ["r", "rock"]:
                await ctx.send(embed=endgame(ctx.author.mention, "Rock", botC))
            elif choice.lower() in ["p", "paper"]:
                await ctx.send(embed=endgame(ctx.author.mention, "Paper", botC))
            else:
                await ctx.send(embed=endgame(ctx.author.mention, "Scissors", botC))

    @commands.command()
    async def annoy(self, ctx, member: discord.Member, times: int = 1):
        if times > 20:
            return await ctx.send(":x: Max 20 times.")
        if member in annoyed_members:
            return await ctx.send(":x: That member is already being annoyed.")
        nick = self.mname(member)
        minutes = round((30 * times) / 60, 1)
        if times <= 0:
            return await ctx.send(":x: Positive numbers only.")
        elif times == 1:
            start_msg = f":white_check_mark: Annoyed {nick}"
            end_msg = None
        elif times > 1:
            start_msg = (
                ":white_check_mark: Started annoying {} ".format(self.mname(member))
                + f"(**{times}** times)"
            )
            end_msg = ":white_check_mark: Done annoying {0.mention} • `{1}min`".format(
                member, minutes
            )
        with open(os.path.join(PATH, "text/bad_words.txt")) as file:
            bad_words = [line.rstrip("\n") for line in file]
        annoyed_members.append(member)
        await ctx.send(start_msg)
        for i in range(0, times):
            word = random.choice(bad_words)
            await member.send(
                "**{}** • I was sent here to annoy ".format(i + 1)
                + "you by {0.author.mention}, **{1}**.".format(ctx, word)
            )
            if not i == times - 1:  # If not done yet
                await asyncio.sleep(30)
        if end_msg:
            await ctx.send(end_msg)

    @commands.command()
    async def sound(self, ctx, option, repeat: int = False):
        sounds_path = os.path.join(PATH, "sounds")

        def soundobj(sound):
            return discord.FFmpegPCMAudio(sounds_path + sound)

        async def playsound(file, repeat, duration):
            if repeat is False:
                vc.play(soundobj(file))
            else:
                for i in range(0, repeat):
                    vc.play(soundobj(file))
                    await asyncio.sleep(duration)
                    vc.stop()
            await asyncio.sleep(duration)

        voice = ctx.author.voice
        if voice is None:
            return await ctx.send(":x: Join a voice channel first.")
        channel = voice.channel
        options = {
            "1": "Doin' your mom",
            "2": "Deja vu duck",
            "3": "Pedron smashing keyboard",
            "4": "Surprise motherfucker",
            "5": "Lorengay singing",
        }
        if option not in options:
            return await ctx.send(":x: Option `{}` not found.".format(option))

        vc = await channel.connect()
        await ctx.send(
            ":white_check_mark: *Playing sound* `{}`".format(options[option])
        )

        if option == "1":
            await playsound("doinurmom.mp3", repeat, 8.2)
        elif option == "2":
            await playsound("initialduck.mp3", repeat, 14.7)
        elif option == "3":
            await playsound("smashingKB.mp3", repeat, 7)
        elif option == "4":
            await playsound("surpriseMF.mp3", repeat, 2.5)
        elif option == "5":
            await playsound("lorensing.mp3", repeat, 31)
        await vc.disconnect()

    @commands.command()
    async def fact(self, ctx):
        with open(os.path.join(PATH, "text", "facts.txt")) as file:
            facts = [line.rstrip("\n") for line in file]
        fact = random.choice(facts)
        await ctx.send(fact)

    @commands.command()
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        nick1 = self.mname(member1)
        nick2 = self.mname(member2)
        half_index1 = int(len(nick1) / 2)
        half1 = nick1[:half_index1]
        half_index2 = int(len(nick2) / 2)
        half2 = nick2[half_index2:]
        ship_name = (half1 + half2).strip()
        em = discord.Embed(
            title=":heart: I ship {} and {} :heart:".format(nick1, nick2),
            description=":two_hearts::revolving_hearts: {} ".format(ship_name)
            + ":revolving_hearts::two_hearts:",
            color=0xFF2B29,
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["unigger", "unniger"])
    async def unnigger(self, ctx, member: discord.Member):
        if ctx.author == member:
            return await ctx.send(":x: You can't un-nigger yourself.")
        nick = self.mname(member)
        nigger_role = discord.utils.get(ctx.guild.roles, name="NIGGER")
        if nigger_role not in member.roles:
            return await ctx.send(":x: That member isn't even a nigger.")
        await member.remove_roles(nigger_role)
        await ctx.send(":white_check_mark: {} is no longer a nigger.".format(nick))

    @commands.command()
    @commands.is_owner()
    async def pt(self, ctx, member: discord.Member, times: int = 1):
        if times == 1:
            duration = 600
            how_long = "10 minutes!"
        elif times == 2:
            duration = 1800
            how_long = "30 minutes!"
        elif times == 3:
            duration = 3600
            how_long = "1 hour!"
        elif times == 4:
            duration = 7200
            how_long = "2 hours!"
        elif times == 5:
            duration = 18000
            how_long = "5 hours!"
        gay_role = discord.utils.get(ctx.guild.roles, name="GAY")
        try:
            await member.add_roles(gay_role)
        except:
            return await ctx.send(
                ":x: I wasn't able to do that. Check if a "
                + "'GAY' role exists in this server."
            )
        await ctx.send(
            ":white_check_mark: {0.mention} is now ".format(member)
            + "GAY for {}".format(how_long)
        )
        await asyncio.sleep(duration)
        await member.remove_roles(gay_role)
        await ctx.send("{0.mention} is no longer GAY.".format(member))

    @commands.command()
    async def cum(self, ctx):
        global on_cooldown
        if on_cooldown is True:
            return await ctx.send(":x: Please wait.")
        else:
            on_cooldown = True
            timer = threading.Timer(10.0, self.cooldown_timer)
            timer.start()
        await asyncio.sleep(2)
        await ctx.send("**Fase 1: Iniciación** :smiling_imp:")
        await ctx.send("https://tenor.com/view/he-hehe-boy-boi-boyi-gif-7890844")
        await asyncio.sleep(5)
        await ctx.send("**Fase 2: Excitación** :flushed:")
        await ctx.send(
            "https://tenor.com/view/hmm-sulley-monsters-inc-james-sullivan-shocked-gif-15802869"
        )
        await asyncio.sleep(5)
        await ctx.send("**Fase 3: Finalización** :sunglasses:")
        await ctx.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:CUM:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await ctx.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:AHHHHH IM COOOMING:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await ctx.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:FUCK:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:SEX:sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await asyncio.sleep(5)
        await ctx.send("**5 minutos después:**")
        await ctx.send(
            "https://tenor.com/view/mike-wazowski-cursed-terror-moving-move-gif-16644513"
        )


async def setup(bot):
    await bot.add_cog(Fun(bot))
