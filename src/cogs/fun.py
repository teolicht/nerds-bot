#!/usr/bin/env python3

from discord.ext import commands
import discord
import asyncio
import random
import datetime
import os


THIS_PATH = os.path.dirname(__file__)
dead_members = []

class Fun(object):
    def __init__(self, bot):
        self.bot = bot

    def mname(self, member):
        """If member.nick exists, return it, otherwise,
        return member.name"""
        if member.nick:
            return member.nick
        else:
            return member.name

    @commands.command()
    async def say(self, ctx, *, text):
        try:
            await ctx.message.delete()
            text = ''.join(text)
            await ctx.send(text)
        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Manage Messages** permission " +
                "so I can delete your message.")

    @commands.command()
    async def sayto(self, ctx, member: discord.Member, *, text):
        text = ''.join(text)
        em = discord.Embed(
            title='Dear {0.name}'.format(member),
            description='*I was sent here by {0.author.mention} '.format(ctx) +
                'to tell you this:*\n\n{}\n\u200b'.format(text),
            timestamp=datetime.datetime.utcnow())
        await member.send(embed=em)
        await ctx.send(":white_check_mark: Sent message to `{0.name}`".format(
            member))

    @commands.command()
    async def big(self, ctx, *, text):
        msg = ''
        def big(letter):
            return ':regional_indicator_{}: '.format(letter)

        for char in ''.join(text):
            char = char.lower()
            if char == '0':
                msg += ':zero:'
            elif char == '1':
                msg += ':one:'
            elif char == '2':
                msg += ':two:'
            elif char == '3':
                msg += ':three:'
            elif char == '4':
                msg += ':four:'
            elif char == '5':
                msg += ':five:'
            elif char == '6':
                msg += ':six:'
            elif char == '7':
                msg += ':seven:'
            elif char == '8':
                msg += ':eight:'
            elif char == '9':
                msg += ':nine:'
            elif char in ['a', 'ã', 'á', 'à', 'â', 'å']:
                msg += big('a')
            elif char == 'b':
                msg += big('b')
            elif char == 'c':
                msg += big('c')
            elif char == 'd':
                msg += big('d')
            elif char in ['e', 'é', 'è', 'ê']:
                msg += big('e')
            elif char == 'f':
                msg += big('f')
            elif char == 'g':
                msg += big('g')
            elif char == 'h':
                msg += big('h')
            elif char in ['i', 'í', 'ì', 'î']:
                msg += big('i')
            elif char == 'j':
                msg += big('j')
            elif char == 'k':
                msg += big('k')
            elif char == 'l':
                msg += big('l')
            elif char == 'm':
                msg += big('m')
            elif char in ['n', 'ñ']:
                msg += big('n')
            elif char in ['o', 'õ', 'ó', 'ò', 'ô', 'ø']:
                msg += big('o')
            elif char == 'p':
                msg += big('p')
            elif char == 'q':
                msg += big('q')
            elif char == 'r':
                msg += big('r')
            elif char == 's':
                msg += big('s')
            elif char == 't':
                msg += big('t')
            elif char in ['u', 'ú', 'ù', 'û']:
                msg += big('u')
            elif char == 'v':
                msg += big('v')
            elif char == 'w':
                msg += big('w')
            elif char == 'x':
                msg += big('x')
            elif char == 'y':
                msg += big('y')
            elif char == 'z':
                msg += big('z')
            elif char == ' ':
                msg += '    '
            else:
                msg += str(char)

        try:
            await ctx.message.delete()
            await ctx.send(msg)
        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Manage Messages** permission so " +
                "I can delete your message first.")

    @commands.command()
    async def gg(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.message.add_reaction('\U0001f1f3') # N
            await ctx.message.add_reaction('\U0001f1f4') # O
            await ctx.message.add_reaction('\U0001f1f5') # P
            return await ctx.message.add_reaction('\U0001f1ea') # E
        else:
            text = "**É** gordo & gay!"

        em = discord.Embed(description='🌈🏳️‍🌈🍔🌭 {0.mention} {1} 🌭🍔🏳️‍🌈🌈'.format(
            member, text))
        await ctx.send(embed=em)

    @commands.command()
    async def roast(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.message.add_reaction('\U0001f1f3') # N
            await ctx.message.add_reaction('\U0001f1f4') # O
            await ctx.message.add_reaction('\U0001f1f5') # P
            return await ctx.message.add_reaction('\U0001f1ea') # E

        with open(os.path.join(THIS_PATH, "text", "roasts.txt")) as file:
            roasts = [line.rstrip('\n') for line in file]
        roast = random.choice(roasts)

        em = discord.Embed(
            description='{0.mention},\n{1}'.format(member, roast),
            color=discord.Colour.red())
        await ctx.send(embed=em)

    @commands.command()
    async def suicide(self, ctx):
        member = ctx.author
        if member in dead_members:
            return await ctx.send(":x: You're already dead.")

        nick = self.mname(member)
        em = discord.Embed(
            description=':skull: {0.mention} has suicided!'.format(member),
            color=discord.Colour.red())
        if len(nick) > 25:
            return await ctx.send(embed=em)
        try:
            await member.edit(nick='{} (DEAD)'.format(nick))
            dead_members.append(member)
            await ctx.send(embed=em)
        except discord.errors.Forbidden:
            await ctx.send(embed=em)

    @commands.command()
    async def kill(self, ctx, member: discord.Member):
        try:
            if member == self.bot.user:
                await ctx.message.add_reaction('\U0001f1f3')
                await ctx.message.add_reaction('\U0001f1f4')
                await ctx.message.add_reaction('\U0001f1f5')
                return await ctx.message.add_reaction('\U0001f1ea')
        except:
            await ctx.send("No.")

        if member == ctx.author:
            return await ctx.send("If you want to kill yourself, " +
                "~~you should totally type `n!suicide`~~")
        if member in dead_members:
            return await ctx.send(":x: That member is already dead.")

        nick = self.mname(member)
        em = discord.Embed(
            description=':skull: {0.mention} has been killed by '.format(
                member) + '{0.author.mention}!'.format(ctx),
            color=discord.Colour.red())
        if len(nick) > 25:
            return await ctx.send(embed=em)
        try:
            await member.edit(nick='{} (DEAD)'.format(nick))
            await ctx.send(embed=em)
            dead_members.append(member)
        except discord.errors.Forbidden:
            await ctx.send(embed=em)

    @commands.command()
    async def respawn(self, ctx, member: discord.Member):
        if member == ctx.author:
            return await ctx.send(":x: Sorry, you can't respawn yourself.")
        if member not in dead_members:
            if member == ctx.author:
                await ctx.send(":x: You're not even dead, mate.")
            else:
                nick = self.mname(member)
                await ctx.send(":x: {} is not even dead, mate.".format(nick))
            return

        if member.nick and '(DEAD)' in member.nick:
            new_name = member.nick[:-7] # Cuts out '(DEAD)' from member's nick
            await member.edit(nick=new_name)
            nick = self.mname(member)
            dead_members.remove(member)
            await ctx.send(":innocent: Welcome back, {}.".format(nick))
        else:
            nick = self.mname(member)
            await ctx.send(":innocent: Welcome back, {}.".format(nick))

    @commands.command()
    async def rps(self, ctx, choice):
        def comparison(userC, botC):
            if userC == botC:
                return 'Tie'
            elif userC == 'Rock' and botC == 'Scissors':
                return 'Win'
            elif userC == 'Paper' and botC == 'Rock':
                return 'Win'
            elif userC == 'Scissors' and botC == 'Paper':
                return 'Win'
            else:
                return 'Lose'

        def endgame(member, userC, botC):
            em = discord.Embed()
            if comparison(userC, botC) == 'Tie':
                em = discord.Embed(
                    description=member + ', it\'s a tie!')
            elif comparison(userC, botC) == 'Win':
                em = discord.Embed(
                    description=member + ', you won!',
                    color=discord.Colour.green())
            else:
                em = discord.Embed(
                    description=member + ', you lost!',
                    color=discord.Colour.red())
            return em

        choices = ['Rock', 'Paper', 'Scissors']
        botC = random.choice(choices)
        if choice.lower() not in ['r', 'rock', 'p', 'paper', 's', 'scissors']:
            await ctx.send("`{}` is not a valid choice.".format(choice))
        else:
            await ctx.send("I choose **{}**".format(botC))
            await asyncio.sleep(1)

            if choice.lower() in ['r', 'rock']:
                await ctx.send(
                    embed=endgame(ctx.author.mention, 'Rock', botC))
            elif choice.lower() in ['p', 'paper']:
                await ctx.send(
                    embed=endgame(ctx.author.mention, 'Paper', botC))
            else:
                await ctx.send(
                    embed=endgame(ctx.author.mention, 'Scissors', botC))

    @commands.command()
    async def pr(self, ctx):
        picklerick = os.path.join(THIS_PATH, "images", "picklerick.png")
        with open(picklerick, 'rb') as pic:
            await ctx.send(file=discord.File(pic))

    @commands.command()
    async def annoy(self, ctx, member: discord.Member, times: int = 2):
        nick = self.mname(member)
        with open(os.path.join(THIS_PATH, "text", "bad_words.txt")) as file:
            bad_words = [line.rstrip('\n') for line in file]

        await ctx.send(":white_check_mark: *Started annoying* {} ".format(
            self.mname(member)) + "**{}** time(s)".format(times))
        for i in range(0, times):
            word = random.choice(bad_words)
            await member.send("**{}** • I was sent here to annoy ".format(
                i + 1) + "you by {0.author.mention}, **{1}**.".format(
                    ctx, word))
            if not i == times - 1: # If not done yet
                await asyncio.sleep(30)

        minutes = round((30 * times) / 60, 1)
        await ctx.send(":white_check_mark: *Done annoying* {0.mention} • ".format(member) +
            "`{}min`".format(minutes))

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        answers = ['Concentrate and ask again', 'Outlook good',
                   'Without a doubt', 'You may rely on it', 'Ask again later',
                   'It is certain', 'Reply hazy, try again', 'My reply is no',
                   'My sources say no']
        answer = random.choice(answers)
        await ctx.send(":8ball: {}".format(answer))

    @commands.command()
    async def sound(self, ctx, option, repeat: int = False):
        await ctx.send("This command is currently disabled because I can't fucking get it to work.")
        sounds_path = os.path.join(THIS_PATH, "sounds/")
        def soundobj(sound):
            return discord.FFmpegPCMAudio(sounds_path + sound)

        async def playsound(file, repeat, duration):
            if repeat is False:
                vc.play(soundobj(file))
            else:
                for i in range(0, repeat):
                    vc.play(soundobj(file))
                    await asyncio.sleep(duration)
                    vc.stop()
            await asyncio.sleep(duration)

        voice = ctx.author.voice
        if voice is None:
            return await ctx.send(":x: Join a voice channel first.")
        channel = voice.channel
        options = {
            '1': 'My name is jeff',
            '2': 'Doin\' your mom',
            '3': 'Somebody toucha my spaghet',
            '4': 'Deja vu duck',
            '5': 'Pedron\'s keyboard',
            '6': 'Surprise motherfucker',
            '7': 'Precious foot lettuce'}
        if option not in options:
            return await ctx.send(":x: Option `{}` not found.".format(option))

        vc = await channel.connect()
        await ctx.send(":white_check_mark: *Playing sound* `{}`".format(
            options[option]))

        if option == '1':
            await playsound('jeff.mp3', repeat, 2)
        elif option == '2':
            await playsound('doinurmom.mp3', repeat, 8.2)
        elif option == '3':
            await playsound('spaghet.mp3', repeat, 4.7)
        elif option == '4':
            await playsound('initialduck.mp3', repeat, 14.7)
        elif option == '5':
            await playsound('smashingKB.mp3', repeat, 7)
        elif option == '6':
            await playsound('surprise_motherfucker.mp3', repeat, 2.5)
        elif option == '7':
            await playsound('preciousfoot.mp3', repeat, 31)
        await vc.disconnect()

    @commands.command()
    async def fact(self, ctx):
        with open(os.path.join(THIS_PATH, "text", "facts.txt")) as file:
            facts = [line.rstrip('\n') for line in file]
        fact = random.choice(facts)
        await ctx.send(fact)

    @commands.command()
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        nick1 = self.mname(member1)
        nick2 = self.mname(member2)
        half_index1 = int(len(nick1) / 2)
        half1 = nick1[:half_index1]
        half_index2 = int(len(nick2) / 2)
        half2 = nick2[half_index2:]
        ship_name = (half1 + half2).strip()
        em = discord.Embed(
            title=':heart: I ship {} and {} :heart:'.format(nick1, nick2),
            description=':two_hearts::revolving_hearts: {} '.format(ship_name) +
                ':revolving_hearts::two_hearts:',
            color=0xE10D91)
        await ctx.send(embed=em)

    @commands.command()
    async def nigger(self, ctx, member: discord.Member):
        nick = self.mname(member)
        nigger_role = discord.utils.get(ctx.guild.roles, name="NIGGER")
        try:
            await member.add_roles(nigger_role)
            await ctx.send(":white_check_mark: {} is now a nigger!!!".format(nick))
        except:
            return await ctx.send(":x: I wasn't able to do that. Check if a " +
                "'NIGGER' role exists in this server.")

    @commands.command(aliases=['unigger', 'unniger'])
    async def unnigger(self, ctx, member: discord.Member):
        if ctx.author == member:
            return await ctx.send(":x: You can't un-nigger yourself.")
        nick = self.mname(member)
        nigger_role = discord.utils.get(ctx.guild.roles, name="NIGGER")
        await member.remove_roles(nigger_role)
        await ctx.send(":white_check_mark: {} is no longer a nigger.".format(
            nick))

    @commands.command()
    @commands.is_owner()
    async def pt(self, ctx, member: discord.Member, times: int = 1):
        if times == 1:
            duration = 600
            how_long = "10 minutes!"
        elif times == 2:
            duration = 1800
            how_long = "30 minutes!"
        elif times == 3:
            duration = 3600
            how_long = "1 hour!"
        elif times == 4:
            duration = 7200
            how_long = "2 hours!"
        elif times == 5:
            duration = 18000
            how_long = "5 hours!"
        gay_role = discord.utils.get(ctx.guild.roles, name="GAY")
        try:
            await member.add_roles(gay_role)
        except:
            return await ctx.send(":x: I wasn't able to do that. Check if a " +
                "'GAY' role exists in this server.")
        await ctx.send(":white_check_mark: {0.mention} is now ".format(member) +
            "GAY for {}".format(how_long))
        await asyncio.sleep(duration)
        await member.remove_roles(gay_role)
        await ctx.send("{0.mention} is no longer GAY.".format(member))


def setup(bot):
    bot.add_cog(Fun(bot))
