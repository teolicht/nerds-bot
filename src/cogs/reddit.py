from discord.ext import commands
import discord
import praw
import random
from pprint import pprint
from .config import Reddit

r = praw.Reddit(client_id=Reddit.client_id,
                client_secret=Reddit.client_secret, password=Reddit.password,
                user_agent="teodorlicht", username=Reddit.username)

class Reddit(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def reddit(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("**https://www.reddit.com/**")

    @reddit.command()
    async def meirl(self, ctx):
        submissions = []
        for submission in r.subreddit('me_irl').hot(limit=100):
            if not submission.id == '80ib9u':
                submissions.append(submission)
        post = random.choice(submissions)
        em = discord.Embed(title='me irl',
                           url="https://www.reddit.com" + post.permalink)
        em.set_image(url=post.url)
        em.set_footer(text='u/{0.author.name} • {0.ups}'.format(post))
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Reddit(bot))
