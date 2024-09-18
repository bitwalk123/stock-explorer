from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')
print(driver.title)