from typing import Tuple, Dict, Set

# from chempy.chemistry import Substance, Reaction, balance_stoichiometry


def replace_square_bracket(raw: str) -> str:
    formatted = raw.replace('[', '(')
    formatted = raw.replace(']', ')')
    return formatted


def prepare_reaction(reactants_str: str, products_str: str) -> Tuple[Set[str], Set[str]]:
    reactants_str, products_str = map(replace_square_bracket, (reactants_str, products_str))
    
    reactants_set = set(s.strip() for s in reactants_str.split(','))
    products_set = set(s.strip() for s in products_str.split(','))

    duplicate = reactants_set.intersection(products_set)

    reactants_set.difference_update(duplicate)
    products_set.difference_update(duplicate)
    return reactants_set, products_set


def format_reaction(reactants_bal: Dict, products_bal: Dict) -> str:
    keys = (*(r for r in reactants_bal.keys()), *(p for p in products_bal.keys()))
    substances = {k:Substance.from_formula(k) for k in keys}
    reaction = Reaction(reactants_bal, products_bal)
    return reaction.unicode(substances)


def bal_stoich(reactants_set: Set, products_set: Set) -> Tuple[Dict, Dict]:
    reactants_bal, products_bal = balance_stoichiometry(reactants_set, products_set)
    reactants_bal, products_bal = map(dict, (reactants_bal, products_bal))
    return reactants_bal, products_bal


def simple_balance(reactants_str: str, products_str: str) -> Tuple[Dict, Dict]: 
    reactants_set, products_set = prepare_reaction(reactants_str, products_str)

    reactants_charge = sum(Substance.from_formula(s).charge for s in reactants_set)
    products_charge = sum(Substance.from_formula(s).charge for s in products_set)

    if reactants_charge > products_charge:
        reactants_set.add('e-')
    elif reactants_charge < products_charge:
        products_set.add('e-')

    return bal_stoich(reactants_set, products_set)

def simple_balance(reactants_str: str, products_str: str) -> Tuple[Dict, Dict]: 
    reactants_set, products_set = prepare_reaction(reactants_str, products_str)
    reduction = [[], []]
    oxidation = [[], []]
