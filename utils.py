import enum
from operator import sub
from typing import Tuple, Dict


from chempy.chemistry import Substance, Reaction, Equilibrium
# from chempy.chemistry import balance_stoichiometry


def replace_square_bracket(raw: str) -> str:
    formatted = raw.replace('[', '(')
    formatted = raw.replace(']', ')')
    return formatted


def remove_duplicate(
    reactants_str: str, 
    products_str: str
    ) -> Tuple[Tuple[Substance], Tuple[Substance]]:
        reactants = set(r.strip() for r in reactants_str.split(','))
        products = set(p.strip() for p in products_str.split(','))
        duplicate = reactants.intersection(products)
        if duplicate:
            for d in duplicate:
                reactants.remove(d)
                products.remove(d)
        return reactants, products


def format_reaction(reactants: Dict, products: Dict) -> str:
    keys = (*(r for r in reactants.keys()), *(p for p in products.keys()))
    substances = {k:Substance.from_formula(k) for k in keys}
    reaction = Reaction(reactants, products)
    return reaction.unicode(substances)


def simple_balance(reactants: str, products: str):    
    reactants, products = map(replace_square_bracket, (reactants, products))
    reactants, products = remove_duplicate(reactants, products)
    # return balance_stoichiometry(reactants, products)


substances={x: Substance.from_formula(x) for x in 'MnO4-, C2O4-2, Fe+2, H+, Mn+2, CO2, Fe+3, H2O'.split(',')}

print(substances)

print(Reaction.from_string('MnO4- + C2O4-2 + Fe+2 + H+ -> Mn+2 + CO2 + Fe+3 + H2O', substances))
# print(simple_balance("MnO4-, C2O4-2, Fe+2, H+" , "Mn+2, CO2, Fe+3, H2O"))

