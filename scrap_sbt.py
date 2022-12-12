import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from lmt.dprocess import scrapman
from lmt.vendor import sbt


if __name__ == '__main__':
    # Init file
    # dman.init('data/rinput/sbt-notlisted.csv', 'sbt', 'notlisted_revision')

    FILENAME = '202212070957-4319-sbt-notlisted_revision'

    # Clean file
    # dman.clean(filename=FILENAME)

    # Get remaining
    rem = dman.get_remaining(filename=FILENAME, column='Part #')

    # Initialize WebDriver
    driver = webdriver.Firefox(service=Service('webdriver/geckodriver'))

    # Get WebPage
    driver.get('https://www.shopsbt.com/BASK.html')

    # Login
    sbt.login(driver)

    # Scrap
    for i in tqdm(range(len(rem))):
        sbt.search(driver, rem[i], wait_time=2)
        m = sbt.find_match(driver, rem[i], wait_time=2)

        dman.process(filename=FILENAME, info=m, success=not pd.isna(m['part_number']))