from typing import Union, List, Tuple
from timeit import default_timer
from concurrent.futures import as_completed

from bs4 import BeautifulSoup, element
from discord import Embed, Colour
from discord.ext.commands import Bot
from requests_futures.sessions import FuturesSession

from chemistry.solvers.solver_base_class import ChemistrySolverBaseClass
from chemistry.solvers.utils import SUPERSCRIPTIONS, SUBSCRIPTIONS, SPECIAL_TO_NORMAL

class Periodni(ChemistrySolverBaseClass):
    @staticmethod
    def _prepare_query(queries: Tuple[str]) -> str:
        res = []
        for query in queries:
            query = query.replace(',', ' ').replace(' + ', ' ')
            query_r, query_p = query.split('=')
            query_r = '%2B'.join(r.strip() for r in query_r.split())
            query_p = '%2B'.join(p.strip() for p in query_p.split())
            res.append(f'{query_r}%3D{query_p}')
        return tuple(res)
    
    @staticmethod
    def _prepare_page_source(
        base_url: str,
        queries: Tuple[str]
    ) -> Tuple[str]:
        session = FuturesSession()
        lookup = {}
        reqs = []
        for query in queries:
            req = session.get(f'{base_url}{query}')
            lookup[req] = None
            reqs.append(req)
        for req in as_completed(reqs):
            resp = req.result()
            content = resp.content.decode('utf-8')
            lookup[req] = content
        return tuple(lookup.values())
    
    @staticmethod
    def _prepare_result_unicode(result_element: element.Tag):
        res = ''
        for child in result_element.childGenerator():
            if isinstance(child, element.Comment):
                continue
            if isinstance(child, element.NavigableString):
                res += child.text
            elif child.name == 'sub':
                res += ''.join(SUBSCRIPTIONS.get(key, key) for key in child.text)
            elif child.name == 'sup':
                res += ''.join(SUPERSCRIPTIONS.get(key, key) for key in child.text)
            elif child.name == 'span':
                res += ' → '
        res = res.split(' + ')
        res = ' + '.join(x.strip() for x in res)
        res = res.split('→')
        res = ' ⇆ '.join(x.strip() for x in res)
        return res.replace('\n', ' ')

    @staticmethod
    def _prepare_result(result_unicode: str) -> str:
        return ''.join(SPECIAL_TO_NORMAL.get(key, key) for key in result_unicode)
    
    @staticmethod
    def _embed_info(
        embed: Embed,
        succeed_percentage: float,
        inputs: Tuple[str],
        interpreted_as: Tuple[str], 
        time_elasped: float
    ) -> Embed:
        if succeed_percentage < 50:
            embed.color = Colour.red()
            embed.add_field(name='Status', value=f'❎ Failed ({succeed_percentage}%)', inline=False)
        else:
            embed.color = Colour.green()
            embed.add_field(name='Status', value=f'✅ Success ({succeed_percentage}%)', inline=False)
        embed.add_field(
            name='Inputs',
            value=' and '.join(f'" **{i}** "' for i in inputs),
            inline=False
            )
        embed.add_field(
            name='Interpreted as',
            value=' and '.join(f'" **{i}** "' for i in interpreted_as),
            inline=False
            )
        embed.add_field(
            name='Finished in',
            value=f'{time_elasped:.2f}s',
            inline=False
            )
        embed.set_footer(text='Powered by www.periodni.com')
        return embed


