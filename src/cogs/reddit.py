from discord.ext import commands
import discord
import praw
import random
from .config import Reddit

r = praw.Reddit(client_id=Reddit.client_id,
                client_secret=Reddit.client_secret, password=Reddit.password,
                user_agent="teodorlicht", username=Reddit.username)

class Reddit(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, ctx, subreddit):
        try:
            submissions = []
            for submission in r.subreddit(subreddit).hot(limit=100):
                submissions.append(submission)
            post = random.choice(submissions)

            em = discord.Embed(title=post.title,
                               url='https://www.reddit.com' + post.permalink)
            em.set_footer(text='u/{0.author.name} • {0.ups}'.format(post))
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

def setup(bot):
    bot.add_cog(Reddit(bot))
