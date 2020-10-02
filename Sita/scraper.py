from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')

driver.get('https://www.artfinder.com/aarti-bartake#/')

    
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")







driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.find_element_by_xpath('//a[class="af-place fit-in"]').get_attribute("href")