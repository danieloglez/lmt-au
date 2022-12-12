import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

HEADERS = ['Description', 'Applications']


def search(driver: webdriver, value: str, wait_time=5):
    time.sleep(wait_time)

    # Find search box
    search_box = driver.find_element(By.CSS_SELECTOR, value='div.input-group input.js-autocomplete-input')

    # Insert value in search box
    search_box.clear()
    search_box.send_keys(value)
    search_box.send_keys(Keys.ENTER)


def find_match(driver: webdriver, value: list, wait_time=5, exact_match=True):
    # Initialize match variable
    match = {
        'init_id': value,
        'part_number': np.nan,
        'title': np.nan,
        'sbt_price': np.nan,
        'cost': np.nan,
        'has_stock': False,
        'stock_eta': np.nan,
        'description': np.nan,
        'applications': np.nan
    }

    # Give Time For Full Load
    time.sleep(wait_time)

    # Store found values -- if not found return empty match
    try:
        found_values = driver.find_element(By.ID, value='prod_wrapper').find_elements(By.CSS_SELECTOR,
                                                                                      value='div.column, div.category-product, div.outer')
    except NoSuchElementException:
        return match

    # Find match
    for fv in found_values:
        # Extract and clean console data
        console = fv.find_element(By.CSS_SELECTOR, value='div.console').get_attribute('innerText')
        console = [float(i.replace('$', '').replace(',', '')) if '$' in i else i for i in
                   console.split('\n')[0].replace('Code: ', '').split(' ')]

        # Determine if is a match
        if exact_match:
            if value != console[2]:
                continue
        elif not exact_match:
            if value not in console[2]:
                continue

        # Assign console values
        match['sbt_price'] = console[0]
        match['cost'] = console[1]
        match['part_number'] = console[2]

        # Go to detailed information
        details_button = fv.find_element(By.CSS_SELECTOR, value='h2.clearfix a.catprod_link')
        details_button.click()

        # Wait until full load
        time.sleep(wait_time)

        # Assign title
        try:
            match['title'] = driver.find_element(By.CSS_SELECTOR,
                                                 value='div#main-content h1, div.main-content h1').get_attribute(
                'innerText')
        except NoSuchElementException:
            pass

        # Extract detailed information
        try:
            add_to_cart_button = driver.find_element(By.ID, value='js-add-to-cart')
            match['has_stock'] = True
        except NoSuchElementException:
            pass

        try:
            in_stock_date_span = driver.find_element(By.ID, value='in-stock-date')
            match['stock_eta'] = in_stock_date_span.get_attribute('innerText')
        except NoSuchElementException:
            pass

        # Extract tabs information
        tab_headings = driver.find_element(By.CSS_SELECTOR, value='div#tabs ul.ptabs_ul').find_elements(By.CSS_SELECTOR,
                                                                                                        value='li')
        tabs = driver.find_element(By.CSS_SELECTOR, value='div#tabs').find_elements(By.CSS_SELECTOR, value='div.ptab')

        for i in range(len(tab_headings)):
            heading = tab_headings[i].get_attribute('innerText')

            if heading in HEADERS:
                match[heading.lower()] = tabs[i].get_attribute('innerText').replace(heading, '')

        break

    return match
