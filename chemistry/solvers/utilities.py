# -*- coding: utf-8 -*-
from typing import Dict

SUPERSCRIPTIONS = {key: val for key, val in zip("0123456789-+", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺")}
SUBSCRIPTIONS = {key: val for key, val in zip("0123456789", "₀₁₂₃₄₅₆₇₈₉")}

SPECIAL_TO_NORMAL = {
    key: val for key, val in zip("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "01234567890123456789-+")
}


def _text_translate(text: str, lookup: Dict[str, str]) -> str:
    return "".join(lookup.get(key, key) for key in text)
