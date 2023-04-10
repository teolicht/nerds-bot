import json
import discord
from discord.ext import commands
from discord import app_commands
from bs4 import BeautifulSoup
from urllib.request import urlopen


transparent_color = 0x302C34

with open("cogs/text/config.json", "r") as file:
    emojis = json.load(file)["emojis"]
    file.close()


def delta_time(date: discord.utils.utcnow):
    delta_time = discord.utils.utcnow() - date
    hour, remainder = divmod(int(delta_time.total_seconds()), 3600)
    min = int(remainder / 60)
    day, hour = divmod(hour, 24)
    month, day = divmod(day, 30)
    year, month = divmod(month, 12)
    if year > 0:
        return f"**{year}** year(s), **{month}** month(s) ago"
    if month > 0:
        return f"**{month} month(s), **{day}** day(s) ago"
    if day > 0:
        return f"**{day} day(s), **{hour}** hour(s) ago"
    return f"**{hour}** hour(s), **{min}** minute(s) ago"


def get_status(user: discord.User):
    """Get a user's status emoji"""
    if user.bot:
        return ""
    elif user.status == discord.Status.online:
        return emojis["online"]
    elif user.status == discord.Status.offline:
        return emojis["offline"]
    elif user.status == discord.Status.idle:
        return emojis["idle"]
    elif user.status in [discord.Status.dnd, discord.Status.do_not_disturb]:
        return emojis["dnd"]
    else:
        return emojis["offline"]


def get_roles(user: discord.User):
    """Return a user's list of roles"""
    user_roles = []
    for role in user.roles:
        user_roles.append(f"`{role.name}`")
    return user_roles


def get_userstatus(guild: discord.Guild):
    """Get status of each user in a guild"""
    on_users, off_users, idle_users, dnd_users, bot_users = (
        0, 0, 0, 0, 0,  # fmt: skip
    )
    for user in guild.members:
        if user.bot:
            bot_users += 1
        elif user.status == discord.Status.online:
            on_users += 1
        elif user.status == discord.Status.offline:
            off_users += 1
        elif user.status == discord.Status.idle:
            idle_users += 1
        elif user.status in [
            discord.Status.dnd,
            discord.Status.do_not_disturb,
        ]:
            dnd_users += 1
        else:
            off_users += 1
    return on_users, off_users, idle_users, dnd_users, bot_users


def get_verificationlevel(guild: discord.Guild):
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


def get_contentfilter(guild: discord.Guild):
    """Get a guild's explicit content filter setting"""
    if guild.explicit_content_filter == discord.ContentFilter.disabled:
        return "Disabled"
    elif guild.explicit_content_filter == discord.ContentFilter.no_role:
        return "No role"
    else:
        return "All members"


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        em = discord.Embed(title="🏓 Pong!", description=f"*{ping}ms*", color=color)
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="View information on a member.")
    @app_commands.describe(user="A member in this server.")
    async def member(self, interaction: discord.Interaction, user: discord.Member):
        discord_join_date = user.created_at.strftime("%d/%m/%Y • %H:%M")
        discord_join_ago = delta_time(user.created_at)
        guild_join_date = user.joined_at.strftime("%d/%m/%Y • %H:%M")
        guild_join_ago = delta_time(user.joined_at)

        if user.bot:
            status = emojis["bot"]
        else:
            status = get_status(user)
        roles = get_roles(user)
        avatar = user.display_avatar

        em = discord.Embed(
            title="User Information",
            color=transparent_color,
            description=f"{user.mention}{status}",
        )
        em.set_thumbnail(url=avatar)
        em.add_field(name="Name:", value=user.name)
        em.add_field(name="ID:", value=f"`{user.id}`")
        em.add_field(name="Tag number:", value=user.discriminator)
        em.add_field(name="Discord name:", value=f"`{user}`")
        em.add_field(name=f"Roles ({len(roles)}):", value=", ".join(roles))
        em.add_field(name="Top role:", value=f"`{user.top_role.name}`")
        em.add_field(
            name="Joined server:", value=f"{guild_join_date} (UTC)\n└ {guild_join_ago}"
        )
        em.add_field(
            name="Joined Discord:",
            value=f"{discord_join_date} (UTC)\n└ {discord_join_ago}",
        )
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="View the latest Google News.")
    async def news(self, interaction: discord.Interaction):
        news_url = "https://news.google.com/news/rss/?ned=us&gl=US&hl=en"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = BeautifulSoup(xml_page, "xml")
        news_list = soup_page.findAll("item", limit=13)

        em = discord.Embed(color=transparent_color)
        amount = 0
        for news in news_list:
            em.add_field(
                name="\u200b",
                value="[{0.title.text}]({0.link.text})\n{0.pubDate.text}".format(news),
            )
        em.set_author(name="Google News", icon_url="https://i.imgur.com/8bgnHPW.jpg")
        await interaction.response.send_message(embed=em)

    ##### Move to music commands, this is hardcoding
    @commands.command()
    async def sounds(self, ctx):
        em = discord.Embed(
            title="``n!sound`` Sounds list",
            color=transparent_color,
            description="""**1.** Doin' your mom
**2.** Deja vu duck
**3.** Pedron smashing keyboard
**4.** Surprise motherfucker
**5.** Lorengay singing
""",
        )
        await ctx.send(embed=em)


