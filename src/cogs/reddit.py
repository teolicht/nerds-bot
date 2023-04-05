from discord import app_commands
from discord.ext import commands
import discord
import asyncpraw
import asyncprawcore
import random
import os
import threading
import json

with open("cogs/text/config.json", "r") as file:
    reddit_json = json.load(file)["reddit"]
    file.close()
ban_cooldown = []

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=reddit_json["client_id"],
            client_secret=reddit_json["client_secret"],
            password=reddit_json["password"],
            user_agent=reddit_json["username"],
            username=reddit_json["username"],
        )
    
    def ban_done(self, sub):
        ban_cooldown.remove(sub)

    # async def close(self):
    #     await self.reddit.close()

    # async def fetch_post(self, choice: str):
    #     submissions = []
    #     self.subreddit = await self.reddit.subreddit(choice)
    #     async for submission in self.subreddit.hot(limit=25):
    #         submissions.append(submission)
    #     return random.choice(submissions)

    # Remaking reddit commands #################################################################
    # @app_commands.Group
    # @app_commands.command(description="Reddit commands.")
    # @app_commands.choices(option=[
    #     app_commands.Choice(name="ban", value="ban"),
    #     app_commands.Choice(name="unban", value="unban"),
    #     app_commands.Choice(name="banlist", value="banlist")
    # ])
    # async def reddit(self, interaction: discord.Interaction, option: str, subreddit: str = None):
    #     await interaction.response.send_message(f"You have chosen to {option} {subreddit}")

    # @app_commands.command(description="Get a random post from a subreddit.")
    # @app_commands.describe(subreddit="The name of the subreddit.")
    # async def subreddit(self, interaction: discord.Interaction, subreddit: str):
    #     post = await self.fetch_post(subreddit)
    #     print(f"https://www.reddit.com{post.permalink}")

    @commands.command()
    async def reddit(self, ctx, option, subreddit=None):
        with open("cogs/text/text.json", "r") as file:
            subs_json = json.load(file)
            file.close()

        if option == "ban":
            if subreddit is None:
                await ctx.send(
                    ":x: Specify the subreddit.\nCommand usage: `n!reddit ban <subreddit>`"
                )
            elif subreddit in subs_json["bannedsubs"]:
                await ctx.send(":x: That subreddit is already banned.")
            else:
                subs_json["bannedsubs"].append(subreddit)
                with open("cogs/text/text.json", "w") as file:
                    json.dump(subs_json, file, indent=4)
                    file.close()
                await ctx.send(":white_check_mark: Banned ``r/{}``".format(subreddit))
                ban_cooldown.append(subreddit)
                timer = threading.Timer(600.0, self.ban_done, args=[subreddit])
                timer.start()

        elif option == "unban":
            if subreddit is None:
                await ctx.send(
                    ":x: Specify the subreddit.\nCommand usage: `n!reddit unban <subreddit>`"
                )
            elif subreddit not in subs_json["bannedsubs"]:
                await ctx.send(":x: That subreddit isn't even banned.")
            elif subreddit in ban_cooldown:
                await ctx.send(":x: Please wait before unbanning that subreddit.")
            else:
                subs_json["bannedsubs"].remove(subreddit)
                with open("cogs/text/text.json", "w") as file:
                    json.dump(subs_json, file, indent=4)
                    file.close()
                await ctx.send(":white_check_mark: Unbanned ``r/{}``".format(subreddit))

        elif option == "banlist":
            subs_list = subs_json["bannedsubs"]
            try:
                blank_line = "\u200b" * 22
                subs_print = [f"{blank_line}\n"]
                amount = 0
                for sub in subs_list:
                    amount += 1
                    subs_print.append(f"**{amount}.** {sub}\n")
                subs_print = "".join(subs_print)
                em = discord.Embed(
                    title="Banned subreddits ({})".format(amount),
                    color=0xFF2B29,
                    description=subs_print,
                )
                await ctx.send(embed=em)
            except discord.errors.HTTPException:
                ####### This only separates the list in 2. Hardcoding. What if more than two is needed?
                half_list = len(subs_list) / 2
                half_list = int(round(half_list, 0))
                # First half of the list
                subs_print_1 = [f"{blank_line}\n"]
                amount = 0
                for sub in subs_list[:half_list]:
                    amount += 1
                    subs_print_1.append(f"**{amount}.** {sub}\n")
                subs_print_1 = "".join(subs_print_1)
                # Second half of the list
                subs_print_2 = [f"{blank_line}\n"]
                for sub in subs_list[half_list:]:
                    amount += 1
                    subs_print_2.append(f"**{amount}.** {sub}\n")
                subs_print_2 = "".join(subs_print_2)

                em_1 = discord.Embed(
                    title="Banned subreddits ({})".format(amount),
                    color=0xFF2B29,
                    description=subs_print_1,
                )
                em_2 = discord.Embed(color=0xFF2B29, description=subs_print_2)
                await ctx.send(embed=em_1)
                await ctx.send(embed=em_2)

        else:
            if option in subs_json["bannedsubs"]:
                return await ctx.send(":x: That subreddit is banned.")
            try:
                self.reddit.subreddits.search_by_name(option, exact=True)
            except asyncprawcore.exceptions.NotFound:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            except discord.errors.HTTPException:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            except asyncprawcore.exceptions.Forbidden:
                return await ctx.send(":x: Private subreddit.")
            try:
                subreddit = await self.reddit.subreddit(option)
                submissions = []
                async for post in subreddit.hot(limit=25):
                    submissions.append(post)
                if submissions == []:
                    return await ctx.send(":x: That subreddit is empty.")
                post = random.choice(submissions)

                em = discord.Embed(
                    title=post.title, url="https://www.reddit.com" + post.permalink
                )
                em.set_footer(text="u/{0.author.name} • {0.ups} points".format(post))
                em.set_author(name=post.subreddit_name_prefixed)
                if post.selftext:
                    em.description = post.selftext
                elif post.url.endswith(("jpg", "png")):
                    em.set_image(url=post.url)
                else:
                    em.description = post.url
                await ctx.send(embed=em)
            except discord.errors.HTTPException:
                em.description = post.url
                await ctx.send(embed=em)
            except (
                asyncprawcore.exceptions.NotFound,
                asyncprawcore.exceptions.Redirect,
            ):
                await ctx.send(":x: I wasn't able to find that subreddit.")
            except asyncprawcore.exceptions.Forbidden:
                await ctx.send(":x: Private subreddit.")


async def setup(bot):
    await bot.add_cog(Reddit(bot))
