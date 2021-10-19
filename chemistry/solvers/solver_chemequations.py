from typing import Tuple, Union
from json import loads
from concurrent.futures import as_completed
from timeit import default_timer

from discord import Embed, Colour
from bs4 import BeautifulSoup, element
from requests_futures.sessions import FuturesSession

from chemistry.solvers.solver_base_class import ChemistrySolverBaseClass

class ChemEquation(ChemistrySolverBaseClass):
    pass
    

class _ReactionPrediction(ChemEquation):
    def solve(self, reactants: str='', products: str='', page_num: int=1) -> Embed:
        if reactants is None and products is None:
            raise ValueError("Both reactants and products are empty.")
        if page_num < 1:
            raise IndexError(f'Page {page_num} is out of range.')
        timer_start = default_timer()
        reactants = reactants.replace(",", " ").replace(" ", " + ")
        products = products.replace(",", " ").replace(" ", " + ")
        page_num -= 1
        query = self._prepare_query(reactants, products)
        page_source = self._prepare_page_source(
            'https://chemequations.com/en/advanced-search/?',
            f'{query}&submit='
            )
        result = self._format_page_source(page_source, page_num)
        timer_end = default_timer()
        return self._prepare_embed(
            result,
            (reactants, products),
            f'\"{reactants}\" --> \"{products}\"',
            timer_end - timer_start
        )

    @staticmethod
    def _prepare_query(reactants: str, products: str) -> str:
        def _prepare(string: str, type: str) -> str:
            if not string:
                return (f'{type}1=', )
            string = string.replace(',', ' ').replace(' + ', ' ')
            string = '&'.join(f'{type}{i}={f}' for i, f in enumerate(string.split(), 1))
            return string
        r = _prepare(reactants, 'reactant')
        p = _prepare(products, 'product')
        return f'{r}&{p}'

    @staticmethod
    def _prepare_page_source(base_url: str, query: str) -> str:
            session = FuturesSession()
            rqs = (session.get(f'{base_url}{query}'))
            content = ''
            for req in as_completed(rqs):
                resp = req.result()
                content = resp.content.decode('utf-8')
            return content

    def _format_page_source(self, page_source: str, page_num: int) -> Union[Tuple, None]:
        soup = BeautifulSoup(page_source, 'html.parser')
        div_table = soup.find('div', {'class': 'search-results-async'})
        if not div_table:
            return None
        div_attrs = div_table.attrs
        reactantids = div_attrs.get('data-reactantids')
        productids = div_attrs.get('data-productids')
        offset = page_num * 10
        r = self._prepare_page_source(
            'https://chemequations.com/api/search-reactions-by-compound-ids?',
            f'reactantIds={reactantids}&productIds={productids}&offset={offset}'
        )
        json_dict = loads(r)
        results = self._prepare_result(json_dict)
        return results

    @staticmethod
    def _prepare_result(json_dict: dict) -> Tuple[str, str, str]:
        formatted_equations = []
        for equation in json_dict.get('searchResults'):
            soup = BeautifulSoup(equation.get('equationStrBold', ''), 'html.parser')
            eq = ' '.join(f'__{s.text.strip()}__' 
                        if isinstance(s, element.Tag) else s.text.strip()
                        for s in soup.childGenerator()
                        )
            eq = eq.replace(':', '')
            formatted_equations.append(eq)
        return json_dict.get('resultCount', 0), json_dict.get('offset', 0), tuple(formatted_equations)
        
    @staticmethod
    def _prepare_embed(
        result: Tuple[str, Tuple[str]], 
        inputs: Tuple[str], 
        interpreted_as: str, 
        time_elasped: float
    ) -> Embed:
        embed = Embed()
        if not result:
            embed.title = '😐 Something went wrong.'
            embed.color = Colour.red()
            embed.add_field(name='Status', value='❎ Failed', inline=False)
        else:
            result_total, offset, eqs = result
            embed.title = f'Found {result_total} equation(s)!'
            embed.color = Colour.green()
            embed.description = f'Showing result {offset+1} - {((offset//10)+1)*10} of **{result_total}** equations\n'
            embed.description += '\n'.join(f'{i}. {eq}\n' for i, eq in enumerate(eqs, offset+1))
            embed.add_field(name='Status', value='✅ Success', inline=False)
        embed.add_field(
            name='Inputs',
            value=' and '.join(f'" **{i}** "' for i in inputs),
            inline=False
            )
        embed.add_field(
            name='Interpreted as',
            value=interpreted_as,
            inline=False
            )
        embed.add_field(
            name='Finished in',
            value=f'{time_elasped:.2f}s',
            inline=False
            )
        embed.set_footer(text='Powered by www.chemequations.com')
        return embed
        
