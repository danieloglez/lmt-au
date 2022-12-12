import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FIELD_MAP = {'Weight:': 'weight', 'Cross Ref #:': 'cr_number', 'Mfg Part #:': 'mfg'}


def search(driver: webdriver, value: str):
    # Find SearchBox Component
    search_box = driver.find_element(By.NAME, value='AQSRKEY')

    # Insert Value In SearchBox
    search_box.send_keys(value)
    search_box.send_keys(Keys.ENTER)


def find_match(driver: webdriver, value: str, wait_time=5, exact_match=True):
    # Initialize Match Variable
    match = {
        'init_id': value,
        'id': np.nan,
        'description': np.nan,
        'has_stock': np.nan,
        'cost': np.nan,
        'weight': np.nan,
        'cr_number': np.nan,
        'mfg': np.nan
    }

    # Give Time For Full Load
    time.sleep(wait_time)

    # Store Found Values
    found_values = driver.find_elements(By.XPATH,
                                        value='/html/body/form/div[2]/div/div[4]/div[2]/div/div/div/div/div/div/table/tbody/tr/td/table[3]/tbody/tr')[
                   1:]

    # Search For Match
    for fv in found_values:
        # Find All Data Cells
        tds = fv.find_elements(By.CSS_SELECTOR, value='td.rowCellData, td.rowCellDataR')

        # Extract ID
        td_id = tds[2].get_attribute('innerText')

        # Continue To Next Item If Current Does Not Match
        if exact_match:
            if value != td_id:
                continue
        elif not exact_match:
            if value not in td_id:
                continue

        # If Matches Extract The Rest Of Data
        match['id'] = td_id
        match['description'] = tds[3].find_element(By.CSS_SELECTOR, value='a').get_attribute('innerText')
        match['has_stock'] = tds[5].get_attribute('innerText') == 'In Stock'
        match['cost'] = float(
            tds[6].find_element(By.CSS_SELECTOR, value='.dropPrice').get_attribute('innerHTML').replace('$', ''))

        # Go detailed information
        di = tds[3].find_element(By.CSS_SELECTOR, value='a')
        di.click()

        # Give time for full load
        time.sleep(wait_time)

        # Extract detailed information
        tbs = driver.find_elements(By.XPATH,
                                   value='/html/body/form/div[2]/div/div[4]/div[2]/div/div/div/div/div/div/table/tbody/tr/td[1]/table[1]/tbody')
        titles = tbs[1].find_elements(By.CSS_SELECTOR, value='tr > td.text1b')
        infos = tbs[1].find_elements(By.CSS_SELECTOR, value='tr > td.text1')

        for i in range(len(titles)):
            title = titles[i].get_attribute('innerText')
            info = infos[i].get_attribute('innerText')

            if title in FIELD_MAP.keys():
                match[FIELD_MAP[title]] = info

        if not pd.isna(match['id']):
            break

    print(match)

    return match
