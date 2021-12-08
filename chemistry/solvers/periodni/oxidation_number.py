# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Iterable, List, Tuple
from timeit import default_timer

from bs4 import BeautifulSoup, element
from discord import Embed

from chemistry.solvers.solver_base_class import Periodni
from chemistry.solvers.periodni.utilities import (
    _prepare_page_sources,
    _text_translate,
    _add_embed_info,
    SUPERSCRIPTIONS,
    SUBSCRIPTIONS,
    SPECIAL_TO_NORMAL,
)


def _prepare_result_unicode(result_div: element.Tag) -> str:
    res = ""
    for child in result_div.childGenerator():
        if child.name == "span":
            res += child.get_text(" ", strip=True).split()[0]
        elif child.name == "sup":
            res += _text_translate(child.text, SUPERSCRIPTIONS)
        elif child.name == "sub":
            res += _text_translate(child.text, SUBSCRIPTIONS)
        else:
            res += child.text
    return res


def _prepare_result(result_element: element.Tag) -> Tuple[str]:
    res = []
    for child in result_element.childGenerator():
        if (
            isinstance(child, element.Tag)
            and child.name == "span"
            and child.find("span", {"class": "oxbr"})
        ):
            result = child.text
            if "+" in result:
                sign_index = result.find("+")
                seperator = ">" * (3 - sign_index)
                result = result.replace("+", f"{seperator} +")
            else:
                sign_index = result.find("-")
                seperator = ">" * (3 - sign_index)
                result = result.replace("-", f"{seperator} -")
            res.append(result)
    return tuple(res)


def _prepare_embed(
    inputs: Iterable[str],
    read_as: Iterable[str],
    unicodes: Iterable[str],
    results: Iterable[str],
    time_elapsed: float,
) -> Embed:
    succeed = 0
    embed = Embed()
    for compound, uni, res in zip(inputs, unicodes, results):
        if res:
            res = "\n".join(res)
            f_value = f"Unicode: ```{uni}``````{res}```"
            succeed += 1
        else:
            f_value = "😐 Something went wrong."
        embed.add_field(name=compound, value=f_value)

    total = len(inputs)
    embed.title = f"Assigned {succeed} of {total} Compound(s)."
    success_rate = round(succeed / total, 2) * 100

    _add_embed_info(
        embed=embed,
        success_rate=success_rate,
        inputs=inputs,
        read_as=read_as,
        time_elasped=time_elapsed,
    )
    return embed


class _OxidationNumberAssignment(Periodni):
    def solve(self, compounds: Tuple[str]) -> Embed:
        timer_start = default_timer()

        inputs_normalized = []
        for c in compounds:
            normalized = _text_translate(c, SPECIAL_TO_NORMAL)
            inputs_normalized.append(normalized)

        read_as_s = []
        unicode_s = []
        result_s = []
        base_url = "https://www.periodni.com/oxidation_numbers_calculator.php?eq="
        page_sources = _prepare_page_sources(
            base_url=base_url, queries=inputs_normalized
        )
        for page_source in page_sources:
            self._format_page_source(
                read_as_target=read_as_s,
                unicode_target=unicode_s,
                result_target=result_s,
                page_source=page_source,
            )

        timer_end = default_timer()
        return _prepare_embed(
            inputs=compounds,
            read_as=read_as_s,
            unicodes=unicode_s,
            results=result_s,
            time_elapsed=timer_end - timer_start,
        )

    def _format_page_source(
        self,
        read_as_target: List[str],
        unicode_target: List[str],
        result_target: List[str],
        page_source: str,
    ) -> None:
        soup = BeautifulSoup(page_source, "html.parser")

        input_field = soup.find("input", {"name": "equation", "class": "txt-c"})
        read_as = input_field.get("value")
        read_as_target.append(read_as)

        result_element = soup.find("div", {"class": "onresult"})
        error_blocks = soup.findAll(attrs={"class": "crven"})
        if not result_element or error_blocks:
            unicode = None
            result = None
        else:
            unicode = _prepare_result_unicode(result_element)
            result = _prepare_result(result_element)
        unicode_target.append(unicode)
        result_target.append(result)
