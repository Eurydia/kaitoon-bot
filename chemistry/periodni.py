from asyncio import sleep
from typing import Union, List, Tuple

from bs4 import BeautifulSoup, element
from discord import Embed, Colour
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver

from .chemistry_command_bc import ChemistryCommandsBaseClass
from .utils import SUPERSCRIPTIONS, SUBSCRIPTIONS

class Periodni(ChemistryCommandsBaseClass):
    def __init__(self, bot: 'Kaitoon'):
        self.bot = bot
    
    @staticmethod
    def _prepare_ub(reatants: str, products: str) -> str:
        reatants, products = map(lambda s: s.replace(',', ' ').replace(' + ', ' '), (reatants, products))
        reatants, products = map(lambda s: s.split(), (reatants, products))
        reatants = ' + '.join(c.strip() for c in reatants)
        products = ' + '.join(c.strip() for c in products)
        reaction: str = f'{reatants} = {products}'
        return reaction
    
    @staticmethod
    def _prepare_b(result_div: element.Tag) -> str:
        answer = ['', '']
        i = 0
        for child in result_div.childGenerator():
            if isinstance(child, element.Comment):
                continue
            if isinstance(child, element.Tag):
                if 'dblarrow' in child.get('class'):
                    i = 1
                elif child.name == 'sup':
                    answer[i] += ''.join(SUPERSCRIPTIONS.get(key) for key in child.string)
                elif child.name == 'sub':
                    answer[i] += ''.join(SUBSCRIPTIONS.get(key) for key in child.string)
            else:		
                answer[i] += child.string
        answer = map(lambda x: x.replace('\n', ''), answer)
        answer = map(lambda x: x.replace('\t', ''), answer)
        r, p = map(lambda x: x.split('+'), answer)
        r = ' + '.join(c.strip() for c in r)
        p = ' + '.join(c.strip() for c in p)
        return f'{r} ⇆ {p}'

    @staticmethod
    def _prepare_embed(result: str, inputs: str, interpreted: str) -> Embed:
        embed = Embed(
            title=result,
            color=Colour.green()
        )
        if not result:
            embed.title = '😐Something went wrong.'
            embed.color = Colour.red()
            embed.add_field(name='Status', value='❎Failed', inline=False)
        else:
            embed.add_field(name='Status', value='✅Success', inline=False)
        embed.add_field(name='Input', value=inputs, inline=False)
        embed.add_field(name='Interpreted as', value=interpreted, inline=False)
        embed.set_footer(text='Powered by www.periodni.com')
        return embed


class _OxidationNumberAssignment(Periodni):
    def __init__(self, bot):
        super().__init__(bot)
    
    async def solve(self, formula: str, *args) -> List[Embed]:
        stack = (formula, *args)
        
        driver = self.bot.get_driver()
        driver.get('https://www.periodni.com/oxidation_numbers_calculator.php')
        results_data = []
        for formula in stack:
            page_source = self._prepare_page_source(driver, formula)
            result = self._format_page_source(page_source)
            results_data.append((formula, result))
        driver.quit()

        result_embeds = []
        for key, val in results_data:
            title = ''
            if val:
                title = ', '.join(f'{x}: {y}' for x, y in val)
            embed = self._prepare_embed(title, key, key)
            result_embeds.append(embed)
        return result_embeds

    @staticmethod
    async def _prepare_page_source(driver:WebDriver, formula: str) -> str:
        form: WebElement = driver.find_element_by_id('phpforma')

        text_input: WebElement = form.find_element_by_name('equation')
        text_input.send_keys(formula)

        submit: WebElement = form.find_element_by_name('submit')
        submit.click()
        await sleep(0.5)

        page_source = driver.page_source
        return page_source
    
    def _format_page_source(self, page_source: str) -> Union[Tuple[str, str], None]:
        soup = BeautifulSoup(page_source, 'html.parser')
        result_div = soup.find('table', {'class': 'ontable'})
        if not result_div:
            return None
        result = self._prepare_b(result_div)
        return result
    
    @staticmethod
    def _prepare_b(result_div: element.Tag) -> Tuple[str, str]:
        body = result_div.find('tbody')
        rows= body.findAll('tr')
        result_arr = []
        i = -1
        for key, val in zip(*(row.childGenerator() for row in rows)):
            if key.name != 'td' or val.name != 'td':
                continue
            i += 1
            result_arr.append((key.string, val.string))
        result_arr.pop(0)
        return tuple(result_arr)

        
class _SimpleBalance(Periodni):
    def __init__(self, bot):
        super().__init__(bot)
    
    async def solve(self, reactants: str, products: str) -> Embed:
        reaction_ub = self._prepare_ub(reactants, products)
    
        driver = self.bot.get_driver()
        driver.get('https://www.periodni.com/balancing_chemical_equations.php')
        page_source = await self._prepapre_page_source(driver, reaction_ub)
        driver.quit()

        reaction_b = self._format_page_source(page_source)
        embed = self._prepare_embed(
            reaction_b,
            f'{reactants} and {products}',
            reaction_ub
        )
        return embed

    @staticmethod
    async def _prepare_page_source(driver: WebDriver, reaction_ub: str) -> str:
        form: WebElement = driver.find_element_by_id("phpforma")
        
        text_input: WebElement = form.find_element_by_name('equation')
        text_input.send_keys(reaction_ub)

        submit: WebElement = form.find_element_by_id("submit")
        submit.click()
        await sleep(0.75)

        page_source = driver.page_source
        return page_source

    def _format_page_source(self, page_source: str) -> Union[str, None]:
        soup = BeautifulSoup(page_source, 'html.parser')
        result_div = soup.find('div', {'class': 'eqbody eqcenter'})
        if not result_div: 
            return None
        reaction_b = self._prepare_balanced(result_div)
        return reaction_b
    

class _RedoxBalance(Periodni):
    def __init__(self, bot): 
        super().__init__(bot)
    
    async def solve(self, median: str, reactants: str, products: str) -> Embed:
        if not any(median.lower() == m for m in ('a', 'acidic', 'b', 'basic')):
            raise ValueError('Medium must be "(A)cidic" or "(B)asic" only.')
        
        reaction_ub = self._prepare_ub(reactants, products)

        driver = self.bot.get_driver()
        driver.get('https://www.periodni.com/ars_method.php')
        page_source = await self._prepare_page_source(driver, reaction_ub, median)
        driver.quit()

        result = self._format_page_source(page_source)
        embed = self._prepare_embed(
            result,
            f'{median} and {reactants} and {products}',
            reaction_ub
        )
        return embed
    
    @staticmethod
    async def _prepare_page_source(driver: WebDriver, reaction_ub: str, median: str) -> str:
        form: WebElement = driver.find_element_by_id("phpforma")
        
        text_input: WebElement = form.find_element_by_name('equation')
        text_input.send_keys(reaction_ub)

        if median.lower().startswith('b'):
            basic_median_radio: WebElement = form.find_element_by_id("intBasic")
            basic_median_radio.click()

        submit: WebElement = form.find_element_by_id("submit")
        submit.click()
        await sleep(0.75)
        form: WebElement = driver.find_element_by_id("phpforma")
        submit: WebElement = form.find_element_by_id("submit")
        submit.click()
        await sleep(0.75)
        
        page_source = driver.page_source
        return page_source

    def _format_page_source(self, page_source: str) -> Union[str, None]:
        soup = BeautifulSoup(page_source, 'html.parser')
        result_div = soup.find('div', {'class': 'eq-final'})
        if not result_div:
            return None
        reaction_b = self._prepare_b(result_div)
        return reaction_b
        
