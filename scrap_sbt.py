import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from lmt.dprocess import scrapman
from lmt.vendor import sbt

if __name__ == '__main__':
    # Init file
    # scrapman.init('data/scrap/rinput/20230109-sbtpricelist_unmatched.csv', 'sbt', 'sbtnotlisted')

    FILENAME = '202301101331-9298-sbt-sbtnotlisted'
    COLUMN = 'sbt_partnumber'
    ADDITIONAL = ['sbt_title', 'sbt_dealercost']

    # Clean file
    # dman.clean(filename=FILENAME)

    # Get remaining
    rem = scrapman.get_remaining(filename=FILENAME)

    # Initialize WebDriver
    # driver = webdriver.Firefox(service=Service('webdriver/geckodriver'))
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    # Get WebPage
    driver.get('https://www.shopsbt.com/BASK.html')

    # Login
    sbt.login(driver)

    # Scrap
    for i in tqdm(range(len(rem))):
        print(rem)
        sbt.search(driver, rem.iloc[i][COLUMN], wait_time=2)
        m = sbt.find_match(driver, rem.iloc[i][COLUMN], wait_time=2)

        scrapman.process(filename=FILENAME, info=m, additional=rem.iloc[[i]][ADDITIONAL].to_dict(),
                         success=not pd.isna(m['part_number']))
