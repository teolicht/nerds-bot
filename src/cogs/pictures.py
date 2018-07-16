#!/usr/bin/env python3

from discord.ext import commands
import discord
import random
import os

IMGUR = 'https://i.imgur.com/'
NSFW_MSG = ":x: This must be a NSFW channel."
THIS_PATH = os.path.dirname(__file__)
# Take lists of links in file and put them all in a single list
with open(os.path.join(THIS_PATH, "text", "pics_links.txt")) as links:
    links = links.readlines()
    pics_links = [links[0], links[1], links[2], links[3], links[4]]
    # Remove the '\n' from the last link of each list
    for x, links in enumerate(pics_links):
        pics_links[x] = pics_links[x].split()

class Pictures(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        picture = random.choice(pics_links[0])
        em = discord.Embed(title=':smiley_cat: A cat pic/GIF')
        em.set_image(url=IMGUR + picture)
        await ctx.send(embed=em)

    @commands.command()
    async def dog(self, ctx):
        picture = random.choice(pics_links[1])
        em = discord.Embed(title=':dog: A dog pic/GIF')
        em.set_image(url=IMGUR + picture)
        await ctx.send(embed=em)

    # @commands.command(name='nsfw', aliases=['Nsfw', 'NSFW'])
    # async def _nsfw(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(NSFW_MSG)
    #
    #     picture = random.choice(pics_links[2])
    #     em = discord.Embed(title=':warning: A NSFW pic/GIF')
    #     em.set_image(url=IMGUR + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)
    #
    #
    # @commands.command(name='tits', aliases=['Tits', 'TITS', 'tit'])
    # async def _tits(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(NSFW_MSG)
    #
    #     picture = random.choice(pics_links[3])
    #     em = discord.Embed(title=':warning: A tits pic/GIF')
    #     em.set_image(url=IMGUR + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)
    #
    # @commands.command(name='pussy', aliases=['Pussy', 'PUSSY', 'pusy'])
    # async def _pussy(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(NSFW_MSG)
    #
    #     picture = random.choice(pics_links[4])
    #     em = discord.Embed(title=':warning: A pussy picture')
    #     em.set_image(url=IMGUR + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)


def setup(bot):
    bot.add_cog(Pictures(bot))
