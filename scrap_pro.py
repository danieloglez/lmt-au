import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from lmt.dprocess import scrapman
from lmt.vendor import promarine

if __name__ == '__main__':
    # Init file
    # dman.init('data/rinput/pro-notlisted.csv', 'don', 'promarine_replaces_revision')

    FILENAME = '202211181503-4602-don-promarine_replaces_revision'

    # Clean file
    # dman.clean(filename=FILENAME)

    # Get remaining
    rem = dman.get_remaining(filename=FILENAME, column='Item #')

    # Initialize WebDriver
    driver = webdriver.Firefox(service=Service('webdriver/geckodriver'))

    # Get WebPage
    driver.get('https://parts.promarineusa.com')

    # Login
    promarine.login(driver)

    # Scrap
    for r in rem:
        promarine.search(driver, r)
        m = promarine.find_match(driver, r)

        dman.process(filename=FILENAME, info=m, success=not pd.isna(m['id']))