class _OxidationNumberAssignment(Periodni):
    def solve(self, compound: str, *args) -> List[Embed]:
        timer_start = default_timer()
        compounds = (compound, *args)
        c_urls = self._prepare_query(compounds)
        interpreted = []
        unicode = []
        result = []
        page_sources = self._prepare_page_source(
            'https://www.periodni.com/oxidation_numbers_calculator.php?eq=',
            c_urls
            )
        for page_source in page_sources:
            interp, uni, res = self._format_page_source(page_source)
            interpreted.append(interp)
            unicode.append(uni)
            result.append(res)
        timer_end = default_timer()
        return self._prepare_embed(
            compounds, 
            tuple(interpreted),
            tuple(unicode),
            tuple(result),
            timer_end-timer_start
            )
    
    @staticmethod
    def _prepare_query(compounds: Tuple[str]) -> Tuple[str]:
        res = []
        for compound in compounds:
            compound = compound.strip()
            compound = compound.replace('+', '%2B')
            compound = compound.replace('^', '%5E')
            compound = compound.replace('-', '%2D')
            res.append(compound)
        return tuple(res)

    def _format_page_source(
        self,
        page_source: str
    ) -> Tuple[str, Union[str, None], Union[str, None]]: 
        soup = BeautifulSoup(page_source, 'html.parser')

        interpreted_as = soup.find('input', {'name': 'equation', 'class': 'txt-c'}).get('value')
        
        result_element = soup.find('div', {'class': 'onresult'})
        error_blocks = soup.findAll(attrs={'class': 'crven'})
        if not result_element or error_blocks:
            return interpreted_as, None, None
        return (
            interpreted_as,
            self._prepare_result_unicode(result_element), 
            self._prepare_result(result_element)
            )
    
    @staticmethod
    def _prepare_result_unicode(result_div: element.Tag) -> str:
        res = ''
        for child in result_div.childGenerator():
            if child.name == 'span':
                res += child.get_text(' ', strip=True).split()[0]
            elif child.name == 'sup':
                res += ''.join(SUPERSCRIPTIONS.get(key, key) for key in child.text)
            elif child.name == 'sub':
                res += ''.join(SUBSCRIPTIONS.get(key, key) for key in child.text)
            else:
                res += child.text
        return res

    @staticmethod
    def _prepare_result(result_element: element.Tag) -> Tuple[str]:
        res = []
        for child in result_element.childGenerator():
            if (isinstance(child, element.Tag) and
                child.name == 'span' and
                child.find('span', {'class': 'oxbr'})
            ):
                result = child.text
                symbol_index = result.find('+') if '+' in result else result.find('-')
                result = result.replace('+', f' {">"*(3-symbol_index)} +')
                result = result.replace('-', f' {">"*(3-symbol_index)} -')
                res.append(result)
        return tuple(res)
    
    def _prepare_embed(
        self,
        compounds: Tuple[str],
        interpreted_as: Tuple[str],
        result_unicodes: Tuple[str],
        results: Tuple[str],
        time_elapsed: float
    ) -> Embed:
        total_coumpound = len(compounds)
        succeed = sum(1 for res in results if res is not None)
        embed = Embed(title=f'Assigned {succeed} of {total_coumpound} Compound(s).')
        for compound, uni, res in zip(compounds, result_unicodes, results):
            if res:
                res = '\n'.join(res)
                f_value = f'Unicode: ||```{uni}```||```{res}```'
            else:
                f_value = '😐 Something went wrong.'
            embed.add_field(
                name=compound,
                value=f_value
                )
        succeed_percentage = round(succeed / total_coumpound, 2) * 100
        return self._embed_info(
            embed,
            succeed_percentage,
            compounds,
            interpreted_as,
            time_elapsed
            )

        
class _SimpleBalance(Periodni):
    def solve(self, reactions: Tuple[str]) -> Embed:
        time_start = default_timer()
        r_urls = self._prepare_query(reactions)
        page_sources = self._prepare_page_source(
            'https://www.periodni.com/balancing_chemical_equations.php?eq=',
            r_urls
            )
        interpreted = []
        unicodes = []
        results = []
        for page_source in page_sources:
            interp, unicode, result = self._format_page_source(page_source)
            interpreted.append(interp)
            unicodes.append(unicode)
            results.append(result)

        time_end = default_timer()
        return self._prepare_embed(
            reactions,
            tuple(interpreted), 
            tuple(unicodes),
            tuple(results),
            time_end-time_start
        )

    def _format_page_source(self, page_source: str) -> Tuple[str, Union[str, None], Union[str, None]]:
        soup = BeautifulSoup(page_source, 'html.parser')
        
        interpreted_as = soup.find('input', {'name': 'equation', 'class': 'txt-c'}).get('value')

        result_div = soup.find('div', {'class': 'eqbody'})
        error_blocks = soup.findAll(attrs={'class': 'crven'})
        if not result_div or error_blocks: 
            return interpreted_as, None, None
        unicode = self._prepare_result_unicode(result_div)
        normal = self._prepare_result(unicode)
        return interpreted_as, unicode, normal

    def _prepare_embed(
        self,
        reactions: Tuple[str],
        interpreted_as: Tuple[str],
        result_unicodes: Tuple[str],
        results: Tuple[str], 
        time_elasped: float
    ) -> Embed:
        total_coumpound = len(results)
        succeed = sum(1 for res in results if res)
        embed = Embed(title=f'Balanced {succeed} of {total_coumpound} Reaction(s).')
        for reaction, uni, res in zip(reactions, result_unicodes, results):
            reaction = reaction.replace("=", "=")
            reaction = f'Original: ```{reaction}```'
            if res:
                f_name = res
                f_value = f'Unicode: ||```{uni}```||\n{reaction}'
            else:
                f_name = '😐 Something went wrong.'
                f_value = reaction
            embed.add_field(
                name=f_name,
                value=f_value,
                inline=False
                )
        succeed_percentage = round(succeed / total_coumpound, 2) * 100
        return self._embed_info(
            embed,
            succeed_percentage,
            reactions,
            interpreted_as,
            time_elasped
        )


