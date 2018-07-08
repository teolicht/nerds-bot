#!/usr/bin/env python3

from discord.ext import commands
import discord

import time
import ago
import bs4
import lxml # xml parser

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime

class Emoji(object):
    on = "<:ON:425085623490052096>"
    off = "<:OFF:425085623150444565>"
    idle = "<:IDLE:425085623183998986>"
    dnd = "<:DND:425085623028678657>"

class Information():
    def __init__(self, bot):
        self.bot = bot

    def get_digits(self, string):
        """Get all the digit characters in a string"""
        new_string = ''
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
        new_string = ''
        for char in string:
            if char == old_char:
                new_string += new_char
            else:
                new_string += char
        return new_string

    def get_status(self, member):
        """Get a member's status emoji"""
        if member.status == discord.Status.online:
            return Emoji.on
        elif member.status == discord.Status.offline:
            return Emoji.off
        elif member.status == discord.Status.idle:
            return Emoji.idle
        elif member.status in [discord.Status.dnd, discord.Status.do_not_disturb]:
            return Emoji.dnd
        else:
            return Emoji.off

    def get_roles(self, member):
        """Return a member's list of roles"""
        member_roles = []
        for role in member.roles:
            member_roles.append('`{0.name}`'.format(role))
        return member_roles

    @commands.group(name='help', aliases=['Help', 'HELP'])
    async def _help(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="Commands (40)", color=0xffc700)
            em.add_field(name='info', value='Informative commands.')
            em.add_field(name='pics', value='Picture commands.')
            em.add_field(name='fun', value='Fun commands.', inline=False)
            em.add_field(name='mod', value='Moderation commands.')
            em.add_field(name='utilities', value='Utility commands.')
            em.set_footer(text='To view category: "n!help <category>"')
            await ctx.send(embed=em)

        # formats = " Must be in the following formats: `ID`, `name`, `name#tag` or `mention`."
        #
        # if command in ['invite', 'Invite']:
        #     em = discord.Embed(
        #         title='`n!invite`',
        #         description='Get the link to invite me to any server you own.')
        #
        # elif command in ['svinvite', 'Svinvite']:
        #     em = discord.Embed(
        #         title='`n!svinvite`',
        #         description='Send the link you get from this command to anyone so they can join this server.')
        #
        # elif command in ['member', 'Member']:
        #     em = discord.Embed(
        #         title='`n!member`',
        #         description='Obtain various information on a member.')
        #     em.add_field(
        #         name='Format',
        #         value='**`n!member`**` <member>`')
        #     em.add_field(
        #         name='Parameters',
        #         value='Required:\n    1. `member` : The member to obtain the information from.\n       `member`' + formats)
        #     em.add_field(
        #         name='Examples',
        #         value='`n!member @testuser` • `n!member testuser#0000` • `n!member testuser`')
        #     em.set_footer(text='If the member\'s name has a space, wrap it up in quotes, like this: `"test user"`')
        #
        # elif command in ['server', 'Server']:
        #     em = discord.Embed(
        #         title='`n!server`',
        #         description='Obtain various information on this server.')
        #
        # elif command in ['ips', 'Ips', 'IPs', 'IPS']:
        #     em = discord.Embed(
        #         title='`n!ips`',
        #         description='Check IPv4 addresses.')
        #
        # elif command in ['ping', 'Ping']:
        #     em = discord.Embed(
        #         title='`n!ping`',
        #         description='Check my latency in microseconds (*ms*).')
        #
        # elif command in ['cat', 'Cat']:
        #     em = discord.Embed(
        #         title='`n!cat`',
        #         description='Executing this command will simply show you a cat pic/GIF.')
        #
        # elif command in ['dog', 'Dog']:
        #     em = discord.Embed(
        #         title='`n!dog`',
        #         description='Executing this command will simply show you a dog pic/GIF')
        #
        # elif command in ['nsfw', 'Nsfw', 'NSFW']:
        #     em = discord.Embed(
        #         title='`n!nsfw`',
        #         description='Executing this command will simply show you a NSFW pic/GIF. Channel must be NSFW.')
        #
        # elif command in ['tits', 'Tits']:
        #     em = discord.Embed(
        #         title='`n!tits`',
        #         description='Executing this command will simply show you a tits pic/GIF. Channel must be NSFW.')
        #
        # elif command in ['pussy', 'Pussy']:
        #     em = discord.Embed(
        #         title='`n!pussy`',
        #         description='Executing this command will simply show you a pussy pic/GIF. Channel must be NSFW.')
        #
        # elif command in ['say', 'Say']:
        #     em = discord.Embed(
        #         title='`n!say`',
        #         description='I will delete your message and send whatever you said in it.')
        #     em.add_field(
        #         name='Format',
        #         value='`n!say <text>`')
        #     em.add_field(
        #         name='Parameters',
        #         value='Required:\n    1. `text` : Whatever text you want the bot to send.')
        #     em.add_field(
        #         name='Example',
        #         value='`n!say hello friend`')
        #
        # elif command in ['sayto', 'Sayto']:
        #     em = discord.Embed(
        #         title='`n!sayto`',
        #         description='I will send the text you put to the member you specify (as a private message).')
        #     em.add_field(
        #         name='Format',
        #         value='`n!sayto <member> <text>`')
        #     em.add_field(
        #         name='Parameters',
        #         value='Required:\n    1. `member` : the member you want to send the msg to.\n    2. `text` : the text you want to send to the member.\n       `member`' + formats)
        #     em.add_field(
        #         name='Examples',
        #         value='`n!sayto @testuser you suck` • `n!sayto testuser#0000 you suck` • `n!sayto testuser you suck`')
        #     em.set_footer(text='if the member name has a space in it, wrap it up in quotes: "test user"')
        #
        # elif command in ['big', 'Big']:
        #     em = discord.Embed(
        #         title='`n!big`',
        #         description='I will delete your message and send whatever you said in it, replacing the letters and numbers with their respective emoji.')
        #     em.add_field(
        #         name='Format',
        #         value='`n!big <text>`')
        #     em.add_field(
        #         name='Parameters',
        #         value='- Required:\n    `text` : The text you want the bot to send. Only letters and numbers will be replaced.')
        #     em.add_field(
        #         name='Example',
        #         value='`n!big hello 123` = :regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_l: :regional_indicator_o:   :one: :two: :three:')
        #
        # elif command in ['gg', 'Gg', 'GG']:
        #     em = discord.Embed(
        #         title='`n!gg`',
        #         description='Call someone gordo & gay.')
        #     em.add_field(
        #         name='Format',
        #         value='`n!gg <member>`')
        #     em.add_field(
        #         name='Parameters',
        #         value='- Required:\n    1. `member` : The member you want to call gordo & gay.\n    `member`' + formats)
        #     em.add_field(
        #         name='Examples',
        #         value='`n!gg @testuser` • `n!gg testuser#0000` • `n!gg testuser`')
        #     em.set_footer(text='If the user\'s name has a space in it, wrap it up in quotes, like this: "test user"')
        #
        # elif command in ['poll', 'Poll', 'POLL', 'pol', 'pool']:
        #     em = discord.Embed(
        #         title='`n!poll`',
        #         description='Start a poll, up to 5 options.')
        #     em.add_field(
        #         name='Format',
        #         value='`n!poll <question> <duration> <option1> <option2> [option3] [option4] [option5]`')
        #     em.add_field(
        #         name='Parameters',
        #         value='- Required:\n    1. `question` : The poll\'s question.\n    2. `duration` : How long before the poll closes.\n    3. `option1 & option2` : The first two required options.\n- Optional:\n    1. `option3, option4 & option5` : The three last options.')
        #     em.add_field(
        #         name='Example',
        #         value='`n!poll "Who came first?" 300 Chicken Egg "No one knows"`')
        #     em.set_footer(text='If the question or option has a space in it, wrap it up in quotes, like this: "Nice poll"')
        #
        # else:
        #     return await ctx.send(":x: Command not found.")

    @_help.command(name='info', aliases=['Info', 'information'])
    async def _info(self, ctx):
        em = discord.Embed(title="Informative commands (5)", color=0xffc700)
        em.clear_fields()
        em.add_field(name='member <member>', value='Get info on a member.')
        em.add_field(name='server', value='Get info on this server.', inline=False)
        em.add_field(name='ping', value='Check my latency.', inline=False)
        em.add_field(name='info', value='Check some info about me.')
        await ctx.send(embed=em)

    @_help.command(name='pics', aliases=['Pics', 'PICs', 'PICS', 'pictures', 'images'])
    async def _pics(self, ctx):
        em = discord.Embed(title="Picture commands (5)", color=0xffc700)
        em.clear_fields()
        em.add_field(name='cat', value='A cat pic/GIF.')
        em.add_field(name='dog', value='A dog pic/GIF.', inline=False)
        # em.add_field(name='nsfw', value='A NSFW pic/GIF.')
        # em.add_field(name='tits', value='A tits pic/GIF.', inline=False)
        # em.add_field(name='pussy', value='A pussy pic/GIF.')
        await ctx.send(embed=em)

    @_help.command(name='fun', aliases=['Fun', 'FUN'])
    async def _fun(self, ctx):
        em = discord.Embed(title="Fun commands (16)", color=0xffc700)
        em.clear_fields()
        em.add_field(name='say <text>', value='Speak as if you were me.')
        em.add_field(name='big <text>', value='Speak as if you were me, but with emoji letters.', inline=False)
        em.add_field(name='sayto <member> <text>', value='Send someone a message.  ')
        em.add_field(name='gg <member>', value='Call someone gordo & gay.', inline=False)
        em.add_field(name='roast <member>', value='Roast someone.')
        em.add_field(name='kill <member>', value='Kill someone.', inline=False)
        em.add_field(name='suicide', value='Kill yourself.')
        em.add_field(name='respawn <member>', value='Respawn someone.', inline=False)
        em.add_field(name='rps', value='Play Rock, Paper, Scissors.')
        em.add_field(name='pr', value='Pickle rick.', inline=False)
        em.add_field(name='annoy <member> [times]', value='Annoy someone.')
        em.add_field(name='8ball <question>', value='Ask a question to the magic 8-ball.', inline=False)
        em.add_field(name='sound <number> [times]', value='Play a sound.')
        em.add_field(name='sounds', value='View the list of available sounds.', inline=False)
        em.add_field(name='fact', value='Get a random fact.')
        em.add_field(name='ship <member1> <member2>', value='Ship two members.', inline=False)
        await ctx.send(embed=em)

    @_help.command(name='mod', aliases=['Mod', 'MOD', 'moderation'])
    async def _mod(self, ctx):
        em = discord.Embed(title="Moderation commands (6)", color=0xffc700)
        em.clear_fields()
        em.add_field(name='kick <member> [reason]', value='Kick someone.')
        em.add_field(name='ban <member> [reason]', value='Ban someone.', inline=False)
        em.add_field(name='unban <userID> [reason]', value='Unban someone.')
        em.add_field(name='bans', value='View banned users.', inline=False)
        em.add_field(name='mute <member> <duration>', value='Mute someone (voice).')
        em.add_field(name='unmute <member>', value='Unmute someone.', inline=False)
        await ctx.send(embed=em)

    @_help.command(name='utilities', aliases=['Utilities', 'utilitis', 'utlities', 'utilties'])
    async def _utilities(self, ctx):
        em = discord.Embed(title="Utility commands (7)", color=0xffc700)
        em.clear_fields()
        em.add_field(name='delete <amount>', value='Delete messages in the channel.')
        em.add_field(name='timer <secs>', value='Start a timer.', inline=False)
        em.add_field(name='calc <expr>', value='Do a calculation.')
        em.add_field(name='flip', value='Flip a coin. Can land on heads or tails.', inline=False)
        em.add_field(name='randnum <min> <max>', value='Generate a random number between min and max.')
        em.add_field(name='poll <question> <duration> <option1> <option2> [options3-10]', value='Start a poll.', inline=False)
        em.add_field(name='choose', value='Choose from a list of options.')
        await ctx.send(embed=em)

    @commands.command(name='sounds', aliases=['Sounds', 'SOUNDS'])
    async def _sounds(self, ctx):
        em = discord.Embed(
        title='`n!sound` Sounds list',
        description="""
**1.** My name is jeff
**2.** Doin' your mom
**3.** Somebody toucha my spaghet
**4.** Deja vu duck
**5.** Pedron smashing keyboard
**6.** Surprise motherfucker
**7.** Precious foot lettuce
""")
        await ctx.send(embed=em)

    @commands.command(name='member', aliases=['Member', 'MEMBER', 'user', 'memberinfo', 'userinfo'])
    async def _member(self, ctx, member: discord.Member):
        # Member's current status
        status = self.get_status(member)
        # List with member's roles' names
        roles = self.get_roles(member)
        avatar = member.avatar_url
        # String containing date & time of guild join, format: YYYY/MM/DD HH:MM:SS
        guild_join = self.replace_chars(str(member.joined_at).split('.', 1)[0], '-', '/')
        # String containing date & time of Discord join, format: YYYY/MM/DD HH:MM:SS
        discord_join = self.replace_chars(str(member.created_at).split('.', 1)[0], '-', '/')
        # String containing date & time of guild join, format: DD/MM/YYYY • HH:MM
        joined_guild_date = '{} • {}'.format(datetime.strptime(guild_join[:-9], '%Y/%m/%d').strftime('%d/%m/%Y'), guild_join[-8:-3])
        # String containing date & time of Discord join, format: DD/MM/YYYY • HH:MM
        joined_discord_date = '{} • {}'.format(datetime.strptime(discord_join[:-9], '%Y/%m/%d').strftime('%d/%m/%Y'), discord_join[-8:-3])
        # Each time unit separated into different variables
        year, month, day, hour, minute = self.get_times(member.joined_at)
        # How long ago joined guild
        joined_guild_ago = ago.human(datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1)
        # Each time unit separated into different variables
        year, month, day, hour, minute = self.get_times(member.created_at)
        # How long ago joined Discord
        joined_discord_ago = ago.human(datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1)
        days_ago = '{}\n└ **{}** day(s) ago.'
        years_ago = '{}\n└ **{}** year(s) ago.'

        if 'day' in joined_guild_ago:
            # Less than one year ago, display "day(s) ago"
            joined_guild = days_ago.format(joined_guild_date, self.get_digits(joined_guild_ago))

        else:
            # More than one year ago, display "year(s) ago"
            joined_guild = years_ago.format(joined_guild_date, self.get_digits(joined_guild_ago))

        if 'day' in joined_discord_ago:
            # Less than one year ago, display "day(s) ago"
            joined_discord = days_ago.format(joined_discord_date, self.get_digits(joined_discord_ago))

        else:
            # More than one year ago, display "year(s) ago"
            joined_discord = years_ago.format(joined_discord_date, self.get_digits(joined_discord_ago))


        em = discord.Embed(
            title='User Information',
            description='{}{}'.format(member.mention, status),
            color=0xffd000)
        em.set_thumbnail(url=avatar)
        em.add_field(
            name='Name:',
            value=member.name)
        em.add_field(
            name='ID:',
            value='`{0.id}`'.format(member))
        em.add_field(
            name='Tag number:',
            value=member.discriminator)
        em.add_field(
            name='Discord name:',
            value='`{}`'.format(member))
        em.add_field(
            name='Roles ({}):'.format(len(roles)),
            value=', '.join(roles))
        em.add_field(
            name='Top role:',
            value='`{0.name}`'.format(member.top_role))
        em.add_field(
            name='Joined server:',
            value=joined_guild)
        em.add_field(
            name='Joined Discord:',
            value=joined_discord)
        await ctx.send(embed=em)

    @commands.command(name='server', aliases=['Server', 'SERVER', 'sever'])
    async def _server(self, ctx):
        def get_memberstatus(self, guild):
            """Get status of each member in a guild"""
            on_members, off_members, idle_members, dnd_members = 0, 0, 0, 0
            for member in guild.members:
                if member.status == discord.Status.online:
                    on_members += 1
                elif member.status == discord.Status.offline:
                    off_members += 1
                elif member.status == discord.Status.idle:
                    idle_members += 1
                elif member.status in [discord.Status.dnd, discord.Status.do_not_disturb]:
                    dnd_members += 1
                else:
                    off_members += 1
            return on_members, off_members, idle_members, dnd_members

        def get_verificationlevel(guild):
            """Get the verification level of a guild"""
            if guild.verification_level == discord.VerificationLevel.low:
                return 'Low'
            elif guild.verification_level == discord.VerificationLevel.medium:
                return 'Medium'
            elif guild.verification_level in [discord.VerificationLevel.high, discord.VerificationLevel.table_flip]:
                return 'High'
            elif guild.verification_level in [discord.VerificationLevel.extreme, discord.VerificationLevel.double_table_flip]:
                return 'Extreme'
            else:
                return 'None'

        def get_contentfilter(guild):
            """Get a guild's explicit content filter setting"""
            if guild.explicit_content_filter == discord.ContentFilter.disabled:
                return "Disabled"
            elif guild.explicit_content_filter == discord.ContentFilter.no_role:
                return "No role"
            else:
                return "All members"

        guild = ctx.guild
        roles, emojis = [], []
        textchannels, voicechannels, to_remove = 0, 0, 0
        on_members, off_members, idle_members, dnd_members = get_memberstatus(self, guild)
        verificationlevel = get_verificationlevel(guild)
        contentfilter = get_contentfilter(guild)

        # String containing date & time of guild creation, format: YYYY/MM/DD HH:MM:SS
        created_guild = self.replace_chars(str(guild.created_at).split('.', 1)[0], '-', '/')
        # String containing date & time of guild creation, format: DD/MM/YYYY • HH:MM
        created_guild_date = '{} • {}'.format(datetime.strptime(created_guild[:-9], '%Y/%m/%d').strftime('%d/%m/%Y'), created_guild[-8:-3])
        # Each time unit separated into variables
        year, month, day, hour, minute = self.get_times(guild.created_at)
        # How long ago guild creation
        created_guild_ago = ago.human(datetime(year=year, month=month, day=day, hour=hour, minute=minute), 1)

        if 'day' in created_guild_ago:
            # Less than one year ago, display "day(s) ago"
            created_format = "{}\n└ **{}** day(s) ago."
        else:
            # More than one year ago, display "year(s) ago"
            created_format = "{}\n└ **{}** year(s) ago."
        guild_created = created_format.format(created_guild_date, self.get_digits(created_guild_ago))


        if guild.mfa_level == 1:
            mfa_level = 'Yes'
        else:
            mfa_level = 'No'
        if guild.afk_channel:
            afk_channel = guild.afk_channel.name
        else:
            afk_channel = None
        for role in guild.roles:
            roles.append('`{0.name}`'.format(role))
        for channel in guild.text_channels:
            # If channel isn't #testing or #nerds
            if channel.id in [425023136673562625, 400773541945147402]:
                to_remove += 1
        textchannels = len(guild.text_channels) - to_remove
        for channel in guild.voice_channels:
            voicechannels += 1
        for emoji in guild.emojis:
            emojis.append('<:{0.name}:{0.id}>'.format(emoji))

        em = discord.Embed(
            title='Server Information')
        em.add_field(
            name='Name:',
            value=guild.name)
        em.add_field(
            name='ID:',
            value='`{0.id}`'.format(guild))
        em.add_field(
            name='Owner:',
            value='`{0.owner}`'.format(guild))
        em.add_field(
            name='Members:',
            value='{0.on}{1}   {0.off}{2}   {0.idle}{3}   {0.dnd}{4}'.format(
                   Emoji, on_members, off_members, idle_members, dnd_members))
        em.add_field(
            name='Channels ({}):'.format(textchannels + voicechannels),
            value='Text: **{}**\nVoice: **{}**'.format(textchannels, voicechannels))
        em.add_field(
            name='Region:',
            value=guild.region)
        em.add_field(
            name='Created:',
            value=guild_created)
        em.add_field(
            name='Roles ({}):'.format(len(roles)),
            value=', '.join(roles))
        if len(emojis) == 0:
            em.add_field(
                name='Emojis:',
                value='None')
        else:
            em.add_field(
                name='Emojis ({}):'.format(len(emojis)),
                value=' '.join(emojis))
        em.add_field(
            name='AFK channel:',
            value=afk_channel)
        em.add_field(
            name='2-FA:',
            value=mfa_level)
        em.add_field(
            name='Verification level:',
            value=verificationlevel)
        em.add_field(
            name='Explicit content filter:',
            value=contentfilter)
        em.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=em)

    @commands.command(name='news', aliases=['News', 'NEWS'])
    async def _news(self, ctx):
        news_url = "https://news.google.com/news/rss/?ned=us&gl=US&hl=en"

        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()

        soup_page = soup(xml_page, 'xml')
        news_list = soup_page.findAll('item')

        em = discord.Embed(title='Google News')
        for news in news_list:
            em.add_field(name=news.title.text, value=news.link.text + '\n' + news.pubDate.text + '\n' + '▁' * 32)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Information(bot))
