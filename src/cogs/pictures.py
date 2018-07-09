#!/usr/bin/env python3

from discord.ext import commands
import discord

import random


imgur = 'https://i.imgur.com/'
nsfw_msg = ":x: This must be a NSFW channel."


class Pictures():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        pictures = ['D7slglx.jpg', 'tTazYTJ.jpg', '7P3XJSb.gif', 'EHC0tGc.jpg', 'tIR9mOk.gif', 'qaG8zRt.jpg',
                    'kuKam1M.gif', 'WM22gA7.gif', 'S0nvOVx.jpg', 'owQqVlZ.jpg', 'PxYsA84.jpg', 'gQAHTbw.jpg',
                    'Z1Jputc.jpg', 'R3UB9Es.jpg', 'kDS1u7Y.jpg', 'CGrEZp8.jpg', 'hYozkVO.jpg', 'FqfUdZD.jpg',
                    'qx2FRFY.jpg', '7poWAFc.jpg', 'rgcWXPj.jpg', '2q4vgps.png', '0uVluZJ.jpg', 'TUUHrGX.png',
                    'qo3H2Q0.jpg', '3G3k6UR.jpg', 'k8vt44s.jpg', 'Y8Gi8Wh.jpg', 'GYY0uZa.jpg', 'kOea3ma.jpg',
                    'MW7P2Lx.png', 'LjYc6sE.jpg', '5Xr9ZXE.png', 'v7Q2WK2.jpg', 'RXWrHMP.jpg', 'JDZduCb.jpg']
        picture = random.choice(pictures)

        em = discord.Embed(title=':smiley_cat: A cat pic/GIF')
        em.set_image(url=imgur + picture)
        await ctx.send(embed=em)

    @commands.command()
    async def dog(self, ctx):
        pictures = ['4pjxBbU.jpg', 'OE2Y4Up.gif', 'ZeyNiVN.jpg', 'e1iQ9ON.jpg', 'PMALJsz.jpg', 'Xb4Anu4.gif',
                    'C96HHvf.jpg', 'dzifbAM.gif', 'yW1lgbW.jpg', 'LhGZWTo.jpg', 'n3wajqy.gif', 'fwelOiw.jpg',
                    'V3qLi4T.jpg', 'YJs3JF5.jpg', 'Dz8HIU3.gif', 'pFG1Vt3.jpg', '2dOQ8cX.jpg', '9DCOnGA.jpg',
                    '5KmeC75.gif', 'Zv7Wn2Z.jpg', 'jdYiPYg.jpg', 'sOuAGw7.gif', 'mmvSaf9.jpg', 'Q2Cijdi.jpg',
                    'aNHs6az.jpg', 'zu7Lx9j.gif', 'fJpQLU5.jpg', 'hG4f7zJ.jpg', 'UKhWR6k.jpg', 'bfu6JPv.gif',
                    'QVk71pA.jpg', 'uAKo3Qk.jpg', 'DEGYqKw.png', '0xjsiL3.jpg', '8qYmgsY.jpg', 'R8bqHEH.jpg']
        picture = random.choice(pictures)

        em = discord.Embed(title=':dog: A dog pic/GIF')
        em.set_image(url=imgur + picture)
        await ctx.send(embed=em)

    # @commands.command(name='nsfw', aliases=['Nsfw', 'NSFW'])
    # async def _nsfw(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(nsfw_msg)
    #
    #     pictures = ['Fe8uKGb.jpg', '2EMMEjD.jpg', 'hTFwdD2.jpg', 'aUfmUNA.jpg', '0trtQhu.jpg',
    #                 '1BSclpy.gif', 'TK7bEUC.gif', '5w9lZdW.jpg', 'SxC488W.jpg', 'qMcjfML.jpg',
    #                 '4QkrgLe.jpg', 'NSTkcUq.jpg', 'NqTNFZt.jpg', 'WYl5i5B.jpg', 'y917MDd.jpg',
    #                 '6fXiF11.jpg', 'jG1qEX7.jpg', 'C2b2Nbl.jpg', 'mjZ9Llv.jpg', 'UdrnQ6k.gif']
    #     picture = random.choice(pictures)
    #
    #     em = discord.Embed(title=':warning: A NSFW pic/GIF')
    #     em.set_image(url=imgur + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)
    #
    #
    # @commands.command(name='tits', aliases=['Tits', 'TITS', 'tit'])
    # async def _tits(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(nsfw_msg)
    #
    #     pictures = ['sh2N8U3.jpg', 'smi1RCf.jpg', 'TWJfw8G.png', 'NRDmdSk.png', '6f84FZS.png', 'n3IpCbH.png',
    #                 'OWDzjwh.png', 'oKXXTQ1.png', 'dBFKqsc.jpg', 'IA8AmfK.png', 'OwsZgzs.png', 'sufbpw9.jpg',
    #                 'bCQ4bne.jpg', 'KDxBfGf.jpg', '5FNjGYn.png', 'eBVHjH0.jpg', 'WScEJfJ.jpg', 'NfnBE9i.jpg',
    #                 '22RqMkb.jpg', 'uugd2yf.jpg', 'yQTzARM.jpg', '9f5X3Sk.jpg', 'nJY3lCO.jpg', 'uTbyzVw.jpg',
    #                 'zc7f8j0.jpg', 'i10zrFO.jpg', 'a7WNr7f.png', 'mBKYDW7.jpg', 'upyFZwp.jpg', 'yNyfnxv.jpg',
    #                 'wWQRNq6.gif', 'H4BUKet.jpg', 'ZLJzcWO.jpg', 'NAOoeZm.png', 'DMp9b4g.png', 'YrCpnLq.jpg']
    #     picture = random.choice(pictures)
    #
    #     em = discord.Embed(title=':warning: A tits pic/GIF')
    #     em.set_image(url=imgur + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)
    #
    # @commands.command(name='pussy', aliases=['Pussy', 'PUSSY', 'pusy'])
    # async def _pussy(self, ctx):
    #     if not ctx.channel.is_nsfw():
    #         return await ctx.send(nsfw_msg)
    #
    #     pictures = ['cKINeCG.jpg', 'B8Xss4J.jpg', '0DzogRR.jpg', 'hXa8p8s.jpg', 'Gr9Llaa.png',
    #                 'ToWATjf.jpg', 'eiQupQC.jpg', 'OTKwNWZ.jpg', 'ZBJXsvm.jpg', 'zHFW8Sx.jpg']
    #     picture = random.choice(pictures)
    #
    #     em = discord.Embed(title=':warning: A pussy picture')
    #     em.set_image(url=imgur + picture)
    #     em.set_footer(text='This message will be deleted after 60 seconds.')
    #     await ctx.send(embed=em, delete_after=60.0)


def setup(bot):
    bot.add_cog(Pictures(bot))
