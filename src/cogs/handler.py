import traceback
import sys
import discord

from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        try:
            cmd = ctx.command.qualified_name
        except AttributeError:
            pass
        error = getattr(error, "original", error)
        if isinstance(error, commands.NotOwner):
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            if cmd == "sound":
                return await ctx.send(
                    ":x: Specify the sound you want "
                    + "me to play.\nCommand usage: `n!sound <sound> "
                    + "[times to repeat]`\nType `n!sounds` for a list "
                    + "of available sounds."
                )
            elif cmd == "poll":
                return await ctx.send(
                    ":x: Missing an argument.\n"
                    + "Command usage: `n!poll <question> <duration> <option1> "
                    + '<option2> [option3–10]`\nExample: `n!poll "Is my '
                    + 'name Jeff?" 60 Yes No Maybe`'
                )

        elif isinstance(error, commands.BadArgument):
            if cmd == "poll":
                return await ctx.send(
                    ":x: An error occurred. Make sure "
                    + "you entered the duration correctly as a number."
                )

        elif isinstance(error, discord.errors.ClientException):
            if cmd == "sound":
                return await ctx.send(
                    ":x: *A sound is already playing.* "
                    + "Wait until the bot disconnects from the voice channel."
                )

        await ctx.send(
            ":warning: The following error has occurred: "
            + "```python\n{}: {}```".format(type(error).__name__, error),
            delete_after=5.0,
        )

        print("-" * 79)
        print("Ignoring exception in command {0.command}:".format(ctx, file=sys.stderr))
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )
        print("-" * 79)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
