# -*- coding: utf-8 -*-
from __future__ import absolute_import
from concurrent.futures import as_completed

from discord import Embed
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from chemistry.solvers.utilities import SPECIAL_TO_NORMAL, _text_translate


def _prepare_query(reactants: str, products: str) -> str:
    def _prepare_inner(string: str, type: str) -> str:
        if string == "[u]":
            return f"{type}1="
        string = string.replace(" +", " ")
        string = "&".join(
            f"{type}{i}={f.strip()}" for i, f in enumerate(string.split(), 1)
        )
        return string

    r = _prepare_inner(reactants, "reactant")
    p = _prepare_inner(products, "product")
    return f"{r}&{p}&submit="


def _prepare_page_source(base_url: str, query: str) -> str:
    session = FuturesSession()
    rqs = (session.get(f"{base_url}{query}"),)
    for req in as_completed(rqs):
        resp = req.result()
        return resp.content.decode("utf-8")


def _extract_api_page_source(page_source: str, page_num: int) -> str:
    soup = BeautifulSoup(page_source, "html.parser")
    div_table = soup.find("div", {"class": "search-results-async"})
    if not div_table:
        return None
    reactantids = div_table.attrs.get("data-reactantids")
    productids = div_table.attrs.get("data-productids")
    offset = page_num * 10

    query = f"reactantIds={reactantids}&productIds={productids}&offset={offset}"
    base_url = "https://chemequations.com/api/search-reactions-by-compound-ids?"
    return _prepare_page_source(base_url=base_url, query=query)


def _add_embed_info(
    embed: Embed, inputs: str, read_as: str, time_elapsed: float
) -> Embed:
    embed.add_field(name="Inputs", value=inputs, inline=False)
    embed.add_field(name="Interpreted as", value=read_as, inline=False)
    embed.add_field(name="Finished in", value=f"{time_elapsed:.2f}s", inline=False)
    embed.set_footer(text="Powered by www.chemequations.com")
