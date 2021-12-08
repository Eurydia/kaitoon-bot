# -*- coding: utf-8 -*-
from typing import Tuple
from chemistry.cogs._errors_msg import (
    A_REACTION_COMPONENT_IS_EMPTY_MSG,
    REACTION_COMPONENTS_ARE_UNSPECIFIED_MSG,
    UNSPECIFIED_NOT_ALLOWED_MSG,
)


ACCEPTED_ARROWS = {" = "}
ACCEPTED_MEDIAN = {"a", "acidic", "b", "basic"}


def _is_valid_reaction(reaction: str) -> None:
    return any(arr in reaction for arr in ACCEPTED_ARROWS)


def _split_reaction(reaction: str, allow_unspecified: bool = False) -> Tuple[str, str]:
    for arr in ACCEPTED_ARROWS:
        if arr in reaction:
            r, p = reaction.split(arr, maxsplit=1)
            break
    r = r.strip()
    p = p.strip()
    if not r or not p:
        raise ValueError(A_REACTION_COMPONENT_IS_EMPTY_MSG)
    if r == "[u]" and p == "[u]":
        raise ValueError(REACTION_COMPONENTS_ARE_UNSPECIFIED_MSG)
    if r == "[u]" or p == "[u]":
        if not allow_unspecified:
            raise ValueError(UNSPECIFIED_NOT_ALLOWED_MSG)
    return r, p
