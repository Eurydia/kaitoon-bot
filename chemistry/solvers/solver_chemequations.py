from typing import Tuple, Union
from json import loads

from discord import Embed, Colour
from bs4 import BeautifulSoup, element
from requests import get

from bot.bot import Kaitoon
from chemistry.solvers.solver_base_class import ChemistrySolverBaseClass

class ChemEquation(ChemistrySolverBaseClass):
    def __init__(self, bot: Kaitoon):
        self.bot = bot
    
    
class _ReactionPrediction(ChemEquation):
    def __init__(self, bot):
        super().__init__(bot)
    
    async def solve(self, reactants: str, products: str='', page_num: int=0) -> Embed:
        def p_string(string: str) -> str:
            string = string.replace(',', ' ').replace(' + ', ' ')
            return string
        p_reactants, p_products = map(p_string, (reactants, products))
        prep_r, prep_p = self._prepare_query(reactants, products)

        page_source = await self._prepare_page_source(prep_r, prep_p)
        result = self._format_page_source(page_source, page_num)
        embed = self._prepare_embed(
            result,
            f'"{reactants}" and "{products}"',
            f'\"{p_reactants.replace(" ", " + ")}\" --> \"{p_products.replace(" ", " + ")}\"'
        )
        return embed

    @staticmethod
    def _prepare_query(reactants: str, products: str) -> Tuple[str]:
        def _prepare(string: str, type: str) -> str:
            if not string:
                return (f'{type}1=', )
            string = '&'.join(f'{type}{i}={f}' for i, f in enumerate(string.split(' '), 1))
            return string
        prep_r = _prepare(reactants, 'reactant')
        prep_p = _prepare(products, 'product')
        return prep_r, prep_p

    @staticmethod
    def _prepare_result(json_dict: dict):
        formatted_equations = []
        for equation in json_dict.get('searchResults'):
            soup = BeautifulSoup(equation.get('equationStrBold', ''), 'html.parser')
            eq = ' '.join(f'__{s.text.strip()}__' if isinstance(s, element.Tag) else s.text.strip()
                            for s in soup.childGenerator()
                            )
            eq = eq.replace(':', '')
            formatted_equations.append(eq)
        return json_dict.get('resultCount', 0), json_dict.get('offset', 0), tuple(formatted_equations)

    @staticmethod
    async def _prepare_page_source(
        prep_r: Tuple, 
        prep_p: Tuple
        ) -> str:
            url = f'https://chemequations.com/en/advanced-search/?{prep_r}&{prep_p}&submit='
            r = get(url)
            return r.text

    def _format_page_source(self, page_source: str, page_num: int) -> Union[Tuple, None]:
        soup = BeautifulSoup(page_source, 'html.parser')
        div_table = soup.find('div', {'class': 'search-results-async'})
        if not div_table:
            return None
        div_attrs = div_table.attrs
        reactantids = div_attrs.get('data-reactantids')
        productids = div_attrs.get('data-productids')
        offset = page_num * 10
        api_url = f'https://chemequations.com/api/search-reactions-by-compound-ids?reactantIds={reactantids}&productIds={productids}&offset={offset}'
        r = get(api_url)
        json_dict = loads(r.text)
        results = self._prepare_result(json_dict)
        return results
    
    @staticmethod
    def _prepare_embed(result: Tuple[str, Tuple[str]], inputs: str, interpreted: str) -> Embed:
        embed = Embed(
            color=Colour.green()
        )
        if not result:
            embed.title = '😐 Something went wrong.'
            embed.color = Colour.red()
            embed.add_field(name='Status', value='❎ Failed', inline=False)
        else:
            result_total, offset, eqs = result
            embed.title = f'Found {result_total} equation(s)!'
            embed.description = f'Showing result {offset+1} - {((offset//1)+1)*10} of **{result_total}** equations\n'
            embed.description += '\n'.join(f'{i}. {eq}\n' for i, eq in enumerate(eqs, offset+1))
            embed.add_field(name='Status', value='✅ Success', inline=False)

        embed.add_field(name='Input', value=inputs, inline=False)
        embed.add_field(name='Interpreted as', value=interpreted, inline=False)
        embed.set_footer(text='Powered by www.chemequations.com')
        return embed
        
