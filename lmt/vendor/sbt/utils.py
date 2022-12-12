from selenium import webdriver
from selenium.webdriver.common.by import By


def login(driver: webdriver):
    # Find login menu button
    login_menu_button = driver.find_element(By.XPATH, value='/html/body/div[2]/header/div[1]/div[2]/div[3]/div[2]/a[2]')

    # Go to login menu
    login_menu_button.click()

    # Find Credentials Components
    username_input = driver.find_element(By.ID, value='Customer_LoginEmail')
    password_input = driver.find_element(By.ID, value='l-Customer_Password')
    signin_button = driver.find_element(By.XPATH, value='/html/body/div[2]/main/div/div[1]/div/div/div[2]/div[1]/form/div[3]/input')

    # Insert Credentials And Login
    username_input.send_keys('feles99')
    password_input.send_keys('User#5825DawsonStreet')
    signin_button.click()
