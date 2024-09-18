from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get('https://www.insource.co.jp/bup/middle-schedule.html')
driver.maximize_window()
form = driver.find_element(By.XPATH, '//*[@id="search"]/div/input')
form.send_keys('Python')
#form.submit()