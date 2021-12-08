# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Iterable, List, Tuple
from timeit import default_timer

from bs4 import BeautifulSoup
from discord import Embed


from chemistry.solvers.solver_base_class import Periodni
from chemistry.solvers.periodni.utilities import (
    _prepare_queries,
    _prepare_page_sources,
    _text_translate,
    _parse_tag_to_unicode,
    _add_embed_info,
    SPECIAL_TO_NORMAL,
)


def _prepare_embed(
    inputs: Iterable[str],
    read_as: Iterable[str],
    unicodes: Iterable[str],
    results: Iterable[str],
    time_elasped: float,
) -> Embed:
    succeed = 0
    embed = Embed()
    for reaction, uni, res in zip(inputs, unicodes, results):
        if res:
            f_name = res
            f_value = f"""\
Unicode: ```{uni}```
Original: {reaction}\
"""
            succeed += 1
        else:
            f_name = "😐 Something went wrong."
            f_value = f"Original: {reaction}"
        embed.add_field(name=f_name, value=f_value, inline=False)
    total = len(results)
    embed.title = f"Balanced {succeed} of {total} Reaction(s)."
    success_rate = round(succeed / total, 2) * 100

    _add_embed_info(
        embed=embed,
        success_rate=success_rate,
        inputs=inputs,
        read_as=read_as,
        time_elasped=time_elasped,
    )
    return embed


class _SimpleBalance(Periodni):
    def solve(self, reactions: Tuple[str]) -> Embed:
        time_start = default_timer()

        reactions_normalized = []
        for r in reactions:
            normalized = _text_translate(r, SPECIAL_TO_NORMAL)
            reactions_normalized.append(normalized)

        queries = _prepare_queries(reactions_normalized)
        base_url = "https://www.periodni.com/balancing_chemical_equations.php?eq="
        page_sources = _prepare_page_sources(base_url=base_url, queries=queries)

        read_as_s = []
        unicode_s = []
        result_s = []
        for page_source in page_sources:
            self._format_page_source(
                read_as_target=read_as_s,
                unicode_traget=unicode_s,
                result_target=result_s,
                page_source=page_source,
            )

        time_end = default_timer()
        return _prepare_embed(
            inputs=reactions,
            read_as=read_as_s,
            unicodes=unicode_s,
            results=result_s,
            time_elasped=time_end - time_start,
        )

    def _format_page_source(
        self,
        read_as_target: List[str],
        unicode_traget: List[str],
        result_target: List[str],
        page_source: str,
    ) -> None:
        soup = BeautifulSoup(page_source, "html.parser")

        input_field = soup.find("input", {"name": "equation", "class": "txt-c"})
        read_as = input_field.get("value")
        read_as_target.append(read_as)

        result_div = soup.find("div", {"class": "eqbody"})
        error_blocks = soup.findAll(attrs={"class": "crven"})
        if not result_div or error_blocks:
            unicode = None
            result = None
        else:
            unicode = _parse_tag_to_unicode(result_div)
            result = _text_translate(unicode, SPECIAL_TO_NORMAL)
        unicode_traget.append(unicode)
        result_target.append(result)
