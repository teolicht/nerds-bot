import asyncio
import logging
import pickle
import discord
from typing import cast
from discord.ext import commands
from cogs import config

description = "A private Discord bot for friends."
command_prefix = ("n!", "N!")
intents = discord.Intents().all()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
discord.utils.setup_logging(handler=handler)

initial_extensions = [
    "cogs.fun",
    "cogs.handler",
    "cogs.help",
    "cogs.information",
    "cogs.moderation",
    "cogs.pictures",
    "cogs.reddit",
    "cogs.utilities",
]

class NerdsBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=command_prefix,
            description=description,
            help_command=None,
            intents=intents,
        )
        self.nerds_guild: discord.Guild
        self.general_channel: discord.TextChannel
        self.zap_channel: discord.TextChannel


    async def setup_hook(self) -> None:
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}:\n{e}")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="/help")
        )
        try:
            print("-" * 50)
            print("Logged in as")
            print("> " + self.user.name)
            print("> ID: " + str(self.user.id))
            print("-" * 50)
        except Exception as e:
            print(e)

        bot_launch_time = discord.utils.utcnow()
        with open("bot_launch_time.pkl", "wb") as file:
            pickle.dump(bot_launch_time, file, pickle.HIGHEST_PROTOCOL)
            file.close()

        self.nerds_guild = cast(discord.Guild, self.get_guild(config.NERDS["GUILD"]))
        self.general_channel = cast(discord.TextChannel, discord.utils.get(self.nerds_guild.channels, id=config.NERDS["GENERAL"]))
        self.zap_channel = cast(discord.TextChannel, discord.utils.get(self.nerds_guild.channels, id=config.NERDS["ZAP"]))

    async def on_message(self, message):
        if message.guild is None:
            return
        await self.process_commands(message)
        if "tenor" in message.content and "superman" in message.content:
            await message.delete()
        await message.channel.send("nao quero ver superman voando com a lingua pra fora")
            

    async def on_member_join(self, member):
        nrd_role = cast(discord.Role, discord.utils.get(self.nerds_guild.roles, name="NRD"))
        zap_role = cast(discord.Role, discord.utils.get(self.nerds_guild.roles, name="ZAP"))
        if member.bot is True:
            return
        if member.guild != self.nerds_guild:
            return
        if member.id in config.NERDS_MEMBERS:
            await member.add_roles(nrd_role)
        else:
            await member.add_roles(zap_role)
        await self.general_channel.send(
            f":clown: **{member.mention} has joined the server** :white_check_mark:"
        )
        await self.zap_channel.send(
            f":clown: **{member.mention} has joined the server** :white_check_mark:"
        )

    async def on_member_remove(self, member: discord.Member):
        if member.guild == self.nerds_guild and member.bot is False:
            await self.general_channel.send(f"**{member.mention} has left the server** :x:")
            await self.zap_channel.send(f"**{member.mention} has left the server** :x:")

    async def run_bot(self) -> None:
        await super().start(config.TOKEN, reconnect=True)


# NerdsBot instance
bot = NerdsBot()


@bot.command()
async def sync(ctx):
    if ctx.author.id != config.NERDS_MEMBERS[0]:
        return
    synced = await ctx.bot.tree.sync()
    await ctx.send(f":white_check_mark: Synced `{len(synced)}` commands")


# Maybe move this to a launcher file at some point?
asyncio.run(bot.run_bot())
