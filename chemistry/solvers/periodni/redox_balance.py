# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Iterable, Tuple
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


def _prepare_queries_redox(
    reactions_with_median: Tuple[Tuple[str, str], ...]
) -> Tuple[str]:
    res = []
    for react, m in reactions_with_median:
        m = "acidic" if m.startswith("a") else "basic"
        react = _prepare_queries((react,))[0]
        res.append(f"{react}&medium={m}")
    return tuple(res)


def _prepare_embed(
    inputs: Iterable[Tuple[str, str]],
    read_as: Iterable[Tuple[str, str]],
    unicodes: Iterable[str],
    results: Iterable[str],
    time_elasped: float,
) -> Embed:
    succeed = 0
    embed = Embed()
    for reaction, uni, res in zip(inputs, unicodes, results):
        r, m = reaction
        if res:
            f_name = f"({m}) {res}"
            f_value = f"""\
Unicode: ```{uni}```
Original: {r} {m}\
"""
            succeed += 1
        else:
            f_name = "😐 Something went wrong."
            f_value = f"Original: {r} {m}"
        embed.add_field(name=f_name, value=f_value, inline=False)
    total_coumpound = len(results)
    embed.title = f"Balanced {succeed} of {total_coumpound} Redox Reaction(s)."
    success_rate = round(succeed / total_coumpound, 2) * 100

    _add_embed_info(
        embed=embed,
        success_rate=success_rate,
        inputs=(f"({m}) {r}" for r, m in inputs),
        read_as=read_as,
        time_elasped=time_elasped,
    )
    return embed


class _RedoxBalance(Periodni):
    def solve(self, reactions_with_median: Tuple[Tuple[str, str], ...]) -> Embed:
        timer_start = default_timer()

        reactions_median_normalized = []
        for r, m in reactions_with_median:
            r_normalized = _text_translate(r, SPECIAL_TO_NORMAL)
            reactions_median_normalized.append((r_normalized, m))

        queries = _prepare_queries_redox(reactions_median_normalized)
        base_url = "https://www.periodni.com/ars_method.php?eq="
        page_sources = _prepare_page_sources(base_url=base_url, queries=queries)

        read_as_s = []
        unicode_s = []
        result_s = []
        for page_source in page_sources:
            self._format_page_source(
                read_as_target=read_as_s,
                unicode_target=unicode_s,
                result_target=result_s,
                page_source=page_source,
            )

        timer_end = default_timer()
        return _prepare_embed(
            inputs=reactions_with_median,
            read_as=read_as_s,
            unicodes=unicode_s,
            results=result_s,
            time_elasped=timer_end - timer_start,
        )

    def _format_page_source(
        self,
        read_as_target: Iterable[str],
        unicode_target: Iterable[str],
        result_target: Iterable[str],
        page_source: str,
    ) -> None:
        soup = BeautifulSoup(page_source, "html.parser")

        input_field = soup.find("input", {"name": "equation", "class": "txt-c"})
        value = input_field.get("value")
        radio_button = soup.find("input", {"name": "radioMedium", "id": "intAcidic"})
        median = "acidic" if radio_button.get("value") == "0" else "basic"
        read_as_target.append(f"({median}) {value}")

        result_div = soup.find("div", {"class": "eq-final"})
        error_blocks = soup.findAll(attrs={"class": "crven"})
        if not result_div or any(e.name != "span" for e in error_blocks):
            unicode = None
            result = None
        else:
            unicode = _parse_tag_to_unicode(result_div)
            result = _text_translate(unicode, SPECIAL_TO_NORMAL)
        unicode_target.append(unicode)
        result_target.append(result)
