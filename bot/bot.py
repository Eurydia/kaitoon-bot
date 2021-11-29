# -*- coding: utf-8 -*-
from os import environ

from discord.ext import commands


class Kaitoon(commands.Bot):
    def __init__(self, command_prefix: str) -> None:
        super().__init__(command_prefix)

        self.DEBUG = True
        self.remove_command("help")

        cogs = ("chemistry.cogs", "bot.listeners")

        for cog in cogs:
            self.load_extension(cog)
