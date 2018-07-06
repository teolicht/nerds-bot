#! /usr/bin/env python3

from discord.ext import commands
import discord

import traceback
import sys

from emojis import Emoji


class ErrorHandler():
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        content = ctx.message.content
        cmd = ctx.message.content.split()[0]
        cmd = cmd[2:]

        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            logfile = open('/Users/Teolicht/Box Sync/Python/Bots/NerdsBot/notfound.txt', 'a')
            logfile.write("{0} • {1.author}\n".format(content, ctx))
            logfile.close()
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            if cmd == 'member':
                return await ctx.send(":x: You must specify a member.\nCommand usage: `n!member <member>`")

            elif cmd == 'say':
                return await ctx.send(":x: Type the text you want me to repeat.\nCommand usage: `n!say <text>`")

            elif cmd == 'sayto':
                return await ctx.send(":x: To who do you want to say? And what? \nCommand usage: `n!sayto <member> <text>`")

            elif cmd == 'big':
                return await ctx.send(":x: Type the text you want me to repeat in letter emojis.\nCommand usage: `n!big <text>`")

            elif cmd == 'rps':
                em = discord.Embed(
                    title='Rock, Paper, Scissors')
                em.add_field(
                    name='To choose Rock:',
                    value='`n!rps R`')
                em.add_field(
                    name='To choose Paper:',
                    value='`n!rps P`')
                em.add_field(
                    name='To choose Scissors:',
                    value='`n!rps S`')
                em.set_footer(text='I choose randomly.')
                return await ctx.send(embed=em)

            elif cmd == 'gay':
                return await ctx.send(":x: You must specify a member.\nCommand usage: `n!gay <member`")

            elif cmd == 'gg':
                return await ctx.send(":x: You must specify a member.\nCommand usage: `n!gg <member>`")

            elif cmd == 'annoy':
                return await ctx.send(":x: You must specify a member.\nCommand usage: `n!annoy <member> [times]`")

            elif cmd == '8ball':
                return await ctx.send(":x: What question do you want to ask the magic 8-ball?\nCommand usage: `n!8ball <question>`")

            elif cmd == 'sound':
                return await ctx.send(":x: Specify the sound you want me to play.\nCommand usage: `n!sound <sound> [times to repeat]`\nType `n!sounds` for a list of available sounds.")

            elif cmd == 'kick':
                return await ctx.send(":x: You need to specify a member.\nCommand usage: `n!kick <member> [reason]`")

            elif cmd == 'ban':
                return await ctx.send(":x: You need to specify a member.\nCommand usage: `n!ban <member> [reason]`")

            elif cmd == 'unban':
                return await ctx.send(":x: Enter the ID of the user you want me to unban.\nCommand usage: `n!unban <userID> [reason]`\nExample: `n!unban 300761654411526154`\n**Don't know how to find an user's ID?** Go here: **http://bit.ly/finduserID**")

            elif cmd == 'delete':
                return await ctx.send(":x: Enter the amount of messages to delete.\nCommand usage: `n!delete <amount>`")

            elif cmd == 'timer':
                return await ctx.send(":x: Enter the seconds.\nCommand usage: `n!timer <secs>`")

            elif cmd == 'calc':
                return await ctx.send(":x: Enter the expression you wish me to calculate.\nCommand usage: `n!calc <expr>`\nExamples: `n!calc 2 + 3`, `n!calc 2 + 3 / 2`")

            elif cmd == 'poll':
                return await ctx.send(":x: Missing an argument.\nCommand usage: `n!poll <question> <duration> <option1> <option2> [option3–10]`\nExample: `n!poll \"Is my name Jeff?\" 60 Yes No Maybe`")

            elif cmd == 'randnum':
                return await ctx.send(":x: Missing an argmument.\nCommand usage: `n!randnum <min> <max>`\nExample: `n!randnum 50 700`")

        elif isinstance(error, commands.BadArgument):
            if cmd in ['member', 'gay', 'gg', 'kick', 'ban', 'sayto', 'annoy']:
                return await ctx.send(":x: I wasn't able to find that member.")

            elif cmd == 'unban':
                return await ctx.send(":x:  I wasn't able to find an user with that ID.\nHaving trouble? Example: `n!unban 300761654411526154`\n*Don't know how to get an user's ID?* Go here: **http://bit.ly/finduserID**")

            elif cmd in ['delete', 'timer', 'randnum']:
                return await ctx.send(":x: Numbers only. No decimals.")

            elif cmd == 'poll':
                return await ctx.send(":x: An error occurred. Make sure you entered the duration correctly as a number.")

        elif isinstance(error, discord.errors.ClientException):
            if cmd == 'sound':
                return await ctx.send(":x: *A sound is already playing.* Wait until the bot disconnects from the voice channel.")

        elif isinstance(error, commands.NotOwner):
            return

        print("Ignoring exception in command {0.command}:".format(ctx, file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.send(":warning: The following error has occurred: ```python\n{}: {}```".format(type(error).__name__, error))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
