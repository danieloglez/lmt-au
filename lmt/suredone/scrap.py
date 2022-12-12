from selenium import webdriver
from selenium.webdriver.common.by import By


def get(driver: webdriver):
    driver.get('https://app.suredone.com/login')


def login(driver: webdriver):
    # Find Credentials Components
    username_input = driver.find_element(By.ID, value='email')
    password_input = driver.find_element(By.ID, value='password')
    signin_button = driver.find_element(By.XPATH, value='/html/body/div[1]/div/form/div[3]/button')

    # Insert Credentials And Login
    username_input.send_keys('importexportoffice2@gmail.com')
    password_input.send_keys('Felipe#5825O02')
    signin_button.click()    

    print('[INFO] Successfully Logged In')