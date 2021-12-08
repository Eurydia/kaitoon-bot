# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Tuple
from json import loads
from timeit import default_timer

from discord import Embed, Colour
from bs4 import BeautifulSoup, element

from chemistry.solvers.solver_base_class import ChemEquation
from chemistry.solvers.chemequations.utilities import (
    _add_embed_info,
    _prepare_page_source,
    _prepare_query,
    _extract_api_page_source,
    _text_translate,
    SPECIAL_TO_NORMAL,
)


def _prepare_embed(
    total: int,
    offset: int,
    formatted_equation: Tuple[str],
    inputs: str,
    read_as: str,
    time_elapsed: float,
) -> Embed:
    embed = Embed()
    if not formatted_equation:
        title = "😐 Something went wrong."
        desc = ""
        embed.color = Colour.red()
        embed.add_field(name="Status", value="❎ Failed", inline=False)
    else:
        title = f"Found {total} equation(s)!"
        embed.color = Colour.green()
        embed.add_field(name="Status", value="✅ Success", inline=False)
        f_index = offset + 1
        l_index = 0

        to_display = []
        for i, eq in enumerate(formatted_equation, f_index):
            l_index = i
            to_display.append(f"{i}. {eq}")

        to_display = "\n".join(to_display)
        desc = f"""\
Showing result {f_index} - {l_index} of **{total}** equations
{to_display}\
"""
    embed.title = title
    embed.description = desc

    _add_embed_info(
        embed=embed, inputs=inputs, read_as=read_as, time_elapsed=time_elapsed
    )
    return embed


class _ReactionPrediction(ChemEquation):
    def solve(self, reactants: str, products: str, page_num: int) -> Embed:
        timer_start = default_timer()

        react_normalized = _text_translate(reactants, SPECIAL_TO_NORMAL)
        prod_normalized = _text_translate(products, SPECIAL_TO_NORMAL)

        query = _prepare_query(react_normalized, prod_normalized)
        base_url = "https://chemequations.com/en/advanced-search/?"
        page_source = _prepare_page_source(base_url=base_url, query=query)
        api_page_source = _extract_api_page_source(
            page_source=page_source, page_num=page_num
        )
        total, offset, formatted_eq = self._format_page_source(api_page_source)

        def _input_given(input_: str) -> str:
            if input_ == "[u]":
                return "[unspecified]"
            return input_

        i_react = _input_given(reactants)
        i_prod = _input_given(products)
        inputs = f'"{i_react} and {i_prod}" (Page {page_num + 1})'

        def _input_read_as(input_: str) -> str:
            if input_ == "[u]":
                return _input_given(input_)
            input_ = input_.replace(" +", " ")
            input_ = (i.strip() for i in input_.split())
            return " + ".join(input_)

        r_react = _input_read_as(reactants)
        r_prod = _input_read_as(products)
        read_as = f'"{r_react} = {r_prod}" (Page {page_num + 1})'

        timer_end = default_timer()
        return _prepare_embed(
            total=total,
            offset=offset,
            formatted_equation=formatted_eq,
            inputs=inputs,
            read_as=read_as,
            time_elapsed=timer_end - timer_start,
        )

    def _format_page_source(self, page_source: str) -> Tuple[int, Tuple[str]]:
        json_dict = loads(page_source)

        formatted_equations = []
        for equation in json_dict.get("searchResults"):
            soup = BeautifulSoup(equation.get("equationStrBold", ""), "html.parser")
            component = []
            for child in soup.childGenerator():
                if isinstance(child, element.Tag):
                    c = f"__{child.text.strip()}__"
                else:
                    c = child.text.strip()
                component.append(c)
            eq = " ".join(component)
            eq = eq.replace(":", "")
            formatted_equations.append(eq)
        return (
            json_dict.get("resultCount", 0),
            json_dict.get("offset", 0),
            tuple(formatted_equations),
        )
