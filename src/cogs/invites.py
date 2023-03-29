from discord.ext import commands
import discord
import json
import os


CONFIG = json.load(
    open(os.path.join(os.path.dirname(__file__), "text", "config.json"), "r")
)


class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(CONFIG["invite"])

    @commands.command()
    async def svinvite(self, ctx):
        invite_channel = self.bot.get_channel(ctx.channel.id)
        invite = await invite_channel.create_invite(unique=False)
        await ctx.send("**{}**".format(invite))


async def setup(bot):
    await bot.add_cog(Invites(bot))
