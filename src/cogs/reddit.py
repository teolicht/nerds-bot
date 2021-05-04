from discord.ext import commands
import discord
import asyncpraw as praw
import asyncprawcore
import random
import os
import threading
import json


REDDIT = json.load(open(os.path.join(os.path.dirname(__file__), "text", "config.json"), 'r'))["reddit"]
r = praw.Reddit(client_id=REDDIT["client_id"], client_secret=REDDIT["client_secret"], 
                password=REDDIT["password"], user_agent=REDDIT["username"], username=REDDIT["username"])
SUBS_PATH = os.path.join(os.path.dirname(__file__), "text", "bannedsubs.txt")
ban_cooldown = []

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ban_done(self, sub):
        ban_cooldown.remove(sub)

    @commands.command()
    async def reddit(self, ctx, option, subreddit=None):
        subs = open(SUBS_PATH, "r")
        subs_list = subs.read().split(",")

        if option == "ban":
            if subreddit is None:
                await ctx.send(":x: Specify the subreddit.\nCommand usage: `n!reddit ban <subreddit>`")
            elif subreddit in subs_list:
                await ctx.send(":x: That subreddit is already banned.")
            else:
                subs = open(SUBS_PATH, "a+")
                subs.write(subreddit + ",")
                subs.close()
                await ctx.send(":white_check_mark: Banned ``r/{}``".format(subreddit))

                ban_cooldown.append(subreddit)
                timer = threading.Timer(600.0, self.ban_done, args=[subreddit])
                timer.start()

        elif option == "unban":
            subs.close()
            if subreddit is None:
                await ctx.send(":x: Specify the subreddit.\nCommand usage: `n!reddit unban <subreddit>`")
            elif subreddit not in subs_list:
                await ctx.send(":x: That subreddit isn't even banned.")
            elif subreddit in ban_cooldown:
                await ctx.send(":x: Please wait before unbanning that subreddit.")
            else:
                subs_list.remove(subreddit)
                subs = open(SUBS_PATH, "w")
                subs.write(",".join(subs_list))
                subs.close()
                await ctx.send(":white_check_mark: Unbanned ``r/{}``".format(subreddit))

        elif option == "banlist":
            try:
                amount = 0
                subs_print = []
                for sub in subs_list:
                    amount += 1
                    subs_print.append(f"**{amount}.** {sub}\n")
                subs_print = "".join(subs_print[:-1]) # [:-1] is to exclude \n in last line
                em = discord.Embed(title="Banned subreddits ({})".format(len(subs_list) - 1),
                                   color=0xff2b29, description=subs_print)
                await ctx.send(embed=em)
            except discord.errors.HTTPException:
                half_list = len(subs_list) / 2 # Middle point of the list as an int
                half_list = int(round(half_list, 0))
                # First half of the list
                amount_1 = 0
                subs_print_1 = []
                for sub in subs_list[:half_list]:
                    amount_1 += 1
                    subs_print_1.append(f"**{amount_1}.** {sub}\n")
                subs_print_1 = "".join(subs_print_1[:-1]) # [:-1] is to exclude \n in last line
                # Second half of the list
                amount_2 = amount_1
                subs_print_2 = []
                for sub in subs_list[half_list:]:
                    amount_2 += 1
                    subs_print_2.append(f"**{amount_2}.** {sub}\n")
                subs_print_2 = "".join(subs_print_2[:-1]) # [:-1] is to exclude \n in last line

                em_1 = discord.Embed(title="Banned subreddits ({})".format(len(subs_list) - 1),
                                     color=0xff2b29, description=subs_print_1)
                em_2 = discord.Embed(color=0xff2b29, description=subs_print_2)
                await ctx.send(embed=em_1)
                await ctx.send(embed=em_2)

        else:
            if option in subs_list:
                return await ctx.send(":x: That subreddit is banned.")
            try:
                r.subreddits.search_by_name(option, exact=True)
            except asyncprawcore.exceptions.NotFound:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            except discord.errors.HTTPException:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            except asyncprawcore.exceptions.Forbidden:
                return await ctx.send(":x: Private subreddit.")
            try:
                subreddit = await r.subreddit(option)
                submissions = []
                async for post in subreddit.hot(limit=100):
                    submissions.append(post)
                if submissions == []:
                    return await ctx.send(":x: That subreddit is empty.")
                post = random.choice(submissions)

                em = discord.Embed(title=post.title,
                                   url='https://www.reddit.com' + post.permalink)
                em.set_footer(text='u/{0.author.name} • {0.ups} points'.format(post))
                em.set_author(name=post.subreddit_name_prefixed)
                if post.selftext:
                    em.description = post.selftext
                elif post.url.endswith(('jpg', 'png')):
                    em.set_image(url=post.url)
                else:
                    em.description = post.url
                await ctx.send(embed=em)
            except discord.errors.HTTPException:
                em.description = post.url
                await ctx.send(embed=em)
            except (asyncprawcore.exceptions.NotFound, asyncprawcore.exceptions.Redirect):
                await ctx.send(":x: I wasn't able to find that subreddit.")
            except asyncprawcore.exceptions.Forbidden:
                await ctx.send(":x: Private subreddit.")


def setup(bot):
    bot.add_cog(Reddit(bot))
