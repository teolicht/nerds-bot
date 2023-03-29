from discord.ext import commands
import discord
import time
import ago
import bs4

# import lxml
import random
import json
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime


EMOJI = json.load(
    open(os.path.join(os.path.dirname(__file__), "text/config.json"), "r")
)["emojis"]


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_digits(self, string):
        """Get all the digit characters in a string"""
        new_string = ""
        for char in string:
            if char.isdigit():
                new_string += char
        return new_string

    def get_times(self, date):
        """Get year, month, day, hour and minute from a datetime object"""
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        return year, month, day, hour, minute

    def replace_chars(self, string, old_char, new_char):
        """Replace certain character in a string with another one"""
        new_string = ""
        for char in string:
            if char == old_char:
                new_string += new_char
            else:
                new_string += char
        return new_string

    def get_status(self, member):
        """Get a member's status emoji"""
        if member.bot:
            return
        elif member.status == discord.Status.online:
            return EMOJI["online"]
        elif member.status == discord.Status.offline:
            return EMOJI["offline"]
        elif member.status == discord.Status.idle:
            return EMOJI["idle"]
        elif member.status in [discord.Status.dnd, discord.Status.do_not_disturb]:
            return EMOJI["dnd"]
        else:
            return EMOJI["offline"]

    def get_roles(self, member):
        """Return a member's list of roles"""
        member_roles = []
        for role in member.roles:
            member_roles.append("`{0.name}`".format(role))
        return member_roles

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="Commands", color=0xFF2B29)
            em.add_field(name="info", value="Informative commands.")
            em.add_field(name="pics", value="Picture commands.", inline=False)
            em.add_field(name="fun", value="Fun commands.", inline=False)
            # em.add_field(name='mod', value='Moderation commands.')
            em.add_field(name="util", value="Useful commands.", inline=False)
            em.add_field(name="reddit", value="Reddit commands.", inline=False)
            em.set_footer(text='To view category: "n!help <category>"')
            await ctx.send(embed=em)

    @help.command()
    async def info(self, ctx):
        em = discord.Embed(color=0xFF2B29)
        em.clear_fields()
        em.add_field(name="member <member>", value="Get info on a member.")
        em.add_field(name="server", value="Get info on this server.", inline=False)
        em.add_field(name="ping", value="Check my latency.")
        em.add_field(name="info", value="Check some info about me.", inline=False)
        em.add_field(name="news", value="Check the latest news (Google News).")
        em.title = f"Informative commands ({len(em.fields)})"
        em.set_footer(text="<required> | [optional]")
        await ctx.send(embed=em)

    @help.command()
    async def pics(self, ctx):
        em = discord.Embed(title="Picture commands (2)", color=0xFF2B29)
        em.clear_fields()
        em.add_field(name="cat", value="A cat pic/GIF.")
        em.add_field(name="dog", value="A dog pic/GIF.", inline=False)
        em.set_footer(text="<required> | [optional]")
        await ctx.send(embed=em)

    @help.command()
    async def fun(self, ctx):
        em = discord.Embed(title="Fun commands (13)", color=0xFF2B29)
        em.clear_fields()
        em.add_field(name="say <text>", value="Speak as if you were me.")
        em.add_field(
            name="big <text>",
            value="Speak as if you were me, but with emoji letters.",
            inline=False,
        )
        em.add_field(name="sayto <member> <text>", value="Send someone a message.")
        em.add_field(name="roast <member>", value="Roast someone.", inline=False)
        em.add_field(name="kill <member>", value="Kill someone.")
        em.add_field(name="suicide", value="Kill yourself.", inline=False)
        em.add_field(name="respawn <member>", value="Respawn someone.")
        em.add_field(name="rps", value="Play Rock, Paper, Scissors.", inline=False)
        em.add_field(
            name="annoy <member> [times]", value="Annoy someone.")
        em.add_field(name="fact", value="Get a random fact.", inline=False)
        em.add_field(
            name="ship <member1> <member2>", value="Ship two members.")
        em.title = f"Fun commands ({len(em.fields)})"
        em.set_footer(text="<required> | [optional]")
        await ctx.send(embed=em)

    # @help.command()
    # async def mod(self, ctx):
    #     em = discord.Embed(title="Moderation commands (8)", color=0xff2b29)
    #     em.clear_fields()
    #     em.add_field(name='kick <member> [reason]', value='Kick someone.')
    #     em.add_field(name='ban <member> [reason]', value='Ban someone.',
    #         inline=False)
    #     em.add_field(name='unban <usernum>', value='Unban someone. Check bans' +
    #         ' to get user\'s number.')
    #     em.add_field(name='bans', value='View banned users.', inline=False)
    #     em.add_field(name='mute <member> [duration]', value='Mute someone ' +
    #         '(voice).')
    #     em.add_field(name='unmute <member>', value='Unmute someone.',
    #         inline=False)
    #     em.add_field(name='chatmute <member> [duration]', value='Chat-mute ' +
    #         'someone.')
    #     em.add_field(name='unchatmute <member>', value='Un-chat-mute someone.',
    #         inline=False)
    #     em.set_footer(text='<required> | [optional]')
    #     await ctx.send(embed=em)

    @help.command(aliases=["utilities", "utils"])
    async def util(self, ctx):
        em = discord.Embed(color=0xFF2B29)
        em.clear_fields()
        em.add_field(
            name="delete <amount>", value="Delete messages in the " + "channel."
        )
        em.add_field(name="timer <secs>", value="Start a timer.", inline=False)
        em.add_field(name="calc <expr>", value="Do a calculation.")
        em.add_field(
            name="flip",
            value="Flip a coin. Can land on heads or tails.",
            inline=False,
        )
        em.add_field(
            name="randnum <min> <max>",
            value="Generate a random number between min and max.",
        )
        em.add_field(
            name="poll <question> <duration> <option1> <option2> [options3-10]",
            value="Start a poll.",
            inline=False,
        )
        em.add_field(name="choose", value="Choose from a list of options.")
        em.add_field(
            name="tag <create|delete|edit|list>",
            value="Various tag commands.",
            inline=False,
        )
        em.title = f"Useful commands ({len(em.fields)})"
        em.set_footer(text="<required> | [optional]")
        await ctx.send(embed=em)

    @help.command()
    async def reddit(self, ctx):
        em = discord.Embed(color=0xFF2B29)
        em.clear_fields()
        em.add_field(
            name="reddit <subreddit>",
            value="Random hot post from specified subreddit.",
        )
        em.add_field(
            name="reddit ban <subreddit>", value="Ban a subreddit.", inline=False
        )
        em.add_field(
            name="reddit unban <subreddit>", value="Unban a subreddit.", inline=False
        )
        em.add_field(
            name="reddit banlist", value="List of banned subreddits.", inline=False
        )
        em.title = f"Reddit commands ({len(em.fields)})"
        em.set_footer(text="<required> | [optional]")
        await ctx.send(embed=em)

    @commands.command()
    async def member(self, ctx, member: discord.Member):
        # Member's current status
        status = self.get_status(member)
        if member.bot:
            status = f'{status}{EMOJI["bot"]}'
        # List with member's roles' names
        roles = self.get_roles(member)
        avatar = member.display_avatar
        # String containing date & time of guild join - YYYY/MM/DD HH:MM:SS
        guild_join = self.replace_chars(
            str(member.joined_at).split(".", 1)[0], "-", "/"
        )
        # String containing date & time of Discord join- YYYY/MM/DD HH:MM:SS
        discord_join = self.replace_chars(
            str(member.created_at).split(".", 1)[0], "-", "/"
        )
        # String containing date & time of guild join - DD/MM/YYYY • HH:MM
        joined_guild_date = "{} • {}".format(
            datetime.strptime(guild_join[:-9], "%Y/%m/%d").strftime("%d/%m/%Y"),
            guild_join[-8:-3],
        )
        # String containing date & time of Discord join - DD/MM/YYYY • HH:MM
        joined_discord_date = "{} • {}".format(
            datetime.strptime(discord_join[:-9], "%Y/%m/%d").strftime("%d/%m/%Y"),
            discord_join[-8:-3],
        )
        # Each time unit separated into different variables
        year, month, day, hour, minute = self.get_times(member.joined_at)
        # How long ago joined guild
        joined_guild_ago = ago.human(
            datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1
        )
        # Each time unit separated into different variables
        year, month, day, hour, minute = self.get_times(member.created_at)
        # How long ago joined Discord
        joined_discord_ago = ago.human(
            datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1
        )
        days_ago = "{}\n└ **{}** day(s) ago."
        years_ago = "{}\n└ **{}** year(s) ago."

        if "day" in joined_guild_ago:
            # Less than one year ago, display "day(s) ago"
            joined_guild = days_ago.format(
                joined_guild_date, self.get_digits(joined_guild_ago)
            )
        else:
            # More than one year ago, display "year(s) ago"
            joined_guild = years_ago.format(
                joined_guild_date, self.get_digits(joined_guild_ago)
            )

        if "day" in joined_discord_ago:
            # Less than one year ago, display "day(s) ago"
            joined_discord = days_ago.format(
                joined_discord_date, self.get_digits(joined_discord_ago)
            )
        else:
            # More than one year ago, display "year(s) ago"
            joined_discord = years_ago.format(
                joined_discord_date, self.get_digits(joined_discord_ago)
            )

        em = discord.Embed(
            title="User Information",
            color=0xFF2B29,
            description="{}{}".format(member.mention, status),
        )
        em.set_thumbnail(url=avatar)
        em.add_field(name="Name:", value=member.name)
        em.add_field(name="ID:", value="`{0.id}`".format(member))
        em.add_field(name="Tag number:", value=member.discriminator)
        em.add_field(name="Discord name:", value="`{}`".format(member))
        em.add_field(name="Roles ({}):".format(len(roles)), value=", ".join(roles))
        em.add_field(name="Top role:", value="`{0.name}`".format(member.top_role))
        em.add_field(name="Joined server:", value=joined_guild)
        em.add_field(name="Joined Discord:", value=joined_discord)
        await ctx.send(embed=em)

    @commands.command()
    async def server(self, ctx, emoji=None):
        emojis = []
        if emoji == "emojis":
            for emoji in ctx.guild.emojis:
                emojis.append("<:{0.name}:{0.id}>".format(emoji))
            return await ctx.send(" ".join(emojis))

        for emoji in ctx.guild.emojis:
            emojis.append("<:{0.name}:{0.id}>".format(emoji))

        def get_memberstatus(self, guild):
            """Get status of each member in a guild"""
            on_members, off_members, idle_members, dnd_members, bot_members = (
                0,
                0,
                0,
                0,
                0,
            )
            for member in guild.members:
                if member.bot:
                    bot_members += 1
                elif member.status == discord.Status.online:
                    on_members += 1
                elif member.status == discord.Status.offline:
                    off_members += 1
                elif member.status == discord.Status.idle:
                    idle_members += 1
                elif member.status in [
                    discord.Status.dnd,
                    discord.Status.do_not_disturb,
                ]:
                    dnd_members += 1
                else:
                    off_members += 1
            return on_members, off_members, idle_members, dnd_members, bot_members

        def get_verificationlevel(guild):
            """Get the verification level of a guild"""
            if guild.verification_level == discord.VerificationLevel.low:
                return "Low"
            elif guild.verification_level == discord.VerificationLevel.medium:
                return "Medium"
            elif guild.verification_level in [
                discord.VerificationLevel.high,
                discord.VerificationLevel.table_flip,
            ]:
                return "High"
            elif guild.verification_level in [
                discord.VerificationLevel.extreme,
                discord.VerificationLevel.double_table_flip,
            ]:
                return "Extreme"
            else:
                return "None"

        def get_contentfilter(guild):
            """Get a guild's explicit content filter setting"""
            if guild.explicit_content_filter == discord.ContentFilter.disabled:
                return "Disabled"
            elif guild.explicit_content_filter == discord.ContentFilter.no_role:
                return "No role"
            else:
                return "All members"

        guild = ctx.guild
        roles = []
        textchannels, voicechannels, to_remove = 0, 0, 0
        (
            on_members,
            off_members,
            idle_members,
            dnd_members,
            bot_members,
        ) = get_memberstatus(self, guild)
        verificationlevel = get_verificationlevel(guild)
        contentfilter = get_contentfilter(guild)

        # String containing date & time of guild creation - YYYY/MM/DD HH:MM:SS
        created_guild = self.replace_chars(
            str(guild.created_at).split(".", 1)[0], "-", "/"
        )
        # String containing date & time of guild creation - DD/MM/YYYY • HH:MM
        created_guild_date = "{} • {}".format(
            datetime.strptime(created_guild[:-9], "%Y/%m/%d").strftime("%d/%m/%Y"),
            created_guild[-8:-3],
        )
        # Each time unit separated into variables
        year, month, day, hour, minute = self.get_times(guild.created_at)
        # How long ago guild creation
        created_guild_ago = ago.human(
            datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1
        )

        if "day" in created_guild_ago:
            # Less than one year ago, display "day(s) ago"
            created_format = "{}\n└ **{}** day(s) ago."
        else:
            # More than one year ago, display "year(s) ago"
            created_format = "{}\n└ **{}** year(s) ago."
        guild_created = created_format.format(
            created_guild_date, self.get_digits(created_guild_ago)
        )

        if guild.mfa_level == 1:
            mfa_level = "Yes"
        else:
            mfa_level = "No"
        if guild.afk_channel:
            afk_channel = guild.afk_channel.name
        else:
            afk_channel = None
        for role in guild.roles:
            roles.append("`{0.name}`".format(role))
        for channel in guild.text_channels:
            # If channel isn't #testing or #nerds
            if channel.id in [425023136673562625, 400773541945147402]:
                to_remove += 1
        textchannels = len(guild.text_channels) - to_remove
        for channel in guild.voice_channels:
            voicechannels += 1

        em = discord.Embed(title="Server Information", color=0xFF2B29)
        em.add_field(name="Name:", value=guild.name)
        em.add_field(name="ID:", value="`{0.id}`".format(guild))
        em.add_field(name="Owner:", value="`{0.owner}`".format(guild))
        em.add_field(
            name=f"Members ({len(guild.members)}):",
            value=f'{EMOJI["online"]}{on_members}   {EMOJI["offline"]}{off_members}   {EMOJI["idle"]}{idle_members}'
            + f'   {EMOJI["dnd"]}{dnd_members}   \n{EMOJI["bot"]}{bot_members}',
        )

        em.add_field(
            name="Channels ({}):".format(textchannels + voicechannels),
            value="Text: **{}**\nVoice: **{}**".format(textchannels, voicechannels),
        )
        em.add_field(name="Created:", value=guild_created)
        em.add_field(name="Roles ({}):".format(len(roles)), value=", ".join(roles))
        if len(emojis) == 0:
            em.add_field(name="Emojis:", value="None")
        elif len(emojis) > 10:
            em.add_field(
                name="Emojis:",
                value="*Too many to display. Type ``n!server emojis`` if you want to view this server's emojis.*",
            )
        else:
            em.add_field(
                name="Emojis ({}):".format(len(emojis)), value=" ".join(emojis)
            )
        em.add_field(name="AFK channel:", value=afk_channel)
        em.add_field(name="2-FA:", value=mfa_level)
        em.add_field(name="Verification level:", value=verificationlevel)
        em.add_field(name="Explicit content filter:", value=contentfilter)
        em.set_thumbnail(url=guild.icon)
        await ctx.send(embed=em)

    @commands.command()
    async def news(self, ctx):
        news_url = "https://news.google.com/news/rss/?ned=us&gl=US&hl=en"

        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()

        soup_page = soup(xml_page, "xml")
        news_list = soup_page.findAll("item")

        em = discord.Embed(color=0xFFFFFF)
        amount = 0
        for news in news_list:
            amount += 1
            if amount == 13:
                break
            em.add_field(
                name="\u200b",
                value="[{0.title.text}]({0.link.text})\n{0.pubDate.text}".format(news),
            )
        em.set_author(name="Google News", icon_url="https://i.imgur.com/8bgnHPW.jpg")
        await ctx.send(embed=em)

    @commands.command()
    async def sounds(self, ctx):
        em = discord.Embed(
            title="``n!sound`` Sounds list",
            color=0xFF2B29,
            description="""**1.** Doin' your mom
**2.** Deja vu duck
**3.** Pedron smashing keyboard
**4.** Surprise motherfucker
**5.** Lorengay singing
""",
        )
        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Information(bot))
