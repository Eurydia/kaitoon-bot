from asyncio import sleep

from discord import Embed
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from chemistry.utils import  prepare_unbalanced, prepare_balanced, prepare_dict, prepare_embed

async def _simple_page_source(driver: WebDriver, reaction_ub: str) -> str:
    driver.get('https://www.periodni.com/balancing_chemical_equations.php')
        
    form: WebElement = driver.find_element_by_id("phpforma")
    
    text_input: WebElement = form.find_element_by_name('equation')
    text_input.send_keys(reaction_ub)

    submit: WebElement = form.find_element_by_id("submit")
    submit.click()
    await sleep(0.75)
    return driver.page_source


async def _simple_balance(bot, reactants: str, products: str) -> Embed:
        reaction_ub = prepare_unbalanced(reactants, products)
        
        driver: WebDriver = bot.get_driver()
        page_source = await _simple_page_source(driver, reaction_ub)
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')

        result_div = soup.find('div', {'class': 'eqbody eqcenter'})
        reaction_b = prepare_balanced(result_div)
        
        error_p = soup.find('p', {'class': 'crven'})
        error_msg = None if not error_p else error_p.text
        
        d = prepare_dict(
            f'{reactants} and {products}',
            f'{reaction_ub}',
            f'{reaction_b}',
            error_msg
        )
        result = prepare_embed(
            d,
            footer='Powered by www.periodni.com',
        )
        return result


async def _redox_page_source(driver: WebDriver, reaction_ub: str, median: str) -> str:
    driver.get('https://www.periodni.com/ars_method.php')
    
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
    return driver.page_source

async def _redox_balance(bot, median: str, reactants: str, products: str) -> Embed:
    if not any(median.lower() == m for m in ('a', 'acidic', 'b', 'basic')):
        raise ValueError('Medium must be "(A)cidic" or "(B)asic" only.')

    reaction_ub = prepare_unbalanced(reactants, products)

    driver: WebDriver = bot.get_driver()
    page_source = await _redox_page_source(driver, reaction_ub, median)
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    result_div = soup.find('div', {'class': 'eq-final'})           
    error_div = soup.find('div', {'class': 'eq-c'})
    
    if median.lower().startswith('a'):
        median_t = 'acidic median'
    else:
        median_t = 'basic median'

    if result_div:
        reaction_b = prepare_balanced(result_div)
        error_msg = ''
    elif error_div:
        reaction_b = prepare_balanced(error_div)
        error_msg = 'Unknown formula or error in equation!'
    else:
        reaction_b = prepare_balanced(soup.find('div', {'class': 'eqbody eqcenter'}))
        error_msg = 'It was not possible to calculate the stoichiometric coefficients of the equation with the mathematical method.'
    
    d = prepare_dict(
        f'{median} and {reactants} and {products}',
        f'({median_t}) {reaction_ub}',
        f'{reaction_b} ({median_t.title()})',
        error_msg
    )
         
    result = prepare_embed(
        d,
        footer='Powered by www.periodni.com',
    )
    return result
