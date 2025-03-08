import asyncio
import random
import json
import threading
import discord

from discord.ext import commands
from discord import app_commands


delete_cooldown: dict[str, int] = {}


class Timer(discord.ui.View):
    paused = False
    pause_user = None
    canceled = False
    cancel_user = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable_all_items()

    @discord.ui.button(label="Pause/Resume", style=discord.ButtonStyle.success)
    async def pause_resume(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
            self.pause_user = interaction.user
        await interaction.response.defer()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.disable_all_items()
        self.canceled = True
        self.cancel_user = interaction.user


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def delete_cooldown_done(self, user_id, amount):
        delete_cooldown[user_id] -= amount

    @app_commands.command(description="Delete messages in the channel.")
    @app_commands.describe(amount="Number of messages to delete.")
    async def delete(self, interaction: discord.Interaction, amount: int):
        user_id = str(interaction.user.id)
        if amount > 30:
            return await interaction.response.send_message(
                ":x: Each user can delete max 30 messages per minute."
            )
        elif amount <= 0:
            return await interaction.response.send_message(
                f":x: How am I supposed to delete `{amount}` messages?"
            )
        if user_id in delete_cooldown:
            if delete_cooldown[user_id] + amount > 30:
                return await interaction.response.send_message(
                    ":x: That exceeds your 30 messages per minute limit. Please wait."
                )
            else:
                delete_cooldown[user_id] += amount
        else:
            delete_cooldown[user_id] = amount
            timer = threading.Timer(
                60.0, self.delete_cooldown_done, args=[user_id, amount]
            )
            timer.start()

        msgs_to_delete: list[discord.Message] = []
        async for msg in interaction.channel.history(limit=amount):
            msgs_to_delete.append(msg)
        await interaction.response.send_message(
            f":recycle: `{len(msgs_to_delete)}` message(s) deleted.", delete_after=5.0
        )
        await interaction.channel.delete_messages(msgs_to_delete)

    @app_commands.command(description="Start a timer.")
    @app_commands.describe(secs="Duration of the timer (in seconds).")
    async def timer(self, interaction: discord.Interaction, secs: int):
        start_utc = discord.utils.utcnow()
        clocks = "🕛 🕐 🕑 🕒 🕓 🕔 🕕 🕖 🕗 🕘 🕙 🕚".split()
        clock_index = 0
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)

        # Initial messages
        view = Timer(timeout=None)
        em = discord.Embed(title="`%02d:%02d:%02d` 🕛" % (h, m, s))
        await interaction.response.send_message(embed=em)
        view.timer_message = await interaction.original_response()
        view.message = await interaction.channel.send(view=view)

        # Main loop
        while secs > 0:
            if view.canceled:
                em.color = discord.Colour.red()
                em.title = "`%02d:%02d:%02d` :x:" % (h, m, s)
                em.description = f"Timer canceled by {view.cancel_user.mention}"
                return await interaction.edit_original_response(embed=em)
            if view.paused:
                em.title = "`%02d:%02d:%02d` :pause_button:" % (h, m, s)
                em.description = f"Timer paused by {view.pause_user.mention}"
                await interaction.edit_original_response(embed=em)
            else:
                secs -= 1
                clock_index += 1
                if clock_index == 12:
                    clock_index = 0
                m, s = divmod(secs, 60)
                h, m = divmod(m, 60)
                em.title = "`%02d:%02d:%02d` %s" % (h, m, s, clocks[clock_index])
                em.description = None
                await interaction.edit_original_response(embed=em)
                if not view.paused and not view.canceled:
                    await asyncio.sleep(1)

        # When timer completes
        start_time = discord.utils.format_dt(start_utc)
        em.title = "`00:00:00` :white_check_mark:"
        em.color = discord.Colour.brand_green()
        await interaction.edit_original_response(embed=em)
        await view.disable_all_items()
        return await interaction.channel.send(
            f":bell:  The timer started by {interaction.user.mention} on {start_time} has finished."
        )

    @app_commands.command(description="Solve a math expression.")
    @app_commands.describe(expression="The math expression. Example: '3 + 10 / 2'")
    async def calc(self, interaction: discord.Interaction, expression: str):
        try:
            result = eval(expression)
            await interaction.response.send_message("`{}`".format(result))
        except:
            await interaction.response.send_message(
                ":x: I couldn't calculate that, I'm sure it's your fault."
            )

    @commands.command()
    async def flip(self, ctx):
        side = random.choice(["heads", "tails"])
        await ctx.channel.typing()
        await asyncio.sleep(2)
        await ctx.send(":coin: I flipped a coin and it landed on **{}**.".format(side))

    @app_commands.command(description="Pick a random number between a min and a max.")
    @app_commands.describe(minimum="The smallest number in the range.")
    @app_commands.describe(maximum="The largest number in the range.")
    async def randnum(
        self, interaction: discord.Interaction, minimum: int, maximum: int
    ):
        if minimum > maximum:
            return await interaction.response.send_message(
                ":x: Your first number must be smaller than your second number.",
                ephemeral=True,
            )
        number = random.randint(minimum, maximum)
        em = discord.Embed(title=number)
        await interaction.response.send_message(
            f"A number between `{minimum}` and `{maximum}`:", embed=em
        )

    @app_commands.command(description="Choose from a list of options.")
    @app_commands.describe(
        options="The options you want to randomly choose from. Separate with comma."
    )
    async def choose(self, interaction: discord.Interaction, options: str):
        options = options.split(",")
        if "" in options:
            options.remove("")
        chosen_option = random.choice(options)
        em = discord.Embed(description="*List:* " + ", ".join(options))
        em.set_footer(text="Choosing...")
        await interaction.response.send_message(embed=em)

        # Simulate bot is choosing between the options
        await asyncio.sleep(2)

        for x, option in enumerate(options):
            if option == chosen_option:
                options[x] = f"**> {option} <**"
        em.description = "*List:* " + ", ".join(options)
        em.set_footer(text=f"✅ Chosen: {chosen_option.strip()}")
        await interaction.edit_original_response(embed=em)

    @app_commands.command(description="Create an invite link for this server.")
    @app_commands.describe(
        duration="Duration (in seconds), after which the link will no longer be valid."
    )
    @app_commands.describe(uses="Maximum amount of times the link can be used.")
    async def invite(
        self, interaction: discord.Interaction, duration: int = 0, uses: int = 0
    ):
        invite_link = await interaction.channel.create_invite(
            max_age=duration,
            max_uses=uses,
            reason=f"Invite requested by {interaction.user.name}",
        )
        await interaction.response.send_message(f"There you go!\n**{invite_link}**")

    # This command shall be rewritten and moved to utilities cog

    @commands.command()
    async def poll(
        # fmt: off
        self, ctx, question, duration: int, option1, option2,
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
        options = [option for option in initial_options if option]
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
        em.set_author(
            name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar
        )
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
                if user != self.bot.user:
                    for x, voter in enumerate(voters):
                        if reaction.emoji == reactions[x]:
                            numbers[x] += 1
                            voter.append(user.mention)

        highest_nums = [num for num in numbers if num == max(numbers)]
        if len(highest_nums) > 1:
            winner_option = False
            try:
                tie_options = [
                    options[x]
                    for x, num in enumerate(numbers)
                    if num == highest_nums[0]
                ]
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
                    "".join(total), winner_option
                ),
            )
        else:
            em = discord.Embed(
                title=question, description="__Result__{}".format("".join(total))
            )
        em.set_author(
            name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar
        )
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
                    "".join(total), tie_winner
                ),
            )
            em.set_author(
                name=f"{ctx.author.name}'s poll", icon_url=ctx.author.display_avatar
            )
            em.set_footer(text="❌ This poll has ended.")
            await react_msg.edit(embed=em)


