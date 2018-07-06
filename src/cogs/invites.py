#!/usr/bin/env python3

from discord.ext import commands
import discord


class Invites():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='invite', aliases=['Invite', 'INVITE', 'convite'])
	async def _invite(self, ctx):
		await ctx.send("**http://bit.ly/invitenerdsbot**")

	@commands.command(name='svinvite', aliases=['Svinvite', 'SVINVITE', 'inviteserver'])
	async def _svinvite(self, ctx):
		invite_channel = self.bot.get_channel(ctx.channel.id)
		invite = await invite_channel.create_invite(unique=False)
		await ctx.send("**{}**".format(invite))


def setup(bot):
	bot.add_cog(Invites(bot))
