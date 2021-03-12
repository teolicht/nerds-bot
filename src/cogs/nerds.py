import discord


def nerds(guild, option: str = False):
    if option is False:
        return guild

    if option == 'clachip':
        return guild.get_member(311560201197191169)
    elif option == 'jeff':
        return guild.get_member(388637185328545793)
    elif option == 'jhkm':
        return guild.get_member(306850362051002370)
    elif option == 'lanit':
        return guild.get_member(300761654411526154)
    elif option == 'leo':
        return guild.get_member(310876103575076864)
    elif option == 'lorenzo':
        return guild.get_member(310603895238033413)
    elif option == 'mesh':
        return guild.get_member(306542879520849922)
    elif option == 'ogdroid':
        return guild.get_member(249639204441686016)
    elif option == 'pedron':
        return guild.get_member(366304595015892994)
    elif option == 'poketheo':
        return guild.get_member(301084407509286913)
    elif option == 'sucumaracuja':
        return guild.get_member(383679852227854336)
    elif option == 'lorenzo_role':
        return discord.utils.get(guild.roles, id=425688731190820864)
    elif option == 'nrd':
        return discord.utils.get(guild.roles, id=434417111629299712)
    else:
        return None