class Server(app_commands.Group):
    @app_commands.command(description="View information on this server.")
    async def info(self, interaction: discord.Interaction):
        guild = interaction.guild
        guild_create_date = guild.created_at.strftime("%d/%m/%Y • %H:%M")
        guild_create_ago = delta_time(guild.created_at)

        emojis_list = []
        for emoji in guild.emojis:
            emojis_list.append(f"<:{emoji.name}:{emoji.id}>")

        (
            on_users,
            off_users,
            idle_users,
            dnd_users,
            bot_users,
        ) = get_userstatus(guild)
        verificationlevel = get_verificationlevel(guild)
        contentfilter = get_contentfilter(guild)

        if guild.mfa_level == 1:
            mfa_level = "Yes"
        else:
            mfa_level = "No"

        if guild.afk_channel:
            afk_channel = guild.afk_channel.name
        else:
            afk_channel = None

        roles = []
        for role in guild.roles:
            roles.append(f"`{role.name}`")

        text_channels_amount = len(guild.text_channels)
        voice_channels_amount = len(guild.voice_channels)
        total_channels_amount = len(guild.text_channels) + len(guild.voice_channels)

        em = discord.Embed(title="Server Information", color=transparent_color)
        em.add_field(name="Name:", value=guild.name)
        em.add_field(name="ID:", value=f"`{guild.id}`")
        em.add_field(name="Owner:", value=f"`{guild.owner}`")
        em.add_field(
            name=f"Members ({len(guild.members)}):",
            value=f'{emojis["online"]}{on_users}   {emojis["offline"]}{off_users}   {emojis["idle"]}{idle_users}'
            + f'   {emojis["dnd"]}{dnd_users}   \n{emojis["bot"]}{bot_users}',
        )
        em.add_field(
            name=f"Channels ({text_channels_amount + voice_channels_amount}):",
            value=f"Text: **{text_channels_amount}**\nVoice: **{voice_channels_amount}**",
        )
        em.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles))
        if len(emojis_list) == 0:
            em.add_field(name="Emojis:", value="None")
        elif len(emojis_list) > 10:
            em.add_field(
                name=f"Emojis ({len(guild.emojis)}):",
                value="*Too many to display. Type* ``/server emojis`` *instead.*",
            )
        else:
            em.add_field(
                name=f"Emojis ({len(emojis_list)}):", value=" ".join(emojis_list)
            )
        em.add_field(name="AFK channel:", value=afk_channel)
        em.add_field(name="2-FA:", value=mfa_level)
        em.add_field(name="Verification level:", value=verificationlevel)
        em.add_field(name="Explicit content filter:", value=contentfilter)
        em.add_field(
            name="Created:", value=f"{guild_create_date} (UTC)\n└ {guild_create_ago}"
        )
        em.set_thumbnail(url=guild.icon)
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="View a list of this server's emojis.")
    async def emojis(self, interaction: discord.Interaction):
        animated_emojis_list = []
        normal_emojis_list = []
        for emoji in interaction.guild.emojis:
            if emoji.animated is True:
                animated_emojis_list.append(f"<a:{emoji.name}:{emoji.id}>")
            else:
                normal_emojis_list.append(f"<:{emoji.name}:{emoji.id}>")
        em = discord.Embed(
            color=transparent_color,
            description=f"Custom emojis **({len(normal_emojis_list)}):**\n{' '.join(normal_emojis_list)}"
            + f"\n\u200b\nAnimated emojis **({len(animated_emojis_list)}):**\n{' '.join(animated_emojis_list)}",
        )
        em.set_author(
            name=f"Server emojis ({len(interaction.guild.emojis)})",
            icon_url=interaction.guild.icon,
        )
        await interaction.response.send_message(embed=em)


async def setup(bot):
    bot.tree.add_command(Server(name="server", description="Server commands."))
    await bot.add_cog(Information(bot))
