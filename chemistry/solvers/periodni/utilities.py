# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Iterable, Tuple
from concurrent.futures import as_completed

from bs4 import element
from discord import Embed, Colour
from requests_futures.sessions import FuturesSession

from chemistry.solvers.utilities import (
    SUBSCRIPTIONS,
    SUPERSCRIPTIONS,
    SPECIAL_TO_NORMAL,
    _text_translate,
)


def _prepare_queries(inputs: Tuple[str]) -> Tuple[str]:
    def _prepare_query_inner(q: str) -> str:
        q = q.replace(" +", " ")
        res = (x.strip() for x in q.split())
        res = "%2B".join(res)
        res = res.replace("+", "%2B")
        return res

    res = []
    for query in inputs:
        r, p = query.split("=")
        r = _prepare_query_inner(r)
        p = _prepare_query_inner(p)
        res.append(f"{r}%3D{p}")
    return tuple(res)


def _prepare_page_sources(base_url: str, queries: Tuple[str]) -> Tuple[str]:
    session = FuturesSession()
    # We use a dictionary here
    # to keep request queries
    # in the same order
    lookup = {}
    requests = []
    for query in queries:
        query = query.replace(" ", "")
        request = session.get(f"{base_url}{query}")
        lookup[request] = None
        requests.append(request)

    for request in as_completed(requests):
        respond = request.result()
        content = respond.content.decode("utf-8")
        lookup[request] = content
    return tuple(lookup.values())


def _parse_tag_to_unicode(result_element: element.Tag):
    res = ""
    for child in result_element.childGenerator():
        if isinstance(child, element.Comment):
            continue
        if isinstance(child, element.NavigableString):
            res += child.text
        elif child.name == "sub":
            res += _text_translate(child.text, SUBSCRIPTIONS)
        elif child.name == "sup":
            res += _text_translate(child.text, SUPERSCRIPTIONS)
        elif child.name == "span":
            res += " → "
    res = res.replace("\n", " ")

    res = res.split(" + ")
    res = " + ".join(x.strip() for x in res)

    res = res.split("→")
    res = " ⇆ ".join(x.strip() for x in res)
    return res


def _add_embed_info(
    embed: Embed,
    success_rate: int,
    inputs: Iterable[str],
    read_as: Iterable[str],
    time_elasped: float,
) -> Embed:
    if success_rate == 0:
        embed.color = Colour.red()
        embed.add_field(
            name="Status", value=f"❎ Failed ({success_rate}%)", inline=False
        )
    else:
        embed.color = Colour.green()
        embed.add_field(
            name="Status", value=f"✅ Success ({success_rate}%)", inline=False
        )
    embed.add_field(
        name="Inputs", value="\n".join(f'🔹 " {x} "' for x in inputs), inline=False
    )
    embed.add_field(
        name="Interpreted as",
        value="\n".join(f'🔸 " {x} "' for x in read_as),
        inline=False,
    )
    embed.add_field(name="Finished in", value=f"{time_elasped:.2f}s", inline=False)
    embed.set_footer(text="Powered by www.periodni.com")
