from typing import Union, Dict

from discord import Embed, Colour
from bs4 import BeautifulSoup, element


SUPERSCRIPTIONS = {key:val for key, val in zip('0123456789-+', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺')}
SUBSCRIPTIONS = {key:val for key, val in zip('0123456789', '₀₁₂₃₄₅₆₇₈₉')}


def prepare_unbalanced(r: str, p: str) -> str:
    r, p = map(lambda s: s.replace(',', ' ').replace(' + ', ' '), (r, p))
    r, p = map(lambda s: s.split(), (r, p))
    reaction: str = f'{" + ".join(c.strip() for c in r)} = {" + ".join(c.strip() for c in p)}'
    return reaction


def prepare_balanced(result_div: Union[element.Tag, element.NavigableString]) -> str:    
    answer = ''
    for child in result_div.childGenerator():
        if isinstance(child, element.Tag):
            if child.name == 'sub':
                answer += ''.join(SUBSCRIPTIONS.get(key) for key in child.string)
            elif child.name == 'sup':
                answer += ''.join(SUPERSCRIPTIONS.get(key) for key in child.string)
            elif child.name == 'span':
                for sub_child in child.childGenerator():
                    if isinstance(sub_child, element.NavigableString):
                        answer += sub_child.strip()
            elif child['class'] == 'dblarrow':
                answer += ' ⇆ '
        elif isinstance(child, element.Comment):
            pass
        elif isinstance(child, element.NavigableString):
            answer += child.string.strip()
    return answer.replace('\n', '')


def prepare_dict(input_as: str, interpreted_as: str, result: str, error_msg: str) -> dict:
    d = {
        'embed': {
            'title': result,
        },
        'fields': dict()
    }
    if error_msg:
        d['fields']['Status'] = ('Failed', False)
        d['fields']['Cause of Error'] = (error_msg, False)
        d['embed']['color'] = Colour.red()
    else:
        d['fields']['Status'] = ('Success', False)
        d['embed']['color'] = Colour.green()
    d['fields']["Input"] = (input_as, False)
    d['fields']["Interpreted as"] = (interpreted_as, False)
    return d


def prepare_embed(d: dict, footer: str) -> Embed:
    embed = Embed(**d.get('embed', ''))
    embed.set_footer(text=footer)

    for key in d.get('fields').keys():
        value, inline = d['fields'][key]
        embed.add_field(name=key, value=value, inline=inline)
    return embed
