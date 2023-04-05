from discord.ext import commands
from discord import app_commands
import discord
import time
import ago
import json
import os
from bs4 import BeautifulSoup
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
            return ""
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
    

    @app_commands.command(description="Test the bot's response time.")
    async def ping(self, interaction: discord.Interaction):
        ping = int(self.bot.latency * 1000)
        if ping <= 100:
            color = discord.Colour.dark_green()
        elif ping <= 200:
            color = discord.Colour.brand_green()
        elif ping <= 500:
            color = discord.Colour.gold()
        elif ping <= 800:
            color = discord.Colour.orange()
        elif ping <= 1000:
            color = discord.Colour.red()
        elif ping > 1000:
            color = discord.Colour.dark_red()
        em = discord.Embed(title="🏓 Pong!", description="*{}ms*".format(ping), color=color)
        await interaction.response.send_message(embed=em)


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

        soup_page = BeautifulSoup(xml_page, "xml")
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
