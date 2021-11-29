# -*- coding: utf-8 -*-
from discord import Message, Game
from discord.ext.commands import Cog, Bot


class EventListener(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if self.bot.DEBUG:
            print(f"Bot ready {self.bot.user}.")

        await self.bot.change_presence(activity=Game("#on | #bal | #re | #predict"))

    @Cog.listener()
    async def on_disconnect(self):
        if self.bot.DEBUG:
            print(f"Bot disconnect from Discord.")

    @Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        if self.bot.DEBUG:
            pass

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        if self.bot.DEBUG:
            pass


def setup(bot):
    bot.add_cog(EventListener(bot))
