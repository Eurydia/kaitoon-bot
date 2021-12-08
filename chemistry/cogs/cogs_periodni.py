# -*- coding: utf-8 -*-
from typing import Any, Tuple
from discord.ext.commands import Bot, command, Context


from chemistry.solvers.periodni import (
    _RedoxBalance,
    _SimpleBalance,
    _OxidationNumberAssignment,
)
from chemistry.cogs._errors_msg import (
    NO_ARGUMENT_GIVEN_MSG,
    NO_ARROW_SEP_FOUND_MSG,
    INCORRECT_MEDIAN_MSG,
    KaitoonValueError,
)

from chemistry.cogs.cogs_base import ChemistryCogBase
from chemistry.cogs.uilities import _is_valid_reaction, _split_reaction, ACCEPTED_MEDIAN


class ONAssignment(ChemistryCogBase):
    def __init__(self, bot) -> None:
        super().__init__(bot, _OxidationNumberAssignment())

    @command(name="on")
    async def solve(self, ctx: Context, *args: str) -> None:
        args = [arg for arg in args if arg]
        if len(args) == 0:
            raise KaitoonValueError(NO_ARGUMENT_GIVEN_MSG)
        result = self.solver.solve(args)
        await ctx.send(embed=result)


class SimpleBalance(ChemistryCogBase):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _SimpleBalance())

    @command(name="balance", aliases=["bal"])
    async def solve(self, ctx: Context, *args: str) -> None:
        args = [arg for arg in args if arg]
        match len(args):
            case 0:
                raise KaitoonValueError(NO_ARGUMENT_GIVEN_MSG)
            case 1:
                # Assumes input is in this format
                # [reaction]
                if not _is_valid_reaction(args[0]):
                    raise KaitoonValueError(NO_ARROW_SEP_FOUND_MSG)
                reaction = args[0]
            case _:
                # Assumes input is in this format
                # [reactants] [products]
                reaction = f"{args[0]} = {args[1]}"

        r, p = _split_reaction(reaction)
        reactions = (f"{r} = {p}",)
        result = self.solver.solve(reactions)
        await ctx.send(embed=result)


class RedoxBalance(ChemistryCogBase):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _RedoxBalance())

    @command(name="redox", aliases=["re"])
    async def solve(self, ctx: Context, *args: str) -> None:
        args = [arg for arg in args if arg]
        match len(args):
            case 0:
                raise KaitoonValueError(NO_ARGUMENT_GIVEN_MSG)
            case 1:
                # Assumes input is in this format
                # [reaction]
                if not _is_valid_reaction(args[0]):
                    raise KaitoonValueError(NO_ARROW_SEP_FOUND_MSG)
                reaction = args[0]
                median = "acidic"
            case 2:
                # Assumes input is in one of these formats
                # [reaction] [median] or
                # [reactatns] [products]
                if _is_valid_reaction(args[0]):
                    # Arrow sep found
                    reaction = args[0]
                    median = args[1]
                else:
                    reaction = f"{args[0]} = {args[1]}"
                    median = "acidic"
            case _:
                # Assumes the input is in this format
                # [reactants] [product] [median]
                reaction = f"{args[0]} = {args[1]}"
                median = args[2]

        if median not in ACCEPTED_MEDIAN:
            raise KaitoonValueError(INCORRECT_MEDIAN_MSG)
        r, p = _split_reaction(reaction)
        reactions_with_median = ((f"{r} = {p}", median),)
        result = self.solver.solve(reactions_with_median)
        await ctx.send(embed=result)


def setup(bot):
    cogs = (ONAssignment, SimpleBalance, RedoxBalance)
    for cog in cogs:
        bot.add_cog(cog(bot))
