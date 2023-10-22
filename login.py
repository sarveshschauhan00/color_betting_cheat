# /html/body/div/div[1]/div[1]/input

# /html/body/div/div[1]/div[2]/input

# /html/body/div/div[5]/ul/li[4]

import time, csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Launch the web browser
driver = webdriver.Chrome()  # Change this to the appropriate web driver

# Open the web page
driver.get('https://vespa.games/#/')
time.sleep(3)

# while True:
#     xpath = input("input xpath: ")
#     element = driver.find_element(By.XPATH, xpath)
#     element.click()


my_element = driver.find_element(By.XPATH, "/html/body/div/div[5]/ul/li[4]")

my_element.click()
time.sleep(1)

# Find the input element using XPath
input_number = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/input")
input_password = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/input")
submit_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[3]/button")

# Input a value
input_number.send_keys("8824655613")
input_password.send_keys("Sarvesh@2000")
submit_button.click()
time.sleep(1)

win_element = driver.find_element(By.XPATH, "/html/body/div/div[4]/ul/li[3]")
win_element.click()
time.sleep(1)