class Tags(app_commands.Group):
    def tags_json(self, mode, new_content=None):
        if mode == "r":
            with open("cogs/text/tags.json", "r") as file:
                tags_json = json.load(file)
                file.close()
                return tags_json
        else:
            with open("cogs/text/tags.json", "w") as file:
                json.dump(new_content, file, indent=4)
                file.close()

    async def tag_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id in tags_json:
            tags = tags_json[guild_id]
            choices = [tag for tag in tags]
            return [
                app_commands.Choice(name=choice, value=choice)
                for choice in choices
                if current.lower() in choice.lower()
            ]

    ### test all these list comprehensions
    @app_commands.command(description="Create a new tag.")
    @app_commands.describe(name="The tag's name.")
    @app_commands.describe(content="The tag's content.")
    async def create(self, interaction: discord.Interaction, name: str, content: str):
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id in tags_json:
            if name in tags_json[guild_id]:
                return await interaction.response.send_message(
                    ":x: A tag with that name already exists.", ephemeral=True
                )
            tags_json[guild_id][name] = content
        else:
            tags_json[guild_id] = {}
            tags_json[guild_id][name] = content
        self.tags_json("w", new_content=tags_json) 
        await interaction.response.send_message(
            f":white_check_mark: Tag `{name}` created successfully."
        )

    @app_commands.command(description="Delete a saved tag.")
    @app_commands.describe(name="The tag's name.")
    @app_commands.autocomplete(name=tag_autocomplete)
    async def delete(self, interaction: discord.Interaction, name: str):
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id not in tags_json:
            return await interaction.response.send_message(
                ":x: This server doesn't have any saved tags.", ephemeral=True
            )
        if name not in tags_json[guild_id]:
            return await interaction.response.send_message(
                ":x: That tag doesn't exist.", ephemeral=True
            )
        tags_json[guild_id].pop(name)
        self.tags_json("w", new_content=tags_json)
        await interaction.response.send_message(
            f":white_check_mark: Deleted tag `{name}`"
        )

    @app_commands.command(description="Edit a saved tag.")
    @app_commands.describe(name="The tag's name.")
    @app_commands.describe(content="The tag's new content. Replaces the old.")
    @app_commands.autocomplete(name=tag_autocomplete)
    async def edit(self, interaction: discord.Interaction, name: str, content: str):
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id not in tags_json:
            return await interaction.response.send_message(
                ":x: This server doesn't have any saved tags.", ephemeral=True
            )
        if name not in tags_json[guild_id]:
            return await interaction.response.send_message(
                ":x: That tag doesn't exist.", ephemeral=True
            )
        tags_json[guild_id][name] = content
        self.tags_json("w", new_content=tags_json)
        await interaction.response.send_message(
            f":white_check_mark: Tag `{name}` edited successfully."
        )

    @app_commands.command(description="List of saved tags.")
    async def list(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id not in tags_json:
            return await interaction.response.send_message(
                ":x: This server doesn't have any saved tags.", ephemeral=True
            )
        tag_list = ""
        for x, tag in enumerate(tags_json[guild_id]):
            tag_list += f"**{x + 1}.** {tag}\n"
        if tag_list == "":
            em = discord.Embed(description="*This server has no saved tags.*")
        else:
            em = discord.Embed(
                title=f"Saved tags ({len(tags_json[guild_id])})", description=tag_list
            )
        em.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Show a saved tag.")
    @app_commands.describe(name="The tag's name.")
    @app_commands.autocomplete(name=tag_autocomplete)
    async def show(self, interaction: discord.Interaction, name: str):
        # A way to put these 6 following lines into a function, since they got repeated multiple times?
        guild_id = str(interaction.guild.id)
        tags_json = self.tags_json("r")
        if guild_id not in tags_json:
            return await interaction.response.send_message(
                ":x: This server doesn't have any saved tags.", ephemeral=True
            )
        if name not in tags_json[guild_id]:
            return await interaction.response.send_message(
                ":x: That tag doesn't exist.", ephemeral=True
            )
        await interaction.response.send_message(tags_json[guild_id][name])


async def setup(bot):
    bot.tree.add_command(Tags(name="tag", description="Tag commands."))
    await bot.add_cog(Utilities(bot))
