from discord.ext import commands
import discord
import praw, prawcore
import random
import os
from .config import Reddit

r = praw.Reddit(client_id=Reddit.client_id,
                client_secret=Reddit.client_secret, password=Reddit.password,
                user_agent="teodorlicht", username=Reddit.username)
subs_path = os.path.join(os.path.join(os.path.dirname(__file__), "text/bannedsubs.txt"))

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, ctx, option, subreddit=None):
        subs = open(subs_path, "r")
        subs_list = subs.read().split(",")

        if option == "ban":
            if subreddit is None:
                await ctx.send(":x: Specify the subreddit.\nCommand usage: `n!reddit ban <subreddit>`")
            elif subreddit in subs_list:
                await ctx.send(":x: That subreddit is already banned.")
            else:
                subs = open(subs_path, "a+")
                subs.write(subreddit + ",")
                subs.close()
                await ctx.send(":white_check_mark: Banned ``r/{}``".format(subreddit))

        elif option == "unban":
            subs.close()
            if subreddit is None:
                await ctx.send(":x: Specify the subreddit.\nCommand usage: `n!reddit unban <subreddit>`")
            elif subreddit not in subs_list:
                await ctx.send(":x: That subreddit isn't even banned.")
            else:
                subs_list.remove(subreddit)
                subs = open(subs_path, "w")
                subs.write(",".join(subs_list))
                subs.close()
                await ctx.send(":white_check_mark: Unbanned ``r/{}``".format(subreddit))

        elif option == "banlist":
            amount = 0
            subs_print = []
            for sub in subs_list:
                amount += 1
                subs_print.append(f"**{amount}.** {sub}\n")
            subs_print = "".join(subs_print[:-1])
            if subs_print == "":
                await ctx.send("There are no banned subreddits.")
            else:
                em = discord.Embed(title="Banned subreddits", color=0xffc700,
                                   description=subs_print)
                await ctx.send(embed=em)

        else:
            if option in subs_list:
                return await ctx.send(":x: That subreddit is banned.")
            try:
                r.subreddits.search_by_name(option, exact=True)
            except prawcore.exceptions.NotFound:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            except discord.errors.HTTPException:
                return await ctx.send(":x: I wasn't able to find that subreddit.")
            try:
                submissions = []
                for submission in r.subreddit(option).hot(limit=100):
                    submissions.append(submission)
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
            except prawcore.exceptions.NotFound:
                await ctx.send(":x: I wasn't able to find that subreddit.")


def setup(bot):
    bot.add_cog(Reddit(bot))
