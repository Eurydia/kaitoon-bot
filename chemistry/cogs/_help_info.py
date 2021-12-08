# -*- coding: utf-8 -*-
REACTANTS_INFO = """\
Specify the reactants of the reaction.
More than one reactants should be joined
with
• "+" (plus symbol), or
• "`🧊`" (space).\
"""

PRODUCTS_INFO = """\
Specify the products of the reaction.
Formatting is the same as [<reactants>].\
"""

COMMAND = {
    "help": {
        "aliases": [],
        "syntax": "help🧊[<command name>]",
        "description": """\
Provides more infomation for commands.\
""",
        "arguments": {
            "[<command name>]": """\
Specify the name of the command you want to learn more about.\
"""
        },
        "examples": ["#help balance", "]]help help"],
        "notion_link": "https://www.notion.so/help-e72cde2a635b46e6bac6d4406741b328",
    },
    "on": {
        "aliases": [],
        "syntax": "on🧊[<chemical compound>]",
        "description": """\
Assigns an oxidation number to each element compound(s).\
""",
        "arguments": {
            "[<chemical compound>]": """\
Specify the chemical compound to
assign oxidation number to.
More than one [<chemical compound>]
should be joined together with spaces.\
"""
        },
        "examples": ["#on C2H4", "]]on H2O MnO4- CH4"],
        "notion_link": "https://www.notion.so/on-23b2cc49a06f4def8f80594c6c945466",
    },
    "balance": {
        "aliases": ["bal"],
        "syntax": 'balance🧊"[<reactants>]"🧊"[<products>]"',
        "description": """\
Solves the stoichometry of non-redox reactions.\
""",
        "arguments": {"[<reactants>]": REACTANTS_INFO, "[<products>]": PRODUCTS_INFO},
        "examples": ['#balance "H2O" "H + O"', ']]balance "CH4 + O2" "H2O + CO2"'],
        "notion_link": "https://www.notion.so/balance-acb161411da1467ab1531de2cfd4b0a2",
    },
    "redox": {
        "aliases": ["re"],
        "syntax": 'redox🧊"[<reactants>]"🧊"[<products>]"🧊"[<median>]"',
        "description": """\
Solves the stoichometry of redox reactions.\
""",
        "arguments": {
            "[<reactants>]": REACTANTS_INFO,
            "[<products>]": PRODUCTS_INFO,
            "[<median>]": """\
Specify the condition of the reaction.
Valid symbols for [<median>] are
• "a" or "acidic" for acidic environment,
and
• "b" or "basic" for basic environment.
When not given any value, [<median>]
defaults to acidic condition.\
""",
        },
        "examples": [
            '#redox "H2O2" "H2O + O2"',
            ']]redox "ClO3- + N2H4" "NO + Cl-" "basic"',
        ],
        "notion_link": "https://www.notion.so/redox-cd40dff1f9eb4daaba5ab1cc2baca348",
    },
    "predict": {
        "aliases": ["pred"],
        "syntax": 'predict🧊"[<reactants>]"🧊"[<products>]"🧊"[<page>]"',
        "description": """\
Search and display all equations that contains reactants and products given.\
""",
        "arguments": {
            "[<reactants>]": f"""\
{REACTANTS_INFO}
Use "[u]" when you want to mark the
reactants as "unspecified".
("unspecified" reactants will match any
reactants)\
""",
            "[<products>]": PRODUCTS_INFO,
            "[<page>]": """\
Specify the number of page result to
display.
[<page>] takes an integer greater than zero.
When not given any value, [<page>] defaults
to 1.\
""",
        },
        "examples": [
            'predict "O2" "CO2 + H2O"',
            'predict "O2" "[u]" "2"',
            'predict "[u]" "CO2 + H2O" "3"',
        ],
        "notion_link": "https://www.notion.so/predict-2616ea33712646e3ab2a741c47b8d09c",
    },
}
