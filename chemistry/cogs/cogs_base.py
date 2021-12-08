# -*- coding: utf-8 -*-
from discord import Message
from discord.ext.commands import Cog, Bot, Context
from discord.ext.commands.errors import (
    CommandInvokeError,
    CommandNotFound,
    ExpectedClosingQuoteError,
    InvalidEndOfQuotedStringError,
)

from chemistry.solvers.solver_base_class import ChemistrySolverBaseClass
from chemistry.cogs._errors_msg import (
    NO_SPACE_BETWEEB_ARGS_MSG,
    UNCLOSED_ARGUMENT_MSG,
    KaitoonValueError,
)


class ChemistryCogBase(Cog):
    def __init__(self, bot: Bot, solver: ChemistrySolverBaseClass = None) -> None:
        self.bot = bot
        self.solver = solver

    async def cog_command_error(self, ctx: Context, e: Exception) -> None:
        if isinstance(e, CommandNotFound):
            return
        message: Message = ctx.message
        await message.remove_reaction("⌛", self.bot.user)
        await message.remove_reaction("👌", self.bot.user)
        await message.add_reaction("⚠")
        if isinstance(e, CommandInvokeError):
            if isinstance(e.original, KaitoonValueError):
                msg = ", ".join(e.original.args)
            else:
                print(e.args, type(e))
                msg = """\
Something went wrong. Please try again later.
(This is most likely the bot's fault.)\
"""
        elif isinstance(e, InvalidEndOfQuotedStringError):
            msg = NO_SPACE_BETWEEB_ARGS_MSG
        elif isinstance(e, ExpectedClosingQuoteError):
            msg = UNCLOSED_ARGUMENT_MSG

        await ctx.send(content=f"> {message.content}\n{msg}")

    async def cog_before_invoke(self, ctx: Context) -> None:
        message: Message = ctx.message
        await message.add_reaction("⌛")

    async def cog_after_invoke(self, ctx: Context) -> None:
        message: Message = ctx.message
        await message.remove_reaction("⌛", self.bot.user)
        await message.add_reaction("👌")
