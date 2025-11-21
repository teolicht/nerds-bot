import os
import random
import sqlite3
import threading
import asyncio
import asyncpraw
import asyncprawcore
import discord

from datetime import datetime
from discord import app_commands
from typing import Tuple, List, Any

from cogs.config import REDDIT

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "nerds_bot.db")
)

class Reddit(app_commands.Group):
    reddit = asyncpraw.Reddit(
        client_id=REDDIT["CLIENT_ID"],
        client_secret=REDDIT["CLIENT_SECRET"],
        password=REDDIT["PASSWORD"],
        user_agent=REDDIT["USERNAME"],
        username=REDDIT["USERNAME"],
    )

    subreddit_ban_cooldown: dict[str, datetime] = {}

    """
    Takes a SQL query as a string and parameters for the query,
    executes the query, and returns the rows of the query result as a list.
    """
    def sql_read(self, string, params: Tuple[Any, ...] = ()) -> List:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(string, params)
            return c.fetchall()

    """
    Takes a SQL query as string and the parameters for the query,
    executes the query, and returns the number of rows affected as int.
    """
    def sql_write(self, string, params: Tuple[Any, ...] = ()) -> int:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(string, params)
            conn.commit()
            return c.rowcount

    """
    Autocomplete functionality when user is typing command.
    """
    # TODO: show the 25 most recently banned subreddits when user hasn't typed anything yet 
    # (discord limit is 25), and could be cool to try to implement some fzf funcitonality here
    async def banlist_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        guild_id = interaction.guild.id # type: ignore
        raw_banned_subs = self.sql_read(
            "SELECT name FROM banned_subreddits WHERE guild_id = ?",
            (guild_id,)
        )
        banned_subs = [sub[0] for sub in raw_banned_subs] # flatten list of tuples into list of strings
        current_clean = current.lower().removeprefix("r/")
        choices = [
            app_commands.Choice(name=f"r/{name}", value=name) # show r/ in choices but return clena name as value
            for name in banned_subs
            if current_clean in name.lower()
        ]
        # Discord only accepts up to 25 autocomplete choices
        return choices[:25]

    def ban_done(self, subreddit):
        self.subreddit_ban_cooldown.pop(subreddit)

    submissions_cooldown: list[asyncpraw.models.Submission] = [] # type: ignore
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
        name = name.lower()
        guild_id = interaction.guild.id # type: ignore
        banned_subs = self.sql_read(
            "SELECT name FROM banned_subreddits WHERE guild_id = ?",
            (guild_id,)
        )
        banned_sub_names = [sub[0] for sub in banned_subs] # flatten list of tuples into list of strings
        # Handlers
        if name in banned_sub_names:
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
        await interaction.edit_original_response(
            content=submission_link, embed=em
        )

    @app_commands.command(description="Ban a subreddit.")
    @app_commands.describe(name="The subreddit's name.")
    async def ban(self, interaction: discord.Interaction, name: str):
        name = name.lower().removeprefix("r/")
        print(name)
        guild_id = interaction.guild.id # type: ignore
        now = discord.utils.utcnow().isoformat()
        private = False
        try:
            await interaction.response.defer()
            # Test if the subreddit actually exists
            await self.fetch_submission(name)
        except (asyncprawcore.exceptions.NotFound, 
                asyncprawcore.exceptions.Redirect):
            return await interaction.edit_original_response(
                content=":x: I wasn't able to find that subreddit."
            )
        except asyncprawcore.exceptions.Forbidden:
            # Still ban the subreddit even if it's private
            private = True
            pass
        except Exception as e:
            return await interaction.edit_original_response(
                content=f":x: The following error occured:\n`{type(e).__name__}: {e}`"
            )
        try:
            self.sql_write("""
                INSERT INTO banned_subreddits (
                    guild_id,
                    name,
                    banned_at
                ) VALUES (?, ?, ?)
            """, (guild_id, name, now))
            if private:
                await interaction.edit_original_response(content=
                    f":white_check_mark: Banned `r/{name}` (private subreddit)"
                )
            else:
                await interaction.edit_original_response(content=
                    f":white_check_mark: Banned `r/{name}`"
                )
            self.subreddit_ban_cooldown[name] = discord.utils.utcnow()
            timer = threading.Timer(600.0, self.ban_done, args=[name])
            timer.start()
        except sqlite3.IntegrityError:
            await interaction.edit_original_response(
                content=":x: That subreddit is already banned."
            )

    @app_commands.command(description="Unban a subreddit.")
    @app_commands.describe(name="The subreddit's name.")
    @app_commands.autocomplete(name=banlist_autocomplete)
    async def unban(self, interaction: discord.Interaction, name: str):
        name = name.lower()
        guild_id = interaction.guild.id # type: ignore
        if name in self.subreddit_ban_cooldown:
            delta_time = discord.utils.utcnow() - self.subreddit_ban_cooldown[name]
            remaining_ban_seconds = 600 - delta_time.seconds
            m, s = divmod(remaining_ban_seconds, 60)
            time_format = "%02dm%02ds" % (m, s)
            return await interaction.response.send_message(
                f":x: Please wait `{time_format}` before unbanning that subreddit."
            )
        rowcount = self.sql_write(
            "DELETE FROM banned_subreddits WHERE name = ? AND guild_id = ?",
            (name, guild_id)
        )
        if rowcount == 0:
            return await interaction.response.send_message(
                ":x: That subreddit isn't even banned."
            )
        await interaction.response.send_message(
            f":white_check_mark: Unbanned `r/{name}`"
        )

    @app_commands.command(description="List of banned subreddits.")
    async def banlist(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id # type: ignore
        raw_banlist = self.sql_read(
            "SELECT name FROM banned_subreddits WHERE guild_id = ?",
            (guild_id,)
        )
        # Flatten list of tuples to list of strings
        banlist = [sub[0] for sub in raw_banlist]
        # TODO: use pagination to separate this list into different pages (right now max is embeds)
        try:
            subs_print = []
            for x, sub in enumerate(banlist):
                subs_print.append(f"**{x + 1}.** r/{sub}\n")
            em = discord.Embed(
                title=f"Banned subreddits ({len(banlist)})",
                description="".join(subs_print),
            )
            await interaction.response.send_message(embed=em)
        # If message is too long
        except discord.errors.HTTPException:
            half_list = len(banlist) / 2
            half_list = int(round(half_list, 0))
            # First half of the list
            subs_print_1 = []
            for x, sub in enumerate(banlist[:half_list]):
                subs_print_1.append(f"**{x + 1}.** {sub}\n")
            # Second half of the list
            subs_print_2 = []
            for x, sub in enumerate(banlist[half_list:]):
                subs_print_2.append(f"**{x + 1}.** {sub}\n")

            em_1 = discord.Embed(
                title=f"Banned subreddits ({len(banlist)})",
                description="".join(subs_print_1),
            )
            em_2 = discord.Embed(description="".join(subs_print_2))
            await interaction.response.send_message(embed=em_1)
            await interaction.channel.send(embed=em_2)


async def setup(bot):
    bot.tree.add_command(Reddit(name="subreddit", description="Subreddit commands."))
