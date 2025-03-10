import random
import json
import threading
import asyncio
import asyncpraw
import asyncprawcore
import discord

from datetime import datetime
from discord import app_commands

from cogs.config import REDDIT


class Reddit(app_commands.Group):
    reddit = asyncpraw.Reddit(
        client_id=REDDIT["CLIENT_ID"],
        client_secret=REDDIT["CLIENT_SECRET"],
        password=REDDIT["PASSWORD"],
        user_agent=REDDIT["USERNAME"],
        username=REDDIT["USERNAME"],
    )

    subreddit_ban_cooldown: dict[str, datetime] = {}

    def reddit_json(self, mode, new_content=None):
        if mode == "r":
            with open("cogs/text/reddit.json", "r") as file:
                subs_json = json.load(file)
                file.close()
                return subs_json
        else:
            with open("cogs/text/reddit.json", "w") as file:
                json.dump(new_content, file, indent=4)
                file.close()

    def ban_done(self, subreddit):
        self.subreddit_ban_cooldown.pop(subreddit)

    submissions_cooldown: list[asyncpraw.models.Submission] = []
    async def cooldown_submission(self, submission, delay):
        self.submissions_cooldown.append(submission)
        await asyncio.sleep(delay)
        self.submissions_cooldown.remove(submission)

    async def fetch_submission(self, subreddit_name: str):
        subreddit = await self.reddit.subreddit(subreddit_name)
        submissions = []
        async for submission in subreddit.hot(limit=50):
            if not submission.stickied and submission not in self.submissions_cooldown:
                submissions.append(submission)
        if submissions == []:
            return None

        submission = random.choice(submissions)
        asyncio.create_task(self.cooldown_submission(submission, 600))
        return submission 

    @app_commands.command(description="Get a random post from the specified subreddit.")
    @app_commands.describe(name="The subreddit's name.")
    async def show(self, interaction: discord.Interaction, name: str):
        reddit_json = self.reddit_json("r")
        # Handlers
        if name in reddit_json["banned_subs"]:
            return await interaction.response.send_message(
                ":x: That subreddit is banned."
            )
        try:
            submission = await self.fetch_submission(name.lower())
        except (
            asyncprawcore.exceptions.NotFound,
            asyncprawcore.exceptions.Redirect,
            discord.errors.HTTPException,
        ):
            return await interaction.response.send_message(
                ":x: I wasn't able to find that subreddit."
            )
        except asyncprawcore.exceptions.Forbidden:
            return await interaction.response.send_message(
                ":x: That subreddit is private."
            )
        if submission is None:
            # All the posts may be on cooldown
            if len(self.submissions_cooldown) > 0:
                message = ":x: I can't find any more posts from that subreddit at this time."
            else:
                message = ":x: That subreddit is empty."
            return await interaction.response.send_message(message)
        # Deferring is needed because this command can take over 3 seconds to complete
        # over 3 seconds before interaction response results in interaction failed message
        await interaction.response.defer()
        # Create bot embed message
        submission_url = "https://www.reddit.com" + submission.permalink
        submission_link = None
        em = discord.Embed(title=submission.title, url=submission_url)
        em.set_author(name=submission.subreddit_name_prefixed)
        em.set_footer(text="u/{0.author.name} • {0.ups} upvotes • {0.num_comments} comments".format(submission))
        if submission.over_18:
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/477239188203503628/1098250769884512266/nsfw_icon.png"
            )
        description = ""
        if submission.selftext:
            description += submission.selftext
        if submission.url.endswith(("jpg", "png", "gif", "jpeg")):
            em.set_image(url=submission.url)
        elif "gallery" in submission.url:
            description += "\n:frame_photo: *This post contains a gallery, and I can't show galleries* :pensive:"
        elif "v.redd.it" in submission.url:
            description += f"\n:cinema: ***[Video link]({submission.url})***" 
            ## The four lines below can be used to extract the video link from the submission's JSON.
            ## This is unfortunately the only way a video posted to Reddit's host (v.redd.it) can be accessed directly.
            ## I gave up on using this because 1) the video extracted doesn't have any sound
            ## and 2) I would often get HTTP error 429: too many requests.
            # post_json = urlopen(post_url + ".json").read()
            # post_dict = json.loads(post_json.decode()) # decode() is because urlopen().read() returns bytes type
            # media_dict = post_dict[0]["data"]["children"][0]["data"]["media"]
            # post_video_link = media_dict["reddit_video"]["fallback_url"].strip("?source=fallback")
        else:
            submission_link = submission.url
        em.description = description
        await interaction.edit_original_response(content=submission_link, embed=em)

    @app_commands.command(description="Ban a subreddit.")
    @app_commands.describe(name="The subreddit's name.")
    async def ban(self, interaction: discord.Interaction, name: str):
        subreddit = name.lower()
        subs_json = self.reddit_json("r")
        if subreddit in subs_json["banned_subs"]:
            return await interaction.response.send_message(
                ":x: That subreddit is already banned."
            )
        subs_json["banned_subs"].append(subreddit)
        self.reddit_json("w", new_content=subs_json)
        self.subreddit_ban_cooldown[subreddit] = discord.utils.utcnow()
        timer = threading.Timer(600.0, self.ban_done, args=[subreddit])
        timer.start()
        await interaction.response.send_message(f":white_check_mark: Banned `r/{name}`")

    @app_commands.command(description="Unban a subreddit.")
    @app_commands.describe(name="The subreddit's name.")
    async def unban(self, interaction: discord.Interaction, name: str):
        subreddit = name.lower()
        subs_json = self.reddit_json("r")
        if subreddit not in subs_json["banned_subs"]:
            return await interaction.response.send_message(
                ":x: That subreddit isn't even banned."
            )
        if subreddit in self.subreddit_ban_cooldown:
            delta_time = discord.utils.utcnow() - self.subreddit_ban_cooldown[subreddit]
            remaining_ban_seconds = 600 - delta_time.seconds
            m, s = divmod(remaining_ban_seconds, 60)
            time_format = "%02dm%02ds" % (m, s)
            return await interaction.response.send_message(
                f":x: Please wait `{time_format}` before unbanning that subreddit."
            )
        subs_json["banned_subs"].remove(subreddit)
        self.reddit_json("w", new_content=subs_json)
        await interaction.response.send_message(
            f":white_check_mark: Unbanned `r/{name}`"
        )

    @app_commands.command(description="List of banned subreddits.")
    async def banlist(self, interaction: discord.Interaction):
        subs_json = self.reddit_json("r")
        subs_list = subs_json["banned_subs"]
        
        # Idea: use pagination to separate this list into different pages
        try:
            blank_line = "\u200b" * 22
            subs_print = [f"{blank_line}\n"]
            for x, sub in enumerate(subs_list):
                subs_print.append(f"**{x + 1}.** {sub}\n")
            em = discord.Embed(
                title=f"Banned subreddits ({len(subs_list)})",
                description="".join(subs_print),
            )
            await interaction.response.send_message(embed=em)
        # If message is too long
        except discord.errors.HTTPException:
            ####### This only separates the list in 2. Hardcoding. What if more than two is needed?
            half_list = len(subs_list) / 2
            half_list = int(round(half_list, 0))
            # First half of the list
            subs_print_1 = [f"{blank_line}\n"]
            for x, sub in enumerate(subs_list[:half_list]):
                subs_print_1.append(f"**{x + 1}.** {sub}\n")
            # Second half of the list
            subs_print_2 = [f"{blank_line}\n"]
            for x, sub in enumerate(subs_list[half_list:]):
                subs_print_2.append(f"**{x + 1}.** {sub}\n")

            em_1 = discord.Embed(
                title=f"Banned subreddits ({len(subs_list)})",
                description="".join(subs_print_1),
            )
            em_2 = discord.Embed(description="".join(subs_print_2))
            await interaction.response.send_message(embed=em_1)
            await interaction.channel.send(embed=em_2)


async def setup(bot):
    bot.tree.add_command(Reddit(name="subreddit", description="Subreddit commands."))
