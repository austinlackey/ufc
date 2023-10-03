from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

url = 'https://www.ufc.com/event/ufc-fight-night-september-23-2023#10848'

driver = webdriver.Chrome()
URL = "https://www.ufc.com/event/ufc-fight-night-september-23-2023#10848"
driver.get(URL)
l = driver.find_element("xpath", '//*[@id="main-card"]/div/section/ul/li[1]/div/div/div/button')
driver.execute_script("arguments[0].click();", l)
time.sleep(1)
l = driver.find_element("xpath", '//*[@id="main-card"]/div/section/ul/li[2]/div/div/div/button')
driver.execute_script("arguments[0].click();", l)
time.sleep(1)
l = driver.find_element("xpath", '//*[@id="main-card"]/div/section/ul/li[3]/div/div/div/button')
driver.execute_script("arguments[0].click();", l)
time.sleep(1)