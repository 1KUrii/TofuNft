import loguru
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tofunft_bot.src.parser_bot.data import URL
from tofunft_bot.src.parser_bot.data import DRIVER

# Initialize Chrome webdriver with options to disable GPU and automation features
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
webdriver = webdriver.Chrome(executable_path=DRIVER, options=chrome_options)

# Load the webpage in the webdriver
webdriver.get(URL)

# Initialize variables
current_price = 0
lowest_price_found = float('inf')


async def get_current_price():
    """Return the current price as a float."""
    return current_price


async def set_current_price(new_price):
    """Set the current price to the given value."""
    global current_price
    current_price = new_price


async def parse_lowest_price():
    """
    Parse the lowest price from the webpage.
    Return the lowest price as a float, or 'inf' if no price was found.
    """
    global lowest_price_found

    try:
        webdriver.refresh()

        # Get the raw HTML of the webpage
        page_html = webdriver.page_source

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(page_html, 'html.parser')

        # Find the element containing the lowest price
        lowest_price_element = soup.find('p', {'class': 'chakra-text css-0'})

        # Extract the numerical value from the element's text
        if lowest_price_element:
            lowest_price = float(lowest_price_element.text.replace(' ', '').replace('BNB', ''))
        else:
            lowest_price = float('inf')

        # Update the lowest price found so far
        lowest_price_found = min(lowest_price, lowest_price_found)

        return lowest_price

    except Exception as ex:
        # Log any errors that occur
        loguru.logger.error(ex)
        return float('inf')
