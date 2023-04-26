import random
import discord

from discord import app_commands


imgur = "https://i.imgur.com/"
transparent_color = 0x302C34

##### Isn't there an easier way to do this? Put the links as json
# Take lists of links in file and put them all in a single list
with open("cogs/text/pics_links.txt", "r") as file:
    links = file.readlines()
    pics_links = [links[0], links[1], links[2], links[3], links[4]]
    file.close()
    # Remove the '\n' from the last link of each list
    for x, links in enumerate(pics_links):
        pics_links[x] = pics_links[x].split()


class Pictures(app_commands.Group):
    @app_commands.command(description="A cat pic/GIF.")
    async def cat(self, interaction: discord.Interaction):
        picture = random.choice(pics_links[0])
        em = discord.Embed(title=":smiley_cat: A cat pic/GIF", color=transparent_color)
        em.set_image(url=imgur + picture)
        await interaction.response.send_message(embed=em)

    @app_commands.command(description="A dog pic/GIF")
    async def dog(self, interaction: discord.Interaction):
        picture = random.choice(pics_links[1])
        em = discord.Embed(title=":dog: A dog pic/GIF", color=transparent_color)
        em.set_image(url=imgur + picture)
        await interaction.response.send_message(embed=em)


async def setup(bot):
    bot.tree.add_command(Pictures(name="pic", description="Picture commands."))
