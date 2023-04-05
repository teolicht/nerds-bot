import discord
from discord import app_commands


class Help(app_commands.Group):
    @app_commands.command(description="All command categories.")
    async def categories(self, interaction: discord.Interaction):
        bot = discord.utils.get(interaction.guild.members, id=465945853220093954)
        em = discord.Embed(color=0xFF0414)
        em.set_author(name="NerdsBot Commands", icon_url=bot.display_avatar)
        em.add_field(
            name="/help info",
            value=":information_source: View the informative commands.",
        )
        em.add_field(
            name="/help pics", value=":camera: View the picture commands.", inline=False
        )
        em.add_field(
            name="/help fun", value=":jigsaw: View the fun commands.", inline=False
        )
        em.add_field(
            name="/help utils",
            value=":wrench: View the utility commands.",
            inline=False,
        )
        em.add_field(
            name="/help reddit",
            value="<:REDDIT:1093033093687951451> View the Reddit commands.",
            inline=False,
        )
        em.add_field(
            name="/help music", value=":musical_note: View the music commands."
        )
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Informative commands.")
    async def info(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(name="/member", value="Get info on a member.")
        em.add_field(name="/server", value="Get info on this server.", inline=False)
        em.add_field(name="/ping", value="Check my latency.")
        em.add_field(name="/info", value="Check some info about me.", inline=False)
        em.add_field(name="/news", value="Check the latest news (Google News).")
        em.title = f":information_source: Informative commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Picture commands.")
    async def pics(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(name="/pic cat", value="A cat pic/GIF.")
        em.add_field(name="/pic dog", value="A dog pic/GIF.", inline=False)
        em.title = f":camera: Picture commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Fun commands.")
    async def fun(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(name="n!say <text>", value="Speak as if you were me.")
        em.add_field(
            name="n!big <text>",
            value="Speak as if you were me, but through letter-emojis.",
            inline=False,
        )
        em.add_field(name="/sayto", value="Send someone a message.")
        em.add_field(name="/roast", value="Roast someone.", inline=False)
        em.add_field(name="/kill", value="Kill someone.")
        em.add_field(name="/suicide", value="Kill yourself.", inline=False)
        em.add_field(name="/respawn", value="Respawn someone.")
        em.add_field(name="/rps", value="Play Rock, Paper, Scissors.", inline=False)
        em.add_field(name="/annoy", value="Annoy someone.")
        em.add_field(name="/fact", value="Get a random fact.", inline=False)
        em.add_field(name="/ship", value="Ship two members.")
        em.add_field(name="/cum", value="Don't try this one.", inline=False)
        em.title = f":jigsaw: Fun commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Useful commands.")
    async def utils(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(name="/delete", value="Delete messages in the channel.")
        em.add_field(name="/timer", value="Start a timer.", inline=False)
        em.add_field(name="/calc", value="Do a calculation.")
        em.add_field(
            name="/flip",
            value="Flip a coin. Can land on heads or tails.",
            inline=False,
        )
        em.add_field(
            name="/randnum",
            value="Generate a random number between min and max.",
        )
        em.add_field(
            name="/poll",
            value="Start a poll.",
            inline=False,
        )
        em.add_field(name="/choose", value="Choose from a list of options.")
        em.add_field(
            name="/tag",
            value="Various tag commands.",
            inline=False,
        )
        em.title = f":wrench: Utility commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Reddit commands.")
    async def reddit(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(
            name="/reddit",
            value="Random hot post from specified subreddit.",
        )
        em.add_field(name="/reddit ban", value="Ban a subreddit.", inline=False)
        em.add_field(name="/reddit unban", value="Unban a subreddit.", inline=False)
        em.add_field(
            name="/reddit banlist", value="List of banned subreddits.", inline=False
        )
        em.title = f"<:REDDIT:1093033093687951451> Reddit commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="Music commands.")
    async def music(self, interaction: discord.Interaction):
        em = discord.Embed(color=0xFF0414)
        em.add_field(name="Coming soon", value="...")
        em.title = f":musical_note: Music commands ({len(em.fields)})"
        await interaction.response.send_message(embed=em)


async def setup(bot):
    bot.tree.add_command(
        Help(name="help", description="Information on all the commands.")
    )