class _RedoxBalance(Periodni):
    def solve(self, reactions_with_median: Tuple[str, str]) -> Embed:
        if any(median.lower() not in {'a', 'acidic', 'b', 'basic'} 
        for median, _ in reactions_with_median):
            raise ValueError('Medium must be "A, Acidic, B, or Basic" only.')
        timer_start = default_timer()
        
        medians = []
        reactions = []
        for m, r in reactions_with_median:
            m = 'acidic' if m.startswith('a') else 'basic'
            medians.append(m)
            reactions.append(r)
        medians, reactions = map(tuple, (medians, reactions))

        r_urls = self._prepare_query(reactions)
        queries = tuple(f'{r_url}&medium={m}' for m, r_url in zip(medians, r_urls))
        page_sources = self._prepare_page_source(
            'https://www.periodni.com/ars_method.php?eq=',
            queries
            )
        interpreted = []
        unicodes = []
        results = []
        for page_source in page_sources:
            interp, unicode, result = self._format_page_source(page_source)
            interpreted.append(interp)
            unicodes.append(unicode)
            results.append(result)
            
        timer_end = default_timer()
        return self._prepare_embed(
            reactions_with_median,
            tuple(zip(medians, interpreted)),
            tuple(unicodes),
            tuple(results),
            timer_end - timer_start
        )

    def _format_page_source(self, page_source: str) -> Tuple[str, Union[str, None], Union[str, None]]:
        soup = BeautifulSoup(page_source, 'html.parser')

        interpreted_as = soup.find('input', {'name': 'equation', 'class': 'txt-c'}).get('value')

        result_div = soup.find('div', {'class': 'eq-final'})
        error_blocks = soup.findAll(attrs={'class': 'crven'})
        if (
            not result_div or 
            sum(1 for e in error_blocks if e.name != 'span')
        ):
            return interpreted_as, None, None
        unicode = self._prepare_result_unicode(result_div)
        normal = self._prepare_result(unicode)
        return interpreted_as, unicode, normal

    def _prepare_embed(
        self,
        reactions_with_median: Tuple[str],
        interpreted_as: Tuple[str],
        result_unicodes: Tuple[str],
        results: Tuple[str], 
        time_elasped: float
    ) -> Embed:
        total_coumpound = len(results)
        succeed = sum(1 for res in results if res)
        embed = Embed(title=f'Balanced {succeed} of {total_coumpound} Redox Reaction(s).')
        for reaction, uni, res in zip(reactions_with_median, result_unicodes, results):
            m, r = reaction
            r = r.replace('=', ' = ')
            r = f'Original: ```{r}```'
            if res:
                f_name = f'({m}) {res}'
                f_value = f'Unicode: ||```{uni}```||\n{r}'
            else:
                f_name = '😐 Something went wrong.'
                f_value = r
            embed.add_field(
                name=f_name,
                value=f_value,
                inline=False
                )
        succeed_percentage = round(succeed / total_coumpound, 2) * 100
        return self._embed_info(
            embed,
            succeed_percentage,
            tuple(f'{m} {r}' for m, r in reactions_with_median),
            tuple(f'({m}) {r}' for m, r in interpreted_as),
            time_elasped
        )
