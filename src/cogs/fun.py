import asyncio
import random
import threading
import discord
from discord import app_commands
from discord.ext import commands


annoyed_members = []
cure_members = []
on_cooldown = False
transparent_color = 0x302C34


class RPSView(discord.ui.View):
    choice = None
    user = None
    choice_message = "> {0.user.mention} chooses **{1.choice}** {2}"

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable_all_items()

    @discord.ui.button(emoji="👊", label="Rock", style=discord.ButtonStyle.gray)
    async def rock_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.user = interaction.user
        self.choice = "rock"
        await interaction.response.send_message(
            self.choice_message.format(self, self, ":punch:")
        )
        self.stop()

    @discord.ui.button(emoji="🖐", label="Paper", style=discord.ButtonStyle.gray)
    async def paper_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.user = interaction.user
        self.choice = "paper"
        await interaction.response.send_message(
            self.choice_message.format(self, self, ":hand_splayed:")
        )
        self.stop()

    @discord.ui.button(emoji="✌", label="Scissors", style=discord.ButtonStyle.gray)
    async def scissors_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.user = interaction.user
        self.choice = "scissors"
        await interaction.response.send_message(
            self.choice_message.format(self, self, ":v:")
        )
        self.stop()

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.danger)
    async def quit_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.choice = "quit"
        await interaction.message.delete()
        self.stop()


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

    @app_commands.command(description="Speak as if you were me.")
    @app_commands.describe(message="The message you want me to send to the chat.")
    async def say(self, interaction: discord.Interaction, message: str):
        em = discord.Embed(description=":white_check_mark: *Sent message*")
        await interaction.response.send_message(embed=em, ephemeral=True)
        await interaction.channel.send(message)

    @app_commands.command(
        description="Speak as if you were me, but through emoji-letters."
    )
    @app_commands.describe(
        message="The message you want me to convert to emoji-letters, and then send to the chat."
    )
    async def saybig(self, interaction: discord.Interaction, message: str):
        def big(letter):
            return f":regional_indicator_{letter}: "

        msg = ""
        for char in message:
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
        em = discord.Embed(description=":white_check_mark: *Sent message*")
        await interaction.response.send_message(embed=em, ephemeral=True)
        await interaction.channel.send(msg)

    @app_commands.command(description="Make the bot send someone a DM.")
    @app_commands.describe(user="A member in this server.")
    @app_commands.describe(message="Message content.")
    async def dm(
        self, interaction: discord.Interaction, user: discord.Member, message: str
    ):
        em = discord.Embed(
            title=f"Dear {user.name}",
            description=f"*I was sent here by {interaction.user.mention} to tell you this:*\n\n{message}\n\u200b",
            timestamp=discord.utils.utcnow(),
        )
        await user.send(embed=em)
        em = discord.Embed(
            description=f":white_check_mark: Sent message to {user.mention}"
        )
        em.set_author(
            name=self.mname(interaction.user), icon_url=interaction.user.display_avatar
        )
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Roast someone in the server.")
    @app_commands.describe(user="A member in this server.")
    async def roast(self, interaction: discord.Interaction, user: discord.Member):
        if user == self.bot.user:
            return await interaction.response.send_message(
                ":regional_indicator_n::regional_indicator_o::regional_indicator_p::regional_indicator_e:"
                ":exclamation: I shall not roast myself!"
            )

        with open("cogs/text/roasts.txt", "r") as file:
            roasts = [line.rstrip("\n") for line in file]
            file.close()
        roast = random.choice(roasts)

        em = discord.Embed(
            description=f"{user.mention},\n{roast}",
            color=transparent_color,
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
            color=transparent_color,
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
    @app_commands.describe(user="A member in this server.")
    async def kill(self, interaction: discord.Interaction, user: discord.Member):
        user_nick = self.mname(user)
        author_nick = self.mname(interaction.user)
        if user == self.bot.user:
            return await interaction.response.send_message(
                ":regional_indicator_n::regional_indicator_o::regional_indicator_p::regional_indicator_e::exclamation: I shall not kill myself!"
            )
        if user == interaction.user:
            return await interaction.response.send_message(
                ":x: If you want to kill yourself, you should use `/suicide`"
            )
        if "💀" in user_nick:
            return await interaction.response.send_message(
                ":x: That member is already dead."
            )
        if "💀" in author_nick:
            return await interaction.response.send_message(
                ":x: How are you going to kill someone if YOU are dead?"
            )
        em = discord.Embed(
            description=f":skull: **{user.mention} has been killed by {interaction.user.mention}!** :skull_crossbones:",
            color=transparent_color,
        )
        amongus_gifs = [
            "https://media.tenor.com/F__GSvFsf20AAAAC/among-us-kill.gif",
            "https://media.tenor.com/Zi1l60KaBGMAAAAC/among-us-kill.gif",
            "https://media.tenor.com/0l5kHLfHhhgAAAAC/among-us.gif",
        ]
        em.set_image(url=random.choice(amongus_gifs))

        # If the nick is longer than 31 characters (limit is 32), the skull cannot be added, send just the message instead
        if len(user_nick) > 31:
            return await interaction.response.send_message(embed=em)
        try:
            await user.edit(nick=f"💀{user_nick}")
        except discord.errors.Forbidden:
            pass
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Respawn a dead member.")
    @app_commands.describe(user="A member in this server.")
    async def respawn(self, interaction: discord.Interaction, user: discord.Member):
        nick = self.mname(user)
        if user == interaction.user:
            return await interaction.response.send_message(
                ":x: You can't respawn yourself, that's not how it works..."
            )
        if "💀" in nick:
            new_name = nick.replace("💀", "")
            await user.edit(nick=new_name)
            em = discord.Embed(color=transparent_color)
            em.description = (
                f":innocent: **Welcome back, {user.mention}.** You have been respawned!"
            )
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(
                f":x: {user.mention} is not even dead, mate."
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

    # COMMAND WITH CHOICES -------------------------------------------------------
    # @app_commands.command(description="Testing command.")
    # @app_commands.choices(choice=[
    #     app_commands.Choice(name="Rock", value="rock"),
    #     app_commands.Choice(name="Paper", value="paper"),
    #     app_commands.Choice(name="Scissors", value="scissors")
    # ])
    # async def test(self, interaction: discord.Interaction, choice: str):
    #     await interaction.response.send_message(f"{choice} is a good choice!")
    # ----------------------------------------------------------------------------

    @app_commands.command(description="Play a game of Rock, Paper, Scissors.")
    async def rps(self, interaction: discord.Interaction):
        em = discord.Embed(
            title="Rock, Paper, Scissors",
            description="Click on your choice below! Then I'll make mine.",
        )
        await interaction.response.send_message(embed=em)

        view = RPSView(timeout=300.0)
        message = await interaction.channel.send(view=view)
        view.message = message
        await view.wait()
        if view.choice == "quit":
            return await interaction.delete_original_response()
        await view.disable_all_items()
        # If no one made a choice, and the game timed out, then just return
        if view.choice is None:
            return

        def comparison(user_choice, bot_choice):
            if user_choice == bot_choice:
                return "tie"
            elif user_choice == "rock" and bot_choice == "scissors":
                return "win"
            elif user_choice == "paper" and bot_choice == "rock":
                return "win"
            elif user_choice == "scissors" and bot_choice == "paper":
                return "win"
            else:
                return "loss"

        def end_message(user, user_choice, bot_choice):
            em = discord.Embed()
            if comparison(user_choice, bot_choice) == "tie":
                em.description = f"{user.mention}**, it's a TIE!**"
            elif comparison(user_choice, bot_choice) == "win":
                em.description = f"{user.mention}**, you WON!**"
                em.color = discord.Colour.brand_green()
            else:
                em.description = f"{user.mention}**, you LOST!**"
                em.color = discord.Colour.red()
            return em

        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "rock":
            bot_emoji = ":fist:"
        elif bot_choice == "paper":
            bot_emoji = ":hand_splayed:"
        else:
            bot_emoji = ":v:"
        await asyncio.sleep(3)
        await interaction.channel.send(f"> I choose **{bot_choice}** {bot_emoji}")
        await asyncio.sleep(3)

        em = end_message(view.user, view.choice, bot_choice)
        await interaction.channel.send(embed=em)

    @app_commands.command(description="Annoy a member in the server.")
    @app_commands.describe(user="A member in this server.")
    @app_commands.describe(
        times="How many times you want to annoy them. Defaults to 1."
    )
    async def annoy(
        self, interaction: discord.Interaction, user: discord.Member, times: int = 1
    ):
        if times > 20:
            return await interaction.response.send_message(":x: Max 20 times.")
        if user in annoyed_members:
            return await interaction.response.send_message(
                ":x: That member is already being annoyed."
            )
        if times <= 0:
            return await interaction.response.send_message(":x: Positive numbers only.")
        nick = self.mname(user)
        minutes = round((30 * times) / 60, 1)
        if times == 1:
            start_msg = f":white_check_mark: Annoyed {nick}"
            end_msg = None
        elif times > 1:
            start_msg = f":white_check_mark: Started annoying {nick} (**{times}** times)"
            end_msg = (
                f":white_check_mark: Done annoying {user.mention} • `{minutes}min`"
            )
        with open("cogs/text/bad_words.txt", "r") as file:
            bad_words = [line.rstrip("\n") for line in file]
            file.close()
        annoyed_members.append(user)
        await interaction.response.send_message(start_msg)
        for i in range(0, times):
            word = random.choice(bad_words)
            await user.send(
                f"**{i + 1}** • I was sent here to annoy you by {interaction.user.mention}, **{word}**."
            )
            if not i == times - 1:  # If not done yet
                await asyncio.sleep(30)
        if end_msg:
            await interaction.channel.send(end_msg)
        annoyed_members.remove(user)

    @commands.command()
    async def sound(self, ctx, option, repeat: int = 0):
        sounds_path = "cogs/sounds/"
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

        def soundobj(sound):
            return discord.FFmpegPCMAudio(sounds_path + sound)

        async def playsound(file, repeat, duration=None):
            if repeat == 0:
                vc.play(soundobj(file))
            else:
                for i in range(0, repeat):
                    vc.play(soundobj(file))
                    await asyncio.sleep(duration)
                    vc.stop()
            await asyncio.sleep(duration)

        vc = await channel.connect()
        await ctx.send(f":white_check_mark: *Playing sound* `{options[option]}`")

        if option == "1":  # duration 8.2
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

    @app_commands.command(description="Get a random fact.")
    async def fact(self, interaction: discord.Interaction):
        with open("cogs/text/facts.txt", "r") as file:
            facts = [line.rstrip("\n") for line in file]
            file.close()
        fact = random.choice(facts)
        await interaction.response.send_message(fact)

    @app_commands.command(
        description="Ship two members in this server. Love is in the air!"
    )
    @app_commands.describe(user1="A member in this server.")
    @app_commands.describe(user2="A member in this server")
    async def ship(
        self,
        interaction: discord.Interaction,
        user1: discord.Member,
        user2: discord.Member,
    ):
        nick1 = self.mname(user1)
        nick2 = self.mname(user2)
        half_index1 = int(len(nick1) / 2)
        half1 = nick1[:half_index1]
        half_index2 = int(len(nick2) / 2)
        half2 = nick2[half_index2:]
        ship_name = (half1 + half2).strip()
        em = discord.Embed(
            title=f":heart: I ship {nick1} and {nick2} :heart:",
            description=f"\u200b\n:two_hearts::revolving_hearts: **{ship_name}** :revolving_hearts::two_hearts:\n\u200b",
            color=transparent_color,
        )
        love_gifs = [
            "https://media3.giphy.com/media/3o7TKoWXm3okO1kgHC/giphy.gif",
            "https://media1.giphy.com/media/3CCXHZWV6F6O9VQ7FL/giphy.gif",
            "https://media0.giphy.com/media/l0K4kWJir91VEoa1W/giphy.gif",
            "https://media0.giphy.com/media/l0HlGdXFWYbKv5rby/giphy.gif",
        ]
        em.set_image(url=random.choice(love_gifs))
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Use at your own discretion.")
    async def cum(self, interaction: discord.Interaction):
        global on_cooldown
        if on_cooldown is True:
            return await interaction.response.send_message(
                ":x: Go easy on yourself. Please wait before cumming again."
            )
        else:
            on_cooldown = True
            timer = threading.Timer(30.0, self.cooldown_timer)
            timer.start()
        await asyncio.sleep(2)
        await interaction.response.send_message("**Fase 1: Iniciación** :smiling_imp:")
        await interaction.channel.send(
            "https://tenor.com/view/he-hehe-boy-boi-boyi-gif-7890844"
        )
        await asyncio.sleep(5)
        await interaction.channel.send("**Fase 2: Excitación** :flushed:")
        await interaction.channel.send(
            "https://tenor.com/view/hmm-sulley-monsters-inc-james-sullivan-shocked-gif-15802869"
        )
        await asyncio.sleep(5)
        await interaction.channel.send("**Fase 3: Finalización** :sunglasses:")
        await interaction.channel.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:CUM:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await interaction.channel.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:AHHHHH IM COOOMING:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await interaction.channel.send(
            """
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:FUCK:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:SEX:sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:
:sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops::sweat_drops:"""
        )
        await asyncio.sleep(10)
        await interaction.channel.send("**5 minutos después:**")
        await interaction.channel.send(
            "https://tenor.com/view/wazowski-mike-mike-sulivan-meme-monster-inc-gif-19634164"
        )


async def setup(bot):
    await bot.add_cog(Fun(bot))
