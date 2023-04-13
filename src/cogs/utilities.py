import asyncio
import random
import json
import threading
import discord
from discord.ext import commands, tasks
from discord import app_commands


transparent_color = 0x302C34
delete_cooldown = {}


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

        msgs_to_delete = []
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
            await interaction.respo.send_message("`{}`".format(result))
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

    @commands.command()
    async def randnum(self, ctx, min: int, max: int):
        if min > max:
            return await ctx.send(
                f":x: Your first number ({min}) must be "
                + f"smaller than your second number ({max})."
            )

        number = random.randint(min, max)
        await ctx.send("`{}`".format(number))

    @commands.command()
    async def choose(self, ctx, *, choices):
        choices = choices.split()
        choice = random.choice(choices)
        return await ctx.send(choice)

    @commands.command()
    async def tag(self, ctx, option, name=None, *, content=None):
        with open("cogs/text/text.json", "r") as file:
            tags_json = json.load(file)
            file.close()

        if option == "create":
            if name is None:
                return await ctx.send(":x: Please specify the tag's name.")
            if name in ["create", "delete", "edit", "list"]:
                return await ctx.send(":x: You cannot create a tag with that name.")
            if name in tags_json["tags"]:
                return await ctx.send(":x: That tag already exists.")
            if content is None:
                return await ctx.send(":x: Please enter some content for the tag.")
            content = "".join(content)
            tags_json["tags"][name] = content
            with open("cogs/text/text.json", "w") as file:
                json.dump(tags_json, file, indent=4)
                file.close()
            await ctx.send(":white_check_mark: Created tag sucessfully.")

        elif option == "delete":
            if name is None:
                return await ctx.send(":x: Please specify the tag's name.")
            if name not in tags_json["tags"]:
                await ctx.send(":x: That tag doesn't exist.")
            tags_json["tags"].pop(name)
            with open("cogs/text/text.json", "w") as file:
                json.dump(tags_json, file, indent=4)
                file.close()
            await ctx.send(":white_check_mark: Deleted tag successfully.")

        elif option == "edit":
            if name is None:
                return await ctx.send(":x: Please specify the tag's name.")
            if name not in tags_json["tags"]:
                return await ctx.send(":x: That tag doesn't exist.")
            if content is None:
                return await ctx.send(":x: Please enter some content for the tag.")
            content = "".join(content)
            tags_json["tags"][name] = content
            with open("cogs/text/text.json", "w") as file:
                json.dump(tags_json, file, indent=4)
                file.close()
            await ctx.send(":white_check_mark: Edited tag sucessfully.")

        elif option == "list":
            amount = 0
            tag_list = ""
            for tag in tags_json["tags"]:
                amount += 1
                tag_list += f"**{amount}.** {tag}\n"
            em = discord.Embed(
                title=f"Tag list ({amount})",
                description=tag_list,
                color=transparent_color,
            )
            await ctx.send(embed=em)

        else:
            if option not in tags_json["tags"]:
                return await ctx.send(":x: That tag doesn't exist.")
            await ctx.send(tags_json["tags"][option])

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


async def setup(bot):
    await bot.add_cog(Utilities(bot))
