from discord.ext import commands
import discord
import asyncio
import random
import json
import os


PATH = os.path.dirname(__file__)


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, amount: int):
        if ctx.author.id == 306542879520849922 and amount > random.randint(10, 16):
            return
        if amount > 100:
            return await ctx.send(":x: I can delete max 100 messages.")
        elif amount <= 0:
            return await ctx.send(
                ":x: How am I supposed to delete " + "`{}` messages?".format(amount)
            )

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
                title=":x: I can't delete messages in this channel...",
                description="""
Possible reasons:
⊳ I need the **Manage Messages** permission.
⊳ I need the **Read Message History** permission.""",
                color=discord.Colour.red(),
            )
            await ctx.send(embed=em)

    @commands.command()
    async def timer(self, ctx, secs: int):
        clocks = "🕛 🕐 🕑 🕒 🕓 🕔 🕕 🕖 🕗 🕘 🕙 🕚".split()
        clock_index = 0
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        msg = await ctx.send("`%02d:%02d:%02d` 🕛" % (h, m, s))

        while secs != 0:
            secs -= 1
            clock_index += 1
            if clock_index == 12:
                clock_index = 0
            if secs == 0:
                await msg.edit(content="`00:00:00` :white_check_mark:")
                await ctx.send(f"{ctx.author.mention} The timer has finished.")
            else:
                m, s = divmod(secs, 60)
                h, m = divmod(m, 60)
                await msg.edit(
                    content="`%02d:%02d:%02d` %s" % (h, m, s, clocks[clock_index])
                )
                await asyncio.sleep(1)

    @commands.command()
    async def calc(self, ctx, *, expr):
        expr = "".join(expr)
        try:
            result = eval(expr)
            await ctx.send("`{}`".format(result))
        except:
            await ctx.send(
                ":x: I couldn't calculate that, " + "I'm sure it's your fault."
            )

    @commands.command()
    async def flip(self, ctx):
        side = random.choice(["heads", "tails"])
        await ctx.channel.typing()
        await asyncio.sleep(2)
        await ctx.send("I flipped a coin and it landed on **{}**.".format(side))

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
                title=f"Tag list ({amount})", description=tag_list, color=0xFF2B29
            )
            await ctx.send(embed=em)

        else:
            if option not in tags_json["tags"]:
                return await ctx.send(":x: That tag doesn't exist.")
            await ctx.send(tags_json["tags"][option])


async def setup(bot):
    await bot.add_cog(Utilities(bot))
