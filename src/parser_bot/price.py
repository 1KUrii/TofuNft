import loguru
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tofunft_bot.src.parser_bot.data import URL
from tofunft_bot.src.parser_bot.data import DRIVER

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(
    executable_path=DRIVER,
    options=options)
driver.get(URL)
last_price = 0


async def get_last_price():
    return last_price


async def set_last_price(last):
    global last_price
    last_price = last


async def parsing_floor_price():
    global last_price

    try:
        page = driver.page_source  # raw html
        soup = BeautifulSoup(page, 'html.parser')  # parsing html to text
        lowest_price = soup.find_all('p', {'class': 'chakra-text css-0'})
        best_price = float(lowest_price[0].text.replace(' ', '').replace('BNB', ''))
        return best_price

    except ValueError as ex:
        loguru.logger.error(ex)

    finally:
        driver.refresh()
