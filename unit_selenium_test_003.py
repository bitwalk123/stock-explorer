from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://www.python.org")

search_bar = driver.find_element("name", "q")
search_bar.clear()
search_bar.send_keys("getting started with python")

# Locate the button by its ID attribute
button = driver.find_element("id", "submit")

# Click the button
button.click()
