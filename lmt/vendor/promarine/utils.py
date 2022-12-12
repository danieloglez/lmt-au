from selenium import webdriver
from selenium.webdriver.common.by import By


def login(driver: webdriver):
    # Find Credentials Components
    username_input = driver.find_element(By.NAME, value='LWRKUSER')
    password_input = driver.find_element(By.NAME, value='AWEBPWD')
    signin_button = driver.find_element(By.NAME, value='LOGIN')

    # Show Credential Components
    account_tab = driver.find_element(By.ID, value='accountTab')
    account_tab.click()

    # Insert Credentials And Login
    username_input.send_keys('feles99')
    password_input.send_keys('F.E.#5825DawsonSt.')
    signin_button.click()

    print('[INFO] Successfully Logged In')