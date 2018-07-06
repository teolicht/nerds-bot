#!/usr/bin/env python3

from discord.ext import commands
import discord

import asyncio
import random
import datetime
import os

from emojis import Emoji


this_path = os.path.dirname(__file__)
dead_members = []

class Fun():
    def __init__(self, bot):
        self.bot = bot

    def mname(self, member):
        """If member.nick exists, return it, otherwise, return member.name"""
        if member.nick:
            return member.nick
        else:
            return member.name

    @commands.command(name='say', aliases=['Say', 'SAY'])
    async def _say(self, ctx, *, text):
        try:
            await ctx.message.delete()
            text = ''.join(text)
            await ctx.send(text)
        except discord.errors.Forbidden:
            await ctx.send(":x: I need the **Manage Messages** permission so I can delete your message.")

    @commands.command(name='sayto', aliases=['Sayto', 'SAYTO', 'sendto'])
    async def _sayto(self, ctx, member: discord.Member, *, text):
        text = ''.join(text)
        em = discord.Embed(
            title='Dear {0.name}'.format(member),
            description='*I was sent here by {0.author.mention} to tell you this:*\n\n{1}\n\u200b'.format(ctx, text),
            timestamp=datetime.datetime.utcnow())
        await member.send(embed=em)
        await ctx.send(":white_check_mark: Sent message to `{0.name}`".format(member))

    @commands.command(name='big', aliases=['Big', 'BIG', 'emoji'])
    async def _big(self, ctx, *, text):
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
            await ctx.send(":x: I need the **Manage Messages** permission so I can delete your message first.")

    @commands.command(name='gg', aliases=['Gg', 'GG'])
    async def _gg(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.message.add_reaction('\U0001f1f3') # N
            await ctx.message.add_reaction('\U0001f1f4') # O
            await ctx.message.add_reaction('\U0001f1f5') # P
            return await ctx.message.add_reaction('\U0001f1ea') # E

        else:
            text = "**É** gordo & gay!"

        em = discord.Embed(description='🌈🏳️‍🌈🍔🌭 {0.mention} {1} 🌭🍔🏳️‍🌈🌈'.format(member, text))
        await ctx.send(embed=em)

    @commands.command(name='roast', aliases=['Roast', 'ROAST'])
    async def _roast(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.message.add_reaction('\U0001f1f3') # N
            await ctx.message.add_reaction('\U0001f1f4') # O
            await ctx.message.add_reaction('\U0001f1f5') # P
            return await ctx.message.add_reaction('\U0001f1ea') # E

        roasts = ['yo mama so fat that when she walked past my TV I missed 10 episodes.',
        'yo mama so fat the sat on an iPhone and turned it into an iPad.',
        'when you were little your parents took an eraser that erases big mistakes and rubbed it all over your face.',
        'you bring everyone a lot of joy, when you leave the room.',
        'I\'ll never forget the first day we met, although I\'ll keep trying.',
        'there are more calories in your stomach than in the local supermarket!',
        'wanna know how long it takes for yo mama to take a crap? 9 months.',
        'surprise me, say something intelligent.',
        'if I ever agreed with you, we\'d both be wrong.',
        'yo mama is so fat that when she takes a selfie it\'s via satellite.',
        'you\'re so ugly you make blind kids cry.',
        'you\'re so fat you need cheat codes to play Wii Fit.',
        'if you played Hide\'n\'Seek, no one would look for you.',
        'you\'re a person of rare intelligence, because it\'s rare when you show any.',
        'you must have been born on a highway because that\'s where most accidents happen.',
        'it\'s better to let someone think you\'re an idiot than open your mouth and prove it.',
        'if you want to understand what a true mistake is, you should ask your parents.',
        'not that I hate you, but if you were on fire and I had water, I\'d drink it.',
        'you should check eBay and see if they have a life for sale, because you certainly need one.']
        roast = random.choice(roasts)

        em = discord.Embed(
            description='{0.mention},\n{1}'.format(member, roast),
            color=discord.Colour.red())
        await ctx.send(embed=em)

    @commands.command(name='suicide', aliases=['Suicide', 'SUICIDE'])
    async def _suicide(self, ctx):
        member = ctx.author
        if member in dead_members:
            return await ctx.send(":x: You're already dead.")

        nick = self.mname(member)
        em = discord.Embed(
            description=':skull: {0.mention} has suicided!'.format(member),
            color=discord.Colour.red())
        if len(nick) > 25:
            return await ctx.send(embed=em)
        await ctx.send(embed=em)
        await member.edit(nick='{} (DEAD)'.format(nick))
        dead_members.append(member)

    @commands.command(name='kill', aliases=['Kill', 'KILL', 'murder'])
    async def _kill(self, ctx, member: discord.Member):
        try:
            if member == self.bot.user:
                await ctx.message.add_reaction('\U0001f1f3')
                await ctx.message.add_reaction('\U0001f1f4')
                await ctx.message.add_reaction('\U0001f1f5')
                return await ctx.message.add_reaction('\U0001f1ea')
        except:
            await ctx.send("No.")

        if member in dead_members:
            return await ctx.send(":x: That member is already dead.")

        nick = self.mname(member)
        em = discord.Embed(
            description=':skull: {0.mention} has been killed by {1.author.mention}!'.format(member, ctx),
            color=discord.Colour.red())
        if len(nick) > 25:
            return await ctx.send(embed=em)
        await ctx.send(embed=em)
        await member.edit(nick='{} (DEAD)'.format(nick))
        dead_members.append(member)

    @commands.command(name='respawn', aliases=['Respawn', 'RESPAWN', 'revive', 'live', 'regenerate', 'save'])
    async def _respawn(self, ctx, member: discord.Member):
        if member == ctx.author:
            return await ctx.send(":x: Sorry, you can't revive yourself.")
        if member not in dead_members:
            if member == ctx.author:
                await ctx.send(":x: You're not even dead, mate.")
            else:
                nick = self.mname(member)
                await ctx.send(":x: {} is not even dead, mate.".format(nick))
            return

        if '(DEAD)' in member.nick:
            new_name = member.nick[:-7] # Cuts out '(DEAD)' from the member's server nickname
            await member.edit(nick=new_name)
        await ctx.send(":innocent: Welcome back, {0.mention}.".format(member))
        dead_members.remove(member)

    @commands.command(name='rps', aliases=['Rps', 'RPS'])
    async def _rps(self, ctx, choice):
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
                    description=member + ', it\'s a tie, mate.')
            elif comparison(userC, botC) == 'Win':
                em = discord.Embed(
                    description=member + ', you won retard ass.',
                    color=discord.Colour.green())
            else:
                em = discord.Embed(
                    description=member + ', get __rekt__ you lost.',
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
                await ctx.send(embed=endgame(ctx.author.mention, 'Rock', botC))
            elif choice.lower() in ['p', 'paper']:
                await ctx.send(embed=endgame(ctx.author.mention, 'Paper', botC))
            else:
                await ctx.send(embed=endgame(ctx.author.mention, 'Scissors', botC))

    @commands.command(name='pr', aliases=['Pr', 'PR'])
    async def _pr(self, ctx):
        picklerick = os.path.join(this_path, "images", "picklerick.png")
        with open(picklerick, 'rb') as pic:
            await ctx.send(file=discord.File(pic))

    @commands.command(name='annoy', aliases=['Annoy', 'ANNOY'])
    async def _annoy(self, ctx, member: discord.Member, times: int = 2):
        nick = self.mname(member)
        with open(os.path.join(this_path, "text", "bad_words.txt")) as file:
            bad_words = [line.rstrip('\n') for line in file]

        await ctx.send(":white_check_mark: *Started annoying* **`{}`** **{}** time(s)".format(nick, times))
        for i in range(0, times):
            word = random.choice(bad_words)
            await member.send("**{0}** • I was sent here to annoy you by {1.author.mention}, **{2}**.".format(i + 1, ctx, word))
            if not i == times - 1: # If not done yet
                await asyncio.sleep(30)

        minutes = round((30 * times) / 60, 1)
        await ctx.send(":white_check_mark: *Done annoying* **`{0.name}`** • `{1}min`".format(member, minutes))

    @commands.command(name='8ball', aliases=['8Ball', '8BALL', '8bal'])
    async def _8ball(self, ctx, *, question):
        if 'gay' in ctx.message.content:
            return await ctx.send(":8ball: Of course!")

        answers = ['Concentrate and ask again', 'Outlook good', 'Without a doubt', 'You may rely on it',
                   'Ask again later', 'It is certain', 'Reply hazy, try again', 'My reply is no', 'My sources say no']
        answer = random.choice(answers)
        await ctx.send(":8ball: {}".format(answer))

    @commands.command(name='sound', aliases=['Sound', 'SOUND'])
    async def _sound(self, ctx, option, repeat: int = False):
        sounds_path = os.path.join(this_path, "sounds/")
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
        await ctx.send(":white_check_mark: *Playing sound* `{}`".format(options[option]))

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

    @commands.command(name='fact', aliases=['Fact', 'FACT'])
    async def _fact(self, ctx):
        facts = ['The human nose can distinguish at least 1 trillion smells.',
                 'Mozart, by the time he was 5, had written his first 5 compositions.',
                 'John Tyler, an US ex-president, had 2 wives and 15 children.',
                 'The first basketball game was played in New York on January 20, 1892.',
                 'Percy Spencer invented the first microwave oven after World War II from radar technology developed during the war.',
                 'The first typewriter to be commercially successful was invented in 1868.',
                 'Earth\'s atmosphere is primarily composed of nitrogen (78%) and oxygen (21%) with only small concentrations of other trace gases.',
                 'The first pizza was created by the baker Raffaele Esposito in Naples.',
                 'Male fireflies can fly, but female fireflies often can\'t because their wings are too short.',
                 'The biggest tree in the world is located in California.',
                 'It took Apollo 11 (spaceship that carried Neil Armstrong) 4 days, 6 hours and 45 minutes to get to the moon.',
                 'Hair is made of a tough protein called keratin.',
                 'The last country to join the United Nations was the Republic of South Sudan.',
                 'The gravity on the moon is about 17% what it is on Earth.',
                 'Antarctica is the coldest, driest, and windiest continent in the world.',
                 'The speed of light equals 299792458 meters per second.',
                 'The speed of light equals 1079252848 km/h.',
                 'The human eyes never grow.',
                 'A mushroom isn\'t a fruit, vegetable or plant - it is a special type of fungus.',
                 'The first chocolate chip cookie was invented by Ruth Graves Wakefield in the 1930s.',
                 'Approximately 10% of the world population is left-handed.',
                 'Cold water weighs more than hot water.',
                 'The Sun equals 1.3 million Earth-sized planets.',
                 'A short nap of 20 minutes enhances alertness and concentration, elevates mood, and sharpens motor skills.']
        fact = random.choice(facts)

        await ctx.send("**Fact:**\n{}".format(fact))

    @commands.command(name='ship', aliases=['Ship', 'SHIP'])
    async def _ship(self, ctx, member1: discord.Member, member2: discord.Member):
        nick1 = self.mname(member1)
        nick2 = self.mname(member2)
        half_index1 = int(len(nick1) / 2)
        half1 = nick1[:half_index1]
        half_index2 = int(len(nick2) / 2)
        half2 = nick2[half_index2:]
        ship_name = (half1 + half2).strip()
        em = discord.Embed(
            title=':heart: I ship {} and {} :heart:'.format(nick1, nick2),
            description=':two_hearts::revolving_hearts: {} :revolving_hearts::two_hearts:'.format(ship_name),
            color=0xE10D91)
        await ctx.send(embed=em)

    @commands.command(name='pt')
    @commands.is_owner()
    async def _pt(self, ctx, member: discord.Member, times: int = 1):
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
        await member.add_roles(gay_role)
        await ctx.send(":white_check_mark: {0.mention} is now GAY for {1}".format(member, how_long))
        await asyncio.sleep(duration)
        await member.remove_roles(gay_role)
        await ctx.send("{0.mention} is no longer GAY.".format(member))


def setup(bot):
    bot.add_cog(Fun(bot))
