# -*- coding: utf-8 -*-
from typing import Any, Tuple
from discord.ext.commands import Bot, command, Context
from chemistry.solvers.chemequations import _ReactionPrediction
from chemistry.cogs._errors_msg import (
    NO_ARGUMENT_GIVEN_MSG,
    NO_ARROW_SEP_FOUND_MSG,
    KaitoonValueError,
)

from chemistry.cogs.cogs_base import ChemistryCogBase
from chemistry.cogs.uilities import _is_valid_reaction, _split_reaction


def _to_int(number: Any) -> int:
    try:
        return int(number)
    except ValueError:
        raise KaitoonValueError("The page index you've given is invalid.")


class ReactionPrediction(ChemistryCogBase):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot, _ReactionPrediction())

    @command(name="predict", aliases=["pred"])
    async def solve(self, ctx: Context, *args: str) -> None:
        match len(args):
            case 0:
                raise KaitoonValueError(NO_ARGUMENT_GIVEN_MSG)
            case 1:
                # Assumes input is in this format
                # [reaction]
                if not _is_valid_reaction(args[0]):
                    raise KaitoonValueError(NO_ARROW_SEP_FOUND_MSG)
                reaction = args[0]
                page = 1
            case 2:
                # Two possible cases:
                # [reactants] [products] and
                # [reaction] [page number]
                if not _is_valid_reaction(args[0]):
                    # no arrow seperator,
                    # assumes input is in this format
                    # [reactants] [product]
                    reaction = f"{args[0]} = {args[1]}"
                    page = 1
                else:
                    # Arrow seperator found,
                    # assumes input is in this format
                    # [reaction] [page num]
                    reaction = args[0]
                    page = _to_int(args[1])
            case _:
                # Assumes input is in this format
                # [reactants] [product] [page num]
                reaction = f"{args[0]} = {args[1]}"
                page = _to_int(args[2])

        if page < 1:
            raise KaitoonValueError("The page index you've given is out of range.")
        r, p = _split_reaction(reaction, allow_unspecified=True)
        result = self.solver.solve(r, p, page - 1)
        await ctx.send(embed=result)


def setup(bot):
    bot.add_cog(ReactionPrediction(bot))
